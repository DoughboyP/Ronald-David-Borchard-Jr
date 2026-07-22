"""
Lineshine – Data Models
Core dataclasses for LineshineWorld and RasEyeVision.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

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
    name: str = ""
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
        name: str = "",
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
            name=name,
            creator_note=creator_note,
        )
        w.log(f"World {uid} forged by the controller.")
        return w

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serialisable dictionary representation."""
        return {
            "uid": self.uid,
            "world_type": self.world_type,
            "radius_km": self.radius_km,
            "population": self.population,
            "stability": self.stability,
            "age_ticks": self.age_ticks,
            "name": self.name,
            "creator_note": self.creator_note,
            "visions": [
                {
                    "world_number": v.world_number,
                    "tick": v.tick,
                    "power_level": v.power_level,
                    "insight": v.insight,
                    "population_observed": v.population_observed,
                    "stability_observed": v.stability_observed,
                    "anomaly_detected": v.anomaly_detected,
                    "anomaly_description": v.anomaly_description,
                }
                for v in self.visions
            ],
            "event_log": list(self.event_log),
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "LineshineWorld":
        """Reconstruct a world from a saved dictionary."""
        visions = [
            RasEyeVision(**v) for v in d.get("visions", [])
        ]
        world = cls(
            uid=d["uid"],
            world_type=d["world_type"],
            radius_km=d["radius_km"],
            population=d["population"],
            stability=d["stability"],
            age_ticks=d.get("age_ticks", 0),
            name=d.get("name", ""),
            creator_note=d.get("creator_note", ""),
            visions=visions,
            event_log=d.get("event_log", []),
            is_active=d.get("is_active", True),
        )
        return world

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def log(self, msg: str) -> None:
        self.event_log.append(f"[t={self.age_ticks}] {msg}")

    def status_line(self) -> str:
        active = "✅" if self.is_active else "💤"
        name_part = f" | Name={self.name}" if self.name else ""
        return (
            f"{active} World {self.uid:>4} | "
            f"Type={self.world_type:<12} | "
            f"Pop={self.population:>8,} | "
            f"Stability={self.stability:.2f}"
            f"{name_part}"
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
        if self.name:
            lines.insert(1, f"  Name  : {self.name}")
        if self.creator_note:
            lines.append(f"  Note  : {self.creator_note}")
        if self.visions:
            lines.append(f"  Visions recorded: {len(self.visions)}")
        return "\n".join(lines)
