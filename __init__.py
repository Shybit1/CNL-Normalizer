"""
Canonical Aero — CNL Normalizer
A lightweight, deterministic CNL (Controlled Natural Language) normalizer
that converts messy human speech and text commands for drone swarms
into clean, canonical, parser-ready instructions.
"""

from .normalizer import normalize

__all__ = ["normalize"]