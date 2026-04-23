def validate_output(result):
    issues = []
    if not result.get("plan"):
        issues.append("Missing plan")

    answer = result.get("answer", "")
    if result.get("type") == "query":
        if not answer or len(answer.split()) < 3:
            issues.append("Weak answer")

    tasks = result.get("tasks", [])
    for t in tasks:
        if t.get("time") == "ASAP":
            issues.append("Invalid time")

    return issues
