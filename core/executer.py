def execute_plan(plan, tasks):
    results = []

    for step in plan:
        results.append(f"Executed: {step}")

    return results
