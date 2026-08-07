"""Configure sys.path so grammar_parser and normalizer are importable."""
import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
_grammar_root = _here.parent
# Add grammar_parser root to path (contains __init__.py)
sys.path.insert(0, str(_grammar_root))
# Add shared dir for normalizer package access (normalizer is a package under shared)
_shared = _grammar_root.parent
sys.path.insert(1, str(_shared))
