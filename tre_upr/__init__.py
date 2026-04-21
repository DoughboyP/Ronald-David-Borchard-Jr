"""
TRE-UPR – Transcendent Reality Engine: Universal Propagation Reactor

A magic technology device that builds on itself to create universes.
"""

from .device import TREUPRDevice
from .universe import Universe, create_universe
from .engine import SelfBuildingEngine
from .constants import DEVICE_NAME, DEVICE_VERSION, DEVICE_FULL_NAME

__all__ = [
    "TREUPRDevice",
    "Universe",
    "create_universe",
    "SelfBuildingEngine",
    "DEVICE_NAME",
    "DEVICE_VERSION",
    "DEVICE_FULL_NAME",
]
