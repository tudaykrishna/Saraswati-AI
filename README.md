# 🪷 Saraswati AI

**Saraswati AI** is a multi-page Streamlit app for personalized learning. It combines an AI chatbot with persistent memory, a personalized AI tutor, and a learning-path planner that pulls in live web and YouTube resources. All of these run on large language models through LangChain and LangGraph.

> Named after Saraswati, the Hindu goddess of knowledge, learning, and wisdom.

---

## ✨ Features

| Page | File | What it does | Model |
|------|------|--------------|-------|
| 🏠 **Home** | `streamlit_app.py` | Landing page that introduces the app and its tools. | none |
| 🤖 **Chatbot Guru** | `chatbot.py` | Conversational assistant built as a **LangGraph** `StateGraph`. Conversation history is saved to **SQLite** (`History.sqlite`) with `SqliteSaver`, so each user profile (User1, User2, User3) keeps its own thread across sessions. | Llama 3.2 via **Ollama** (local) |
| 🧑‍🏫 **AI Tutor ("Galileo")** | `Tutor.py` | Step-by-step conversational tutor that adapts to settings you pick in the sidebar: **Depth** (Elementary → Graduate), **Learning style** (Verbal, Active, Intuitive, Reflective, Global), **Tone** (Encouraging, Neutral, Informative, Friendly, Humorous), and **Reasoning framework** (Deductive, Inductive, Abductive, Analogical, Causal). | Gemini Pro via **Google Vertex AI** |
| ✏ **Path Planner** | `Path_planner.py` | Enter a topic and get a structured course plan. It collects resources from **Tavily web search** and **YouTube search**, then has the LLM write a detailed learning roadmap that includes those links. | Llama 3.2 via **Ollama** (local) |
| 📖 **Quiz** | `Quiz.py` | 🚧 Placeholder, not built yet. | none |
| 🎙️ **Interview** | `Interview.py` | 🚧 Placeholder, not built yet. | none |

Page navigation is set up in `App.py` with [`st-pages`](https://github.com/blackary/st_pages).

---

## 🏗️ Architecture

```
                 ┌──────────────────────────┐
                 │   App.py  (st-pages nav) │
                 └────────────┬─────────────┘
     ┌───────────────┬────────┴───────┬──────────────────┐
     ▼               ▼                ▼                  ▼
 Home page     Chatbot Guru       AI Tutor          Path Planner
                    │                 │                  │
           LangGraph StateGraph   PromptTemplate   Tavily + YouTube search
                    │             | VertexAI             │
           SqliteSaver memory    (Gemini Pro)      PromptTemplate | ChatOllama
           (History.sqlite)                         (Llama 3.2)
                    │
            ChatOllama (Llama 3.2)
```

---

## 🧰 Tech Stack

- **UI:** [Streamlit](https://streamlit.io/), `streamlit-chat`, `st-pages`
- **LLM orchestration:** [LangChain](https://python.langchain.com/), [LangGraph](https://langchain-ai.github.io/langgraph/)
- **Models:** Llama 3.2 through [Ollama](https://ollama.com/); Gemini Pro through Google Vertex AI
- **Memory:** LangGraph SQLite checkpointer (`langgraph-checkpoint-sqlite`)
- **Search tools:** [Tavily](https://tavily.com/) web search, YouTube search

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/download) installed and running, with the Llama 3.2 model pulled:
  ```bash
  ollama pull llama3.2
  ```
- *(AI Tutor only)* A Google Cloud project with the Vertex AI API enabled, plus credentials (`gcloud auth application-default login`)
- *(Path Planner only)* A [Tavily API key](https://tavily.com/)

### Installation

```bash
git clone https://github.com/tudaykrishna/Saraswati-AI.git
cd Saraswati-AI

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Configuration

- **Vertex AI (Tutor):** in `Tutor.py`, set your own GCP project ID and region:
  ```python
  vertexai.init(project="<your-gcp-project>", location="us-central1")
  ```
- **Tavily (Path Planner):** set your key as an environment variable before starting the app:
  ```bash
  # Windows (PowerShell)
  $env:TAVILY_API_KEY = "tvly-..."
  # macOS / Linux
  export TAVILY_API_KEY="tvly-..."
  ```
- **Switching models:** `chatbot.py` and `Path_planner.py` contain commented-out Vertex AI code. Swap it in for `ChatOllama` if you'd rather use Gemini than a local model.

### Run the app

```bash
streamlit run App.py
```

Then open http://localhost:8501 in your browser and use the sidebar to switch pages.

---

## 📁 Project Structure

```
Saraswati-AI/
├── App.py              # Entry point: registers pages and sidebar navigation (st-pages)
├── streamlit_app.py    # Home / landing page
├── chatbot.py          # Chatbot Guru: LangGraph + SQLite-backed memory, Ollama Llama 3.2
├── Tutor.py            # Galileo AI Tutor: personalized tutoring with Vertex AI Gemini Pro
├── Path_planner.py     # Path Planner: Tavily + YouTube search, then an LLM-written roadmap
├── Quiz.py             # Quiz page (placeholder)
├── Interview.py        # Interview page (placeholder)
├── requirements.txt    # Python dependencies
└── History.sqlite      # Created at runtime: chatbot history (git-ignored)
```

---

## 🗺️ Roadmap

- [ ] AI-generated quizzes for any topic (`Quiz.py`)
- [ ] Mock interview practice with feedback (`Interview.py`)
- [ ] PDF upload and question answering in Chatbot Guru
- [ ] Working "Create User" flow in the chatbot
- [ ] Make the Vertex AI project ID configurable via an environment variable

---

## 🤝 Contributing

Contributions are welcome! Fork the repo, create a feature branch, and open a pull request.

---

## 👤 Author

**Uday Krishna Tallapalli** · [@tudaykrishna](https://github.com/tudaykrishna)
