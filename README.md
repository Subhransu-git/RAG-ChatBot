# Enterprise Policy RAG Chatbot

A local-first Retrieval-Augmented Generation (RAG) chatbot that helps users search organizational policies and documents using natural-language questions.

## Overview

Finding information in lengthy organizational policies can be time-consuming. This project combines semantic document retrieval with a locally hosted Mistral 7B language model to help users retrieve relevant policy information through a conversational interface.

Users can upload documents, build a searchable vector index, ask questions, and view source-document references associated with the retrieved information.

The application is built with Streamlit, FAISS, Sentence Transformers, and Ollama.

## Key Features

- **Document upload:** Upload PDF, DOCX, TXT, and CSV documents through the Streamlit interface.
- **Document ingestion:** Extract text from supported formats and divide it into smaller chunks.
- **Semantic search:** Generate text embeddings using `all-MiniLM-L6-v2`.
- **Vector search:** Use FAISS to retrieve relevant document chunks.
- **Local language model:** Generate answers using Mistral 7B through Ollama.
- **Source references:** Display the filenames associated with retrieved information.
- **Interactive interface:** Ask policy-related questions through a Streamlit chat interface.
- **PDF OCR support:** Attempt text extraction from scanned PDFs using Tesseract OCR and PDF-to-image conversion.
- **Terminal testing:** Use a command-line script to test the retrieval and answer-generation pipeline.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | User interface |
| Mistral 7B | Answer generation |
| Ollama | Local language-model runtime |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX document extraction |
| Pandas | CSV processing |
| Tesseract OCR | Text extraction from scanned PDFs |

## Architecture

1. **Document upload:** Users upload organizational documents through the interface.
2. **Text extraction:** The ingestion module extracts text from supported document formats.
3. **Chunking:** Extracted text is divided into smaller chunks for retrieval.
4. **Embedding generation:** Sentence Transformers converts document chunks into vector representations.
5. **Index creation:** FAISS stores the vectors for similarity search.
6. **Question processing:** A user's question is converted into an embedding.
7. **Context retrieval:** FAISS retrieves relevant document chunks and their source filenames.
8. **Answer generation:** The retrieved context and question are passed to Mistral 7B through Ollama.
9. **Response display:** The interface displays the generated answer and source references.

## Project Structure

```text
RAG-chatbot/
├── app.py
├── testrag.py
├── requirements.txt
├── .gitignore
└── backend/
    ├── ingest.py
    ├── mistral_model.py
    ├── rag.py
    └── upload.py
```

Generated indexes, uploaded documents, and locally stored models are not included in the repository.

## Prerequisites

- Python 3
- pip
- Ollama
- Sufficient RAM and storage for the selected language model
- The embedding model `all-MiniLM-L6-v2`
- Tesseract OCR and Poppler if scanned-PDF OCR is required

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Subhransu-git/RAG-chatbot.git
cd RAG-chatbot
```

### 2. Create a virtual environment

On Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
```

On Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set up Ollama

Install Ollama from its official website:

https://ollama.com/

Download the model used by the application:

```bash
ollama pull mistral:7b-instruct-q4_K_M
```

Ensure the Ollama service is running and the model is available locally.

### 5. Prepare the embedding model

The application loads `all-MiniLM-L6-v2` with local-only model loading enabled. Make sure this model has been downloaded and is available in the local Sentence Transformers cache before starting the application.

### 6. Prepare the document directory

The application creates an `uploads/` directory for uploaded documents. Only use documents that you are authorized to process.

### 7. Build the vector index

After placing documents in the expected upload directory, run:

```bash
python backend/ingest.py
```

This generates the FAISS index and document metadata files used by the retrieval module.

### 8. Start the application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit in your browser.

## Offline and Privacy Considerations

This project is designed for local language-model inference through Ollama.

After dependencies, the language model, and the embedding model have been downloaded, the core inference pipeline can be configured to run without sending prompts to a hosted language-model API.

However, fully offline operation has not yet been independently verified. Model downloads, dependency installation, and some OCR workflows may require internet access during setup.

For confidential organizational use, deploy on an approved machine or network, restrict access to uploaded files, and verify that logs, backups, indexes, and temporary files do not expose sensitive information.

The current application should be treated as a prototype until access control, secure document storage, and production error handling have been implemented and tested.

## Limitations

- Retrieval quality depends on document extraction, chunking, embeddings, and search settings.
- The current implementation uses similarity search and does not provide a complete enterprise permission system.
- Source references identify retrieved filenames; page-level citations are not currently implemented.
- Document persistence and index rebuilding should be tested when adding, replacing, or deleting files.
- Generated answers may be incomplete or incorrect and should be checked against the original policy.
- Large models require suitable local hardware and memory.

## Future Improvements

- Add authentication and role-based document access.
- Support document deletion and incremental index updates.
- Add page-level citations and direct source excerpts.
- Improve retrieval with configurable chunk sizes and reranking.
- Add document versioning and audit logs.
- Add automated tests for ingestion, retrieval, and answer generation.
- Add encrypted storage and secure handling of confidential documents.
- Improve error handling and model health checks.

## Author

**Subhransu**

GitHub: https://github.com/Subhransu-git

## License

This project is licensed under the MIT License. See the LICENSE file for details.
