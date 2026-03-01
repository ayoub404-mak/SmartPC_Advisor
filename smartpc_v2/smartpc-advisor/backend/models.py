"""
Pydantic models for SmartPC Advisor API.
"""
from pydantic import BaseModel, Field
from typing import Optional


# ============ User Needs / Questionnaire ============
class UserNeeds(BaseModel):
    """User requirements from questionnaire."""
    usage: str = Field(..., description="Primary use case: office, creative, gaming, student, etc.")
    budget: float = Field(..., ge=0, description="Budget in USD")
    multitasking: bool = Field(default=False, description="Heavy multitasking required")
    gaming: bool = Field(default=False, description="Gaming required")


# ============ Specs & Laptops ============
class LaptopSpecs(BaseModel):
    """Laptop specification model."""
    cpu: str = Field(default="", description="CPU model")
    ram_gb: int = Field(default=8, ge=0, description="RAM in GB")
    storage_gb: int = Field(default=256, ge=0, description="Storage in GB")
    storage_type: str = Field(default="SSD", description="SSD or HDD")
    gpu: str = Field(default="", description="GPU model")
    display_inches: float = Field(default=15.6, ge=0, description="Display size in inches")
    battery_life_hours: float = Field(default=6, ge=0, description="Battery life in hours")
    power_draw_watts: float = Field(default=65, ge=0, description="Power draw in watts")


class Laptop(BaseModel):
    """Full laptop model with optional metadata."""
    name: str = Field(default="", description="Laptop name/model")
    specs: LaptopSpecs = Field(default_factory=LaptopSpecs)


# ============ Used Laptop Health ============
class HealthData(BaseModel):
    """Health metrics for used laptop risk assessment."""
    battery_health_percent: float = Field(..., ge=0, le=100, description="Battery health %")
    ssd_health_percent: float = Field(..., ge=0, le=100, description="SSD health %")
    cycle_count: int = Field(..., ge=0, description="Battery cycle count")
    temperature_celsius: Optional[float] = Field(default=None, ge=0, le=100, description="Current temp")


# ============ Upgrade Path ============
class UpgradeInput(BaseModel):
    """Input for upgrade path check."""
    ram_slots: int = Field(..., ge=0, le=4, description="Number of RAM slots")
    storage_type: str = Field(..., description="SSD or HDD")
    max_ram_gb: Optional[int] = Field(default=None, ge=0, description="Max supported RAM")
    has_empty_slot: bool = Field(default=False, description="Has empty RAM slot")


# ============ Budget Stretch ============
class BudgetStretchInput(BaseModel):
    """Input for budget stretch advisor."""
    budget: float = Field(..., ge=0, description="Budget in USD")
    desired_specs: Optional[LaptopSpecs] = Field(default=None, description="Desired specs if any")


# ============ Sustainability ============
class SustainabilityInput(BaseModel):
    """Input for sustainability scoring."""
    battery_life_hours: float = Field(..., ge=0, description="Battery life in hours")
    power_draw_watts: float = Field(..., ge=0, description="Power draw in watts")
    thermal_design: str = Field(default="standard", description="thermal design: standard, efficient, poor")


# ============ AI Chat ============
class ChatMessage(BaseModel):
    """Single message in a chat history."""
    role: str = Field(..., description="user or assistant")
    content: str = Field(..., description="Message text")


class ChatInput(BaseModel):
    """Input for continuous AI chat."""
    history: list[ChatMessage] = Field(default_factory=list, description="Previous messages")
    message: str = Field(..., description="Current user message")
