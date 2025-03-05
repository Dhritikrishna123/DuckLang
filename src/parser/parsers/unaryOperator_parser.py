from ..ast import UnaryOpNode
from ...lexer.token_types import TokenType

class UnaryOperatorParser:
    """Parser for unary operators like 'not' and '-'."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        if self.check(TokenType.NOT, TokenType.MINUS):
            operator = self.consume(self.current_token().token_type, "Expected unary operator.")
            operand_parser = self.__class__(self.tokens[self.current:])
            operand = operand_parser.parse()

            if operand is None:
                raise Exception(f"Expected operand after '{operator.token_type}'")

            self.current += operand_parser.current
            return UnaryOpNode(operator.token_type, operand)

        return None

    def consume(self, token_type, error_message):
        if self.check(token_type):
            token = self.current_token()
            self.advance()
            return token
        raise Exception(error_message)

    def check(self, *token_types):
        if self.is_at_end():
            return False
        return self.current_token().token_type in token_types

    def advance(self):
        if not self.is_at_end():
            self.current += 1

    def current_token(self):
        return self.tokens[self.current]

    def is_at_end(self):
        return self.current >= len(self.tokens)
