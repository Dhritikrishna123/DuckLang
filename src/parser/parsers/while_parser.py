from ..ast import WhileNode
from ...lexer.token_types import TokenType
from .expression_parser import ExpressionParser

class WhileParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        start_pos = self.current
        
        # Consume 'while' keyword
        self.consume(TokenType.WHILE, "Expected 'while'.")
        
        # Skip whitespace after 'while'
        while self.check(TokenType.WHITESPACE):
            self.advance()
        
        # Parse condition
        condition_parser = ExpressionParser(self.tokens[self.current:])
        condition, condition_consumed = condition_parser.parse()
        
        if not condition:
            raise SyntaxError("Expected condition after 'while'.")
            
        self.current += condition_consumed
        
        # Skip whitespace before opening brace
        while self.check(TokenType.WHITESPACE):
            self.advance()
        
        # Consume opening brace
        self.consume(TokenType.LEFT_BRACE, "Expected '{' after condition.")
        
        # Parse body statements
        body = []
        while not self.check(TokenType.RIGHT_BRACE):
            # Skip whitespace between statements
            while self.check(TokenType.WHITESPACE):
                self.advance()
                
            # Check for end of input
            if self.is_at_end():
                raise SyntaxError("Unexpected end of input while parsing while body.")
                
            # Parse statement
            statement_parser = ExpressionParser(self.tokens[self.current:])
            statement, statement_consumed = statement_parser.parse()
            
            if statement:
                body.append(statement)
                self.current += statement_consumed
            else:
                self.advance()  # Skip tokens we can't parse
        
        # Consume closing brace
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after while body.")
        
        # Calculate total tokens consumed
        total_consumed = self.current - start_pos
        
        return WhileNode(condition, body), total_consumed

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