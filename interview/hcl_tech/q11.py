# 10. Implement cosine similarity from scratch and use it to retrieve the top-k most similar chunks.

import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm if norm else 0.0

def top_k(query_vec, doc_vec, k=3):
    scored = [(cosine(query_vec, d), i) for i, d in enumerate(doc_vec)]
    return [i for _, i in sorted(scored, reverse=True)[:k]]


