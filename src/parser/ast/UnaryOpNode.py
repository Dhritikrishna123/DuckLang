from .base_node import ASTNode

class UnaryOpNode(ASTNode):
    """AST node for unary operations."""

    def __init__(self, operator, operand):
        super().__init__("UnaryOp")
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.operator} {self.operand})"
