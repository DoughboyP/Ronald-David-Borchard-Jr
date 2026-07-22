"""
Lineshine – Data Models
Core dataclasses for LineshineWorld and RasEyeVision.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional

from .constants import (
    MAX_WORLD_RADIUS_KM,
    MIN_WORLD_RADIUS_KM,
    WORLD_TYPES,
    INITIAL_POPULATION_MIN,
    INITIAL_POPULATION_MAX,
)


@dataclass
class RasEyeVision:
    """
    A single observation record produced by Ra's Eye.

    Ra's Eye scans every world at creation and on demand, returning
    a structured vision that the controller can inspect.
    """

    world_number: int
    tick: int
    power_level: str
    insight: str
    population_observed: int
    stability_observed: float   # 0.0 (collapsing) – 1.0 (perfect)
    anomaly_detected: bool = False
    anomaly_description: str = ""

    def display(self) -> str:
        lines = [
            f"  👁  Ra's Eye Vision — World {self.world_number}",
            f"     Power level   : {self.power_level}",
            f"     Tick observed : {self.tick}",
            f"     Population    : {self.population_observed:,}",
            f"     Stability     : {self.stability_observed:.2f}",
        ]
        if self.anomaly_detected:
            lines.append(f"     ⚠ Anomaly      : {self.anomaly_description}")
        lines.append(f"     ✦ Insight      : \"{self.insight}\"")
        return "\n".join(lines)


@dataclass
class LineshineWorld:
    """
    A world forged inside the Lineshine computer by the controller.

    Each world is uniquely identified by its numeric ``uid``.
    Worlds evolve over simulation ticks: population grows, stability
    drifts, and Ra's Eye records visions at key moments.
    """

    uid: int
    world_type: str
    radius_km: float
    population: int
    stability: float            # 0.0–1.0
    age_ticks: int = 0
    creator_note: str = ""
    visions: List[RasEyeVision] = field(default_factory=list)
    event_log: List[str] = field(default_factory=list)
    is_active: bool = True

    @classmethod
    def forge(
        cls,
        uid: int,
        rng: random.Random,
        world_type: Optional[str] = None,
        creator_note: str = "",
    ) -> "LineshineWorld":
        """Create a new world with randomised parameters."""
        wtype = world_type or rng.choice(WORLD_TYPES)
        radius = rng.uniform(MIN_WORLD_RADIUS_KM, MAX_WORLD_RADIUS_KM)
        pop = rng.randint(INITIAL_POPULATION_MIN, INITIAL_POPULATION_MAX)
        stability = rng.uniform(0.6, 1.0)
        w = cls(
            uid=uid,
            world_type=wtype,
            radius_km=radius,
            population=pop,
            stability=stability,
            creator_note=creator_note,
        )
        w.log(f"World {uid} forged by the controller.")
        return w

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def log(self, msg: str) -> None:
        self.event_log.append(f"[t={self.age_ticks}] {msg}")

    def status_line(self) -> str:
        active = "✅" if self.is_active else "💤"
        return (
            f"{active} World {self.uid:>4} | "
            f"Type={self.world_type:<12} | "
            f"Pop={self.population:>8,} | "
            f"Stability={self.stability:.2f}"
        )

    def detail(self) -> str:
        lines = [
            f"  World : {self.uid}",
            f"  Type  : {self.world_type}",
            f"  Radius: {self.radius_km:,.0f} km",
            f"  Pop   : {self.population:,}",
            f"  Stab  : {self.stability:.2f}",
            f"  Active: {'Yes' if self.is_active else 'No'}",
        ]
        if self.creator_note:
            lines.append(f"  Note  : {self.creator_note}")
        if self.visions:
            lines.append(f"  Visions recorded: {len(self.visions)}")
        return "\n".join(lines)
