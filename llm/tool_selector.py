from google import genai
from config.settings import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def select_tool(user_input: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        You are a strict tool selector.

        Choose ONE tool based on intent:

        RULES:

        - If the user is asking a QUESTION about past info, memory, or facts → use "query"
        - If the user is giving tasks, todos, or actions → use "task_extractor"
        - If the user is just chatting → use "chat"

        EXAMPLES:

        Input: What time do I go to gym?
        Output: query

        Input: Fix bug and call client
        Output: task_extractor

        Input: How are you?
        Output: chat

        Now classify:

        Input: {user_input}
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["task", "query", "chat"]
                    },
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "task": {"type": "string"},
                                "time": {"type": "string"},
                                "priority": {"type": "string"}
                            },
                            "required": ["task"]
                        }
                    },
                    "answer": {"type": "string"}
                },
                "required": ["type"]
            }
        }
    )

    return response.parsed["tool"]
