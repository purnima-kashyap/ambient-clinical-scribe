from backend.rag.icd10_recommender import ICD10Recommender

def run_demo():
    print("Loading TF-IDF Recommender (Word Bingo Mode)...")
    recommender = ICD10Recommender()
    
    print("\n" + "="*50)
    print("🧪 TEST 1: The 'Perfect' Keyword Match")
    print("="*50)
    assessment1 = "Patient presents with a severe Migraine."
    print(f"Doctor's Assessment: '{assessment1}'\n")
    
    results1 = recommender.recommend(assessment1)
    if not results1:
        print("❌ No matches found! (Score was 0.0)")
    else:
        for r in results1:
            code = r.get('code', 'UNKNOWN')
            disease = r.get('description', r.get('disease', 'UNKNOWN'))
            score = r.get('score', 'Hidden')
            print(f"✅ FOUND -> Code: {code} | Score: {score} | Disease: {disease}")

    print("\n" + "="*50)
    print("🧪 TEST 2: The 'Real-World' Semantic Test")
    print("="*50)
    assessment2 = "Patient presents with a terrible throbbing pain in their head and light sensitivity."
    print(f"Doctor's Assessment: '{assessment2}'\n")
    
    results2 = recommender.recommend(assessment2)
    
    if not results2:
        print("❌ FAILED: No matches found! The exact keyword 'Migraine' or 'Headache' was missing.")
    else:
        for r in results2:
            code = r.get('code', 'UNKNOWN')
            disease = r.get('description', r.get('disease', 'UNKNOWN'))
            score = r.get('score', 'Hidden')
            print(f"✅ FOUND -> Code: {code} | Score: {score} | Disease: {disease}")
            
    print("\n==================================================")

if __name__ == "__main__":
    run_demo()