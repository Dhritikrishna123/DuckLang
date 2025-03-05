from ..ast import PrintNode
from ...lexer.token_types import TokenType
from .expression_parser import ExpressionParser

class PrintParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        start_pos = self.current
        
        # Consume 'print' keyword
        self.consume(TokenType.PRINT_COMMAND, "Expected 'print'.")
        
        # Skip whitespace after 'print'
        while self.check(TokenType.WHITESPACE):
            self.advance()
        
        # Parse expression to print
        expr_parser = ExpressionParser(self.tokens[self.current:])
        expr, expr_consumed = expr_parser.parse()
        
        if not expr:
            raise SyntaxError("Expected expression after 'print'.")
            
        self.current += expr_consumed
        
        # Calculate total tokens consumed
        total_consumed = self.current - start_pos
        
        return PrintNode(expr), total_consumed

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