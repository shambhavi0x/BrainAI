from pypdf import PdfReader
from rag.chunking import chunk_text

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

def ingest_pdf(pdf_file):
    text = extract_text(pdf_file)
    chunks = chunk_text(text)
    return chunks
