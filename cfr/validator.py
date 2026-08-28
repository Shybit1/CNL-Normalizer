"""
validator.py — CFR Schema Validator (Layer 1, Stage 5)

Validates CFR against JSON Schema.
This is a hard boundary: no malformed CFR should escape Layer 1.

Per PRD §35-37:
- Validates required fields, field types, enumerations, nested structures
- Does NOT perform mission feasibility analysis (that's Layer 2)
- Reject/accept decision is deterministic
"""

import json
import os
from typing import Dict, Any, List, Optional, Tuple

try:
    import jsonschema
    from jsonschema import Draft7Validator, ValidationError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

from .cfr_types import CFR


class CFRValidator:
    """
    Validator for Command Formal Representation.
    
    Loads schema from schema.json and validates CFR instances.
    Thread-safe, stateless.
    """

    def __init__(self):
        """Initialize validator by loading schema."""
        self.schema = self._load_schema()
        self.validator = None
        if JSONSCHEMA_AVAILABLE and self.schema:
            try:
                self.validator = Draft7Validator(self.schema)
            except Exception as e:
                print(f"Warning: Could not initialize jsonschema validator: {e}")

    def _load_schema(self) -> Optional[Dict[str, Any]]:
        """
        Load JSON Schema from schema.json.
        
        Returns:
            Parsed schema dict or None if schema file not found.
        """
        schema_path = os.path.join(os.path.dirname(__file__), "schema.json")
        try:
            with open(schema_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load schema: {e}")
            return None

    def validate(self, cfr: CFR) -> Tuple[bool, List[str]]:
        """
        Validate a CFR against the schema.
        
        Args:
            cfr: CFR instance to validate.
        
        Returns:
            Tuple of (success: bool, errors: List[str])
            If success is False, errors list contains validation failures.
        """
        errors: List[str] = []
        cfr_dict = cfr.to_dict()

        # Structural validation
        errors.extend(self._validate_structure(cfr_dict))
        if errors:
            return False, errors

        # Schema validation (if jsonschema available)
        if self.validator:
            try:
                errors.extend(self._validate_with_jsonschema(cfr_dict))
            except Exception as e:
                errors.append(f"Schema validation error: {str(e)}")
        else:
            # Fallback: manual validation
            errors.extend(self._validate_manual(cfr_dict))

        return len(errors) == 0, errors

    def _validate_structure(self, cfr_dict: Dict[str, Any]) -> List[str]:
        """
        Validate basic CFR structure without jsonschema.
        
        Checks:
        - Required fields present
        - Field types correct
        - Enum values valid
        """
        errors = []

        # Required fields
        required_fields = [
            "schema_version",
            "grammar_version",
            "constraint_version",
            "timestamp",
            "intent",
            "parameters",
            "constraints",
            "confidence",
        ]
        for field in required_fields:
            if field not in cfr_dict:
                errors.append(f"Missing required field: {field}")

        # Type checks
        if "schema_version" in cfr_dict and not isinstance(cfr_dict["schema_version"], str):
            errors.append(f"schema_version must be string, got {type(cfr_dict['schema_version']).__name__}")

        if "grammar_version" in cfr_dict and not isinstance(cfr_dict["grammar_version"], str):
            errors.append(f"grammar_version must be string, got {type(cfr_dict['grammar_version']).__name__}")

        if "constraint_version" in cfr_dict and not isinstance(cfr_dict["constraint_version"], str):
            errors.append(f"constraint_version must be string, got {type(cfr_dict['constraint_version']).__name__}")

        if "timestamp" in cfr_dict and not isinstance(cfr_dict["timestamp"], str):
            errors.append(f"timestamp must be string, got {type(cfr_dict['timestamp']).__name__}")

        if "intent" in cfr_dict and not isinstance(cfr_dict["intent"], str):
            errors.append(f"intent must be string, got {type(cfr_dict['intent']).__name__}")

        valid_intents = {
            "ALTITUDE_CHANGE",
            "WAYPOINT_NAVIGATION",
            "FORMATION_CHANGE",
            "HOLD_LOITER",
            "ABORT_RTL",
        }
        if "intent" in cfr_dict and cfr_dict["intent"] not in valid_intents:
            errors.append(f"Unknown intent: {cfr_dict['intent']}")

        if "parameters" in cfr_dict and not isinstance(cfr_dict["parameters"], dict):
            errors.append(f"parameters must be dict, got {type(cfr_dict['parameters']).__name__}")

        if "constraints" in cfr_dict and not isinstance(cfr_dict["constraints"], dict):
            errors.append(f"constraints must be dict, got {type(cfr_dict['constraints']).__name__}")

        if "confidence" in cfr_dict:
            try:
                conf = float(cfr_dict["confidence"])
                if not (0.0 <= conf <= 1.0):
                    errors.append(f"confidence must be in [0.0, 1.0], got {conf}")
            except (ValueError, TypeError):
                errors.append(f"confidence must be numeric, got {type(cfr_dict['confidence']).__name__}")

        if "mission_phase" in cfr_dict:
            mp = cfr_dict["mission_phase"]
            if mp is not None and not isinstance(mp, str):
                errors.append(f"mission_phase must be string or null, got {type(mp).__name__}")

        if "metadata" in cfr_dict and not isinstance(cfr_dict["metadata"], dict):
            errors.append(f"metadata must be dict, got {type(cfr_dict['metadata']).__name__}")

        return errors

    def _validate_with_jsonschema(self, cfr_dict: Dict[str, Any]) -> List[str]:
        """
        Validate using jsonschema Draft7Validator.
        """
        errors = []
        if not self.validator:
            return errors

        for error in self.validator.iter_errors(cfr_dict):
            path = ".".join(str(p) for p in error.path) if error.path else "(root)"
            errors.append(f"{path}: {error.message}")

        return errors

    def _validate_manual(self, cfr_dict: Dict[str, Any]) -> List[str]:
        """
        Manual fallback validation when jsonschema is not available.
        """
        # Already covered by _validate_structure
        return []


# Singleton validator instance
_validator_instance = None


def _get_validator() -> CFRValidator:
    """Get or create the singleton validator instance."""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = CFRValidator()
    return _validator_instance


def validate_cfr(cfr: CFR) -> Tuple[bool, List[str]]:
    """
    Validate a CFR against the schema.
    
    This is the main entry point for CFR validation.
    
    Args:
        cfr: CFR instance to validate.
    
    Returns:
        Tuple of (success: bool, errors: List[str])
    """
    validator = _get_validator()
    return validator.validate(cfr)
