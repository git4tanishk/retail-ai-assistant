
from pathlib import Path
from pypdf import PdfReader

from app.config import DOCUMENTS_DIR


def load_pdfs():
    documents = []

    for pdf_file in Path(DOCUMENTS_DIR).glob("*.pdf"):
        reader = PdfReader(str(pdf_file))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if text.strip():
                documents.append({
                    "text": text,
                    "source": pdf_file.name,
                    "page": page_number
                })

    return documents
