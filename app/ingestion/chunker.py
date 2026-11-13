
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_SIZE, CHUNK_OVERLAP


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []

    for doc in documents:
        text_chunks = splitter.split_text(doc["text"])

        for text in text_chunks:
            chunks.append({
                "text": text,
                "source": doc["source"],
                "page": doc["page"]
            })

    return chunks
