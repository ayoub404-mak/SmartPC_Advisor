"""
Scoring logic for SmartPC Advisor.
Match score: how well a laptop fits user needs.
Future-proof score: how well specs will hold up over time.
"""
from backend.models import LaptopSpecs, UserNeeds, Laptop


def calculate_match_score(user_specs: UserNeeds, laptop: Laptop) -> float:
    """
    Calculate how well a laptop matches user needs (0-100).
    Considers: usage, budget (implicit via specs), multitasking, gaming.
    """
    score = 50.0  # Base score

    specs = laptop.specs

    # RAM: multitasking needs 16GB+
    if user_specs.multitasking and specs.ram_gb >= 16:
        score += 15
    elif user_specs.multitasking and specs.ram_gb >= 12:
        score += 8
    elif not user_specs.multitasking and specs.ram_gb >= 8:
        score += 10

    # GPU: gaming needs dedicated GPU
    if user_specs.gaming:
        if specs.gpu and "integrated" not in specs.gpu.lower():
            score += 20
        else:
            score -= 15
    else:
        if specs.ram_gb >= 8:
            score += 5

    # Storage type: SSD preferred
    if specs.storage_type.upper() == "SSD":
        score += 10
    else:
        score -= 5

    # Usage-based adjustments
    usage = user_specs.usage.lower()
    if "creative" in usage or "video" in usage:
        if specs.ram_gb >= 16 and specs.gpu:
            score += 10
    elif "office" in usage or "student" in usage:
        if specs.battery_life_hours >= 6:
            score += 5

    return max(0, min(100, round(score, 1)))


def future_proof_score(user_specs: UserNeeds) -> float:
    """
    Calculate future-proof score based on user needs (0-100).
    Higher = specs that will age well.
    """
    score = 50.0

    # Multitasking + gaming = need more headroom
    if user_specs.multitasking:
        score += 15  # 16GB+ RAM recommended
    if user_specs.gaming:
        score += 10  # Dedicated GPU recommended

    # Budget proxy: higher budget = more future-proof options
    if user_specs.budget >= 1200:
        score += 15
    elif user_specs.budget >= 800:
        score += 8
    elif user_specs.budget >= 500:
        score += 2

    # Creative/video = need more power
    usage = user_specs.usage.lower()
    if "creative" in usage or "video" in usage:
        score += 10

    return max(0, min(100, round(score, 1)))
