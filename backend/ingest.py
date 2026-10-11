import os
import fitz
import docx
import faiss
import pickle
import random
import pytesseract 
import pandas as pd
from pdf2image import convert_from_path
from PIL import Image
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2",local_files_only=True)

documents = []
metadata = []

def read_pdf(path):
    doc = fitz.open(path)
    text = ""

    for page in doc:
        page_text = page.get_text().strip()
        text += page_text

        
    if len(text.strip()) < 50:
        print(f"OCR applied on: {path}")
        text = ocr_pdf(path)

    return text

def ocr_pdf(path):
    images = convert_from_path(path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def chunk_text(text, size=300):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

# def ingest(folder):
#     for file in os.listdir(folder):
#         if file.endswith(".pdf"):
#             text = read_pdf(os.path.join(folder, file))
#             chunks = chunk_text(text)
#             for chunk in chunks:
#                 documents.append(chunk)
#                 metadata.append(file)
import docx
import pandas as pd

def read_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def read_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def read_csv(path):
    df = pd.read_csv(path)
    return df.to_string()

def ingest(folder):
    for file in os.listdir(folder):

        file_path = os.path.join(folder, file)

        if file.endswith(".pdf"):
            text = read_pdf(file_path)

        elif file.endswith(".docx"):
            text = read_docx(file_path)

        elif file.endswith(".txt"):
            text = read_txt(file_path)

        elif file.endswith(".csv"):
            text = read_csv(file_path)

        else:
            continue

        chunks = chunk_text(text)

        for chunk in chunks:
            documents.append(chunk)
            metadata.append(file)


# ingest("data/finance")
# ingest("data/hotel")
ingest("uploads")

combined = list(zip(documents, metadata))
random.shuffle(combined)
documents,metadata = zip(*combined)
documents = list(documents)
metadata = list(metadata)

embeddings = model.encode( 
    documents,
    normalize_embeddings=True)   #this one

index = faiss.IndexFlatIP(embeddings.shape[1]) #this line
index.add(embeddings)

faiss.write_index(index, "index.faiss")
pickle.dump((documents, metadata), open("docs.pkl", "wb"))

print("Ingestion complete.")