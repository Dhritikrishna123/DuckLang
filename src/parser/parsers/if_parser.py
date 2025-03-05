from ..ast import IfNode
from ...lexer.token_types import TokenType
from .expression_parser import ExpressionParser

class IfParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.debug_mode = True

    def debug(self, message):
        if self.debug_mode:
            print(f"[IfParser DEBUG] {message}")

    def parse(self):
        start_pos = self.current
        
        # Consume 'if' keyword
        self.consume(TokenType.IF, "Expected 'if'.")
        
        # Skip whitespace after 'if'
        while self.check(TokenType.WHITESPACE):
            self.advance()
        
        # Parse condition
        condition_parser = ExpressionParser(self.tokens[self.current:])
        condition, condition_consumed = condition_parser.parse()
        
        if not condition:
            raise SyntaxError("Expected condition after 'if'.")
        
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
                
            # Break if at end of tokens
            if self.is_at_end():
                raise SyntaxError("Unexpected end of input while parsing if body.")
                
            # Parse statement
            statement_parser = ExpressionParser(self.tokens[self.current:])
            statement, statement_consumed = statement_parser.parse()
            
            if statement:
                body.append(statement)
                self.current += statement_consumed
            else:
                self.advance()  # Skip tokens we can't parse
        
        # Consume closing brace
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after if body.")
        
        # Calculate total tokens consumed
        total_consumed = self.current - start_pos
        
        self.debug(f"Parsed If Statement: Condition = {condition}, Body = {body}")
        
        return IfNode(condition, body), total_consumed

    def consume(self, token_type, error_message):
        """Consume a specific token type or raise an error."""
        if self.check(token_type):
            token = self.current_token()
            self.advance()
            return token
        raise SyntaxError(error_message)

    def check(self, *token_types):
        """Check if the current token matches any of the given types."""
        if self.is_at_end():
            return False
        return self.current_token().token_type in token_types

    def advance(self):
        """Move to the next token."""
        if not self.is_at_end():
            self.current += 1

    def current_token(self):
        """Get the current token."""
        return self.tokens[self.current]

    def is_at_end(self):
        """Check if we've reached the end of tokens."""
        return self.current >= len(self.tokens)