def format_context(memories):
    if not memories:
        return ""

    return "\n".join([f"- {m}" for m in memories])
