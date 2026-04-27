"""
MOB CHESS: Universe Control
Entities – data classes for every actor and location in the game.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict


# ──────────────────────────────────────────────
# Solar System
# ──────────────────────────────────────────────

@dataclass
class SolarSystem:
    """One node on the universe board."""
    galaxy_idx: int
    sys_idx:    int
    name:       str
    controller: int = 0           # NEUTRAL / PLAYER / CHAOS / ORDER
    bodies:     List[dict] = field(default_factory=list)   # uncollected bodies here
    has_piece:  Optional[str] = None   # "CHAOS" | "ORDER" | None

    @property
    def coord(self) -> tuple:
        return (self.galaxy_idx, self.sys_idx)

    def __repr__(self) -> str:
        return f"SolarSystem({self.name!r}, ctrl={self.controller})"


# ──────────────────────────────────────────────
# Galaxy
# ──────────────────────────────────────────────

@dataclass
class Galaxy:
    """A collection of five solar systems."""
    idx:     int
    name:    str
    systems: List[SolarSystem] = field(default_factory=list)

    def controlled_by(self, controller: int) -> int:
        return sum(1 for s in self.systems if s.controller == controller)


# ──────────────────────────────────────────────
# Player (The Demigod)
# ──────────────────────────────────────────────

@dataclass
class Player:
    """The player-controlled demigod."""
    name:          str   = "The Demigod"
    hp:            int   = 100
    max_hp:        int   = 100
    power:         int   = 15
    cred:          int   = 0
    position:      tuple = (0, 0)      # (galaxy_idx, sys_idx)
    bodies_worn:   List[dict] = field(default_factory=list)
    abilities_used: Dict[str, bool] = field(default_factory=dict)   # one-shot tracker

    # ── body management ──────────────────────────────────

    def wear_body(self, body: dict) -> None:
        """Put on a collected body, gaining its stats."""
        self.bodies_worn.append(body)
        self.power   += body["power"]
        self.max_hp  += body["hp"]
        self.hp      = min(self.hp + body["hp"], self.max_hp)

    def has_ability(self, ability: str) -> bool:
        return any(b["ability"] == ability for b in self.bodies_worn)

    def ability_available(self, ability: str) -> bool:
        """True if the one-shot ability hasn't been used yet."""
        return self.has_ability(ability) and not self.abilities_used.get(ability, False)

    def use_ability(self, ability: str) -> None:
        self.abilities_used[ability] = True

    # ── stats ────────────────────────────────────────────

    @property
    def bodies_count(self) -> int:
        return len(self.bodies_worn)

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: int) -> None:
        self.hp = min(self.hp + amount, self.max_hp)

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    def status_line(self) -> str:
        bar_len = 20
        filled  = int((self.hp / self.max_hp) * bar_len) if self.max_hp else 0
        bar     = "█" * filled + "░" * (bar_len - filled)
        return (
            f"  👑 {self.name}  |  HP [{bar}] {self.hp}/{self.max_hp}"
            f"  |  PWR {self.power}  |  CRED {self.cred}"
            f"  |  BODIES {self.bodies_count}"
        )


# ──────────────────────────────────────────────
# God Piece (avatar on the board)
# ──────────────────────────────────────────────

@dataclass
class GodPiece:
    """
    A God's physical avatar – moves around the board taking territory
    and threatening the demigod.
    """
    god_name:  str
    position:  tuple
    hp:        int   = 40
    max_hp:    int   = 40
    power:     int   = 22
    symbol:    str   = "???"

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    def heal_full(self) -> None:
        """Gods regenerate between games."""
        self.hp = self.max_hp

    def status_line(self) -> str:
        return (
            f"  ⚡ {self.god_name}'s Avatar  |  HP {self.hp}/{self.max_hp}"
            f"  |  PWR {self.power}  |  Pos {self.position}"
        )
