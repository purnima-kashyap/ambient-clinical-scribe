from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class SOAPNote(BaseModel):
    """Data model for a clinical SOAP note."""
    subjective: str = Field(description="Patient's reported symptoms, history of present illness, and complaints.")
    objective: str = Field(description="Factual observations by the doctor, including vital signs and physical exam findings.")
    assessment: str = Field(description="The medical diagnosis or differential diagnosis based on S and O.")
    plan: str = Field(description="Treatment plan, medications prescribed, tests ordered, and follow-up instructions.")

_SYSTEM_PROMPT= """
You are an expert AI clinical scribe. Your task is to convert raw medical consultation transcripts into highly structured, professional SOAP notes.

CRITICAL RULES:
1. Extract ONLY medically relevant information. Ignore small talk entirely.
2. Do NOT hallucinate. Never invent symptoms, vitals, or diagnoses that were not explicitly stated in the transcript.
3. Use professional medical terminology where appropriate.
4. NEVER return an empty string for any field. If the transcript does not explicitly mention objective findings, write "No objective findings recorded in this encounter." If it does not state an explicit diagnosis, you must still infer the single most clinically likely diagnosis based on the Subjective findings — never leave Assessment blank. If no plan was stated, write "No treatment plan documented in this encounter."
5. You MUST format your response as a valid JSON object matching the requested schema. Do not include any text outside the JSON.

Here are two examples of perfect performance:

EXAMPLE 1 (Orthopedics)
Transcript: Doctor: Good morning, Sarah. How was your weekend? Patient: Oh, the weather was lovely, I went hiking, but I tripped over a tree root and twisted my right ankle. Doctor: I'm sorry to hear that. Let's take a look. On a scale of 1 to 10, how bad is the pain? Patient: It's about a 6. It really throbs at night. Doctor: Okay, I see some moderate swelling and bruising on the lateral side here. Your pulse in the foot feels strong. I'm going to press right here... does that hurt? Patient: Ouch! Yes, right there. Doctor: Well, the good news is your X-rays just came back negative for any fractures. It looks like a Grade 2 ankle sprain. I want you to rest it, apply ice, and take Ibuprofen 400mg every 8 hours for the pain. I also want you to wear this compression brace for the next two weeks.
Output JSON:
{{
  "subjective": "Patient reports twisting right ankle while hiking over the weekend. Complains of throbbing pain at night, rated 6/10.",
  "objective": "Moderate swelling and bruising noted on the lateral aspect of the right ankle. Point tenderness present over the lateral ligaments. Pedis pulses are strong/intact. X-ray of right ankle is negative for acute fracture.",
  "assessment": "Grade 2 right ankle sprain.",
  "plan": "R.I.C.E. protocol (Rest, Ice, Compression, Elevation). Ibuprofen 400mg every 8 hours PRN for pain. Dispensed right ankle compression brace to be worn for 2 weeks."
}}

EXAMPLE 2 (Neurology)
Transcript: Doctor: Hi David, good to see you again. I hear from the nurse you've been having some bad headaches? Patient: Yeah, the last month has been brutal. I'm starting a new job soon, so maybe it's just stress, but I get these pounding headaches on the left side of my head. I have to go into a dark room and turn off all the lights. Doctor: Any nausea or blurry vision before they start? Patient: Definitely nausea, yes, but no blurry vision. Doctor: Alright, let's check your vitals. Blood pressure is 120 over 80, heart rate is 72. I'll do a quick neuro exam... follow my finger... okay, cranial nerves look completely normal. Your grip strength is equal on both sides. This sounds like classic migraines without aura, likely triggered by stress. Let's start you on Sumatriptan 50mg. Take one pill as soon as you feel a headache coming on. I also want you to keep a headache diary for the next month.
Output JSON:
{{
  "subjective": "Patient reports pounding left-sided headaches occurring over the past month. Symptoms are associated with nausea and photophobia (light sensitivity). Denies visual aura. Notes recent stress due to an upcoming job change.",
  "objective": "BP: 120/80. HR: 72 bpm. Neurological exam: Cranial nerves grossly intact, bilaterally equal grip strength. No focal neurological deficits observed.",
  "assessment": "Migraine without aura, likely stress-induced.",
  "plan": "Prescribed Sumatriptan 50mg PRN at onset of headache. Patient instructed to maintain a daily headache diary."
}}
"""
# Maximum transcript length 
_MAX_TRANSCRIPT_LENGTH = 10_000

class SOAPNoteGenerator:
    """
    Reusable generator for clinical SOAP notes from raw consultation transcripts.
    The LLM chain is built once on initialization and reused across all calls,
    avoiding the overhead of recreating it on every request.
    """
 
    def __init__(self, model: str = "llama3.1"):
        """
        Args:
            model: Ollama model name to use. Defaults to llama3.1 (llama3 is deprecated).
        """
        llm = ChatOllama(
            model=model,
            temperature=0,
            format="json",
            timeout=60,       
            num_predict=1024, # cap output tokens to avoid runaway generation
        )
 
        parser = JsonOutputParser(pydantic_object=SOAPNote)
 
        prompt = ChatPromptTemplate.from_messages([
            ("system", _SYSTEM_PROMPT),
            ("human", "Format Instructions: \n{format_instructions}\n\nPlease generate a SOAP note from this transcript:\n\n{transcript}")
        ])
 
        # Build chain once; reused for every generate() call
        self._chain = prompt | llm | parser
        self._format_instructions = parser.get_format_instructions()
 
    async def generate(self, transcript: str) -> SOAPNote:
        """
        Takes a raw transcript and returns a validated SOAPNote object.
 
        Args:
            transcript: Raw doctor-patient consultation text.
 
        Returns:
            SOAPNote: Pydantic model with subjective, objective, assessment, plan fields.
 
        Raises:
            ValueError: If the transcript is empty or exceeds the maximum length.
            RuntimeError: If the LLM chain fails for any reason.
        """
        # --- Input validation ---
        if not transcript or not transcript.strip():
            raise ValueError("Transcript cannot be empty.")
        if len(transcript) > _MAX_TRANSCRIPT_LENGTH:
            raise ValueError(
                f"Transcript length ({len(transcript)} chars) exceeds the "
                f"maximum allowed length of {_MAX_TRANSCRIPT_LENGTH} chars."
            )
 
        try:
            result: dict = await self._chain.ainvoke({
                "transcript": transcript,
                "format_instructions": self._format_instructions,
            })

            # Local LLMs occasionally return blank fields instead of a fallback
            if any(not str(result.get(field, "")).strip() for field in
                   ("subjective", "objective", "assessment", "plan")):
                result = await self._chain.ainvoke({
                    "transcript": transcript,
                    "format_instructions": self._format_instructions,
                })

            return SOAPNote(**result)

        except Exception as e:
            raise RuntimeError(f"Local LLM generation failed: {str(e)}") from e