import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

data_dir = Path(__file__).resolve().parent.parent / "data"
persist_dir = Path(__file__).resolve().parent.parent / "persistent"

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)

def define_get_vectorstore(text_filename: str) -> Chroma:
    txt_file = data_dir / text_filename
    if not persist_dir.exists() or not any(persist_dir.iterdir()):
        text = txt_file.read_text(encoding="utf-8")
        splitter = RecursiveCharacterTextSplitter(chunk_size=30, chunk_overlap=5)
        chunks = splitter.split_text(text)
        docs = [Document(page_content=chunk, metadata={
                    "source": txt_file.name,
                    "chunk_id": idx
                })
                for idx, chunk in enumerate(chunks)]
        vstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=str(persist_dir)
        )
        vstore.persist()
    else:
        vstore = Chroma(
            persist_directory=str(persist_dir),
            embedding_function=embeddings
        )
    return vstore
