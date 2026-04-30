"""
El Capitan – Data Models
Core dataclasses for World, Environment, Resources, and Entities.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .constants import (
    CLIMATE_TYPES,
    ENTITY_TYPES,
    INITIAL_ENERGY_UNITS,
    INITIAL_ENTITY_COUNT,
    INITIAL_FOOD_UNITS,
    INITIAL_MINERAL_UNITS,
    INITIAL_WATER_UNITS,
    MAX_WORLD_RADIUS_KM,
    MIN_WORLD_RADIUS_KM,
    PRECIPITATION_MAX_MM,
    TEMP_MAX_C,
    TEMP_MIN_C,
    TERRAIN_TYPES,
    WIND_SPEED_MAX_KMH,
)


# ──────────────────────────────────────────────
# Environment
# ──────────────────────────────────────────────

@dataclass
class Environment:
    """
    Tier-1 data: atmospheric and geological state of a world.

    All values are updated in-place by the Tier-1 EnvironmentProcessor.
    """

    climate: str
    terrain: str
    temperature_c: float        # current surface temperature (°C)
    precipitation_mm: float     # current precipitation (mm/tick)
    wind_speed_kmh: float       # current wind speed (km/h)
    humidity_pct: float         # 0–100 %
    tectonic_activity: float    # 0.0 (stable) – 1.0 (highly active)
    sea_level_m: float          # current sea level relative to baseline (m)
    event_log: List[str] = field(default_factory=list)

    @classmethod
    def random(cls, rng: random.Random) -> "Environment":
        """Generate a randomised Earth-like environment."""
        return cls(
            climate=rng.choice(CLIMATE_TYPES),
            terrain=rng.choice(TERRAIN_TYPES),
            temperature_c=rng.uniform(TEMP_MIN_C, TEMP_MAX_C),
            precipitation_mm=rng.uniform(0.0, PRECIPITATION_MAX_MM),
            wind_speed_kmh=rng.uniform(0.0, WIND_SPEED_MAX_KMH),
            humidity_pct=rng.uniform(0.0, 100.0),
            tectonic_activity=rng.uniform(0.0, 1.0),
            sea_level_m=0.0,
        )

    def summary(self) -> str:
        return (
            f"Climate={self.climate}, Terrain={self.terrain}, "
            f"Temp={self.temperature_c:.1f}°C, "
            f"Precip={self.precipitation_mm:.1f}mm, "
            f"Wind={self.wind_speed_kmh:.1f}km/h, "
            f"Humidity={self.humidity_pct:.1f}%"
        )


# ──────────────────────────────────────────────
# Resources
# ──────────────────────────────────────────────

@dataclass
class Resources:
    """
    Tier-2 data: natural resource pools of a world.

    All values are updated in-place by the Tier-2 ResourceProcessor.
    """

    water: float = INITIAL_WATER_UNITS
    minerals: float = INITIAL_MINERAL_UNITS
    energy: float = INITIAL_ENERGY_UNITS      # geothermal / solar flux
    food: float = INITIAL_FOOD_UNITS          # arable bio-mass

    water_max: float = INITIAL_WATER_UNITS
    minerals_max: float = INITIAL_MINERAL_UNITS
    energy_max: float = INITIAL_ENERGY_UNITS
    food_max: float = INITIAL_FOOD_UNITS

    consumption_history: List[Dict[str, float]] = field(default_factory=list)

    @classmethod
    def random(cls, rng: random.Random) -> "Resources":
        """Generate randomised resource pools scaled around Earth-like defaults."""
        scale = rng.uniform(0.5, 1.5)
        w = INITIAL_WATER_UNITS * scale
        m = INITIAL_MINERAL_UNITS * rng.uniform(0.5, 1.5)
        e = INITIAL_ENERGY_UNITS * rng.uniform(0.5, 1.5)
        f = INITIAL_FOOD_UNITS * scale
        return cls(
            water=w, water_max=w,
            minerals=m, minerals_max=m,
            energy=e, energy_max=e,
            food=f, food_max=f,
        )

    def total_abundance(self) -> float:
        """Aggregate resource availability as a fraction of maximum (0–1)."""
        totals = self.water + self.minerals + self.energy + self.food
        maxima = self.water_max + self.minerals_max + self.energy_max + self.food_max
        return totals / maxima if maxima > 0 else 0.0

    def summary(self) -> str:
        return (
            f"Water={self.water:.0f}/{self.water_max:.0f}, "
            f"Minerals={self.minerals:.0f}/{self.minerals_max:.0f}, "
            f"Energy={self.energy:.0f}/{self.energy_max:.0f}, "
            f"Food={self.food:.0f}/{self.food_max:.0f}"
        )


# ──────────────────────────────────────────────
# Entity
# ──────────────────────────────────────────────

@dataclass
class Entity:
    """A single species or population group inhabiting a world."""

    uid: int
    kind: str               # one of ENTITY_TYPES
    population: int
    health: float           # 0.0–1.0
    sapient: bool = False
    age_ticks: int = 0

    def is_alive(self) -> bool:
        return self.population > 0 and self.health > 0.0

    def summary(self) -> str:
        tag = "🧠" if self.sapient else "🌿"
        return f"{tag} {self.kind}(uid={self.uid}, pop={self.population}, hp={self.health:.2f})"


# ──────────────────────────────────────────────
# World
# ──────────────────────────────────────────────

@dataclass
class World:
    """
    Top-level model representing one simulated Earth-like world.

    Composed of an Environment, Resources pool, and a population of Entities.
    """

    name: str
    radius_km: float
    environment: Environment
    resources: Resources
    entities: List[Entity] = field(default_factory=list)
    age_ticks: int = 0
    is_habitable: bool = True

    # Metrics accumulated over time
    tick_log: List[str] = field(default_factory=list)

    @classmethod
    def create(cls, name: str, rng: random.Random) -> "World":
        """Spawn a new randomised world."""
        env = Environment.random(rng)
        res = Resources.random(rng)
        radius = rng.uniform(MIN_WORLD_RADIUS_KM, MAX_WORLD_RADIUS_KM)

        entities: List[Entity] = []
        for uid in range(INITIAL_ENTITY_COUNT):
            kind = rng.choice(ENTITY_TYPES[:-1])  # no Sapient at genesis
            entities.append(Entity(
                uid=uid,
                kind=kind,
                population=rng.randint(10, 500),
                health=rng.uniform(0.5, 1.0),
            ))

        return cls(
            name=name,
            radius_km=radius,
            environment=env,
            resources=res,
            entities=entities,
        )

    # ------------------------------------------------------------------
    # Convenience queries
    # ------------------------------------------------------------------

    def total_population(self) -> int:
        return sum(e.population for e in self.entities if e.is_alive())

    def has_sapient_life(self) -> bool:
        return any(e.sapient and e.is_alive() for e in self.entities)

    def alive_entity_count(self) -> int:
        return sum(1 for e in self.entities if e.is_alive())

    def status_line(self) -> str:
        pop = self.total_population()
        sapient = "🧠 YES" if self.has_sapient_life() else "NO"
        return (
            f"{self.name} | age={self.age_ticks}t | "
            f"pop={pop:,} | sapient={sapient} | "
            f"habitable={'YES' if self.is_habitable else 'NO'}"
        )

    def log(self, msg: str) -> None:
        self.tick_log.append(f"[t={self.age_ticks}] {msg}")
