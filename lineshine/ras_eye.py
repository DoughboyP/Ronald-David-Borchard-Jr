"""
Lineshine – Ra's Eye
The all-seeing oversight component installed in the Lineshine computer.

Ra's Eye observes every world the controller creates, surfaces divine
insights, detects anomalies, and records visions for later inspection.
"""

from __future__ import annotations

import random
from typing import List

from .constants import (
    EYE_PREFIX,
    RAS_EYE_DIVINE_INSIGHTS,
    RAS_EYE_POWER_LEVELS,
)
from .models import LineshineWorld, RasEyeVision


class RasEye:
    """
    Ra's Eye — omniscient oversight engine.

    After being seated inside the Lineshine computer the eye operates
    continuously, scanning every world the controller creates or modifies
    and storing structured visions that can be replayed at any time.
    """

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng
        self._tick = 0
        self._power_index = 0          # advances as worlds are created
        self._all_visions: List[RasEyeVision] = []
        self._active = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def awaken(self) -> None:
        """Seat Ra's Eye inside the Lineshine computer."""
        self._active = True
        self._power_index = 0
        print(f"{EYE_PREFIX} ☀  Ra's Eye is awakening inside Lineshine...")
        print(f"{EYE_PREFIX}    Power level → {self._current_power_level}")
        print()

    @property
    def is_active(self) -> bool:
        return self._active

    @property
    def _current_power_level(self) -> str:
        idx = min(self._power_index, len(RAS_EYE_POWER_LEVELS) - 1)
        return RAS_EYE_POWER_LEVELS[idx]

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def observe(self, world: LineshineWorld) -> RasEyeVision:
        """
        Scan a world and return a structured RasEyeVision.

        Side-effect: the vision is appended to the world's vision log and
        to the global vision archive.  Ra's Eye power level grows with
        the number of worlds observed.
        """
        self._require_active()
        self._tick += 1

        # Escalate power as more worlds are observed
        if len(self._all_visions) > 0 and len(self._all_visions) % 3 == 0:
            self._power_index = min(
                self._power_index + 1, len(RAS_EYE_POWER_LEVELS) - 1
            )

        insight = self._rng.choice(RAS_EYE_DIVINE_INSIGHTS)
        anomaly, anomaly_desc = self._detect_anomaly(world)

        vision = RasEyeVision(
            world_number=world.uid,
            tick=self._tick,
            power_level=self._current_power_level,
            insight=insight,
            population_observed=world.population,
            stability_observed=world.stability,
            anomaly_detected=anomaly,
            anomaly_description=anomaly_desc,
        )

        world.visions.append(vision)
        self._all_visions.append(vision)
        return vision

    def scan_all(self, worlds: List[LineshineWorld]) -> List[RasEyeVision]:
        """Observe every active world and return all resulting visions."""
        self._require_active()
        return [self.observe(w) for w in worlds if w.is_active]

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def status(self) -> str:
        return (
            f"  Ra's Eye status\n"
            f"    Active        : {'Yes' if self._active else 'No'}\n"
            f"    Power level   : {self._current_power_level}\n"
            f"    Total visions : {len(self._all_visions)}\n"
            f"    Ticks elapsed : {self._tick}"
        )

    def all_visions(self) -> List[RasEyeVision]:
        return list(self._all_visions)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _detect_anomaly(self, world: LineshineWorld):
        """Return (anomaly_detected, description)."""
        if world.stability < 0.2:
            return True, "Critical stability collapse imminent."
        if world.population == 0:
            return True, "World is uninhabited — void state detected."
        if world.population > 900:
            return True, "Population surge beyond projected bounds."
        if self._rng.random() < 0.08:
            anomalies = [
                "Temporal rift detected in the lower hemisphere.",
                "Uncharted energy signature emanating from the core.",
                "Spontaneous crystalline formation along the equatorial belt.",
                "Micro-singularity observed at world's magnetic pole.",
            ]
            return True, self._rng.choice(anomalies)
        return False, ""

    def _require_active(self) -> None:
        if not self._active:
            raise RuntimeError(
                "Ra's Eye is not active. Call .awaken() before observing worlds."
            )
