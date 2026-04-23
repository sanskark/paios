from utils.formatter import format_context
from llm.client import extract_tasks_structured


def extract_tasks(text: str, context=None):
    context_text = ""

    if context:
        context_text = f"""
        Past relevant context:
        {format_context(context)}
        """

    prompt = f"""
    {context_text}
    Extract tasks from the input.
    Input: {text}
    """

    return extract_tasks_structured(prompt)
