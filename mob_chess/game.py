"""
MOB CHESS: Universe Control
Game – the full game loop, combat resolution, and player interface.

You are the Demigod.
Two Gods – THE ARCHITECT OF CHAOS and THE SOVEREIGN OF ORDER – are
playing a cosmic chess match with the entire universe as the board.
You hustle in the spaces between their moves, collecting the bodies
of fallen soldiers, wearing them like armour, and seizing solar
systems until the whole universe bows to you.

Run the universe on some mob pimp shit.
"""

from __future__ import annotations
import random
import sys
from typing import List, Tuple

from .constants import (
    GAME_TITLE,
    VERSION,
    LINE_WIDTH,
    NEUTRAL,
    PLAYER,
    CHAOS,
    ORDER,
    CONTROL_NAMES,
    TOTAL_SYSTEMS,
    WIN_SYSTEMS,
    GOD_WIN_SYSTEMS,
    NEUTRAL_CLAIM_COST,
    ATTACKER_ROLL_MAX,
    DEFENDER_ROLL_MAX,
    DEFENDER_BONUS,
    CRED_PER_HUSTLE,
    MAX_BODIES_WORN,
    PLAYER_START_HP,
    PLAYER_START_POWER,
    GOD_CHAOS_NAME,
    GOD_ORDER_NAME,
)
from .entities import Player, GodPiece
from .universe import Universe
from .ai import GodAI


# ══════════════════════════════════════════════════════════════════════
# ASCII art / banners
# ══════════════════════════════════════════════════════════════════════

_BANNER = r"""
 ███╗   ███╗ ██████╗ ██████╗      ██████╗██╗  ██╗███████╗███████╗███████╗
 ████╗ ████║██╔═══██╗██╔══██╗    ██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝
 ██╔████╔██║██║   ██║██████╔╝    ██║     ███████║█████╗  ███████╗███████╗
 ██║╚██╔╝██║██║   ██║██╔══██╗    ██║     ██╔══██║██╔══╝  ╚════██║╚════██║
 ██║ ╚═╝ ██║╚██████╔╝██████╔╝    ╚██████╗██║  ██║███████╗███████║███████║
 ╚═╝     ╚═╝ ╚═════╝ ╚═════╝      ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
"""

_SUBTITLE = "  U N I V E R S E   C O N T R O L   ·   Run the cosmos on mob pimp shit"


def _div(char: str = "─") -> str:
    return char * LINE_WIDTH


# ══════════════════════════════════════════════════════════════════════
# Main Game Class
# ══════════════════════════════════════════════════════════════════════

class MobChessGame:
    """Full game controller."""

    def __init__(self, seed: int = None) -> None:
        seed = seed or random.randint(1, 99999)
        self._rng   = random.Random(seed)
        self._turn  = 0
        self._log: List[str] = []

        # Build world
        self._universe = Universe(rng=random.Random(seed + 1))

        # Build player
        self._player = Player(
            hp=PLAYER_START_HP,
            max_hp=PLAYER_START_HP,
            power=PLAYER_START_POWER,
        )

        # Claim starting system for player
        start_sys = self._universe.get_system(0, 0)
        start_sys.controller = PLAYER
        self._player.position = (0, 0)

        # God AIs
        self._chaos_ai = GodAI("CHAOS", random.Random(seed + 2))
        self._order_ai = GodAI("ORDER", random.Random(seed + 3))

        # Track special ability uses
        self._rewind_saved: bool = False
        self._rewind_state: dict = {}

    # ──────────────────────────────────────────────────────────────────
    # Public entry point
    # ──────────────────────────────────────────────────────────────────

    def run(self) -> None:
        """Start and run the game until win/loss."""
        self._print_title()
        self._player.name = self._ask_name()
        print(f"\n  You are {self._player.name}. The universe awaits.\n")
        input("  [Press ENTER to begin your reign...]")

        while True:
            self._turn += 1
            self._render_hud()

            action = self._get_action()
            if action is None:
                continue

            self._execute_action(action)

            # Save rewind state after player acts (before god moves)
            if self._player.ability_available("rewind"):
                self._save_rewind_state()

            # God turns
            self._god_turn()

            # Win / lose check
            outcome = self._check_outcome()
            if outcome == "win":
                self._print_win()
                break
            elif outcome == "lose":
                self._print_lose()
                break

    # ──────────────────────────────────────────────────────────────────
    # HUD / display
    # ──────────────────────────────────────────────────────────────────

    def _render_hud(self) -> None:
        print("\n" + _div("═"))
        print(f"  TURN {self._turn:>3}   |   MOB CHESS: UNIVERSE CONTROL")
        print(_div("═"))
        print(self._universe.render_map(self._player.position))
        print(_div())
        print(self._player.status_line())
        if self._log:
            print(_div())
            for msg in self._log[-6:]:     # show last 6 log lines
                print(msg)
        self._log.clear()
        print(_div())

    # ──────────────────────────────────────────────────────────────────
    # Action selection
    # ──────────────────────────────────────────────────────────────────

    _ACTIONS = {
        "1": "MOVE       – Travel to an adjacent solar system",
        "2": "CLAIM      – Take control of your current system (or defend it)",
        "3": "COLLECT    – Pick up a body in your current system",
        "4": "HUSTLE     – Extract cred from your territory",
        "5": "BODIES     – View your worn bodies and abilities",
        "6": "MAP        – Print the full universe map",
        "7": "SPECIALS   – Use a special ability",
        "0": "QUIT",
    }

    def _get_action(self) -> str | None:
        print("\n  What do you do?")
        for k, v in self._ACTIONS.items():
            print(f"    [{k}] {v}")
        choice = input("\n  > ").strip()
        if choice not in self._ACTIONS:
            print("  ❌ Not a valid move. Try again.")
            return None
        return choice

    # ──────────────────────────────────────────────────────────────────
    # Action execution
    # ──────────────────────────────────────────────────────────────────

    def _execute_action(self, choice: str) -> None:
        if choice == "1":
            self._action_move()
        elif choice == "2":
            self._action_claim()
        elif choice == "3":
            self._action_collect()
        elif choice == "4":
            self._action_hustle()
        elif choice == "5":
            self._action_view_bodies()
        elif choice == "6":
            print(self._universe.render_map(self._player.position))
            input("  [Press ENTER to continue...]")
        elif choice == "7":
            self._action_specials()
        elif choice == "0":
            print("\n  You walk away from the universe. The Gods win.")
            sys.exit(0)

    # ── Move ──────────────────────────────────────────────────────────

    def _action_move(self) -> None:
        pos  = self._player.position
        nbrs = self._universe.neighbors(*pos)
        if not nbrs:
            self._log.append("  No adjacent systems to move to!")
            return

        # Ghost Rider: can move 2 hops
        steps = 2 if self._player.has_ability("dash") else 1

        for step_num in range(steps):
            nbrs = self._universe.neighbors(*self._player.position)
            print(f"\n  Adjacent systems (step {step_num + 1}/{steps}):")
            for i, (gi, si) in enumerate(nbrs, 1):
                sys_obj = self._universe.get_system(gi, si)
                ctrl    = CONTROL_NAMES[sys_obj.controller]
                bodies  = f"  💀×{len(sys_obj.bodies)}" if sys_obj.bodies else ""
                print(f"    [{i}] {sys_obj.name}  ({ctrl}){bodies}")
            print("    [0] Cancel")
            choice = input("  Move to: ").strip()
            if choice == "0":
                break
            try:
                idx = int(choice) - 1
                dest = nbrs[idx]
            except (ValueError, IndexError):
                print("  ❌ Invalid.")
                break
            self._player.position = dest
            dest_sys = self._universe.get_system(*dest)
            self._log.append(
                f"  🚀 You move to {dest_sys.name}."
            )
            # If God piece is there, take automatic damage
            if dest_sys.has_piece:
                self._log.append(
                    f"  ⚡ {dest_sys.has_piece}'s avatar is here! Watch your step."
                )
            if step_num < steps - 1:
                cont = input("  Use second step? [y/n]: ").strip().lower()
                if cont != "y":
                    break

    # ── Claim ─────────────────────────────────────────────────────────

    def _action_claim(self) -> None:
        sys_obj = self._universe.get_system(*self._player.position)
        ctrl    = sys_obj.controller

        if ctrl == PLAYER:
            self._log.append("  ✅ You already run this system.")
            return

        if ctrl == NEUTRAL:
            # Auto-claim with HP cost (a little blood to expand)
            self._player.take_damage(NEUTRAL_CLAIM_COST)
            sys_obj.controller = PLAYER
            self._log.append(
                f"  👑 You claim {sys_obj.name}! "
                f"(Cost: {NEUTRAL_CLAIM_COST} HP)"
            )
            return

        # Enemy-controlled: fight the God's piece (or weaken control)
        god_key = "CHAOS" if ctrl == CHAOS else "ORDER"
        piece   = self._universe.piece_for(god_key)
        self._log.append(
            f"  ⚔  Battling for {sys_obj.name} ({CONTROL_NAMES[ctrl]} territory)..."
        )
        won, dmg_dealt, dmg_taken = self._combat(
            atk_power=self._player.power,
            def_power=piece.power if piece.is_alive else 10,
            has_dodge=self._player.has_ability("dodge"),
            has_crush=self._player.has_ability("crush"),
        )
        if won:
            sys_obj.controller = PLAYER
            self._log.append(
                f"  💥 You took {sys_obj.name}! Dealt {dmg_dealt} dmg."
            )
            # Drain ability
            if self._player.has_ability("drain"):
                heal_amt = 10
                self._player.heal(heal_amt)
                self._log.append(f"  🩸 Soul Collector drains {heal_amt} HP back to you.")
        else:
            self._player.take_damage(dmg_taken)
            self._log.append(
                f"  😤 You got pushed back. Took {dmg_taken} HP damage."
            )
            # Check shield one-shot
            if self._player.hp <= 0 and self._player.ability_available("shield"):
                self._player.hp = 1
                self._player.use_ability("shield")
                self._log.append("  🛡  Cosmic Pawn absorbs the fatal blow! (Shield used)")

    # ── Collect body ──────────────────────────────────────────────────

    def _action_collect(self) -> None:
        sys_obj = self._universe.get_system(*self._player.position)
        if not sys_obj.bodies:
            self._log.append("  No bodies here to collect.")
            return

        if self._player.bodies_count >= MAX_BODIES_WORN:
            self._log.append(
                f"  You're already wearing {MAX_BODIES_WORN} bodies. "
                "That's the limit — you can't wear any more."
            )
            return

        body = sys_obj.bodies.pop(0)
        self._player.wear_body(body)
        self._log.append(
            f"  💀 You put on {body['name']}. "
            f"+{body['power']} PWR  +{body['hp']} HP  |  {body['desc']}"
        )

    # ── Hustle ────────────────────────────────────────────────────────

    def _action_hustle(self) -> None:
        count = self._universe.controlled_count(PLAYER)
        earned = count * CRED_PER_HUSTLE
        self._player.cred += earned
        self._log.append(
            f"  💰 Hustled {earned} cred from {count} systems. "
            f"Total cred: {self._player.cred}"
        )

    # ── View bodies ───────────────────────────────────────────────────

    def _action_view_bodies(self) -> None:
        print(f"\n  {_div()}")
        print(f"  BODIES WORN ({self._player.bodies_count}/{MAX_BODIES_WORN})")
        print(f"  {_div()}")
        if not self._player.bodies_worn:
            print("  You ain't wearing nobody yet. Get out there and catch some.")
        for i, b in enumerate(self._player.bodies_worn, 1):
            used = " [USED]" if self._player.abilities_used.get(b["ability"]) else ""
            print(f"  {i:>2}. {b['name']:<18}  PWR+{b['power']}  HP+{b['hp']}"
                  f"  │ {b['desc']}{used}")
        print(f"  {_div()}")
        input("  [Press ENTER to continue...]")

    # ── Special abilities ─────────────────────────────────────────────

    def _action_specials(self) -> None:
        one_shots = {
            "reap":     "Galaxy Reaper – instantly claim any neutral system",
            "warp":     "Dimensional Lord – warp to any system in the universe",
            "supernova":"Star Crusher – weaken ALL enemy systems in your galaxy",
            "void":     "Void King – nullify the next God action",
            "rewind":   "Time Bender – undo your last combat (restore state)",
        }
        available = {
            k: v for k, v in one_shots.items()
            if self._player.ability_available(k)
        }
        if not available:
            print(
                "\n  You have no special abilities available.\n"
                "  Collect bodies with one-shot powers to unlock them."
            )
            input("  [ENTER]")
            return

        print("\n  SPECIAL ABILITIES:")
        keys = list(available.keys())
        for i, k in enumerate(keys, 1):
            print(f"    [{i}] {available[k]}")
        print("    [0] Cancel")
        choice = input("  > ").strip()
        if choice == "0":
            return
        try:
            ability = keys[int(choice) - 1]
        except (ValueError, IndexError):
            print("  ❌ Invalid choice.")
            return
        self._use_special(ability)

    def _use_special(self, ability: str) -> None:
        u = self._universe
        p = self._player

        if ability == "reap":
            neutrals = [s for s in u.all_systems() if s.controller == NEUTRAL]
            if not neutrals:
                self._log.append("  No neutral systems left to reap.")
                return
            print("\n  Choose a neutral system to claim instantly:")
            for i, s in enumerate(neutrals, 1):
                print(f"    [{i}] {s.name}  ({u.galaxies[s.galaxy_idx].name})")
            try:
                idx  = int(input("  > ").strip()) - 1
                target = neutrals[idx]
                target.controller = PLAYER
                p.use_ability("reap")
                self._log.append(f"  💀 Galaxy Reaper claims {target.name}!")
            except (ValueError, IndexError):
                print("  ❌ Cancelled.")

        elif ability == "warp":
            all_sys = u.all_systems()
            print("\n  Choose your destination:")
            for i, s in enumerate(all_sys, 1):
                gname = u.galaxies[s.galaxy_idx].name
                print(f"    [{i:>2}] {s.name}  ({gname})")
            try:
                idx  = int(input("  > ").strip()) - 1
                dest = all_sys[idx]
                p.position = dest.coord
                p.use_ability("warp")
                self._log.append(f"  🌀 Dimensional Lord warps you to {dest.name}!")
            except (ValueError, IndexError):
                print("  ❌ Cancelled.")

        elif ability == "supernova":
            gi  = p.position[0]
            galaxy = u.galaxies[gi]
            count = 0
            for s in galaxy.systems:
                if s.controller in (CHAOS, ORDER):
                    # Weaken: flip to neutral
                    s.controller = NEUTRAL
                    count += 1
            p.use_ability("supernova")
            self._log.append(
                f"  💥 SUPERNOVA! {count} enemy systems in {galaxy.name} "
                "blasted back to neutral!"
            )

        elif ability == "void":
            # Flagged – GodAI will skip one turn total (handled in god_turn)
            p.use_ability("void")
            p.abilities_used["void_active"] = True
            self._log.append("  🕳  VOID KING nullifies the next God action!")

        elif ability == "rewind":
            if self._rewind_saved:
                self._load_rewind_state()
                p.use_ability("rewind")
                self._log.append(
                    "  ⏪ TIME BENDER rewinds! You're back to before that last battle."
                )
            else:
                self._log.append("  ⏪ No rewind state saved yet.")

    # ──────────────────────────────────────────────────────────────────
    # Combat
    # ──────────────────────────────────────────────────────────────────

    def _combat(
        self,
        atk_power: int,
        def_power: int,
        has_dodge: bool = False,
        has_crush: bool = False,
    ) -> Tuple[bool, int, int]:
        """
        Returns (player_won, damage_dealt, damage_taken).
        """
        atk_roll = self._rng.randint(1, ATTACKER_ROLL_MAX)
        def_roll = self._rng.randint(1, DEFENDER_ROLL_MAX) + DEFENDER_BONUS

        if has_crush:
            atk_roll += 8

        atk_total = atk_power + atk_roll
        def_total = def_power + def_roll

        won = atk_total > def_total

        if won:
            dmg_dealt = atk_roll + (atk_power // 4)
            dmg_taken = max(0, def_roll - atk_roll // 2)
        else:
            dmg_dealt = 0
            dmg_taken = def_roll + (def_power // 5)
            if has_dodge and self._rng.random() < 0.30:
                dmg_taken = 0
                self._log.append("  👻 Shadow Walker dodges the counter-attack!")

        return won, dmg_dealt, dmg_taken

    # ──────────────────────────────────────────────────────────────────
    # God turns
    # ──────────────────────────────────────────────────────────────────

    def _god_turn(self) -> None:
        void_active = self._player.abilities_used.get("void_active", False)

        for god_key, ai, piece in [
            ("CHAOS", self._chaos_ai, self._universe.chaos_piece),
            ("ORDER", self._order_ai, self._universe.order_piece),
        ]:
            if void_active:
                self._log.append(
                    f"  🕳  VOID KING blocks {GOD_CHAOS_NAME if god_key == 'CHAOS' else GOD_ORDER_NAME}!"
                )
                self._player.abilities_used["void_active"] = False
                void_active = False
                continue

            messages, dmg = ai.take_turn(
                universe=self._universe,
                player_pos=self._player.position,
                player_power=self._player.power,
                piece=piece,
            )
            self._log.extend(messages)

            if dmg > 0:
                # Check shield
                if self._player.ability_available("shield"):
                    self._player.use_ability("shield")
                    self._log.append("  🛡  Cosmic Pawn absorbs the God's blow! (Shield used)")
                else:
                    self._player.take_damage(dmg)
                    self._log.append(
                        f"  💥 You took {dmg} damage! HP: {self._player.hp}/{self._player.max_hp}"
                    )

    # ──────────────────────────────────────────────────────────────────
    # Win / lose
    # ──────────────────────────────────────────────────────────────────

    def _check_outcome(self) -> str | None:
        if not self._player.is_alive:
            return "lose"
        player_ctrl = self._universe.controlled_count(PLAYER)
        if player_ctrl >= WIN_SYSTEMS:
            return "win"
        for ctrl_val, name in [(CHAOS, GOD_CHAOS_NAME), (ORDER, GOD_ORDER_NAME)]:
            if self._universe.controlled_count(ctrl_val) >= GOD_WIN_SYSTEMS:
                self._log.append(f"  ⚠  {name} has dominated the universe...")
                return "lose"
        return None

    # ──────────────────────────────────────────────────────────────────
    # Rewind state
    # ──────────────────────────────────────────────────────────────────

    def _save_rewind_state(self) -> None:
        p = self._player
        self._rewind_state = {
            "hp":       p.hp,
            "max_hp":   p.max_hp,
            "power":    p.power,
            "cred":     p.cred,
            "position": p.position,
            "bodies":   list(p.bodies_worn),
        }
        self._rewind_saved = True

    def _load_rewind_state(self) -> None:
        s = self._rewind_state
        p = self._player
        p.hp       = s["hp"]
        p.max_hp   = s["max_hp"]
        p.power    = s["power"]
        p.cred     = s["cred"]
        p.position = s["position"]
        p.bodies_worn = list(s["bodies"])

    # ──────────────────────────────────────────────────────────────────
    # Title / end screens
    # ──────────────────────────────────────────────────────────────────

    def _print_title(self) -> None:
        print(_BANNER)
        print(_SUBTITLE)
        print()
        print(_div("═"))
        print(
            "  Two Gods play a cosmic chess match with the universe as the board.\n"
            "  You are a DEMIGOD rising in the cracks between their moves.\n"
            "  Collect bodies. Wear them. Run the whole universe.\n"
        )
        print(
            f"  {GOD_CHAOS_NAME} controls 5 systems.  "
            f"{GOD_ORDER_NAME} controls 5 systems.\n"
            f"  You control 1 system.  Run the universe from 20 total.\n"
            f"  WIN:  control ≥{WIN_SYSTEMS} systems ({WIN_SYSTEMS}/{TOTAL_SYSTEMS} = majority).\n"
            f"  LOSE: your HP hits 0, or a God controls ≥{GOD_WIN_SYSTEMS} systems."
        )
        print(_div("═"))

    def _ask_name(self) -> str:
        name = input("\n  Enter your demigod name (or ENTER for default): ").strip()
        return name if name else "The Demigod"

    def _print_win(self) -> None:
        print("\n" + _div("═"))
        print(
            f"\n  👑👑👑  {self._player.name.upper()} RUNS THE WHOLE UNIVERSE  👑👑👑\n"
            f"\n  You wore {self._player.bodies_count} bodies."
            f"  You ran {self._universe.controlled_count(PLAYER)} solar systems.\n"
            f"  The Gods bow.\n"
            f"\n  MOB PIMP SHIT.  The cosmos is yours.\n"
        )
        print(_div("═"))

    def _print_lose(self) -> None:
        print("\n" + _div("═"))
        if not self._player.is_alive:
            print(
                f"\n  💀  {self._player.name.upper()} FELL.\n"
                "  The Gods kept playing. You were a piece, not a player.\n"
            )
        else:
            print(
                "\n  ⚫  THE UNIVERSE HAS BEEN TAKEN.\n"
                "  The Gods divided everything. You got left out.\n"
            )
        print(
            f"  Bodies worn: {self._player.bodies_count}  |  "
            f"Systems held at peak: {self._universe.controlled_count(PLAYER)}\n"
        )
        print("  Try again?\n")
        print(_div("═"))
