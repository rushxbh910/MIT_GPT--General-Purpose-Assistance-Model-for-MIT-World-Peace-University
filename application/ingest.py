import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings    
from langchain.schema import Document
import os
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv(r"D:\MIT_GPT_proj25\data\mit_wpu_docs\indexednewtrans.csv")

documents = []
for _, row in df.iterrows():
    if pd.notna(row["answer"]):
        doc = Document(
            page_content=row["answer"],  # <- Embed answer only
            metadata={"question": row["question"]}  # optional
        )
        documents.append(doc)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectordb = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory=os.getenv("CHROMA_PATH")
)
vectordb.persist()
