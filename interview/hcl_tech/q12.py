# 11. Build a simple RAG pipeline in pseudocode or minimal Python: embed query → retrieve → construct prompt → call LLM → return answer with citations.


def rag_answer(query, embed, vector_db, llm, k=3):
    q_vec = embed(query)
    hits = vector_db.search(q_vec, k=k)  # retrieval
    context = "\n\n".join(f"[{i+1}] {h.text}" for i, h in enumerate(hits))
    prompt = f"Answer using only the context below. Cite sources as [n].\n\nContext:\n{context}\n\nQuestion: {query}"
    return llm(prompt), hits  # generation + provenance
