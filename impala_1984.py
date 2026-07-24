"""
1984 Chevrolet Impala - Custom Build
Black on Black | 22" Chrome Forgiatos | Upgraded Engine | Full Sound System
"""


class Engine:
    """Upgraded engine for the 1984 Chevrolet Impala."""

    def __init__(self):
        self.name = "Upgraded 383 Stroker V8"
        self.displacement = "383 cubic inches (6.3L)"
        self.horsepower = 450
        self.torque_lb_ft = 490
        self.fuel_type = "Premium Unleaded"
        self.transmission = "700R4 Automatic Overdrive"
        self.is_running = False

    def start(self):
        self.is_running = True
        return "🔥 Engine roars to life — 383 Stroker V8 is RUNNING!"

    def stop(self):
        self.is_running = False
        return "Engine shut down."

    def rev(self):
        if self.is_running:
            return "VROOOOM 💨 — 450 horses ready to run!"
        return "Engine is off. Start the engine first."

    def status(self):
        state = "RUNNING ✅" if self.is_running else "OFF 🔴"
        return (
            f"\n  ┌─ ENGINE ─────────────────────────────────┐\n"
            f"  │  Name        : {self.name:<26}│\n"
            f"  │  Displacement: {self.displacement:<26}│\n"
            f"  │  Horsepower  : {self.horsepower} hp{'':<22}│\n"
            f"  │  Torque      : {self.torque_lb_ft} lb-ft{'':<20}│\n"
            f"  │  Transmission: {self.transmission:<26}│\n"
            f"  │  Fuel        : {self.fuel_type:<26}│\n"
            f"  │  Status      : {state:<26}│\n"
            f"  └──────────────────────────────────────────┘"
        )


class Wheels:
    """22-inch Chrome Forgiato wheels."""

    def __init__(self):
        self.brand = "Forgiato"
        self.size_inches = 22
        self.finish = "Chrome"
        self.style = "Flosse (5-spoke)"
        self.tire = "265/35ZR22 Pirelli P Zero"
        self.quantity = 4

    def spin(self):
        return "🔘 22\" Chrome Forgatos spinning — turning heads on every block!"

    def status(self):
        return (
            f"\n  ┌─ WHEELS ─────────────────────────────────┐\n"
            f"  │  Brand       : {self.brand:<26}│\n"
            f"  │  Size        : {str(self.size_inches) + ' inches':<26}│\n"
            f"  │  Finish      : {self.finish:<26}│\n"
            f"  │  Style       : {self.style:<26}│\n"
            f"  │  Tires       : {self.tire:<26}│\n"
            f"  │  Quantity    : {self.quantity:<26}│\n"
            f"  └──────────────────────────────────────────┘"
        )


class Interior:
    """Black leather interior with touchscreen head unit."""

    def __init__(self):
        self.seat_material = "Black Leather"
        self.seat_style = "Custom Bucket + Rear Bench"
        self.dashboard = "Custom Black Carbon Trim"
        self.carpet = "Black Plush"
        self.headliner = "Black Suede"
        self.head_unit = TouchscreenHeadUnit()

    def status(self):
        return (
            f"\n  ┌─ INTERIOR ───────────────────────────────┐\n"
            f"  │  Seats       : {self.seat_material:<26}│\n"
            f"  │  Seat Style  : {self.seat_style:<26}│\n"
            f"  │  Dashboard   : {self.dashboard:<26}│\n"
            f"  │  Carpet      : {self.carpet:<26}│\n"
            f"  │  Headliner   : {self.headliner:<26}│\n"
            f"  └──────────────────────────────────────────┘"
        )


class TouchscreenHeadUnit:
    """Touchscreen head unit / infotainment system."""

    def __init__(self):
        self.brand = "Pioneer DMH-WT8600NEX"
        self.screen_size_inches = 10.1
        self.resolution = "1280 x 720 HD"
        self.features = [
            "Apple CarPlay",
            "Android Auto",
            "Bluetooth 5.0",
            "AM/FM/SiriusXM Radio",
            "DVD/CD Player",
            "Backup Camera Input",
            "4-Zone EQ",
            "USB + Aux Input",
        ]
        self.is_on = False

    def power_on(self):
        self.is_on = True
        return "📱 Touchscreen head unit ON — Pioneer 10.1\" display glowing!"

    def power_off(self):
        self.is_on = False
        return "Head unit powered off."

    def status(self):
        state = "ON ✅" if self.is_on else "OFF 🔴"
        features_str = ", ".join(self.features[:4]) + "..."
        return (
            f"\n  ┌─ HEAD UNIT ──────────────────────────────┐\n"
            f"  │  Brand       : {self.brand:<26}│\n"
            f"  │  Screen      : {str(self.screen_size_inches) + '\" Touchscreen':<26}│\n"
            f"  │  Resolution  : {self.resolution:<26}│\n"
            f"  │  Features    : {features_str:<26}│\n"
            f"  │  Power       : {state:<26}│\n"
            f"  └──────────────────────────────────────────┘"
        )


class SoundSystem:
    """Full custom sound system: 2 amps, 2 10\" subs, 8 speakers."""

    def __init__(self):
        self.subwoofers = [
            {"brand": "Rockford Fosgate", "size_inches": 10, "watts": 500, "location": "Trunk"},
            {"brand": "Rockford Fosgate", "size_inches": 10, "watts": 500, "location": "Trunk"},
        ]
        self.amplifiers = [
            {"brand": "Rockford Fosgate T1500-1bdCP", "watts_rms": 1500, "channels": 1, "powers": "Subwoofers"},
            {"brand": "Rockford Fosgate T400-4", "watts_rms": 400, "channels": 4, "powers": "Speakers"},
        ]
        self.speakers = [
            {"location": "Front Doors",   "size_inches": 6.5, "brand": "JL Audio C2-650x"},
            {"location": "Front Doors",   "size_inches": 6.5, "brand": "JL Audio C2-650x"},
            {"location": "Rear Doors",    "size_inches": 6.5, "brand": "JL Audio C2-650x"},
            {"location": "Rear Doors",    "size_inches": 6.5, "brand": "JL Audio C2-650x"},
            {"location": "Front Dash",    "size_inches": 3.5, "brand": "JL Audio C2-350x"},
            {"location": "Front Dash",    "size_inches": 3.5, "brand": "JL Audio C2-350x"},
            {"location": "Rear Deck",     "size_inches": 6.5, "brand": "JL Audio C2-650x"},
            {"location": "Rear Deck",     "size_inches": 6.5, "brand": "JL Audio C2-650x"},
        ]
        self.volume = 0
        self.is_on = False

    def power_on(self):
        self.is_on = True
        self.volume = 20
        return "🔊 Sound system ACTIVATED — 8 speakers + dual 10\" subs ready!"

    def power_off(self):
        self.is_on = False
        self.volume = 0
        return "Sound system powered off."

    def set_volume(self, level: int):
        if not self.is_on:
            return "Sound system is off. Power it on first."
        self.volume = max(0, min(100, level))
        bar = "█" * (self.volume // 5) + "░" * (20 - self.volume // 5)
        return f"🔉 Volume set to {self.volume}/100  [{bar}]"

    def bump(self):
        if not self.is_on:
            return "Sound system is off. Power it on first."
        return (
            "💥 BOOM BOOM BOOM 💥\n"
            "  Two 10\" Rockford Fosgate subs THUMPING at 1500W RMS!\n"
            "  8 JL Audio speakers filling the cabin — the whole block can hear it! 🎵"
        )

    def status(self):
        state = "ON ✅" if self.is_on else "OFF 🔴"
        total_sub_watts = sum(s["watts"] for s in self.subwoofers)
        total_amp_watts = sum(a["watts_rms"] for a in self.amplifiers)
        return (
            f"\n  ┌─ SOUND SYSTEM ───────────────────────────┐\n"
            f"  │  Subwoofers  : {len(self.subwoofers)}x 10\" Rockford Fosgate{'':<5}│\n"
            f"  │  Sub Power   : {str(total_sub_watts) + 'W RMS combined':<26}│\n"
            f"  │  Amplifiers  : {len(self.amplifiers)}x amps ({str(total_amp_watts) + 'W RMS total)':<19}│\n"
            f"  │  Speakers    : {str(len(self.speakers)) + 'x JL Audio (4-door + dash + deck)':<26}│\n"
            f"  │  Volume      : {str(self.volume) + '/100':<26}│\n"
            f"  │  Status      : {state:<26}│\n"
            f"  └──────────────────────────────────────────┘"
        )


class Impala1984:
    """
    1984 Chevrolet Impala — Custom Dream Build

    Exterior : Black
    Interior : Black Leather
    Wheels   : 22" Chrome Forgiato Flosse
    Engine   : 383 Stroker V8 (450 hp)
    Audio    : 2x 10" subs | 2 amps | 8 speakers | Pioneer touchscreen
    """

    def __init__(self):
        self.year = 1984
        self.make = "Chevrolet"
        self.model = "Impala"
        self.trim = "Custom"
        self.exterior_color = "Gloss Black"
        self.body_style = "4-Door Sedan"
        self.engine = Engine()
        self.wheels = Wheels()
        self.interior = Interior()
        self.sound_system = SoundSystem()

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #

    def start(self):
        engine_msg = self.engine.start()
        hu_msg = self.interior.head_unit.power_on()
        sound_msg = self.sound_system.power_on()
        return f"{engine_msg}\n{hu_msg}\n{sound_msg}"

    def stop(self):
        engine_msg = self.engine.stop()
        hu_msg = self.interior.head_unit.power_off()
        sound_msg = self.sound_system.power_off()
        return f"{engine_msg}\n{hu_msg}\n{sound_msg}"

    def drive(self):
        if not self.engine.is_running:
            return "⚠️  Can't drive — start the engine first!"
        return (
            "🚗💨  The blacked-out '84 Impala rolls down the street...\n"
            "     22\" Forgiatos gleaming in the sun, bass thumping from the trunk!\n"
            "     Heads turning, jaws dropping — this build is LEGENDARY. 🖤"
        )

    def honk(self):
        return "📯 BEEP BEEP!"

    # ------------------------------------------------------------------ #
    #  Display                                                             #
    # ------------------------------------------------------------------ #

    def specs(self):
        header = (
            "\n" + "═" * 46 + "\n"
            f"  {self.year} {self.make} {self.model} — {self.trim.upper()} BUILD\n"
            + "═" * 46 + "\n"
            f"  Body Style    : {self.body_style}\n"
            f"  Exterior      : {self.exterior_color}\n"
            f"  Seat Material : {self.interior.seat_material}\n"
        )
        return (
            header
            + self.engine.status()
            + self.wheels.status()
            + self.interior.status()
            + self.interior.head_unit.status()
            + self.sound_system.status()
            + "\n" + "═" * 46 + "\n"
        )

    def __str__(self):
        return (
            f"{self.year} {self.make} {self.model} | {self.exterior_color} | "
            f"22\" Chrome Forgatos | 383 Stroker V8"
        )
