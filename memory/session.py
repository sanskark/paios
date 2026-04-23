session_history = []


def add_to_session(user_input, result):
    session_history.append({
        "input": user_input,
        "output": result
    })


def get_session_context():
    return session_history[-5:]
