from google import genai
from config.settings import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def process_input(user_input: str, context, learning_hints=None):
    memory_block = "\n".join(context.get("memory", [])) or "None"
    conversation_block = "\n".join(context.get("conversation", [])) or "None"

    context_text = f"""
    MEMORY:
    {memory_block}

    CONVERSATION (most recent last):
    {conversation_block}
    """

    learning_text = "\n".join(learning_hints or [])

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        You are a strict AI assistant.

        You MUST always return valid JSON.

        ---------------------
        CONTEXT STRUCTURE:
        - MEMORY: long-term user facts
        - CONVERSATION: recent interactions (latest is most important)
        
        ---------------------
        {context_text}
        --------------------
        
        USER INPUT:
        {user_input}
        ---------------------

        INSTRUCTIONS:

        1. Determine intent:
           - "task" → if user gives actions/todos
           - "query" → if user asks a question
           - "chat" → otherwise

        2. ALWAYS generate a PLAN:
           - A list of reasoning steps
           - Minimum 1 step
           - Be concise
        
        MEMORY IS IMPORTANT:

        - If user provides factual personal info, you MUST extract memory
        - Do NOT skip memory extraction when information is clear
        
        3. MEMORY EXTRACTION:
           Extract structured memory ONLY if user provides clear factual info.

           Format:
           {{
             "entity": "",
             "attribute": "",
             "value": ""
           }}

           Rules:
           - Only extract if confident
           - If incomplete → return null
           - Do NOT guess or infer missing values

        4. TASK RULES:
           - Extract tasks ONLY if clearly present
           - If time not specified → leave empty ""
           - If priority not specified → leave empty ""
           - DO NOT invent values like "ASAP" or "high"

        5. CONVERSATION RULES:
           - Resolve follow-up questions using previous context
           - DO NOT ask for clarification if context exists
           - Always link to prior user inputs when relevant

        6. TEMPORAL REASONING RULES:
           - Interpret "tomorrow", "today", "later"
           - If referring to a known habit (e.g., gym time), assume it continues
           - Answer naturally including time reference

        7. ANSWER QUALITY:
           - Be specific and natural
           - Prefer full sentences over short fragments
           - Example:
             No "Gym time is 6"
             Yes "You go to gym at 6 tomorrow as well."
        
        ADAPTIVE LEARNING RULES:
        {learning_text}
        
        CRITICAL RULE:

        - If context contains relevant information, you MUST use it
        - You are NOT allowed to ignore context and give generic answers
        - If a follow-up question relates to previous input, always answer based on it
        
        CONTEXT PRIORITY RULES:
        - For follow-up questions → use CONVERSATION first
        - For factual queries → use MEMORY
        - If both are relevant → combine them
        ---------------------

        OUTPUT FORMAT (STRICT JSON):

        {{
          "type": "task | query | chat",
          "plan": ["step1", "step2"],
          "tasks": [
            {{
              "task": "",
              "time": "",
              "priority": ""
            }}
          ],
          "answer": "",
          "memory": {{
            "entity": "",
            "attribute": "",
            "value": ""
          }}
        }}
        """,
        config={
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["task", "query", "chat", "memory"]
                    },
                    "plan": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "task": {"type": "string"},
                                "time": {"type": "string"},
                                "priority": {"type": "string"}
                            }
                        }
                    },
                    "answer": {
                        "type": "string"
                    },
                    "memory": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "entity": {"type": "string"},
                                    "attribute": {"type": "string"},
                                    "value": {"type": "string"}
                                }
                            },
                            {"type": "null"}
                        ]
                    }
                },
                "required": ["type", "plan"]
            }
        }
    )

    return response.parsed
