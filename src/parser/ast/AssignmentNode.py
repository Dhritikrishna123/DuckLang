from .base_node import ASTNode

class AssignmentNode(ASTNode):
    """AST node for variable assignments."""

    def __init__(self, name, value):
        super().__init__("Assignment")
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assignment({self.name} = {self.value})"
