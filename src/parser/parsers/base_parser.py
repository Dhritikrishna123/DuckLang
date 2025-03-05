from ...lexer.token_types import TokenType

class BaseParser:
    """Base class for all parsers."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        """Peek at the current token."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def consume(self, expected_type, error_message):
        
        while self.current < len(self.tokens) and self.tokens[self.current].token_type == TokenType.WHITESPACE:
            self.advance()

        if self.current < len(self.tokens) and self.tokens[self.current].token_type == expected_type:
            token = self.tokens[self.current]
            self.advance()
            return token

        raise Exception(error_message)



    def match(self, token_type):
        if self.peek() is not None and self.peek().token_type == token_type:
            return True
        return False

    def advance(self):
        if self.current < len(self.tokens):
            self.current += 1

        
        
    def parse(self):
            raise NotImplementedError("Parse method should be implemented by subclasses.")