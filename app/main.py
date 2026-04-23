from fastapi import FastAPI
from core.agent import agent_loop
from db.models import Memory
from db.session import SessionLocal
from memory.store import get_all_memory

app = FastAPI()

@app.get("/memory")
def get_memory():
    return {"memory": get_all_memory()}

@app.delete("/memory")
def clear_memory():
    db = SessionLocal()
    db.query(Memory).delete()
    db.commit()
    db.close()

    return {"status": "Memory cleared"}

@app.post("/chat")
def chat(input: dict):
    return agent_loop(input["message"])
