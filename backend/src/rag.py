import os
from pathlib import Path
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

data_dir = Path(__file__).resolve().parent.parent / "data"
persist_dir = Path(__file__).resolve().parent.parent / "db"

EMBEDDINGS = OpenAIEmbeddings()

def define_get_vectorstore() -> Chroma:
    txt_paths = list(data_dir.glob("*.txt"))
    if not persist_dir.exists() or not any(persist_dir.iterdir()):
        splitter = RecursiveCharacterTextSplitter(chunk_size=30, chunk_overlap=5)
        documents = []
        ids = []
        for path in txt_paths:
            text = path.read_text(encoding="utf-8")
            chunks = splitter.split_text(text)
            for idx, chunk in enumerate(chunks):
                documents.append(Document(
                    page_content=chunk,
                    metadata={"source": path.name, "chunk_index": idx}
                ))
                ids.append(f"{path.stem}_{idx}")
        vstore = Chroma.from_documents(
            documents=documents,
            ids=ids,
            embedding=EMBEDDINGS,
            persist_directory=str(persist_dir),
            collection_name="docs"
        )
    else:
        vstore = Chroma(
            persist_directory=str(persist_dir),
            embedding_function=EMBEDDINGS,
            collection_name="docs"
        )
    return vstore

if __name__ == "__main__":
    define_get_vectorstore()

