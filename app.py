import gradio as gr
from chains import create_qa_chain, create_summary_chain
from vectorstore import get_vectorstore
from utils import load_document, chunk_documents
from langchain_core.messages import HumanMessage, AIMessage

qa_chain = None

def ingest_file(file):
    global qa_chain

    if not file:
        return "No file selected.", ""

    try:
        docs = load_document(file.name)
        if not docs:
            return "No readable text found in file.", ""

        chunks = chunk_documents(docs)
        if not chunks:
            return "File processed but no meaningful chunks created.", ""

        vectorstore = get_vectorstore()
        vectorstore.add_documents(chunks)

        qa_chain = create_qa_chain()

        summary_chain = create_summary_chain()
        full_text = "\n".join(d.page_content for d in docs)
        summary = summary_chain.invoke(full_text[:15000])

        return (
            f"Document processed successfully\n"
            f"• Pages extracted: {len(docs)}\n"
            f"• Chunks created: {len(chunks)}",
            summary
        )

    except Exception as e:
        return f"Processing failed: {str(e)}", ""


async def chat_stream(message, history):
    if qa_chain is None:
        yield history + [{"role": "user", "content": message},
                         {"role": "assistant", "content": "Please upload and process a document first."}]
        return

    # Convert Gradio history (list of dicts) → LangChain messages
    messages = []
    for msg in history:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))

    full_answer = ""

    try:
        async for chunk in qa_chain.astream({
            "question": message,
            "chat_history": messages
        }):
            full_answer += chunk
            yield history + [{"role": "user", "content": message},
                             {"role": "assistant", "content": full_answer}]

        # Final yield
        yield history + [{"role": "user", "content": message},
                         {"role": "assistant", "content": full_answer}]

    except Exception as e:
        error_msg = f"Error during generation: {str(e)}"
        yield history + [{"role": "user", "content": message},
                         {"role": "assistant", "content": error_msg}]


def clear_chat():
    return []


with gr.Blocks(title="Smart Contract Summary & Q&A Assistant") as demo:
    gr.Markdown("# Smart Contract Summary & Q&A Assistant")
    gr.Markdown(
        "**Disclaimer:** This is a demonstration tool only. "
        "It is **not** legal advice and should not be used as such."
    )

    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(
                label="Upload PDF or DOCX contract",
                file_types=[".pdf", ".docx"]
            )
            ingest_btn = gr.Button("Process Document", variant="primary")
            status = gr.Textbox(label="Status", interactive=False)
            summary_output = gr.Markdown(label="Contract Summary (optional)")

        with gr.Column(scale=3):
            chatbot = gr.Chatbot(height=500)
            msg = gr.Textbox(
                placeholder="Ask a question about the contract...",
                container=False,
                lines=1
            )
            with gr.Row():
                submit_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.Button("Clear Chat")

    ingest_btn.click(
        ingest_file,
        inputs=file_input,
        outputs=[status, summary_output],
        queue=False
    )

    msg.submit(
        chat_stream,
        inputs=[msg, chatbot],
        outputs=chatbot,
        queue=True
    )

    submit_btn.click(
        chat_stream,
        inputs=[msg, chatbot],
        outputs=chatbot,
        queue=True
    )

    clear_btn.click(
        clear_chat,
        outputs=chatbot
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=True
    )