import pytest
from grammar_parser import parse
from grammar_parser import ast as astmod


def test_visitor_produces_ast_nodes():
    r = parse('CLIMB TO 500 METERS')
    assert r.success
    # parse() currently returns ParseResult; visitor is internal. To test visitor AST
    # we generate parse tree then run visitor manually. This requires generated parser.
    from antlr4 import InputStream, CommonTokenStream
    from grammar_parser.DroneCommandsLexer import DroneCommandsLexer
    from grammar_parser.DroneCommandsParser import DroneCommandsParser
    from grammar_parser.visitor import CommandVisitor

    stream = InputStream('CLIMB TO 500 METERS')
    lexer = DroneCommandsLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = DroneCommandsParser(tokens)
    tree = parser.command()
    ast = CommandVisitor().visit(tree)
    assert isinstance(ast, astmod.AltitudeCommand)
    assert ast.altitude == 500

