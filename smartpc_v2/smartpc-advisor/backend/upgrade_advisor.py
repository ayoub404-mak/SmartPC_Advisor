"""
Upgrade path logic for laptops.
Checks RAM and storage upgradeability.
"""
from typing import Optional
from backend.models import UpgradeInput


def check_upgradeability(
    ram_slots: int,
    storage_type: str,
    max_ram_gb: Optional[int] = None,
    has_empty_slot: bool = False,
) -> dict:
    """
    Check upgradeability of a laptop.
    Returns dict with upgradeability score, advice, and details.
    """
    score = 50.0  # Base
    advice = []
    details = []

    # RAM slots
    if ram_slots >= 2:
        score += 25
        advice.append("Dual RAM slots: easy to add or replace memory.")
        details.append("RAM: Upgradable")
    elif ram_slots == 1:
        score += 5
        advice.append("Single RAM slot: can replace but not add. Check if soldered.")
        details.append("RAM: Limited upgrade")
    else:
        score -= 20
        advice.append("Soldered RAM: not upgradable.")
        details.append("RAM: Not upgradable")

    # Storage
    storage_upper = storage_type.upper()
    if "SSD" in storage_upper or "NVME" in storage_upper:
        score += 15
        advice.append("SSD/NVMe: can upgrade to larger/faster drive.")
        details.append("Storage: Upgradable")
    elif "HDD" in storage_upper:
        score += 10
        advice.append("HDD: can swap for SSD for big performance gain.")
        details.append("Storage: Swap to SSD recommended")
    else:
        advice.append("Storage type unclear. Check if M.2 or 2.5\" slot exists.")
        details.append("Storage: Verify compatibility")

    # Empty slot bonus
    if has_empty_slot:
        score += 10
        advice.append("Empty RAM slot available: plug-and-play upgrade.")

    # Max RAM cap
    if max_ram_gb and max_ram_gb >= 32:
        score += 5
        advice.append(f"Supports up to {max_ram_gb}GB RAM.")

    upgrade_score = max(0, min(100, round(score, 1)))
    return {
        "score": upgrade_score,
        "advice": advice,
        "details": details,
        "summary": "Good upgrade path" if upgrade_score >= 70 else "Limited upgrade options",
    }


def check_upgradeability_from_input(input_data: UpgradeInput) -> dict:
    """Convenience wrapper using UpgradeInput model."""
    return check_upgradeability(
        ram_slots=input_data.ram_slots,
        storage_type=input_data.storage_type,
        max_ram_gb=input_data.max_ram_gb,
        has_empty_slot=input_data.has_empty_slot,
    )
