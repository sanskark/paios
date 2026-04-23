from llm.client import extract_tasks_structured
from utils.formatter import format_context


def query_memory(question: str, context):
    context_text = format_context(context)

    prompt = f"""
    Answer the question using only the relevant context.

    Context:
    {context_text}

    Question:
    {question}

    Give a direct answer only.
    """

    return {
        "response": extract_tasks_structured(prompt)
    }
