from google import genai
from config.settings import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def extract_tasks_structured(user_input: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Extract tasks from: {user_input}",
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "task": {"type": "string"},
                                "priority": {"type": "string"},
                                "time": {"type": "string"},
                            },
                            "required": ["task"],
                        },
                    }
                },
                "required": ["tasks"],
            },
        },
    )

    return response.parsed