def score_output(result, issues=None):
    score = 1.0

    # penalize issues
    if issues:
        score -= 0.4 * len(issues)

    answer = result.get("answer", "")
    if result.get("type") == "query":
        if len(answer.split()) < 4:
            score -= 0.3

    if "tomorrow will be" in answer.lower():
        score -= 0.5

    return max(score, 0.0)
