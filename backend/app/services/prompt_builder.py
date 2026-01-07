def format_chat_history(history: list) -> str:
    if not history:
        return ""

    formatted = []
    for turn in history:
        role = "User" if turn["role"] == "user" else "Assistant"
        formatted.append(f"{role}: {turn['content']}")

    return "\n".join(formatted)
