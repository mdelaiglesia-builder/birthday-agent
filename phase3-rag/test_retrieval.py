from retrieval import retrieval 

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}")

chunks_retrieved = retrieval("where's parking?")
check("Retrieval returns three results", len(chunks_retrieved) == 3)
check("Retrieval returns strings", all(isinstance(document, str) for chunk_id, document in chunks_retrieved))
check("Some result contains 'parking' word", any("parking" in document for chunk_id, document in chunks_retrieved))