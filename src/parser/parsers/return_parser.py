from ..ast import ReturnNode
from ...lexer.token_types import TokenType
from .expression_parser import ExpressionParser

class ReturnParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        start_pos = self.current
        
        # Consume 'return' keyword
        self.consume(TokenType.RETURN, "Expected 'return' keyword.")
        
        # Skip whitespace after 'return'
        while self.check(TokenType.WHITESPACE):
            self.advance()
        
        # If there is an expression after return, parse it
        expression = None
        expr_consumed = 0
        
        if not self.check(TokenType.SEMICOLON) and not self.is_at_end():
            expr_parser = ExpressionParser(self.tokens[self.current:])
            expression, expr_consumed = expr_parser.parse()
            self.current += expr_consumed
        
        # Check for semicolon (if your language requires it)
        if self.check(TokenType.SEMICOLON):
            self.advance()
        
        # Calculate total tokens consumed
        total_consumed = self.current - start_pos
        
        return ReturnNode(expression), total_consumed

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