"""
TRE-UPR Universe Model
Each Universe object represents a pocket reality spawned by the device.
"""

import random
import uuid
from dataclasses import dataclass, field
from typing import List, Optional

from .constants import (
    BASE_DIMENSIONS,
    UNIVERSE_STABILITY_THRESHOLD,
    UNIVERSE_SENTIENCE_THRESHOLD,
)


@dataclass
class PhysicsProfile:
    """The fundamental physics rules woven into a universe at creation time."""
    dimensions: int
    gravity_constant: float        # relative to baseline
    speed_of_light_factor: float   # relative multiplier
    entropy_rate: float            # how fast disorder grows [0, 1]
    dark_energy_density: float     # accelerating expansion [0, 1]
    quantum_coupling: float        # strength of quantum effects [0, 1]

    def summary(self) -> str:
        return (
            f"dims={self.dimensions}, G×{self.gravity_constant:.2f}, "
            f"c×{self.speed_of_light_factor:.2f}, entropy={self.entropy_rate:.3f}, "
            f"Λ={self.dark_energy_density:.3f}, ℏ-coupling={self.quantum_coupling:.3f}"
        )


@dataclass
class Universe:
    """A universe created and managed by the TRE-UPR device."""

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    generation: int = 0
    name: str = ""
    age_ticks: int = 0           # simulated time steps since Big Bang
    energy: float = 0.0          # remaining usable energy
    stability: float = 1.0       # health [0, 1] – below threshold → collapse
    complexity: float = 0.0      # emergent complexity score
    physics: Optional[PhysicsProfile] = None
    child_universes: List["Universe"] = field(default_factory=list)
    is_alive: bool = True
    has_sentience: bool = False
    events: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            self.name = f"Universe-{self.id}"

    # ------------------------------------------------------------------
    # Simulation tick
    # ------------------------------------------------------------------

    def tick(self) -> None:
        """Advance this universe by one simulated time step."""
        if not self.is_alive:
            return

        self.age_ticks += 1
        p = self.physics

        # Energy dissipates each tick due to entropy
        dissipation = self.energy * p.entropy_rate * 0.001
        self.energy = max(0.0, self.energy - dissipation)

        # Stability drifts based on dark energy and quantum coupling
        stability_delta = (p.quantum_coupling - p.dark_energy_density) * 0.005
        self.stability = max(0.0, min(1.0, self.stability + stability_delta))

        # Complexity grows when stable and energy-rich
        if self.stability > UNIVERSE_STABILITY_THRESHOLD and self.energy > 0:
            growth = self.stability * p.quantum_coupling * 0.01
            self.complexity += growth
            if self.complexity > 10.0:
                self.complexity = 10.0  # cap

        # Check sentience emergence
        if (
            not self.has_sentience
            and self.stability >= UNIVERSE_SENTIENCE_THRESHOLD
            and self.complexity >= 5.0
        ):
            self.has_sentience = True
            self.events.append(
                f"[tick {self.age_ticks}] Sentient life emerged in {self.name}!"
            )

        # Check collapse
        if self.stability < UNIVERSE_STABILITY_THRESHOLD and self.age_ticks > 10:
            self.is_alive = False
            self.events.append(
                f"[tick {self.age_ticks}] {self.name} collapsed (stability={self.stability:.3f})."
            )

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def status_line(self) -> str:
        state = "✅ ALIVE" if self.is_alive else "💀 COLLAPSED"
        life = "🧬 SENTIENT" if self.has_sentience else "⚛  inert"
        return (
            f"{self.name} [gen {self.generation}] | {state} | {life} | "
            f"age={self.age_ticks} ticks | stability={self.stability:.3f} | "
            f"complexity={self.complexity:.3f} | energy={self.energy:.1f} dU"
        )

    def __repr__(self) -> str:  # pragma: no cover
        return f"Universe(id={self.id!r}, gen={self.generation}, alive={self.is_alive})"


# ------------------------------------------------------------------
# Factory helpers
# ------------------------------------------------------------------

def create_universe(
    generation: int,
    rng: random.Random,
    dimensions: int = BASE_DIMENSIONS,
    energy: float = 100_000.0,
) -> Universe:
    """Construct a new universe with randomised physics."""
    profile = PhysicsProfile(
        dimensions=dimensions,
        gravity_constant=rng.uniform(0.5, 2.0),
        speed_of_light_factor=rng.uniform(0.8, 1.2),
        entropy_rate=rng.uniform(0.01, 0.15),
        dark_energy_density=rng.uniform(0.05, 0.60),
        quantum_coupling=rng.uniform(0.30, 0.95),
    )
    universe = Universe(
        generation=generation,
        energy=energy,
        stability=rng.uniform(0.60, 1.00),
        complexity=rng.uniform(0.0, 0.5),
        physics=profile,
    )
    universe.events.append(
        f"[tick 0] {universe.name} spawned (gen {generation}). "
        f"Physics: {profile.summary()}"
    )
    return universe
