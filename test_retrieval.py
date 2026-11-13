
from app.retrieval.vector_store import search_chunks

question = "How do I troubleshoot my VPN connection?"

results = search_chunks(question)

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("Source:", result["source"])
    print("Page:", result["page"])
    print("Text:", result["text"][:300])
