from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from prompts import QA_PROMPT, SUMMARIZE_PROMPT, DOCUMENT_PROMPT
from vectorstore import get_vectorstore
import os

os.environ["OPENAI_API_KEY"] = "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"

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="openrouter/aurora-alpha",
    temperature=0.1,
    streaming=True,
)

retriever = None

def format_docs(docs):
    print("\nRetrieved chunks:")
    for i, doc in enumerate(docs, 1):
        print(f"[{i}] {doc.page_content[:200]}... (page {doc.metadata.get('page', '?')})")
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown").split('\\')[-1]  # cleaner filename
        page = doc.metadata.get("page", "?")
        formatted.append(f"[{i}] {doc.page_content.strip()}\n(source: {source}, page {page})")
    return "\n\n".join(formatted)

def create_qa_chain():
    global retriever
    if retriever is None:
        vectorstore = get_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(retriever.invoke(x["question"]))
        )
        | QA_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain

def create_summary_chain():
    return (
        {"text": RunnablePassthrough()}
        | SUMMARIZE_PROMPT
        | llm
        | StrOutputParser()
    )