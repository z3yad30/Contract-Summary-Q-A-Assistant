from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

# How each retrieved chunk should be rendered in the prompt
DOCUMENT_PROMPT = PromptTemplate.from_template(
    "[{idx}] {page_content}\n(source: {source}, page {page})"
)

QA_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     """You are a helpful contract analysis assistant.
Answer ONLY using the provided context excerpts.
Use inline citations [1], [2], ... exactly as they appear.
At the end of your answer, list the sources used (if any).

Context excerpts:
{context}

If the question cannot be answered fully from the provided excerpts, you may say so, 
but try to provide any related information that is present and clearly mark what is uncertain.

Do NOT speculate, hallucinate, or provide legal advice."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

SUMMARIZE_PROMPT = ChatPromptTemplate.from_template(
    """Provide a concise, structured summary of the following contract text.
Focus on: parties involved, purpose, key obligations, duration, termination, confidentiality.
Use bullet points.

Text:
{text}"""
)