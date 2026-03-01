"""
Sustainability and energy efficiency scoring.
Evaluates battery life, power draw, and thermal design.
"""
from backend.models import SustainabilityInput


def eco_score(
    battery_life: float,
    power_draw: float,
    thermal_design: str = "standard",
) -> float:
    """
    Calculate eco/sustainability score (0-100).
    Higher = more energy efficient, lower environmental impact.
    """
    score = 50.0

    # Battery life: longer = less charging = less grid draw
    if battery_life >= 12:
        score += 20
    elif battery_life >= 8:
        score += 12
    elif battery_life >= 6:
        score += 5
    else:
        score -= 5

    # Power draw: lower = more efficient
    if power_draw <= 45:
        score += 20
    elif power_draw <= 65:
        score += 10
    elif power_draw <= 90:
        score += 2
    else:
        score -= 10

    # Thermal design: efficient cooling = less throttling = better efficiency
    thermal = thermal_design.lower()
    if "efficient" in thermal or "advanced" in thermal:
        score += 10
    elif "poor" in thermal or "basic" in thermal:
        score -= 10

    return max(0, min(100, round(score, 1)))


def eco_score_from_input(input_data: SustainabilityInput) -> float:
    """Convenience wrapper using SustainabilityInput model."""
    return eco_score(
        battery_life=input_data.battery_life_hours,
        power_draw=input_data.power_draw_watts,
        thermal_design=input_data.thermal_design,
    )
