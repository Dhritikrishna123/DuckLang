from .base_node import ASTNode
from .variable_node import VariableNode

class BinaryOpNode(ASTNode):
    """AST node for binary operations."""

    def __init__(self, left, operator, right, symbol_table=None):
        super().__init__("BinaryOp")
        self.left = self.resolve(left, symbol_table)
        self.operator = operator
        self.right = self.resolve(right, symbol_table)

    def resolve(self, node, symbol_table):
        if isinstance(node, VariableNode) and symbol_table:
            return symbol_table.get(node.name, node)  # Lookup value if exists
        return node

    def __repr__(self):
        return f"BinaryOp({self.left} {self.operator} {self.right})"
