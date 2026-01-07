import sqlite3
from typing import List, Dict

class BM25Store:
    def __init__(self, db_path="bm25.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks
        USING fts5(
            chunk_id,
            content,
            filename,
            page
        )
        """)
        self.conn.commit()

    def upsert_chunk(
        self,
        chunk_id: str,
        content: str,
        filename: str,
        page: int | None
    ):
        self.conn.execute(
            "INSERT INTO chunks VALUES (?, ?, ?, ?)",
            (chunk_id, content, filename, page)
        )
        self.conn.commit()

    def search(self, query: str, limit: int = 20) -> List[Dict]:
        cursor = self.conn.execute(
            """
            SELECT chunk_id, content, filename, page, bm25(chunks) as score
            FROM chunks
            WHERE chunks MATCH ?
            ORDER BY score
            LIMIT ?
            """,
            (query, limit)
        )

        return [
            {
                "chunk_id": row[0],
                "content": row[1],
                "filename": row[2],
                "page": row[3],
                "bm25_score": row[4]
            }
            for row in cursor.fetchall()
        ]
