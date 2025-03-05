from .base_node import ASTNode

class ReturnNode(ASTNode):
    """AST node for return statements."""

    def __init__(self, value):
        super().__init__("Return")
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"
