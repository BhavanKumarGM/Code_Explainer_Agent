# 🧠 Code Explainer Agent

> An AI-powered Code Explainer that understands, analyzes, and explains entire codebases using **Qwen 2.5** running locally through **Ollama**. Built with a privacy-first approach, the entire application operates offline without relying on any cloud-based AI services.

---

## 📖 Overview

Code Explainer Agent is a local-first AI assistant designed to help developers understand unfamiliar codebases quickly. Simply upload a project or repository, and the agent analyzes the complete source code, builds contextual understanding, and answers questions about the architecture, execution flow, dependencies, and implementation details.

Unlike cloud-based coding assistants, all AI inference runs locally on your machine using **Qwen 2.5** via **Ollama**, ensuring that your source code never leaves your computer.

---

# ✨ Features

## 📂 Repository Analysis

* Upload an entire project as a ZIP archive
* Analyze complete folder structures
* Parse thousands of source files
* Support multi-language repositories
* Automatic project indexing

---

## 🧠 Code Understanding

* Explain complete repositories
* Explain files and modules
* Explain classes and methods
* Explain functions line by line
* Identify project architecture
* Detect design patterns
* Trace execution flow
* Analyze dependencies
* Understand configuration files

---

## 💬 AI Chat

Ask questions such as:

* Explain this project.
* How does authentication work?
* Where is the database connection initialized?
* Explain this API.
* How does JWT work here?
* Which module handles payments?
* Explain this function.
* Find where this class is used.
* Why am I getting this error?
* Explain this algorithm.

---

## 🔍 Semantic Search

* Context-aware code search
* Function search
* Class search
* API search
* Configuration search
* Dependency search

---

## 🔒 Privacy First

Your source code never leaves your machine.

This project **does not use**:

* ❌ OpenAI API
* ❌ Anthropic API
* ❌ Gemini API
* ❌ Groq API
* ❌ OpenRouter API
* ❌ Claude API
* ❌ Any cloud-hosted LLM

Everything runs locally through **Ollama**.

---

# 🏗 Architecture

```text
                     User
                       │
                       ▼
              React Frontend
                       │
                       ▼
               FastAPI Backend
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
 Repository Parser            Chat Service
        │                             │
        └──────────────┬──────────────┘
                       ▼
              Chunking & Parsing
                       │
                       ▼
              Embedding Generator
                       │
                       ▼
             Local Vector Database
                       │
                       ▼
                Ollama Server
                       │
                       ▼
                  Qwen 2.5
```

---

# ⚙️ Tech Stack

## Frontend

* React
* TypeScript
* Tailwind CSS
* Vite

## Backend

* Python
* FastAPI
* LangChain

## AI

* Qwen 2.5
* Ollama
* Local Embedding Model
* Retrieval-Augmented Generation (RAG)

## Database

* ChromaDB / FAISS
* SQLite

---

# 🚀 Workflow

### Step 1

Upload a project ZIP file.

or

Select an existing repository.

↓

### Step 2

The repository is extracted locally.

↓

### Step 3

The parser scans:

* Folder structure
* Source files
* Classes
* Functions
* Imports
* Dependencies
* Configuration files

↓

### Step 4

Source code is divided into semantic chunks.

↓

### Step 5

Embeddings are generated locally.

↓

### Step 6

Embeddings are stored in the local vector database.

↓

### Step 7

User asks a question.

↓

### Step 8

Relevant code is retrieved.

↓

### Step 9

Qwen 2.5 generates a contextual explanation.

---

# 📁 Project Structure

```text
Code-Explainer-Agent/

├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   └── assets/
│
├── backend/
│   ├── api/
│   ├── parser/
│   ├── rag/
│   ├── embeddings/
│   ├── services/
│   ├── models/
│   ├── utils/
│   └── main.py
│
├── uploads/
├── vectordb/
├── models/
├── README.md
└── requirements.txt
```

---

# 🖥 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/Code-Explainer-Agent.git

cd Code-Explainer-Agent
```

---

## Backend

```bash
cd backend

pip install -r requirements.txt
```

---

## Frontend

```bash
cd frontend

npm install
```

---

# 🤖 Install Ollama

Download and install Ollama for your operating system.

Start the Ollama server:

```bash
ollama serve
```

Download the Qwen 2.5 model:

```bash
ollama pull qwen2.5
```

Verify installation:

```bash
ollama list
```

---

# ▶ Running the Backend

```bash
uvicorn main:app --reload
```

---

# ▶ Running the Frontend

```bash
npm run dev
```

---

# 🌐 Local URLs

| Service  | URL                    |
| -------- | ---------------------- |
| Frontend | http://localhost:5173  |
| Backend  | http://localhost:8000  |
| Ollama   | http://localhost:11434 |

---

# ⚙ Configuration

```python
OLLAMA_URL = "http://localhost:11434"

MODEL_NAME = "qwen2.5"

EMBEDDING_MODEL = "nomic-embed-text"
```

No API keys are required.

---

# 💬 Example Prompts

```text
Explain this repository.
```

```text
Describe the project architecture.
```

```text
How does authentication work?
```

```text
Explain the API flow.
```

```text
Where is the database initialized?
```

```text
Explain this class.
```

```text
Explain this function.
```

```text
Which files handle routing?
```

```text
Find all usages of UserService.
```

```text
Why is this code throwing an exception?
```

---

# 🎯 Use Cases

* Learning unfamiliar repositories
* Understanding legacy code
* Code reviews
* Architecture exploration
* Developer onboarding
* Debugging
* Documentation generation
* Educational purposes

---

# 🔮 Roadmap

* Multi-Agent Architecture
* Code Editing Agent
* Repository Refactoring
* Git Integration
* GitHub Repository Cloning
* UML Diagram Generation
* Documentation Generator
* Test Case Generation
* Session Memory
* Multi-Repository Support
* Workspace Management

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.
---

# ⭐ Support

If you find this project useful, consider giving it a **Star ⭐** on GitHub.
