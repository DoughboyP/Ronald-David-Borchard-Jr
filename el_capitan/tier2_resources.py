"""
El Capitan – Tier 2: Resource Processor
Manages natural resource dynamics: regeneration, consumption, and scarcity events.
Runs in its own thread as part of the triple-processing architecture.
"""

from __future__ import annotations

import logging
import random
from typing import List

from .constants import (
    LOG_PREFIX,
    RESOURCE_DEPLETION_RATE,
    RESOURCE_REGEN_RATE,
)
from .models import World

logger = logging.getLogger(__name__)


class ResourceProcessor:
    """
    Tier-2 processor: resource management and dynamics.

    Responsibilities:
    - Regenerate renewable resources (water, food, solar energy) each tick
    - Apply consumption pressure from the entity population
    - Trigger scarcity events that affect world habitability
    - Record consumption history for monitoring
    """

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(self, worlds: List[World]) -> None:
        """
        Run one resource tick across all worlds.
        Called by the TripleProcessor from Tier-2 thread.
        """
        for world in worlds:
            if not world.is_habitable:
                continue
            self._regenerate(world)
            self._consume(world)
            self._apply_environment_modifiers(world)
            self._check_scarcity(world)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _regenerate(self, world: World) -> None:
        """Renewable resources slowly regenerate toward their maximum."""
        res = world.resources

        res.water = min(res.water_max, res.water + res.water_max * RESOURCE_REGEN_RATE)
        res.food = min(res.food_max, res.food + res.food_max * RESOURCE_REGEN_RATE)
        # Energy (solar/geothermal) regenerates faster
        res.energy = min(res.energy_max, res.energy + res.energy_max * RESOURCE_REGEN_RATE * 1.5)
        # Minerals are non-renewable – no regeneration

    def _consume(self, world: World) -> None:
        """
        Entities deplete resources proportional to their total population.
        Consumption is tracked per-tick for monitoring.
        """
        res = world.resources
        total_pop = world.total_population()
        if total_pop == 0:
            return

        base = RESOURCE_DEPLETION_RATE * total_pop

        water_consumed = min(res.water, base * 1.2)
        food_consumed = min(res.food, base * 1.0)
        energy_consumed = min(res.energy, base * 0.8)
        mineral_consumed = min(res.minerals, base * 0.3)

        res.water -= water_consumed
        res.food -= food_consumed
        res.energy -= energy_consumed
        res.minerals -= mineral_consumed

        res.consumption_history.append({
            "tick": world.age_ticks,
            "water": water_consumed,
            "food": food_consumed,
            "energy": energy_consumed,
            "minerals": mineral_consumed,
        })

    def _apply_environment_modifiers(self, world: World) -> None:
        """
        Environment affects resource availability:
        - High precipitation boosts water
        - High temperature reduces food
        - Tectonic activity can temporarily boost mineral access
        """
        env = world.environment
        res = world.resources
        rng = self._rng

        # Rain bonus
        if env.precipitation_mm > 200:
            water_bonus = env.precipitation_mm * 0.1
            res.water = min(res.water_max, res.water + water_bonus)

        # Heat stress on food production
        if env.temperature_c > 40:
            food_penalty = res.food_max * 0.01
            res.food = max(0.0, res.food - food_penalty)

        # Tectonic events occasionally expose mineral deposits
        if rng.random() < env.tectonic_activity * 0.02:
            mineral_bonus = res.minerals_max * rng.uniform(0.01, 0.05)
            res.minerals = min(res.minerals_max, res.minerals + mineral_bonus)
            logger.debug(
                "%s %s: Mineral deposit exposed (+%.0f)",
                LOG_PREFIX, world.name, mineral_bonus,
            )

    def _check_scarcity(self, world: World) -> None:
        """
        Emit warnings and affect habitability when critical resources run low.
        """
        res = world.resources

        if res.water < res.water_max * 0.05:
            msg = "⚠ Water critically scarce"
            world.log(msg)
            logger.warning("%s %s: %s", LOG_PREFIX, world.name, msg)

        if res.food < res.food_max * 0.05:
            msg = "⚠ Food critically scarce"
            world.log(msg)
            logger.warning("%s %s: %s", LOG_PREFIX, world.name, msg)

        if res.water <= 0 and res.food <= 0:
            world.is_habitable = False
            msg = "Resource collapse – world marked UNINHABITABLE"
            world.log(msg)
            logger.error("%s %s: %s", LOG_PREFIX, world.name, msg)
