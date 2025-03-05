from .base_node import ASTNode

class ForNode(ASTNode):
    """AST node for for loops."""

    def __init__(self, iterator, iterable, body):
        super().__init__("For")
        self.iterator = iterator
        self.iterable = iterable
        self.body = body

    def __repr__(self):
        return f"For({self.iterator} in {self.iterable}, {self.body})"
