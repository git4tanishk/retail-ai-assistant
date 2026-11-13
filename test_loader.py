from app.ingestion.loader import load_pdfs

documents = load_pdfs()

print("Pages loaded:", len(documents))

for doc in documents[:3]:
    print("\nSource:", doc["source"])
    print("Page:", doc["page"])
    print("Text:", doc["text"][:200])