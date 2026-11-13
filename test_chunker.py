from app.ingestion.loader import load_pdfs
from app.ingestion.chunker import split_documents

documents = load_pdfs()
chunks = split_documents(documents)

print("Pages loaded:", len(documents))
print("Chunks created:", len(chunks))

if chunks:
    print("\nFirst chunk:")
    print(chunks[0]["text"][:300])
    print("\nSource:", chunks[0]["source"])
    print("Page:", chunks[0]["page"])