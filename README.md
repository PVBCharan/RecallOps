# RecallOps

**A Multimodal, Cross-Domain Experience-Aware AI Decision Support Platform**

> Help people learn from experience by turning text, visual evidence, and statistical information into structured, retrievable knowledge that supports traceable, context-sensitive decisions.

Built for **HackwithHyderabad 3.0** | Cost: ₹0 | Fully Local

---

## ✨ Features

- **Multimodal Evidence Processing** — Text, CSV, images, and video
- **Experience Memory** — Stores structured outcomes with context, action, and verification status
- **Contextual Retrieval** — Finds similar past experiences to inform new decisions
- **AI Recommendations** — LLM-powered analysis grounded in evidence and past outcomes
- **Outcome Feedback Loop** — Record whether recommendations worked, building better memory over time
- **4 Domain Support** — Commercial Ops, Healthcare, Defence, Education with domain-specific guardrails
- **Fully Local** — No paid APIs, runs on your laptop

## 🏗️ Architecture

```
Web Interface (HTML/CSS/JS)
        │
  Flask Backend (Python)
        │
   ┌────┼────┐
   │    │    │
 Text Image CSV/Data
   │    │    │
   └────┼────┘
        │
  Evidence Synthesis
        │
   ┌────┼────┐
   │    │    │
Hindsight Domain  Local LLM
 Memory   Rules  (Ollama)
   │    │    │
   └────┼────┘
        │
  Recommendation Engine
        │
  Human Review & Feedback
        │
  Experience Memory Update
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Ollama** (optional, for AI-powered analysis): [ollama.ai](https://ollama.ai)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-team/recallops.git
cd recallops

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment config
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux

# Run the application
python run.py
```

Visit **http://localhost:5000** in your browser.

### Optional: Enable AI Features

```bash
# Install and start Ollama
ollama pull llama3.2          # Text model (~2GB)
ollama pull llava             # Vision model (~4GB)
ollama serve                  # Start the server
```

> **Note:** Core case management works without Ollama. AI analysis features require it.

## 📁 Project Structure

```
recallops/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── routes/
│   │   ├── main.py           # Dashboard, status
│   │   ├── cases.py          # Case CRUD, uploads, feedback
│   │   └── api.py            # JSON API endpoints
│   ├── services/
│   │   ├── database.py       # SQLite data layer
│   │   ├── llm_service.py    # Ollama integration
│   │   ├── hindsight_service.py  # Experience memory
│   │   ├── image_service.py  # Image validation & analysis
│   │   ├── video_service.py  # Frame extraction & analysis
│   │   ├── data_analysis_service.py  # CSV stats & charts
│   │   └── recommendation_service.py # Evidence synthesis & recommendations
│   ├── domain_rules/         # Domain config & guardrails
│   ├── templates/            # Jinja2 HTML templates
│   └── static/               # CSS, JS, images
├── data/
│   └── synthetic/            # Demo CSV datasets
├── uploads/                  # User uploads (git-ignored)
├── run.py                    # Entry point
├── requirements.txt
└── README.md
```

## 🎯 Demo Scenarios

### 1. Commercial Operations (Primary)
Submit a server incident with metrics CSV → Get recommendation based on past incidents

### 2. Healthcare
Upload synthetic patient metrics → See trend analysis for professional review

### 3. Defence
Submit equipment maintenance case with sensor data → Retrieve similar maintenance records

### 4. Education
Track student learning progress → Get personalized exercise recommendations

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | System health check |
| `/api/domains` | GET | List domain configurations |
| `/api/cases` | GET | List all cases |
| `/api/cases/<id>` | GET | Get case details |
| `/api/experiences` | GET | List stored experiences |
| `/api/search?q=...` | GET | Search experiences |

## ⚠️ Important Notices

- **Advisory Only** — All recommendations require human review
- **Synthetic Data** — Demo data is synthetic and fictional
- **Not Production-Ready** — This is a hackathon prototype
- **No Diagnosis** — The healthcare domain does NOT provide medical diagnosis
- **No Combat Decisions** — The defence domain is limited to maintenance support

## 📋 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python + Flask |
| Database | SQLite |
| LLM | Ollama (llama3.2, llava) |
| Memory | Hindsight (self-hosted) |
| Data Analysis | Pandas, NumPy, Matplotlib |
| Video | OpenCV |
| Images | Pillow |

## 📄 License

MIT License — See LICENSE file for details.
