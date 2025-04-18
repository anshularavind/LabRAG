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


def define_get_vectorstore_for_protocol(protocol: str) -> Chroma:
    matches = [p for p in data_dir.glob("*.txt") if protocol.lower() in p.stem.lower()]
    if not matches:
        raise ValueError(f"No protocol files found containing '{protocol}' in {data_dir}")

    store_dir = persist_dir / protocol.lower()
    store_dir.mkdir(parents=True, exist_ok=True)

    if not any(store_dir.iterdir()):
        splitter = RecursiveCharacterTextSplitter(chunk_size=30, chunk_overlap=5)
        documents = []
        ids = []
        for path in matches:
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
            persist_directory=str(store_dir),
            collection_name=protocol.lower()
        )
    else:
        vstore = Chroma(
            persist_directory=str(store_dir),
            embedding_function=EMBEDDINGS,
            collection_name=protocol.lower()
        )
    return vstore


def get_answer_for_protocol(protocol: str, query: str, k: int):
    vstore = define_get_vectorstore_for_protocol(protocol)
    docs = vstore.similarity_search(query, k)

    system_prompt = "Try to answer the question using the provided context."
    context = "\n\n".join(f"{i+1}. {d.page_content}" for i, d in enumerate(docs))
    user_prompt = f"\n\nQuestion: {query}\nAnswer briefly."
    prompt = f"{system_prompt}\n\nContext:\n{context}{user_prompt}"

    llm = ChatOpenAI(model_name="gpt-4.1-nano")
    answer = llm.invoke(prompt)

    sources = [{"source": d.metadata["source"], "chunk_index": d.metadata["chunk_index"]} for d in docs]
    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    result = get_answer_for_protocol("Transfection", 
                                    "What would I do if i do not have a 96 well plate", 
                                    k=3)
    print("Answer:", result["answer"])
    print("Sources:", result["sources"])
