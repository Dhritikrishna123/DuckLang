from .base_node import ASTNode

class BooleanNode(ASTNode):
    """AST node for boolean values."""

    def __init__(self, value):
        super().__init__("Boolean")
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"
