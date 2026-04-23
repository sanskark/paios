from llm.router import classify_intent_llm


def classify_intent(text: str):
    return classify_intent_llm(text)