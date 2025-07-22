import os
from rich import print
from dotenv import load_dotenv
from langchain_core.documents import Document
from PIL import Image
import pytesseract
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

load_dotenv()

# load pdf and preprocessing
pdf_path = "pdfs\\HSC26-Bangla1st-Paper.pdf"


# OCR based text extraction for better result
# both pymupdf and pdfplumber failed in bangla text
def ocr_bangla_pdf(path):
    doc = fitz.open(path)
    texts = []
    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img, lang="ben")  # 'ben' for Bengali
        texts.append(
            Document(page_content=text, metadata={"page": page.number, "source": path})
        )
    return texts


Documents = ocr_bangla_pdf(pdf_path)


# chunking and splitting
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800, chunk_overlap=400, separators=[" "]
)

splits = text_splitter.split_documents(Documents)

print(
    f"Total splits: {len(splits)}\nMetadata of first split: {splits[0].metadata}\nFirst page contents: {splits[0].page_content}"
)


# embedding engine
embedding_engine = OllamaEmbeddings(
    base_url=os.getenv("OLLAMA_EMBEDDING_URL"),
    model="bge-m3:latest",
)

print("loaded embedding model")

SUPABASE_PG_CONN_URL = os.getenv("SUPABASE_PG_CONN_URL")

vector_store = PGVector(
    embeddings=embedding_engine,
    collection_name="hsc_bangla",
    connection=SUPABASE_PG_CONN_URL,
    use_jsonb=True,
)
print("PGVector Store is loaded.")

# push embedding to collection
for i in range(0, len(splits), 10):
    chunk = splits[i : i + 10]
    try:
        # Add the chunk to the vector store
        vector_store.add_documents(documents=chunk)
        print(f"Chunk {i // 10} added successfully")
    except Exception as e:
        print(f"Error adding chunk {i // 10}: {e}")
        continue
