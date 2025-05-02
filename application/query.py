from langchain.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from application.prompts import QA_PROMPT
import os
from dotenv import load_dotenv

load_dotenv()


def get_chain():
    # Load local GGUF model via LlamaCpp
    llm = LlamaCpp(
        model_path=os.getenv("MODEL_PATH"),
        temperature=0.5,
        max_tokens=512,
        n_ctx=2048,
        verbose=False
    )

    # Load embeddings and persistent vector DB
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(
        persist_directory=os.getenv("CHROMA_PATH"),
        embedding_function=embeddings
    )

    # Use top-k retrieval for answer grounding
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    # Retrieval-Augmented QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": QA_PROMPT}
    )
    return qa_chain

def ask_question(query: str):
    chain = get_chain()
    return chain.run(query)

def debug_retrieval(query):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=os.getenv("CHROMA_PATH"), embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 10})
    
    docs = retriever.get_relevant_documents(query)
    print("\n🔍 Top Retrieved Chunks:")
    for doc in docs:
        print("→", doc.page_content)

