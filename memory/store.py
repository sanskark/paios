from db.session import SessionLocal
from db.models import Memory
from memory.embedding import embed
import numpy as np


def upsert_memory(entity, attribute, value):
    db = SessionLocal()

    existing = db.query(Memory).filter_by(
        entity=entity,
        attribute=attribute
    ).first()

    if existing:
        existing.value = value
    else:
        new_memory = Memory(
            entity=entity,
            attribute=attribute,
            value=value
        )
        db.add(new_memory)

    db.commit()
    db.close()



def get_all_memory():
    db = SessionLocal()
    memories = db.query(Memory).all()
    db.close()

    return [
        {
            "entity": m.entity,
            "attribute": m.attribute,
            "value": m.value
        }
        for m in memories
    ]

def get_relevant_memory(query: str):
    db = SessionLocal()
    memories = db.query(Memory).all()
    db.close()

    if not memories:
        return []

    query_vec = np.array(embed(query))
    scored = []
    for m in memories:
        mem_vec = np.array(m.embedding)
        score = np.dot(query_vec, mem_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(mem_vec)
        )
        scored.append((score, m))
    scored.sort(reverse=True, key=lambda x: x[0])

    return [
        f"{m.entity} {m.attribute} is {m.value}"
        for score, m in scored[:3]
        if score > 0.4
    ]

