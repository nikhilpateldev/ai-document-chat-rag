from collections import defaultdict
from datetime import datetime

MAX_HISTORY = 5

class ChatMemoryService:
    def __init__(self):
        self._store = defaultdict(list)

    def add_turn(self, conversation_id: str, role: str, content: str):
        self._store[conversation_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Trim history
        if len(self._store[conversation_id]) > MAX_HISTORY * 2:
            self._store[conversation_id] = self._store[conversation_id][-MAX_HISTORY * 2:]

    def get_history(self, conversation_id: str) -> list:
        return self._store.get(conversation_id, [])
