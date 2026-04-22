"""
TRE-UPR Self-Building Engine
The heart of the device: each generation analyses the previous one and builds
a more complex version of itself, producing richer universes in return.
"""

import math
import random
from typing import List, Tuple

from .constants import (
    BOOTSTRAP_SEED,
    DIMENSION_UNLOCK_GENERATION,
    ENERGY_SCALING_FACTOR,
    INITIAL_ENERGY_BUDGET,
    LOG_PREFIX,
    MAX_DIMENSIONS,
    MAX_GENERATIONS,
    MAX_UNIVERSES_PER_GENERATION,
    MIN_COMPLEXITY_DELTA,
    SELF_BUILD_COST,
    UNIVERSE_CREATION_COST,
)
from .universe import Universe, create_universe


class GenerationReport:
    """Summary of one self-build generation."""

    def __init__(
        self,
        generation: int,
        universes: List[Universe],
        energy_spent: float,
        complexity_score: float,
    ) -> None:
        self.generation = generation
        self.universes = universes
        self.energy_spent = energy_spent
        self.complexity_score = complexity_score
        self.alive_count = sum(1 for u in universes if u.is_alive)
        self.sentient_count = sum(1 for u in universes if u.has_sentience)

    def summary(self) -> str:
        lines = [
            f"\n{'─' * 80}",
            f"{LOG_PREFIX} Generation {self.generation} Report",
            f"{'─' * 80}",
            f"  Universes spawned : {len(self.universes)}",
            f"  Still alive       : {self.alive_count}",
            f"  Sentient life     : {self.sentient_count}",
            f"  Energy spent      : {self.energy_spent:,.1f} dU",
            f"  Complexity score  : {self.complexity_score:.4f}",
            f"{'─' * 80}",
        ]
        for u in self.universes:
            lines.append(f"  » {u.status_line()}")
        lines.append(f"{'─' * 80}")
        return "\n".join(lines)


class SelfBuildingEngine:
    """
    Recursive self-improvement engine.

    Each call to `run_generation()` analyses the prior generation's universes,
    extracts a complexity score, then uses it to seed a more capable next
    generation – more dimensions available, better energy efficiency, finer-
    tuned physics ranges.
    """

    def __init__(self, seed: int = BOOTSTRAP_SEED) -> None:
        self._master_rng = random.Random(seed)
        self._generation = 0
        self._energy_budget = INITIAL_ENERGY_BUDGET
        self._complexity_history: List[float] = []
        self._reports: List[GenerationReport] = []

        # Mutable "firmware" that improves each generation
        self._firmware: dict = {
            "max_universes": 1,
            "ticks_per_universe": 20,
            "energy_per_universe": UNIVERSE_CREATION_COST,
            "dimension_cap": BASE_DIMENSIONS if True else BASE_DIMENSIONS,
        }
        # Import here to avoid circular reference after module-level import above
        from .constants import BASE_DIMENSIONS as _BD
        self._firmware["dimension_cap"] = _BD

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def generation(self) -> int:
        return self._generation

    @property
    def reports(self) -> List[GenerationReport]:
        return list(self._reports)

    def run_generation(self) -> Tuple[GenerationReport, bool]:
        """
        Run one generation of the self-building cycle.

        Returns:
            (report, should_continue) – the report for this generation, and
            whether the engine has enough momentum to keep going.
        """
        if self._generation >= MAX_GENERATIONS:
            print(f"{LOG_PREFIX} Maximum generation ({MAX_GENERATIONS}) reached. Halting.")
            return self._reports[-1], False

        print(f"\n{LOG_PREFIX} ══ Starting Generation {self._generation} ══")
        print(f"{LOG_PREFIX} Energy budget: {self._energy_budget:,.1f} dU | "
              f"Firmware: {self._firmware}")

        energy_spent = SELF_BUILD_COST
        self._energy_budget -= SELF_BUILD_COST
        if self._energy_budget <= 0:
            print(f"{LOG_PREFIX} ⚠  Insufficient energy for self-build. Halting.")
            return self._reports[-1] if self._reports else self._empty_report(), False

        # --- Spawn universes for this generation ---
        universes = self._spawn_universes()
        energy_spent += self._firmware["energy_per_universe"] * len(universes)

        # --- Run simulation ticks ---
        self._simulate(universes)

        # --- Evaluate complexity ---
        complexity_score = self._evaluate_complexity(universes)
        self._complexity_history.append(complexity_score)

        report = GenerationReport(
            generation=self._generation,
            universes=universes,
            energy_spent=energy_spent,
            complexity_score=complexity_score,
        )
        self._reports.append(report)

        # --- Self-upgrade firmware for next generation ---
        should_continue = self._upgrade_firmware(complexity_score)

        self._generation += 1
        self._energy_budget *= ENERGY_SCALING_FACTOR  # energy compounds

        return report, should_continue

    def run_all(self) -> List[GenerationReport]:
        """Run the device until it halts naturally."""
        should_continue = True
        while should_continue and self._generation < MAX_GENERATIONS:
            report, should_continue = self.run_generation()
            print(report.summary())
        return list(self._reports)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _spawn_universes(self) -> List[Universe]:
        fw = self._firmware
        count = min(fw["max_universes"], MAX_UNIVERSES_PER_GENERATION)
        universes: List[Universe] = []
        for _ in range(count):
            dims = self._master_rng.randint(
                3, min(fw["dimension_cap"], MAX_DIMENSIONS)
            )
            u = create_universe(
                generation=self._generation,
                rng=self._master_rng,
                dimensions=dims,
                energy=fw["energy_per_universe"],
            )
            universes.append(u)
            print(f"{LOG_PREFIX}   ✦ Spawned {u.name} ({dims}D)")
        return universes

    def _simulate(self, universes: List[Universe]) -> None:
        ticks = self._firmware["ticks_per_universe"]
        for tick in range(ticks):
            for u in universes:
                u.tick()
            # Print notable events mid-simulation
            for u in universes:
                for event in u.events:
                    if event not in getattr(u, "_printed_events", set()):
                        if not hasattr(u, "_printed_events"):
                            u._printed_events = set()
                        u._printed_events.add(event)
                        print(f"{LOG_PREFIX}   🌌 {event}")

    def _evaluate_complexity(self, universes: List[Universe]) -> float:
        """Aggregate complexity from all universes in this generation."""
        if not universes:
            return 0.0
        alive = [u for u in universes if u.is_alive]
        if not alive:
            return 0.0
        avg_complexity = sum(u.complexity for u in alive) / len(alive)
        sentience_bonus = sum(0.5 for u in alive if u.has_sentience)
        age_bonus = math.log1p(sum(u.age_ticks for u in alive))
        return avg_complexity + sentience_bonus + age_bonus * 0.1

    def _upgrade_firmware(self, complexity_score: float) -> bool:
        """
        Analyse the current complexity score and improve firmware.
        Returns False if complexity has plateaued (signal to halt).
        """
        fw = self._firmware
        gen = self._generation

        # Complexity plateau check
        if len(self._complexity_history) >= 3:
            recent_delta = self._complexity_history[-1] - self._complexity_history[-2]
            if recent_delta < MIN_COMPLEXITY_DELTA:
                print(f"{LOG_PREFIX} Complexity plateau detected (Δ={recent_delta:.4f}). "
                      "Triggering deep rebuild...")
                # Deep rebuild: reset ticks but keep gained knowledge
                fw["ticks_per_universe"] = int(fw["ticks_per_universe"] * 1.5)

        # Unlock additional universes as complexity grows
        new_max = min(1 + int(complexity_score / 2), MAX_UNIVERSES_PER_GENERATION)
        if new_max > fw["max_universes"]:
            print(f"{LOG_PREFIX} 🔓 Universe capacity upgraded: "
                  f"{fw['max_universes']} → {new_max}")
            fw["max_universes"] = new_max

        # Unlock extra dimensions after generation threshold
        if gen >= DIMENSION_UNLOCK_GENERATION:
            new_dim_cap = min(
                BASE_DIMENSIONS + (gen - DIMENSION_UNLOCK_GENERATION + 1),
                MAX_DIMENSIONS,
            )
            if new_dim_cap > fw["dimension_cap"]:
                print(f"{LOG_PREFIX} 🔓 Dimension cap upgraded: "
                      f"{fw['dimension_cap']}D → {new_dim_cap}D")
                fw["dimension_cap"] = new_dim_cap

        # Improve simulation resolution
        fw["ticks_per_universe"] = max(
            fw["ticks_per_universe"],
            20 + gen * 5,
        )

        # Energy efficiency improves with complexity
        fw["energy_per_universe"] = UNIVERSE_CREATION_COST / (
            1 + complexity_score * 0.05
        )

        return True  # always continue unless external halting condition met

    def _empty_report(self) -> GenerationReport:
        return GenerationReport(
            generation=self._generation,
            universes=[],
            energy_spent=0.0,
            complexity_score=0.0,
        )


# Import here to satisfy forward reference inside __init__
from .constants import BASE_DIMENSIONS  # noqa: E402
