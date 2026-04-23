import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"
MEMORY_URL = "http://127.0.0.1:8000/memory"

st.set_page_config(page_title="AI Assistant", layout="wide")

# ---------- STATE ----------
if "history" not in st.session_state:
    st.session_state.history = []

if "input" not in st.session_state:
    st.session_state.input = ""

# ---------- STYLING ----------
st.markdown("""
<style>
.chat-input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #0e1117;
    padding: 10px 20px;
    border-top: 1px solid #333;
    z-index: 100;
}
.block-container {
    padding-bottom: 100px;
}
.chat-user {
    background-color: #1e1e2f;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
}
.chat-ai {
    background-color: #2a2a40;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 12px;
}
.small-text {
    font-size: 12px;
    color: #aaa;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("🧠 AI Assistant")

if st.sidebar.button("Clear Chat"):
    st.session_state.history = []

if st.sidebar.button("🗑 Clear Memory"):
    st.session_state.confirm_delete = True

if st.session_state.get("confirm_delete"):
    st.sidebar.warning("Are you sure?")

    col1, col2 = st.sidebar.columns(2)

    if col1.button("Yes"):
        requests.delete(MEMORY_URL)
        st.session_state.confirm_delete = False
        st.rerun()

    if col2.button("No"):
        st.session_state.confirm_delete = False

st.sidebar.markdown("---")
st.sidebar.markdown("### Stats")
st.sidebar.write(f"Messages: {len(st.session_state.history)}")

st.sidebar.markdown("---")
st.sidebar.markdown("### Memory")

try:
    mem_res = requests.get(MEMORY_URL)
    memory_data = mem_res.json().get("memory", [])

    if memory_data:
        for m in memory_data:
            st.sidebar.markdown(
                f"- **{m['entity']}** → {m['attribute']} = {m['value']}"
            )
    else:
        st.sidebar.markdown("_No memory stored yet_")

except:
    st.sidebar.markdown("⚠Could not load memory")

# ---------- MAIN ----------
st.title("Personal AI Assistant")

# ---------- CHAT DISPLAY ----------
for item in st.session_state.history:
    st.markdown(
        f'<div class="chat-user"><b>🧑 You:</b> {item["input"]}</div>',
        unsafe_allow_html=True
    )

    output = item["output"]

    with st.container():
        st.markdown('<div class="chat-ai">', unsafe_allow_html=True)

        # Answer
        if output.get("answer"):
            st.markdown(f"**{output['answer']}**")

        # Tasks
        tasks = output.get("tasks", [])
        if tasks:
            st.markdown("**Tasks:**")
            for t in tasks:
                time = t.get("time")
                if time:
                    st.markdown(f"- {t.get('task')} ⏰ {time}")
                else:
                    st.markdown(f"- {t.get('task')}")

        # Memory (clean display)
        memory = output.get("memory")
        if isinstance(memory, dict) and memory.get("entity"):
            st.markdown(
                f"🧩 {memory['entity']} → {memory['attribute']} = {memory['value']}"
            )

        # Confidence
        st.markdown(
            f'<div class="small-text">Confidence: {output.get("confidence", 0)}</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ---------- SEND FUNCTION ----------
def send_message():
    user_input = st.session_state.input.strip()

    if not user_input:
        return

    if user_input.lower() in ["give me my memory", "show memory"]:
        try:
            response = requests.get(MEMORY_URL)
            data = response.json()

            formatted = "\n".join([
                f"- {m['entity']} → {m['attribute']} = {m['value']}"
                for m in data.get("memory", [])
            ]) or "No memory found"

            result = {
                "answer": formatted,
                "tasks": [],
                "memory": None,
                "confidence": 1.0
            }

        except:
            result = {
                "answer": "Could not fetch memory",
                "tasks": [],
                "memory": None,
                "confidence": 0
            }

    # 🔹 NORMAL CHAT
    else:
        try:
            response = requests.post(
                API_URL,
                json={"message": user_input}
            )
            result = response.json()
        except:
            result = {
                "answer": "Error from server",
                "tasks": [],
                "memory": None,
                "confidence": 0
            }

    # Save to history
    st.session_state.history.append({
        "input": user_input,
        "output": result
    })

    st.session_state.input = ""

# ---------- INPUT ----------
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)

col1, col2 = st.columns([8, 1])

with col1:
    st.text_input(
        "Message",
        key="input",
        placeholder="Type your message...",
        label_visibility="collapsed"
    )

with col2:
    st.button("➤", on_click=send_message)

st.markdown('</div>', unsafe_allow_html=True)
