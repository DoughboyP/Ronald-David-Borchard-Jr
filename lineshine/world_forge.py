"""
Lineshine – World Forge
Unlimited world-creation logic for the Lineshine computer.

The WorldForge accepts commands from the controller (Ronald) and
materialises new worlds inside the system.  There is no cap on the
number of worlds that can be created — each call to ``forge`` adds
a new world to the ever-growing multiverse.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional

from .constants import (
    LOG_PREFIX,
    POPULATION_GROWTH_RATE,
    WORLD_NAME_POOL,
    WORLD_STABILITY_DECAY,
    WORLD_TYPES,
)
from .models import LineshineWorld


class WorldForge:
    """
    Unlimited world-creation engine.

    The controller can call ``forge()`` as many times as desired.
    Each call mints a new ``LineshineWorld`` with a unique uid,
    optionally driven by user-supplied parameters.
    """

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng
        self._counter = 0
        self._worlds: Dict[int, LineshineWorld] = {}
        self._used_names: set = set()

    # ------------------------------------------------------------------
    # Core creation
    # ------------------------------------------------------------------

    def forge(
        self,
        name: Optional[str] = None,
        world_type: Optional[str] = None,
        creator_note: str = "",
    ) -> LineshineWorld:
        """
        Create a new world and register it in the forge.

        Parameters
        ----------
        name:
            Custom name for the world.  If omitted a unique name is
            drawn from the built-in pool (or auto-generated if the pool
            is exhausted).
        world_type:
            One of the ``WORLD_TYPES``.  If omitted, chosen at random.
        creator_note:
            Optional personal annotation from the controller.

        Returns
        -------
        LineshineWorld
            The freshly forged world.
        """
        self._counter += 1
        uid = self._counter

        resolved_name = self._resolve_name(name)
        if world_type and world_type not in WORLD_TYPES:
            raise ValueError(
                f"Unknown world type '{world_type}'. "
                f"Valid types: {', '.join(WORLD_TYPES)}"
            )

        world = LineshineWorld.forge(
            uid=uid,
            name=resolved_name,
            rng=self._rng,
            world_type=world_type,
            creator_note=creator_note,
        )
        self._worlds[uid] = world
        print(
            f"{LOG_PREFIX} ✦ World #{uid} '{resolved_name}' forged "
            f"({world.world_type}, radius={world.radius_km:,.0f} km, "
            f"pop={world.population:,})"
        )
        return world

    # ------------------------------------------------------------------
    # Management
    # ------------------------------------------------------------------

    def tick_all(self) -> None:
        """Advance all active worlds by one simulation tick."""
        for world in self._worlds.values():
            if not world.is_active:
                continue
            world.age_ticks += 1
            # Population growth
            growth = int(world.population * POPULATION_GROWTH_RATE * self._rng.uniform(0.5, 1.5))
            world.population = max(0, world.population + growth)
            # Stability drift
            delta = self._rng.uniform(-WORLD_STABILITY_DECAY * 2, WORLD_STABILITY_DECAY)
            world.stability = max(0.0, min(1.0, world.stability + delta))
            # Collapse check
            if world.stability <= 0.0:
                world.is_active = False
                world.log("World collapsed — stability reached zero.")
                print(f"{LOG_PREFIX} ⚠ World '{world.name}' has collapsed.")

    def deactivate(self, uid: int) -> None:
        """Put a world into dormant (inactive) state."""
        world = self._get(uid)
        world.is_active = False
        world.log("World deactivated by controller.")
        print(f"{LOG_PREFIX} 💤 World '{world.name}' deactivated.")

    def reactivate(self, uid: int) -> None:
        """Restore a dormant world to active state."""
        world = self._get(uid)
        world.is_active = True
        world.log("World reactivated by controller.")
        print(f"{LOG_PREFIX} ✅ World '{world.name}' reactivated.")

    def destroy(self, uid: int) -> None:
        """Permanently remove a world from the forge."""
        world = self._get(uid)
        name = world.name
        del self._worlds[uid]
        self._used_names.discard(name)
        print(f"{LOG_PREFIX} 💥 World '{name}' (uid={uid}) destroyed.")

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_world(self, uid: int) -> LineshineWorld:
        return self._get(uid)

    def all_worlds(self) -> List[LineshineWorld]:
        return list(self._worlds.values())

    def active_worlds(self) -> List[LineshineWorld]:
        return [w for w in self._worlds.values() if w.is_active]

    @property
    def total_count(self) -> int:
        return len(self._worlds)

    @property
    def active_count(self) -> int:
        return sum(1 for w in self._worlds.values() if w.is_active)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_name(self, name: Optional[str]) -> str:
        if name:
            if name in self._used_names:
                # Append uid to make it unique
                name = f"{name}-{self._counter}"
            self._used_names.add(name)
            return name

        # Draw from pool, fall back to generated name
        available = [n for n in WORLD_NAME_POOL if n not in self._used_names]
        if available:
            chosen = self._rng.choice(available)
        else:
            chosen = f"World-{self._counter}"
        self._used_names.add(chosen)
        return chosen

    def _get(self, uid: int) -> LineshineWorld:
        if uid not in self._worlds:
            raise KeyError(f"No world with uid={uid}.")
        return self._worlds[uid]
