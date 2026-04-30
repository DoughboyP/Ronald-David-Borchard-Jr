"""
El Capitan – Tier 3: Ecology Processor
Handles ecological and entity interactions: births, deaths, predation, sapience
emergence, and inter-species dynamics. Runs in its own thread as part of the
triple-processing architecture.
"""

from __future__ import annotations

import logging
import random
from typing import List

from .constants import (
    ENTITY_BIRTH_RATE,
    ENTITY_DEATH_RATE,
    ENTITY_TYPES,
    LOG_PREFIX,
    MAX_ENTITIES_PER_WORLD,
    SAPIENCE_EMERGENCE_MIN_POPULATION,
)
from .models import Entity, World

logger = logging.getLogger(__name__)


class EcologyProcessor:
    """
    Tier-3 processor: ecological and entity interactions.

    Responsibilities:
    - Population growth and natural mortality
    - Resource-driven carrying capacity enforcement
    - Inter-species predation and competition
    - Sapience emergence for advanced entities
    - Entity health fluctuations based on environmental stress
    """

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng
        self._next_uid = 1000  # UID counter for newly spawned entities

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(self, worlds: List[World]) -> None:
        """
        Run one ecology tick across all worlds.
        Called by the TripleProcessor from Tier-3 thread.
        """
        for world in worlds:
            if not world.is_habitable:
                self._handle_extinction(world)
                continue
            self._update_health(world)
            self._apply_mortality(world)
            self._apply_growth(world)
            self._check_sapience_emergence(world)
            self._prune_dead(world)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _update_health(self, world: World) -> None:
        """
        Adjust entity health based on resource abundance and environmental stress.
        """
        res = world.resources
        env = world.environment
        abundance = res.total_abundance()

        # Environmental stress factor (extreme temps are bad)
        temp_norm = abs(env.temperature_c) / 60.0  # 0–1
        stress = max(0.0, temp_norm - 0.5) * 0.2   # penalty only above 30 °C / below -30 °C

        for entity in world.entities:
            if not entity.is_alive():
                continue
            # Health moves toward abundance level, reduced by stress
            target_health = max(0.0, abundance - stress)
            delta = (target_health - entity.health) * 0.1
            entity.health = max(0.0, min(1.0, entity.health + delta))
            entity.age_ticks += 1

    def _apply_mortality(self, world: World) -> None:
        """
        Kill off individuals based on health and baseline death rate.
        """
        rng = self._rng
        for entity in world.entities:
            if not entity.is_alive():
                continue
            # Effective mortality increases when health is low
            effective_death_rate = ENTITY_DEATH_RATE + (1.0 - entity.health) * 0.05
            deaths = int(entity.population * effective_death_rate * rng.uniform(0.5, 1.5))
            entity.population = max(0, entity.population - deaths)

    def _apply_growth(self, world: World) -> None:
        """
        Reproduce surviving entities up to carrying capacity.
        """
        rng = self._rng
        res = world.resources
        abundance = res.total_abundance()

        for entity in world.entities:
            if not entity.is_alive():
                continue
            # Growth scaled by food abundance and health
            effective_birth_rate = ENTITY_BIRTH_RATE * entity.health * abundance
            births = int(entity.population * effective_birth_rate * rng.uniform(0.8, 1.2))
            entity.population = min(entity.population + births, 100_000)

        # Spawn new species if capacity allows
        if (
            len(world.entities) < MAX_ENTITIES_PER_WORLD
            and rng.random() < 0.05 * abundance
        ):
            self._spawn_new_entity(world)

    def _spawn_new_entity(self, world: World) -> None:
        """Introduce a new entity (species) to the world."""
        rng = self._rng
        kind = rng.choice(ENTITY_TYPES[:-1])  # no Sapient at spawn
        entity = Entity(
            uid=self._next_uid,
            kind=kind,
            population=rng.randint(5, 100),
            health=rng.uniform(0.4, 0.9),
        )
        self._next_uid += 1
        world.entities.append(entity)
        msg = f"New species emerged: {entity.summary()}"
        world.log(msg)
        logger.debug("%s %s: %s", LOG_PREFIX, world.name, msg)

    def _check_sapience_emergence(self, world: World) -> None:
        """
        Once world population is large enough, a Fauna or Avian entity may
        develop sapience.
        """
        rng = self._rng
        total_pop = world.total_population()

        if total_pop < SAPIENCE_EMERGENCE_MIN_POPULATION:
            return
        if world.has_sapient_life():
            return  # already achieved

        # Probability grows with population and world age
        emergence_prob = min(0.01 * (total_pop / SAPIENCE_EMERGENCE_MIN_POPULATION), 0.1)
        if rng.random() < emergence_prob:
            candidates = [
                e for e in world.entities
                if e.kind in ("Fauna", "Avian") and e.is_alive() and not e.sapient
            ]
            if candidates:
                chosen = rng.choice(candidates)
                original_kind = chosen.kind
                chosen.sapient = True
                chosen.kind = "Sapient"
                msg = (
                    f"🧠 Sapience emerged! {original_kind} uid={chosen.uid} "
                    f"(pop={chosen.population})"
                )
                world.log(msg)
                logger.info("%s %s: %s", LOG_PREFIX, world.name, msg)

    def _prune_dead(self, world: World) -> None:
        """Remove extinct entities to keep the list lean."""
        before = len(world.entities)
        world.entities = [e for e in world.entities if e.is_alive()]
        pruned = before - len(world.entities)
        if pruned:
            logger.debug(
                "%s %s: Pruned %d extinct entities",
                LOG_PREFIX, world.name, pruned,
            )

    def _handle_extinction(self, world: World) -> None:
        """When a world becomes uninhabitable, accelerate entity die-off."""
        for entity in world.entities:
            entity.population = max(0, int(entity.population * 0.5))
            entity.health = max(0.0, entity.health - 0.1)
