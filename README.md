
# Smart Contract Summary & Q&A Assistant

A small-scale **Retrieval-Augmented Generation (RAG)** web application that allows users to upload PDF or DOCX legal documents (contracts, NDAs, insurance policies, etc.) and ask natural-language questions about their content. The system extracts text, chunks it intelligently, embeds it using sentence transformers, stores embeddings in a local Chroma vector database, and answers questions using OpenRouter's Aurora model with source citations and basic guardrails.

**Important Disclaimer**  
This application is a **demonstration / educational prototype** built as part of an NVIDIA DLI-aligned workshop project.  
**It is NOT a substitute for professional legal advice.**  
All outputs should be treated as informational only.

## Project Goals (as defined in specification)

- Demonstrate end-to-end RAG pipeline using LangChain  
- Handle long-form document processing (PDF/DOCX)  
- Provide grounded answers with inline source citations  
- Include basic hallucination guardrails via prompt engineering  
- Offer optional document summarization  
- Deliver clean Gradio UI with upload + chat tabs  
- Run entirely locally (except LLM calls via OpenRouter API)  
- Include basic evaluation capability

## Features

- Upload & process PDF or DOCX files  
- Persistent local vector store (Chroma)  
- Conversational Q&A with chat history  
- Answers include inline citations `[1]`, `[2]` and source list  
- Basic safety prompt: refuses to speculate beyond provided text  
- Optional one-click contract summarization  
- Simple evaluation script using predefined QA pairs

## Technology Stack

- **LLM**: Aurora (via OpenRouter)  
- **Embeddings**: `all-MiniLM-L6-v2` (Sentence Transformers – local)  
- **Framework**: LangChain (LCEL chains)  
- **Vector Store**: Chroma (persistent)  
- **UI**: Gradio  
- **Document loading**: PyPDF + python-docx  
- **Chunking**: RecursiveCharacterTextSplitter (legal-aware separators)

## Project Structure

```
smart-contract-rag-assistant/
├── app.py                  # Main script – launches Gradio UI
├── chains.py               # QA chain, summarization chain
├── prompts.py              # All prompt templates
├── vectorstore.py          # Chroma vector store setup
├── utils.py                # File loading, chunking helpers
├── data/
│   └── chroma_db/          # Persistent Chroma database (auto-created)
├── samples/                # Recommended place for test contract PDFs
├── tests/
│   ├── eval_qa.py          # Basic evaluation runner
│   └── qa_pairs.json       # Test questions + expected snippets
├── .env                    # API key
├── requirements.txt
└── README.md
```


## Prerequisites
```
- Python 3.10 – 3.12 (3.11 recommended)  
- Git (optional)  
- Internet connection (for pip install + OpenRouter API calls)
```
## Quick Start – How to Run

### 1. Clone or download the project

```bash
git clone <your-repo-url> smart-contract-rag-assistant
cd smart-contract-rag-assistant
```

(or unzip the downloaded folder)

### 2. Create and activate virtual environment (strongly recommended)

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file in the root folder

Create file named `.env` and paste:

```text
OPENAI_API_KEY=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
```

(This is the OpenRouter-compatible key already used in the code.)

### 5. (Optional but recommended) Add sample documents

Create folder `samples/` and place 2–5 NDA / contract PDFs inside.

Good free sources:

- https://eforms.com/nda/ → download sample PDFs  
- https://nondisclosureagreement.com/ → Basic NDA, Mutual NDA PDFs  
- https://legaltemplates.net/form/non-disclosure-agreement → free PDF

### 6. Launch the application

```bash
python app.py
```

(or `python3 app.py` on some systems)

Gradio will start and show:

```
Running on local URL:  http://127.0.0.1:7860
```

Open this address in your browser.

### 7. How to use the interface

1. **Upload tab** → drag & drop or select a PDF/DOCX contract  
2. Click **Process Document** → wait until status says "processed successfully"  
3. **Chat area** → ask questions about the document  
   Examples:
   - Who are the parties to this agreement?  
   - What is considered Confidential Information?  
   - How long does the confidentiality obligation last?  
   - What happens if there is a breach?

Answers should include `[1]`, `[2]` citations and a sources list at the end.

## Resetting the knowledge base

If you want to start fresh with a new document:

- Delete the folder `data/chroma_db/`  
- Restart the application → upload new file

## Running Evaluation (Day 9 deliverable)

After processing one contract:

```bash
python tests/eval_qa.py
```

This will run the questions from `qa_pairs.json` and print basic pass/fail metrics (contains expected phrase + has citations).

## Limitations & Known Issues

- Only English documents supported  
- Performance depends on document size (aim for < 20 pages for <5s response)  
- Aurora model can be inconsistent — answers may occasionally lack citations  
- No multi-document support in this version  
- API calls go through OpenRouter (requires internet & quota)

## Future Improvements (out of current scope)

- Multi-document / session management  
- Local LLM fallback (Ollama, Llama.cpp)  
- Better citation parsing & highlighting  
- LangServe microservice endpoints  
- Docker support

## License

MIT License (feel free to use and modify for educational purposes)

---

Built as part of NVIDIA DLI-aligned LangChain RAG workshop project – February 2026
```

This README is:

- Self-contained  
- Follows professional structure  
- Includes exact commands  
- Contains clear warnings and disclaimers  
- Explains both quick usage and development context  

- Matches the project specification goals and deliverables


