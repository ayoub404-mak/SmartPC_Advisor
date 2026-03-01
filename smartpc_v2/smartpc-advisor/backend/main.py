"""
SmartPC Advisor - FastAPI Backend
Hackathon-ready PC/laptop recommendation and analysis API.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.models import (
    UserNeeds,
    Laptop,
    HealthData,
    UpgradeInput,
    BudgetStretchInput,
    SustainabilityInput,
    LaptopSpecs,
    ChatInput,
    ChatMessage,
)
from backend.ai_service import generate_ai_response
from backend.scoring import calculate_match_score, future_proof_score
from backend.risk_analyzer import risk_score_from_health
from backend.upgrade_advisor import check_upgradeability_from_input
from backend.sustainability import eco_score_from_input

app = FastAPI(
    title="SmartPC Advisor",
    description="AI-powered PC/laptop recommendation and analysis",
    version="1.0.0",
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ 1. Recommend Specs ============
@app.post("/recommend-specs")
async def recommend_specs(needs: UserNeeds):
    """Return baseline specs + AI explanation based on user needs."""
    # Build baseline specs from needs
    ram = 16 if needs.multitasking or needs.gaming else 8
    storage = 512 if needs.gaming or "creative" in needs.usage.lower() else 256
    storage_type = "SSD"
    gpu = "Dedicated GPU" if needs.gaming else "Integrated graphics"
    battery = 8 if "office" in needs.usage.lower() or "student" in needs.usage.lower() else 6

    baseline = LaptopSpecs(
        cpu="Intel i5 / Ryzen 5 or better" if needs.gaming else "Intel i5 / Ryzen 5",
        ram_gb=ram,
        storage_gb=storage,
        storage_type=storage_type,
        gpu=gpu,
        battery_life_hours=battery,
        power_draw_watts=65 if needs.gaming else 45,
    )

    prompt = f"""As a PC advisor, briefly explain (2-3 sentences) why these specs fit a user who:
- Uses their laptop for: {needs.usage}
- Budget: ${needs.budget}
- Multitasking: {needs.multitasking}, Gaming: {needs.gaming}

Recommended: {ram}GB RAM, {storage}GB {storage_type}, {gpu}. Keep it friendly and actionable."""

    explanation = generate_ai_response(prompt)

    match = future_proof_score(needs)

    return {
        "baseline_specs": baseline.model_dump(),
        "ai_explanation": explanation,
        "future_proof_score": match,
        "match_score": match,  # Same for baseline
    }


# ============ 2. Compare Laptops ============
@app.post("/compare-laptops")
async def compare_laptops(laptops: list[Laptop]):
    """Compare two laptops and return scores + AI comparison."""
    if len(laptops) < 2:
        raise HTTPException(400, "Provide at least 2 laptops to compare")

    # Use first laptop's implied needs for scoring (or generic)
    user_needs = UserNeeds(
        usage="general",
        budget=1000,
        multitasking=True,
        gaming=any("gpu" in str(l.specs.gpu).lower() and "integrated" not in str(l.specs.gpu).lower() for l in laptops),
    )

    scores = []
    for lap in laptops[:2]:
        s = calculate_match_score(user_needs, lap)
        scores.append({"name": lap.name or "Laptop", "match_score": s})

    prompt = f"""Compare these two laptops in 2-3 sentences. Be concise and helpful.

Laptop 1: {laptops[0].name or 'Unknown'}, {laptops[0].specs.ram_gb}GB RAM, {laptops[0].specs.storage_gb}GB {laptops[0].specs.storage_type}, {laptops[0].specs.gpu}
Laptop 2: {laptops[1].name or 'Unknown'}, {laptops[1].specs.ram_gb}GB RAM, {laptops[1].specs.storage_gb}GB {laptops[1].specs.storage_type}, {laptops[1].specs.gpu}

Match scores: Laptop 1={scores[0]['match_score']}, Laptop 2={scores[1]['match_score']}"""

    explanation = generate_ai_response(prompt)

    return {
        "laptops": scores,
        "comparison": explanation,
        "scores": {s["name"]: s["match_score"] for s in scores},
    }


# ============ 3. Risk Check ============
@app.post("/risk-check")
async def risk_check(health: HealthData):
    """Return risk score + AI explanation for used laptop."""
    score = risk_score_from_health(health)

    prompt = f"""A used laptop has: battery health {health.battery_health_percent}%, SSD health {health.ssd_health_percent}%, {health.cycle_count} charge cycles.
Risk score: {score}/100. In 1-2 sentences, advise whether to buy it and what to watch for."""

    explanation = generate_ai_response(prompt)

    return {
        "risk_score": score,
        "ai_explanation": explanation,
        "health": {
            "battery": health.battery_health_percent,
            "ssd": health.ssd_health_percent,
            "cycles": health.cycle_count,
        },
    }


# ============ 4. Upgrade Path ============
@app.post("/upgrade-path")
async def upgrade_path(input_data: UpgradeInput):
    """Return upgradeability advice based on RAM slots and storage type."""
    result = check_upgradeability_from_input(input_data)

    prompt = f"""Laptop has {input_data.ram_slots} RAM slot(s), {input_data.storage_type} storage.
Upgrade score: {result['score']}/100. In 1-2 sentences, give practical upgrade advice."""

    explanation = generate_ai_response(prompt)

    return {
        "upgrade_score": result["score"],
        "advice": result["advice"],
        "details": result["details"],
        "summary": result["summary"],
        "ai_explanation": explanation,
    }


# ============ 5. Sustainability ============
@app.post("/sustainability")
async def sustainability(input_data: SustainabilityInput):
    """Return energy efficiency / eco score + AI explanation."""
    score = eco_score_from_input(input_data)

    prompt = f"""Laptop: {input_data.battery_life_hours}h battery, {input_data.power_draw_watts}W power draw, {input_data.thermal_design} thermal design.
Eco score: {score}/100. In 1-2 sentences, explain its environmental impact and efficiency."""

    explanation = generate_ai_response(prompt)

    return {
        "eco_score": score,
        "ai_explanation": explanation,
        "specs": {
            "battery_life_hours": input_data.battery_life_hours,
            "power_draw_watts": input_data.power_draw_watts,
            "thermal_design": input_data.thermal_design,
        },
    }


# ============ 6. Budget Stretch ============
@app.post("/budget-stretch")
async def budget_stretch(input_data: BudgetStretchInput):
    """Return trade-off suggestions when budget is tight."""
    budget = input_data.budget
    specs = input_data.desired_specs

    prompt = f"""User has ${budget} budget for a laptop. """
    if specs:
        prompt += f"They want: {specs.ram_gb}GB RAM, {specs.storage_gb}GB {specs.storage_type}, {specs.gpu or 'any GPU'}. "
    prompt += """In 2-3 sentences, suggest smart trade-offs: what to prioritize, what to compromise, and one concrete tip to stretch the budget."""

    explanation = generate_ai_response(prompt)

    return {
        "budget": budget,
        "trade_offs": explanation,
        "ai_explanation": explanation,
    }


# ============ 7. AI Chat ============
@app.post("/chat")
async def chat(input_data: ChatInput):
    """Continuous AI chat with history."""
    # Build prompt from history
    messages = []
    for msg in input_data.history:
        messages.append(f"{msg.role.capitalize()}: {msg.content}")
    
    context = "\n".join(messages)
    current_prompt = f"""You are SmartPC Advisor, a helpful PC hardware expert. 
The user is asking a follow-up question. 

### Previous Conversation:
{context}

### User: {input_data.message}

### Guidelines:
1. Provide technical but accessible advice.
2. IMPORTANT: Suggest 2-3 specific, real-world laptop/PC model names that match the discussed configuration.
3. Keep the response concise (max 4-5 sentences)."""

    explanation = generate_ai_response(current_prompt)

    return {
        "response": explanation,
        "history_update": [
            {"role": "user", "content": input_data.message},
            {"role": "assistant", "content": explanation}
        ]
    }


# Health check
@app.get("/")
async def root():
    return {"message": "SmartPC Advisor API", "status": "ok"}
