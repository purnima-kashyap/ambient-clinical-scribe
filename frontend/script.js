const chooseBtn = document.getElementById("chooseBtn");
const audioInput = document.getElementById("audioFile");

chooseBtn.addEventListener("click", () => {
    audioInput.click();
});

audioInput.addEventListener("change", async () => {

    const file = audioInput.files[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {

        chooseBtn.disabled = true;
        chooseBtn.innerHTML = "Uploading...";

        const response = await fetch(
            "http://127.0.0.1:8000/process-consultation",
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const data = await response.json();

        console.log(data);

        // ===========================
        // Transcript
        // ===========================

        const transcriptDiv = document.getElementById("transcript");

        transcriptDiv.innerHTML = "";

        data.transcript.segments.forEach((segment, index) => {

            transcriptDiv.innerHTML += `

                <div class="message">

                    <div class="message-top">

                        <strong>Speaker ${index + 1}</strong>

                        <span>${segment.start}s</span>

                    </div>

                    <p>${segment.text}</p>

                </div>

            `;

        });

        // ===========================
        // SOAP Notes
        // ===========================

        document.getElementById("subjective").innerHTML =
            data.soap_note.subjective;

        document.getElementById("objective").innerHTML =
            data.soap_note.objective;

        document.getElementById("assessment").innerHTML =
            data.soap_note.assessment;

        document.getElementById("plan").innerHTML =
            data.soap_note.plan;

    } catch (error) {

        console.error(error);

        alert("Failed to process consultation.");

    } finally {

        chooseBtn.disabled = false;
        chooseBtn.innerHTML = "Choose File";

    }

});