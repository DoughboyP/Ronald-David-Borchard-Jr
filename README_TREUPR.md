# TRE-UPR
### *Transcendent Reality Engine – Universal Propagation Reactor*

> A magic technology device that builds on itself to create universes.

---

## Overview

The **TRE-UPR** is a self-improving simulation device written in Python.  
It boots from nothing, iteratively upgrades its own internal firmware, and
spawns pocket universes – each generation richer, more dimensional, and more
complex than the last.

```
 _____ ____  _____       _   _ ____  ____
|_   _|  _ \| ____|     | | | |  _ \|  _ \
  | | | |_) |  _| ______| | | | |_) | |_) |
  | | |  _ <| |__|______| |_| |  __/|  _ <
  |_| |_| \_|_____|      \___/|_|   |_| \_\
```

---

## How It Works

```
Boot
 └─► Generation 0
       ├─ Self-build engine initialises firmware
       ├─ 1 universe spawned  (3 spatial dimensions)
       ├─ Universe simulated over N ticks
       └─ Complexity score extracted
            └─► Generation 1
                  ├─ Firmware upgraded (more universes, more dimensions)
                  ├─ 2 universes spawned
                  ├─ Better physics resolution
                  └─ Higher complexity score
                       └─► Generation 2 … → … Generation 12
```

Each generation:

| Step | What happens |
|------|-------------|
| **Self-build** | Engine analyses prior generation and upgrades its own firmware |
| **Spawn** | N pocket universes are created with randomised physics |
| **Simulate** | Each universe ticks forward – stars form, entropy rises, life may emerge |
| **Evaluate** | Complexity is scored; sentient universes earn bonus points |
| **Upgrade** | Dimension cap, universe count, and energy efficiency all improve |
| **Repeat** | Energy budget is multiplied by the golden ratio (φ ≈ 1.618) |

---

## Physics Model

Every universe has a unique `PhysicsProfile`:

| Parameter | Effect |
|-----------|--------|
| `dimensions` | Spatial degrees of freedom (3 → up to 11 with M-theory unlock) |
| `gravity_constant` | Relative gravitational coupling |
| `speed_of_light_factor` | Relativistic envelope |
| `entropy_rate` | How quickly the universe loses usable energy |
| `dark_energy_density` | Accelerated expansion / destabilisation force |
| `quantum_coupling` | Strength of quantum effects; drives complexity growth |

A universe collapses when its stability falls below **0.72**.  
Sentient life emerges when stability ≥ **0.85** *and* complexity ≥ **5.0**.

---

## Quick Start

```bash
# Interactive mode – press ENTER to advance one generation at a time
python tre_upr_main.py

# Automatic mode – run all 12 generations and print the full report
python tre_upr_main.py --auto

# Custom seed (for reproducible universe sets)
python tre_upr_main.py --auto --seed 1337
```

---

## Project Structure

```
tre_upr/
├── __init__.py       – Public API exports
├── constants.py      – All device constants and thresholds
├── universe.py       – Universe data model + physics simulation
├── engine.py         – Self-building recursive engine
└── device.py         – TRE-UPR top-level orchestrator

tre_upr_main.py       – CLI entry point
README_TREUPR.md      – This file
```

---

## Programmatic API

```python
from tre_upr import TREUPRDevice

device = TREUPRDevice(seed=42)
device.boot()

# Run one generation at a time
while device.run_single_generation():
    pass  # returns False when the device halts naturally

device.shutdown()
```

---

## Self-Building Milestones

| Generation | Unlocks |
|-----------|---------|
| 0 | 1 universe · 3D · 20 ticks/universe |
| 1 | 2 universes unlocked |
| 3 | Extra-dimensional physics (4D+) |
| 5+ | Up to 5 simultaneous universes |
| 6+ | Up to 9 spatial dimensions |
| 12 | Maximum generation – device enters stable state |

---

## Design Philosophy

The TRE-UPR is built around three principles:

1. **Self-improvement** – every generation leaves the device smarter than it found it.
2. **Emergence** – complexity and sentience arise naturally from physics, not from explicit rules.
3. **Bounded infinity** – energy compounds by φ each cycle, but hard limits prevent runaway divergence.

---

*All realities simulated within are fictional.*
