"""
Lineshine – Computer
Top-level orchestrator for the Lineshine world-creation engine.

The Lineshine computer sits in Shenzhen, China, with Ra's Eye installed
at its core.  Ronald David Borchard Jr is the sole controller with
authority to forge, inspect, and govern unlimited worlds within its system.
"""

from __future__ import annotations

import os
import random
import sys
from typing import List, Optional

from .constants import (
    COMPUTER_FULL_NAME,
    COMPUTER_LOCATION,
    COMPUTER_NAME,
    COMPUTER_OWNER,
    COMPUTER_VERSION,
    EYE_PREFIX,
    LINE_WIDTH,
    LOG_PREFIX,
    WORLD_TYPES,
)
from .models import LineshineWorld
from .ras_eye import RasEye
from .world_forge import WorldForge


_BANNER = r"""
  _     ___ _   _ _____ ____  _   _ ___ _   _ _____
 | |   |_ _| \ | | ____/ ___|| | | |_ _| \ | | ____|
 | |    | ||  \| |  _| \___ \| |_| || ||  \| |  _|
 | |___ | || |\  | |___ ___) |  _  || || |\  | |___
 |_____|___|_| \_|_____|____/ |_| |_|___|_| \_|_____|

  {full_name}
  Location   : {location}
  Controller : {owner}
  Ra's Eye   : INSTALLED  ☀
"""

_HELP = """
  ── Commands ──────────────────────────────────────────────────
  create  [type] [name]   Forge a new world (type and name optional)
  list                    List all worlds
  info    <num>           Show detailed info for a world
  scan    <num>           Have Ra's Eye observe a specific world
  scan-all                Have Ra's Eye observe every active world
  tick    [n]             Advance all worlds by n ticks (default 1)
  deactivate <num>        Put a world into dormant state
  reactivate <num>        Restore a dormant world
  destroy <num>           Permanently destroy a world
  save    [file]          Save all worlds to a file
  eye                     Show Ra's Eye status
  types                   List available world types
  help                    Show this help message
  quit                    Shut down Lineshine
  ──────────────────────────────────────────────────────────────
  Tip: 'create Volcanic FireReach' forges a named Volcanic world.
       'create MyWorld' forges a world of random type named MyWorld.
"""


class LineshineComputer:
    """
    Lineshine world-creation engine with Ra's Eye installed.

    Lifecycle
    ---------
    1. Call ``boot()`` to initialise Ra's Eye and the WorldForge.
    2. Call ``run_interactive()`` to enter the controller's command loop,
       or use the programmatic API (``forge``, ``tick``, etc.) directly.
    3. Call ``shutdown()`` when finished.

    Parameters
    ----------
    seed:
        Master random seed for reproducibility.
    save_file:
        Path to the JSON file used for auto-save on shutdown and
        auto-load on boot.  If ``None`` no automatic persistence occurs.
    """

    def __init__(self, seed: int = 2025, save_file: Optional[str] = None) -> None:
        self._seed = seed
        self._rng = random.Random(seed)
        self._forge: Optional[WorldForge] = None
        self._eye: Optional[RasEye] = None
        self._booted = False
        self._save_file = save_file

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def boot(self) -> None:
        """Initialise Ra's Eye and the WorldForge, print the boot banner."""
        print(_BANNER.format(
            full_name=COMPUTER_FULL_NAME,
            location=COMPUTER_LOCATION,
            owner=COMPUTER_OWNER,
        ))
        print(f"{LOG_PREFIX} Booting {COMPUTER_NAME} v{COMPUTER_VERSION}...")
        print(f"{LOG_PREFIX} Seed          : {self._seed}")

        self._forge = WorldForge(rng=self._rng)
        self._eye = RasEye(rng=self._rng)
        self._eye.awaken()

        if self._save_file and os.path.isfile(self._save_file):
            try:
                self._forge.load(self._save_file)
            except Exception as exc:
                print(f"{LOG_PREFIX} ⚠ Could not load save file: {exc}")

        self._booted = True
        print(f"{LOG_PREFIX} ✅ {COMPUTER_NAME} online. Unlimited world creation ready.\n")

    def shutdown(self) -> None:
        """Print the final report, auto-save if configured, and power down."""
        self._require_boot()
        worlds = self._forge.all_worlds()

        print(f"\n{'═' * LINE_WIDTH}")
        print(f"{LOG_PREFIX} {COMPUTER_NAME} shutdown sequence initiated")
        print(f"{'═' * LINE_WIDTH}")

        if worlds:
            print(f"\n  {'Num':>4}  {'Type':<12}  {'Name':<16}  {'Pop':>9}  {'Stab'}")
            print(f"  {'─'*4}  {'─'*12}  {'─'*16}  {'─'*9}  {'─'*4}")
            for w in worlds:
                active = "✅" if w.is_active else "💤"
                print(
                    f"  {w.uid:>4}  {w.world_type:<12}  "
                    f"{(w.name or '—'):<16}  "
                    f"{w.population:>9,}  {w.stability:.2f}  {active}"
                )
        else:
            print("\n  No worlds were forged during this session.")

        print(f"\n  Total worlds forged : {self._forge.total_count}")
        print(f"  Active worlds       : {self._forge.active_count}")
        print()
        print(self._eye.status())

        if self._save_file:
            try:
                self._forge.save(self._save_file)
            except Exception as exc:
                print(f"{LOG_PREFIX} ⚠ Could not save worlds: {exc}")

        print(f"\n{LOG_PREFIX} 🛑 {COMPUTER_NAME} powered down. Ra's Eye dimmed.\n")

    # ------------------------------------------------------------------
    # Programmatic API
    # ------------------------------------------------------------------

    def forge(
        self,
        world_type: Optional[str] = None,
        name: str = "",
        creator_note: str = "",
    ) -> LineshineWorld:
        """Forge a new world and immediately observe it with Ra's Eye."""
        self._require_boot()
        world = self._forge.forge(world_type=world_type, name=name, creator_note=creator_note)
        vision = self._eye.observe(world)
        print(vision.display())
        print()
        return world

    def tick(self) -> None:
        """Advance all active worlds by one simulation tick."""
        self._require_boot()
        self._forge.tick_all()

    def scan(self, uid: int) -> None:
        """Have Ra's Eye observe a single world."""
        self._require_boot()
        world = self._forge.get_world(uid)
        vision = self._eye.observe(world)
        print(vision.display())
        print()

    def scan_all(self) -> None:
        """Have Ra's Eye observe every active world."""
        self._require_boot()
        visions = self._eye.scan_all(self._forge.all_worlds())
        for v in visions:
            print(v.display())
            print()

    def save(self, path: Optional[str] = None) -> None:
        """Save all worlds to a file (defaults to the configured save_file)."""
        self._require_boot()
        target = path or self._save_file
        if not target:
            target = "lineshine_worlds.json"
        self._save_file = target
        self._forge.save(target)

    @property
    def worlds(self) -> List[LineshineWorld]:
        self._require_boot()
        return self._forge.all_worlds()

    # ------------------------------------------------------------------
    # Interactive mode
    # ------------------------------------------------------------------

    def run_interactive(self) -> None:
        """Enter the controller's interactive command loop."""
        self._require_boot()
        print(f"{LOG_PREFIX} INTERACTIVE mode — type 'help' for commands.\n")

        while True:
            try:
                raw = input(f"[{COMPUTER_NAME}] > ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not raw:
                continue

            parts = raw.split()
            cmd = parts[0].lower()

            try:
                self._dispatch(cmd, parts[1:])
            except (KeyError, ValueError) as exc:
                print(f"  ❌ {exc}")
            except SystemExit:
                break

        self.shutdown()

    # ------------------------------------------------------------------
    # Internal – command dispatch
    # ------------------------------------------------------------------

    def _dispatch(self, cmd: str, args: List[str]) -> None:
        if cmd in ("quit", "exit", "q"):
            raise SystemExit

        elif cmd == "help":
            print(_HELP)

        elif cmd == "types":
            print("  Available world types:")
            for t in WORLD_TYPES:
                print(f"    • {t}")
            print()

        elif cmd == "create":
            wtype, name = self._parse_create_args(args)
            self.forge(world_type=wtype, name=name)

        elif cmd == "list":
            worlds = self._forge.all_worlds()
            if not worlds:
                print("  No worlds forged yet. Use 'create' to forge one.\n")
            else:
                print(f"\n  {'─' * (LINE_WIDTH - 2)}")
                for w in worlds:
                    print(f"  {w.status_line()}")
                print(f"  {'─' * (LINE_WIDTH - 2)}")
                print(
                    f"  Total: {self._forge.total_count}  "
                    f"Active: {self._forge.active_count}\n"
                )

        elif cmd == "info":
            uid = self._parse_uid(args)
            world = self._forge.get_world(uid)
            print()
            print(world.detail())
            print()

        elif cmd == "scan":
            uid = self._parse_uid(args)
            self.scan(uid)

        elif cmd in ("scan-all", "scanall"):
            self.scan_all()

        elif cmd == "tick":
            count = int(args[0]) if args else 1
            for _ in range(count):
                self.tick()
            print(f"{LOG_PREFIX} ⏩ Advanced {count} tick(s).\n")

        elif cmd == "deactivate":
            uid = self._parse_uid(args)
            self._forge.deactivate(uid)

        elif cmd == "reactivate":
            uid = self._parse_uid(args)
            self._forge.reactivate(uid)

        elif cmd == "destroy":
            uid = self._parse_uid(args)
            confirm = input(
                f"  Are you sure you want to destroy World {uid}? (yes/no): "
            ).strip().lower()
            if confirm == "yes":
                self._forge.destroy(uid)
            else:
                print("  Destruction cancelled.\n")

        elif cmd == "save":
            path = args[0] if args else None
            self.save(path)

        elif cmd == "eye":
            print()
            print(self._eye.status())
            print()

        else:
            print(f"  Unknown command '{cmd}'. Type 'help' for a list of commands.\n")

    @staticmethod
    def _parse_create_args(args: List[str]):
        """
        Parse optional ``[type] [name...]`` arguments for the ``create`` command.

        Rules:
        - If the first token is a valid world type, it is used as the type
          and any remaining tokens form the world name.
        - Otherwise all tokens form the world name and the type is chosen
          at random.
        """
        if not args:
            return None, ""
        if args[0].capitalize() in WORLD_TYPES:
            wtype = args[0].capitalize()
            name = " ".join(args[1:])
        else:
            wtype = None
            name = " ".join(args)
        return wtype, name

    @staticmethod
    def _parse_uid(args: List[str]) -> int:
        if not args:
            raise ValueError("A world uid is required for this command.")
        try:
            return int(args[0])
        except ValueError:
            raise ValueError(f"'{args[0]}' is not a valid uid integer.")

    def _require_boot(self) -> None:
        if not self._booted:
            raise RuntimeError(
                f"{COMPUTER_NAME} must be booted before operation. Call .boot() first."
            )
