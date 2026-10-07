# 🚀 Startup Validator AI

An AI-powered startup idea validation platform that analyzes a startup concept across **market demand, competition, customer personas, pricing, MVP scope, business potential, and overall feasibility** — delivering a structured validation report with a deterministic score.

---

## 📌 Overview

Startup Validator AI helps founders evaluate a startup idea **before** investing significant time and resources into building it.

The user provides:
- **Startup idea / concept** — a detailed description of the value proposition
- **Target country** — the primary market (e.g., India, United States)
- **Target region** — state, city, or region within the target country

The system then processes the idea through **9 specialized AI analysis agents** and generates a comprehensive validation report.

---

## 🎯 What It Evaluates

| Analysis Stage | Description |
|----------------|-------------|
| Idea Analysis | Breaks down the core problem, solution, and target customer |
| Market Research | Evaluates market demand, size, trends, and growth potential |
| Competitor Analysis | Maps existing competitors, their strengths, weaknesses, and market gaps |
| Customer Personas | Generates detailed buyer personas with demographics and pain points |
| SWOT Analysis | Strengths, Weaknesses, Opportunities, and Threats breakdown |
| Pricing Analysis | Recommends pricing models, unit economics, and revenue strategies |
| MVP Analysis | Scopes minimum viable product features, tech stack, and timeline |
| 7-Point Evaluation | Evidence-backed scoring across 7 criteria using RAG knowledge base |
| Overall Validation Score | Weighted deterministic score (0–100) with verdict classification |

---

## 🏗️ Architecture

```
                    USER
                      |
                      v
              React Frontend
                      |
                      | HTTP POST
                      v
              FastAPI Backend
                      |
                      v
           Startup Validation Pipeline (LangGraph)
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
   Idea Analysis   Market       Competitor
                  Research       Analysis
        |             |             |
        +-------------+-------------+
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
     Personas        SWOT        Pricing
        |             |             |
        +-------------+-------------+
                      |
                      v
                    MVP
                      |
                      v
              RAG Knowledge Base (ChromaDB)
                      |
                      v
              Evidence Retrieval
                      |
                      v
             7-Point Evaluation
                      |
                      v
              Overall Validation
                      |
                      v
              React Dashboard
```

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** — REST API framework
- **LangGraph** — Multi-agent orchestration with state checkpointing
- **Groq** — LLM inference (structured JSON output)
- **ChromaDB** — Vector store for RAG knowledge base
- **Tavily** — Web search tool for real-time research
- **Pydantic** — Data validation and settings management
- **SQLite** — LangGraph checkpoint persistence

### Frontend
- **React 19** — UI framework
- **Vite 8** — Build tool and dev server
- **TailwindCSS v4** — Utility-first styling
- **Lucide React** — Icon library

---

## ⚡ Getting Started

### Prerequisites
- Python 3.11 or higher
- Node.js 18+ and npm
- A [Groq API key](https://console.groq.com/)
- A [Tavily API key](https://tavily.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/startup-validator-ai.git
cd startup-validator-ai
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API keys
```

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key for LLM inference |
| `TAVILY_API_KEY` | Your Tavily API key for web search |

### 4. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 5. Run the Application

**Terminal 1 — Start the backend:**

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — Start the frontend:**

```bash
cd frontend
npm run dev
```

Open your browser at **http://localhost:5173**

---

## 📡 API Reference

### Health Check

```
GET /
```

Response:
```json
{
  "message": "AI Startup Idea Validation API is running."
}
```

### Validate Startup Idea

```
POST /api/validate-startup
```

Request body:
```json
{
  "startup_idea": "A subscription-based healthy meal delivery service for working professionals in Pune...",
  "target_country": "India",
  "target_region": "Maharashtra"
}
```

Response includes: `overall_score`, `verdict`, `summary`, `key_strengths`, `key_weaknesses`, `opportunities`, `threats`, `market_research`, `competitor_analysis`, `persona_analysis`, `pricing_analysis`, `mvp_analysis`, `evaluation`, and `research_sources`.

---

## 📂 Project Structure

```
startup-validator-ai/
├── app/
│   ├── agents/          # 9 AI analysis agents
│   ├── config/          # Pydantic settings
│   ├── graph/           # LangGraph pipeline, nodes, state
│   ├── rag/             # ChromaDB vectorstore, ingestion, retrieval
│   ├── schemas/         # Pydantic request/response models
│   ├── scoring/         # Deterministic weighted scoring engine
│   ├── tools/           # Web search integration (Tavily)
│   ├── utils/           # LLM utilities, caching, output parsing
│   └── main.py          # FastAPI application entry point
├── frontend/
│   ├── src/
│   │   ├── components/  # 13 React components
│   │   ├── services/    # API client
│   │   ├── App.jsx      # Main application
│   │   └── main.jsx     # React entry point
│   ├── index.html
│   └── package.json
├── data/
│   └── documents/       # RAG knowledge base documents
├── tests/               # Test suite
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── README.md
```

---

## 🧪 Running Tests

```bash
# Activate virtual environment first
pytest tests/ -v
```

> **Note:** Tests invoke the full AI pipeline and require valid API keys in `.env`.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com/) — Ultra-fast LLM inference
- [LangGraph](https://github.com/langchain-ai/langgraph) — Multi-agent orchestration
- [ChromaDB](https://www.trychroma.com/) — Vector database for RAG
- [Tavily](https://tavily.com/) — AI-optimized web search
- [FastAPI](https://fastapi.tiangolo.com/) — Modern Python web framework
- [Vite](https://vitejs.dev/) — Next-generation frontend build tool
