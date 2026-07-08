import os
import json
import csv
import time
import re
from datetime import datetime

# 1. UPDATED IMPORT: Import the class your teammate wrote
from backend.rag.icd10_recommender import ICD10Recommender 

ANSWER_KEY = {
    "allergic_rhinitis": "J30.9",
    "anxiety": "F41.1",
    "asthma": "J45.909",
    "cervical_spondylosis": "M47.812",
    "diabetes": "E11.9",
    "fever": "R50.9",
    "gastritis": "K29.70",
    "gerd": "K21.9",
    "headache": "R51",
    "hypertension": "I10",
    "insomnia": "G47.00",
    "knee_pain": "M25.569",
    "low_back_pain": "M54.50",
    "migraine": "G43.909",
    "otitis_media": "H66.90",
    "shoulder_pain": "M25.519",
    "sinusitis": "J01.90",
    "uti": "N39.0",
    "viral_gastroenteritis": "A08.4"
}

def normalize_icd10(code: str) -> str:
    """Removes spaces and periods for fair grading (e.g., 'M47.812' == 'M47812')."""
    if not code:
        return ""
    return re.sub(r'[^A-Za-z0-9]', '', str(code)).upper()

def run_comprehensive_evaluation():
    test_cases_dir = 'data/soap_test_cases'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_report_path = f'data/rag_evaluation_report_{timestamp}.csv'
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    total_latency = 0.0
    results_log = []

    print(f"🚀 Starting Comprehensive RAG Evaluation...\n")
    
    # 2. INITIALIZE THE CLASS: Turn on your teammate's recommender engine
    print("Initializing ICD10 Recommender (Loading TF-IDF Matrix)...")
    recommender = ICD10Recommender()
    
    for filename in os.listdir(test_cases_dir):
        if not filename.endswith('.txt'):
            continue
            
        filepath = os.path.join(test_cases_dir, filename)
        
        prefix = filename.split('_case_')[0]
        raw_expected = ANSWER_KEY.get(prefix, "UNKNOWN")
        expected_normalized = normalize_icd10(raw_expected)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                soap_data = json.loads(f.read())
                assessment = soap_data.get("assessment", "")
        except Exception as e:
            print(f"⚠️ Error reading JSON in {filename}: {e}")
            continue
            
        total_tests += 1
        print(f"Testing Case {total_tests}: [{prefix}] -> Expected: {raw_expected}")
        
        start_time = time.time()
        try:
            # 3. CALL THE METHOD: Use synchronous .recommend() instead of await
            ai_response = recommender.recommend(assessment)
            # The teammate's code returns a list of dictionaries. 
            # Converting to string works perfectly for our regex grader!
            ai_response_str = str(ai_response) 
            error_msg = None
        except Exception as e:
            ai_response_str = "SYSTEM_ERROR"
            error_msg = str(e)
        
        latency = time.time() - start_time
        total_latency += latency
        
        ai_normalized = normalize_icd10(ai_response_str)
        if expected_normalized in ai_normalized and expected_normalized != "":
            status = "✅ PASS"
            passed_tests += 1
        else:
            status = "❌ FAIL"
            failed_tests += 1
            
        results_log.append({
            'Test_ID': total_tests,
            'Condition': prefix,
            'Assessment_Text': assessment,
            'Expected_Code': raw_expected,
            'AI_Raw_Output': ai_response_str,
            'Status': status,
            'Latency_Seconds': round(latency, 2),
            'Error': error_msg if error_msg else "None"
        })

    with open(output_report_path, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Test_ID', 'Condition', 'Assessment_Text', 'Expected_Code', 'AI_Raw_Output', 'Status', 'Latency_Seconds', 'Error']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_log)

    print("\n" + "="*40)
    print("📊 RAG PIPELINE PERFORMANCE REPORT")
    print("="*40)
    print(f"Total Cases Run:      {total_tests}")
    print(f"Successful Matches:   {passed_tests}")
    print(f"Failed Matches:       {failed_tests}")
    if total_tests > 0:
        print(f"Overall Accuracy:     {(passed_tests/total_tests)*100:.1f}%")
        print(f"Average Latency:      {total_latency/total_tests:.2f} seconds/query")
    print(f"\n📁 Detailed audit report saved to: {output_report_path}")

if __name__ == "__main__":
    # 4. REMOVED ASYNCIO: Since the teammate's code is synchronous, we just run the function directly
    run_comprehensive_evaluation()