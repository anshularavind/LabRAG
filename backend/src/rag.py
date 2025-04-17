import os
from pathlib import Path
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

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

def get_answer(query, k):
    vectorstore = define_get_vectorstore()
    documents = vectorstore.similarity_search(query,k)
    system_prompt = "Try to answer the question to the best of your ability."
    context = "\n\n".join(f"{i+1}. {d.page_content}" for i, d in enumerate(documents))
    user_prompt = f"\n\n{query}\nAnswer briefly."
    prompt = system_prompt + context + user_prompt

    llm = ChatOpenAI(model_name="gpt-4.1-nano")
    response = llm.invoke(prompt)

    print("Answer:", response)
    print("Sources:", [d.metadata for d in documents])

if __name__ == "__main__":
    get_answer("Detail the first step of CRISPR", 3)