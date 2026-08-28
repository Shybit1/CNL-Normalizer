"""
Canonical Aero — CFR Generation & Validation (Layer 1, Components 4-5)

CFR (Command Formal Representation) generation and validation.

Stage 4: CFR Generator
  Converts ParseResult + ConstraintResult → CFR candidate
  Assembles intent, parameters, constraints into canonical structure

Stage 5: Schema Validator
  Validates CFR against JSON Schema
  Hard boundary: no malformed CFR escapes to Layer 2

See PRD §29-37.
"""

from .generator import generate_cfr
from .validator import validate_cfr, CFRValidator
from .cfr_types import CFR

__all__ = [
    "generate_cfr",
    "validate_cfr",
    "CFRValidator",
    "CFR",
]
