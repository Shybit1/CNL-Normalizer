# Generated from DroneCommands.g4 by ANTLR 4.13.2
# DO NOT modify manually — regenerate from the .g4 file when the grammar changes.

from antlr4.tree.Tree import ParseTreeVisitor
from typing import Any


class DroneCommandsVisitor(ParseTreeVisitor):
    """
    Visitor interface for the DroneCommands parse tree.

    Implementations override these methods to process each command type.
    """

    def visitCommand(self, ctx: Any) -> Any:
        return self.visitChildren(ctx)

    def visitAltitudeCommand(self, ctx: Any) -> Any:
        return self.visitChildren(ctx)

    def visitNavigationCommand(self, ctx: Any) -> Any:
        return self.visitChildren(ctx)

    def visitFormationCommand(self, ctx: Any) -> Any:
        return self.visitChildren(ctx)

    def visitLoiterCommand(self, ctx: Any) -> Any:
        return self.visitChildren(ctx)

    def visitAbortCommand(self, ctx: Any) -> Any:
        return self.visitChildren(ctx)