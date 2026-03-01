# 🤖 SmartPC Advisor

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![AI Powered](https://img.shields.io/badge/AI-Powered-FF6F00?style=for-the-badge&logo=google-gemini&logoColor=white)](#)

**SmartPC Advisor** is an intelligent hardware consultation platform. It simplifies the process of choosing, comparing, and maintaining PC hardware by leveraging cutting-edge LLMs (**Groq** & **Mistral**).

![SmartPC Advisor Dashboard](/C:/Users/hp/.gemini/antigravity/brain/3d6d471d-57b4-464e-8585-e8eb6082fbee/ai_chat_response_1772374611580.png)

---

## 🌟 Key Features

*   **🎯 Intelligent Recommendations**: Tailored specs based on your specific workflow (Creative, Gaming, Office).
*   **💬 AI Chat Expert**: Ask follow-up questions and get **specific, real-world laptop models** suggested as your next purchase.
*   **🛡️ Risk Assessment**: Analyze used laptop health (battery/SSD) with detailed risk scores and expert advice.
*   **📈 Upgrade Logic**: Technical check for RAM and storage expansion opportunities based on slots and interface types.
*   **🌍 Sustainability**: Eco-scoring based on power efficiency and thermal design.
*   **⚖️ Compare Mode**: Head-to-head comparison between two devices with AI-powered "Judgment."

---

## 🚀 Quick Start

### 1. Backend Setup (FastAPI)
```bash
# Navigate to project root
pip install -r requirements.txt

# Configure your .env with MISTRAL_API_KEY and GROQ_API_KEY
# (Refer to .env.example for structure)

# Start the server
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Frontend Setup (Static Web App)
```bash
cd frontend
# Serve locally to avoid CORS issues
python -m http.server 8081
# Access at http://localhost:8081
```

---

## 📂 Architecture

```text
smartpc-advisor/
├── backend/          # FastAPI Python Server
│   ├── main.py       # API Route Definitions
│   ├── ai_service.py # Groq & Mistral integration
│   ├── models.py     # Pydantic Data Schemas
│   ├── scoring.py    # Match & Future-Proof algorithms
│   └── ...           # Modular logic files
├── frontend/         # Web Interface
│   ├── index.html    # UI Structure (Tailwind)
│   ├── form.js       # App Logic & Chat interactivity
│   └── style.css      # Design & Chat Animations
├── .env              # Secrets & Keys
└── requirements.txt  # Dependencies
```

---

## 🔮 Future Roadmap

We aim to make SmartPC Advisor the #1 tool for hardware enthusiasts:
- [ ] **📊 Market Integration**: Live pricing and stock status from Amazon/Newegg/BestBuy.
- [ ] **🖥️ Smart Diagnostics**: A lightweight desktop client to auto-detect your local system health.
- [ ] **☁️ Cloud Sync**: Save your builds and comparisons to your personal account.
- [ ] **🛠️ PC Builder Pro**: Full desktop component compatibility checker (CPU/Motherboard/RAM).

---

## 📜 License
Internal Prototype - Licensed under the MIT License for the Hackathon.

---
*Built with ❤️ for the Hackathon community. Helping you build the future, one byte at a time.*
