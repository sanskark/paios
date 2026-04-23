learning_log = []

patterns = {
    "weak_answer": 0,
    "missing_plan": 0,
    "hallucination": 0
}

def update_patterns(issues):
    for issue in issues:
        if "Weak answer" in issue:
            patterns["weak_answer"] += 1
        if "Missing plan" in issue:
            patterns["missing_plan"] += 1
        if "Invalid time" in issue:
            patterns["hallucination"] += 1


def get_learning_hints():
    hints = []

    if patterns["weak_answer"] > 2:
        hints.append("Give more detailed answers.")

    if patterns["hallucination"] > 2:
        hints.append("Do not invent values like time or priority.")

    if patterns["missing_plan"] > 2:
        hints.append("Always include a reasoning plan.")

    return hints


def log_learning(user_input, result, score):
    entry = {
        "input": user_input,
        "output": result,
        "score": score
    }

    learning_log.append(entry)

    if score < 0.7:
        print("LOW CONFIDENCE:", entry)
