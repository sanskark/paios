from llm.unified import process_input
from memory.store import upsert_memory, get_relevant_memory
from core.cache import make_key, get_cache, set_cache, clear_cache
from core.executer import execute_plan
from memory.session import add_to_session, get_session_context

from core.validator import validate_output
from core.fixer import fix_output
from core.scorer import score_output
from memory.learning import log_learning, update_patterns, get_learning_hints



def agent_loop(user_input: str):
    print(">>> AGENT LOOP HIT")
    memory_context = get_relevant_memory(user_input)
    session_context = get_session_context()

    context = {
        "memory": memory_context,
        "conversation": [
            format_session(s) for s in session_context
        ]
    }

    learning_hints = get_learning_hints()
    flat_context = (
            context.get("memory", []) +
            context.get("conversation", []) +
            (learning_hints or [])
    )

    key = make_key(user_input, flat_context)
    cached = get_cache(key)
    if cached:
        print("CACHE HIT")
        return cached

    result = process_input(user_input, context, learning_hints)
    issues = validate_output(result)
    if issues:
        update_patterns(issues)
        result = fix_output(user_input, context, result, issues)
        validate_output(result)

    score = score_output(result)
    result["confidence"] = score

    log_learning(user_input, result, score)

    add_to_session(user_input, result)

    if score > 0.5:
        execution = execute_plan(result.get("plan") or ["Basic reasoning step"], result.get("tasks", []))
    else:
        execution = ["Skipped execution due to low confidence"]
    result["execution"] = execution

    mem = result.get("memory")

    if isinstance(mem, dict) and mem.get("entity"):
        upsert_memory(
            mem["entity"],
            mem["attribute"],
            mem["value"]
        )
        clear_cache()

    set_cache(key, result)
    return result

def format_session(s):
    answer = s["output"].get("answer")
    memory = s["output"].get("memory")

    if answer:
        return f"User: {s['input']} → Assistant: {answer}"

    if memory and memory.get("entity"):
        return f"User said they {memory['entity']} {memory['attribute']} at {memory['value']}"

    return f"User: {s['input']}"
