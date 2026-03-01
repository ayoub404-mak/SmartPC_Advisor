"""
AI integration for SmartPC Advisor.
Uses Mistral API, with optional Groq fallback (free tier).
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (parent of backend/)
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env")

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

# Initialize Mistral client
mistral_client = None
if MISTRAL_API_KEY:
    try:
        from mistralai import Mistral
        mistral_client = Mistral(api_key=MISTRAL_API_KEY)
    except Exception:
        pass

# Initialize Groq client (optional fallback - free tier at console.groq.com)
groq_client = None
if GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
    except ImportError:
        pass

MISTRAL_MODEL = "mistral-small-latest"
GROQ_MODEL = "llama-3.1-8b-instant"


def generate_ai_response(prompt: str, max_tokens: int = 500) -> str:
    """
    Generate AI response. Tries Groq first (free), then Mistral.
    """
    # Try Groq first (free tier, no card, reliable)
    if groq_client:
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            pass

    # Try Mistral
    if mistral_client:
        try:
            response = mistral_client.chat.complete(
                model=MISTRAL_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            pass

    # Friendly fallback
    return (
        "Add GROQ_API_KEY to .env for free AI (console.groq.com, no card). "
        "Or fix Mistral: activate billing at admin.mistral.ai and regenerate key at console.mistral.ai/api-keys."
    )
