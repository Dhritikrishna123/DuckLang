from ..ast import BinaryOpNode as BinaryOperatorNode
from ...lexer.token_types import TokenType
from .literal_parser import LiteralParser

class BinaryOperatorParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        start_pos = self.current
        
        # Parse the left operand
        literal_parser = LiteralParser(self.tokens[self.current:])
        left, left_consumed = literal_parser.parse()
        if not left:
            return None, 0
        
        self.current += left_consumed
        
        # Check for operator
        if self.is_at_end() or not self.check(TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE):
            # If no operator, return just the left operand
            return left, left_consumed
        
        # Get the operator token
        operator = self.current_token()
        self.advance()
        
        # Parse the right operand
        right_parser = LiteralParser(self.tokens[self.current:])
        right, right_consumed = right_parser.parse()
        if not right:
            raise SyntaxError("Expected right-hand operand.")
        
        self.current += right_consumed
        
        # Calculate total tokens consumed
        total_consumed = self.current - start_pos
        
        return BinaryOperatorNode(left, operator.token_type, right), total_consumed

    def consume(self, token_type, error_message):
        if self.check(token_type):
            token = self.current_token()
            self.advance()
            return token
        raise SyntaxError(error_message)

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