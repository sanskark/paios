import faiss
import numpy as np

dimension = 384

index = faiss.IndexFlatL2(dimension)
documents = []


def add_to_index(text, metadata):
    from memory.embedding import embed

    vector = embed(text)
    index.add(np.array([vector]).astype("float32"))
    documents.append({
        "text": text,
        "metadata": metadata
    })


def search_index(query, k=3):
    from memory.embedding import embed
    import numpy as np

    if len(documents) == 0:
        return []

    query_vector = embed(query)
    distances, indices = index.search(np.array([query_vector]), k)

    results = []
    for i in indices[0]:
        if 0 <= i < len(documents):
            results.append(documents[i])

    return results