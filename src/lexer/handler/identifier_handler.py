from ..token_types import TokenType
from ..state import LexerState, Position
from .base import TokenHandler

class IdentifierHandler(TokenHandler):
    """Handles identifiers and keywords like IF, FOR, RETURN, AND, OR."""

    keywords = {
        # Control Flow
        "for": TokenType.FOR,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "break": TokenType.BREAK,
        "continue": TokenType.CONTINUE,
        "return": TokenType.RETURN,
        
        # Logical Operators
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,
        "in": TokenType.IN,
        "not_in": TokenType.NOT_IN,
        "is": TokenType.IS,
        "is_not": TokenType.IS_NOT,
        
        # Data Types
        "true": TokenType.BOOLEAN,
        "false": TokenType.BOOLEAN,
        "none": TokenType.NONE,
        
        # Commands
        "print": TokenType.PRINT_COMMAND,
        "var": TokenType.VARIABLE_DECLARE,
        "function": TokenType.FUNCTION
    }

    def __init__(self):
        super().__init__()

    def can_handle(self, state: LexerState):
        """Check if the current character starts an identifier (letter or underscore)."""
        char = state.current_char()
        return char is not None and (char.isalpha() or char == "_")
    
    def handle(self, state: LexerState, start_pos: Position):
        """Processes identifiers and keywords."""
        identifier = ""

        # Read while the character is alphanumeric or underscore
        while True:
            char = state.current_char()
            if char is None or not (char.isalnum() or char == "_"):
                break
            identifier += char
            state.advance()

        # Determine token type and value
        token_type = self.keywords.get(identifier.lower(), TokenType.IDENTIFIER)
        value = identifier

        # Handle boolean literals
        if token_type == TokenType.BOOLEAN:
            value = identifier.lower() == "true"

        # Handle none literal
        elif token_type == TokenType.NONE:
            value = None

        # Store the token
        state.add_token(token_type, value, start_pos, identifier)