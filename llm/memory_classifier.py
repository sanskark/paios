from google import genai
from config.settings import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def classify_memory(text: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Classify this memory.

        Types:
        - task (things to do)
        - fact (info)
        - preference (likes/habits)
        - ignore (not useful)

        Also assign importance (1-5).

        Input: {text}
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["task", "fact", "preference", "ignore"]
                    },
                    "importance": {
                        "type": "integer"
                    }
                },
                "required": ["type", "importance"]
            }
        }
    )

    return response.parsed
