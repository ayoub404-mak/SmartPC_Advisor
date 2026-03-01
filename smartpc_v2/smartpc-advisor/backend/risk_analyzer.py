"""
Risk assessment for used laptops.
Evaluates battery, SSD, cycles, and temperature.
"""
from typing import Optional
from backend.models import HealthData


def risk_score(
    battery_health: float,
    ssd_health: float,
    cycles: int,
    temperature: Optional[float] = None,
) -> float:
    """
    Calculate risk score for a used laptop (0-100).
    Higher = higher risk (more likely to fail soon).
    """
    score = 0.0

    # Battery health (0-100, 100 = perfect)
    # Low health = high risk
    if battery_health < 50:
        score += 40
    elif battery_health < 70:
        score += 25
    elif battery_health < 85:
        score += 10

    # SSD health (0-100)
    if ssd_health < 50:
        score += 35
    elif ssd_health < 70:
        score += 20
    elif ssd_health < 85:
        score += 8

    # Cycle count (typical laptop battery: 500-1000 cycles lifespan)
    if cycles > 800:
        score += 25
    elif cycles > 500:
        score += 15
    elif cycles > 300:
        score += 5

    # Temperature (optional)
    if temperature is not None:
        if temperature > 85:
            score += 15
        elif temperature > 75:
            score += 8

    return max(0, min(100, round(score, 1)))


def risk_score_from_health(health: HealthData) -> float:
    """Convenience wrapper using HealthData model."""
    return risk_score(
        battery_health=health.battery_health_percent,
        ssd_health=health.ssd_health_percent,
        cycles=health.cycle_count,
        temperature=health.temperature_celsius,
    )
