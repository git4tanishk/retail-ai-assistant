
import chromadb

from app.config import CHROMA_DIR
from app.ingestion.embedder import create_embeddings

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name="retail_it_documents"
)


def store_chunks(chunks):
    if not chunks:
        return 0

    for start in range(0, len(chunks), 100):
        batch = chunks[start:start + 100]

        texts = [chunk["text"] for chunk in batch]
        embeddings = create_embeddings(texts)

        collection.upsert(
            ids=[
                f"{chunk['source']}_page{chunk['page']}_chunk{start + i}"
                for i, chunk in enumerate(batch)
            ],
            documents=texts,
            embeddings=embeddings,
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"]
                }
                for chunk in batch
            ]
        )

    return len(chunks)


from app.config import TOP_K



def search_chunks(query, top_k=TOP_K, max_distance=1.15):
    query_embedding = create_embeddings([query])[0]

    count = collection.count()
    if count == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, count),
        include=["documents", "metadatas", "distances"],
    )

    matches = []

    for i, text in enumerate(results["documents"][0]):
        distance = results["distances"][0][i]

        # Skip chunks that are too far from the question
        if distance > max_distance:
            continue

        matches.append({
            "text": text,
            "source": results["metadatas"][0][i]["source"],
            "page": results["metadatas"][0][i]["page"],
            "distance": distance,
        })

    print(f"Retrieved {len(matches)} relevant chunks")
    return matches

