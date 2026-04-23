from llm.client import extract_tasks_structured


def chat_response(text: str, context=None):
    context_text = ""

    if context:
        context_text = f"Past context: {context}"

    prompt = f"""
    Use this context if relevant:
    {context_text}

    User: {text}
    """

    return {
        "response": extract_tasks_structured(prompt)
    }
