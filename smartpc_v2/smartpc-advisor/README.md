# SmartPC Advisor

AI-powered PC & laptop recommendation and analysis tool. Built for hackathons with FastAPI, Mistral AI, and TailwindCSS.

## Quick Start

### 1. Backend

```bash
cd smartpc-advisor
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your MISTRAL_API_KEY
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend

Open `frontend/index.html` in a browser, or serve it:

```bash
cd frontend
python -m http.server 8080
# Open http://localhost:8080
```

**Note:** If using `file://`, CORS may block API calls. Use a local server or run the frontend from the same origin.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/recommend-specs` | POST | User needs → baseline specs + AI explanation |
| `/compare-laptops` | POST | Two laptops → comparison + scores |
| `/risk-check` | POST | Health data → risk score + AI explanation |
| `/upgrade-path` | POST | RAM slots + storage → upgradeability advice |
| `/sustainability` | POST | Battery, power, thermal → eco score |
| `/budget-stretch` | POST | Budget → trade-off suggestions |

## Project Structure

```
smartpc-advisor/
├── backend/
│   ├── main.py           # FastAPI entrypoint
│   ├── ai_service.py     # Mistral API integration
│   ├── scoring.py        # Match + future-proof scores
│   ├── risk_analyzer.py  # Used laptop risk logic
│   ├── upgrade_advisor.py # Upgrade path logic
│   ├── sustainability.py # Eco score logic
│   └── models.py         # Pydantic models
├── frontend/
│   ├── index.html
│   ├── form.js
│   └── style.css
└── requirements.txt
```

## Environment

- `MISTRAL_API_KEY` – Required for AI explanations. Without it, fallback messages are shown.
