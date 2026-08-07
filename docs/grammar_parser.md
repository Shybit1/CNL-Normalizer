# Grammar Parser

This module implements the Layer 1 Grammar Parser for Canonical Aero.
It is structured like a compiler front-end:

ANTLR Lexer/Parser -> Parse Tree -> Visitor -> AST -> Intent Mapper -> ParseResult

Key design decisions
- Parser expects canonical uppercase input (the Normalizer must provide that).
- Generated ANTLR files are NOT committed; CI generates them from DroneCommands.g4.
- Visitor builds a strongly typed AST only. Intent mapping is a separate step.
- Error messages are deterministic and match the PRD.

Developer notes
1. Generate ANTLR locally:
   curl -sS -o antlr-4.jar https://www.antlr.org/download/antlr-4.11.1-complete.jar
   java -Xmx500M -jar antlr-4.jar -Dlanguage=Python3 -visitor -o grammar_parser grammar_parser/DroneCommands.g4

2. Install deps:
   python -m pip install --upgrade pip
   pip install -r requirements-dev.txt

3. Run tests:
   pytest -q

Extension guide
- To add a new command family, update DroneCommands.g4, add an AST node in ast.py, update visitor.py to construct it, and add mapping logic in intent_mapper.py. Add unit tests for the new grammar and mapping.
