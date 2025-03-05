from .base_node import ASTNode

class VariableNode(ASTNode):
    """AST node representing variable declarations."""

    def __init__(self, name, value=None, position=None):
        super().__init__("VariableDeclaration")
        self.name = name
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Variable({self.name} = {self.value})"

