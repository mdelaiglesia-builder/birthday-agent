from generation import  generation
from retrieval import retrieval
from typing import Any
from judge import judge

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}")

query = "where's parking?"
chunks_retrieved = retrieval(query)
generation_response: dict[str, Any] = generation(query, chunks_retrieved)

check("Generation response has an answer", generation_response["answer"] is not None and len(generation_response["answer"]) > 0)
check("Generation response has chunks used", generation_response["chunks_used"] is not None and len(generation_response["chunks_used"]) > 0)

chunks_used_ids = [d["chunk_id"] for d in generation_response["chunks_used"]]
chunks_retrieved_ids = [chunk_id for chunk_id, document in chunks_retrieved]
check("Chunks used contained in chunks retrieved", all(used_chunk_id in chunks_retrieved_ids for used_chunk_id in chunks_used_ids))

judge_response: dict[str, Any] = judge(query, chunks_retrieved, generation_response["answer"], generation_response["chunks_used"])
check("Answer generation is grounded", judge_response["grounded"])