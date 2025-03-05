from .base_node import ASTNode

class WhileNode(ASTNode):
    """AST node for while loops."""

    def __init__(self, condition, body):
        super().__init__("While")
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition}, {self.body})"
