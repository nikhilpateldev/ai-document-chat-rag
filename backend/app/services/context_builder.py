def build_context_with_sources(chunks: list):
    context_blocks = []
    source_map = {}

    for idx, chunk in enumerate(chunks, start=1):
        source_id = f"SOURCE_{idx}"
        source_map[source_id] = chunk

        context_blocks.append(
            f"[{source_id}]\n{chunk['content']}"
        )

    return "\n\n".join(context_blocks), source_map
