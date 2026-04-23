from google import genai
from config.settings import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def classify_intent_llm(user_input: str):
    print("ROUTER CALLED")
    print("INPUT:", user_input)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Classify intent: {user_input}",
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["task", "chat"]
                    }
                },
                "required": ["type"]
            }
        }
    )
    print("RAW RESPONSE:", response.text)
    return response.parsed["type"]
