import numpy as np
from typing import List, Dict

class EmbeddingReranker:

    @staticmethod
    def cosine(a, b):
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def rerank(
        self,
        query_vector: List[float],
        chunks: List[Dict],
        top_n: int = 5
    ) -> List[Dict]:

        for chunk in chunks:
            chunk["rerank_score"] = self.cosine(
                query_vector,
                chunk["vector"]
            )

        chunks.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return chunks[:top_n]
