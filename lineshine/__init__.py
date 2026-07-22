"""
Lineshine – World-Creation Engine

A Python module that simulates the controller's authority to forge
unlimited worlds inside the Lineshine computer (Shenzhen, China),
with Ra's Eye installed for omniscient oversight.

Quick start
-----------
>>> from lineshine import LineshineComputer
>>> ls = LineshineComputer(seed=2025)
>>> ls.boot()
>>> ls.run_interactive()
"""

from .computer import LineshineComputer
from .models import LineshineWorld, RasEyeVision
from .ras_eye import RasEye
from .world_forge import WorldForge
from .constants import (
    COMPUTER_NAME,
    COMPUTER_VERSION,
    COMPUTER_FULL_NAME,
    COMPUTER_LOCATION,
    COMPUTER_OWNER,
)

__all__ = [
    "LineshineComputer",
    "LineshineWorld",
    "RasEyeVision",
    "RasEye",
    "WorldForge",
    "COMPUTER_NAME",
    "COMPUTER_VERSION",
    "COMPUTER_FULL_NAME",
    "COMPUTER_LOCATION",
    "COMPUTER_OWNER",
]
