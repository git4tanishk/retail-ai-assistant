
from app.ingestion.loader import load_pdfs
from app.ingestion.chunker import split_documents
from app.retrieval.vector_store import store_chunks, collection

documents = load_pdfs()
chunks = split_documents(documents)

saved = store_chunks(chunks)

print("Pages loaded:", len(documents))
print("Chunks created:", len(chunks))
print("Chunks saved:", saved)
print("Database records:", collection.count())
