import fitz  # PyMuPDF
from io import BytesIO

def hide_in_pdf(pdf_file, message):
    doc = fitz.open(stream=pdf_file.read(), filetype='pdf')
    doc.set_metadata({'keywords': message})
    buf = BytesIO()
    doc.save(buf)
    return buf.getvalue()

def extract_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype='pdf')
    return doc.metadata.get('keywords', '')
