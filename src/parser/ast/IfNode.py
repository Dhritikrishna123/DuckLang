from .base_node import ASTNode

class IfNode(ASTNode):
    """AST node for if-else statements."""

    def __init__(self, condition, body, else_body=None):
        super().__init__("If")
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"If({self.condition}, {self.body}, Else: {self.else_body})"
