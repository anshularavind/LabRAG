from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pathlib import Path

txt_file = Path(__file__).resolve().parent.parent / "data" / "somefile.txt"
with open(txt_file, 'r', encoding="utf-8") as f:
    text = f.read()

chunker = RecursiveCharacterTextSplitter(
    chunk_size = 30, 
    chunk_overlap = 5)

chunks = chunker.split_text(text)

vstore = Chroma.from_documents(documents=chunks, embedding=OpenAIEmbeddings())

retriever = vstore.as_retriever()
