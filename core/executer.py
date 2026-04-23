def execute_plan(plan):
    results = []

    for step in plan:
        results.append(f"Executed: {step}")

    return results
