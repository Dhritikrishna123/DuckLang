from .state import LexerState
from .handler.whitespace_hadler import WhiteSpaceHandler
from .handler.comment_handler import CommentHandler
from .handler.number_handler import NumberHandler
from .handler.string_handler import StringHandler
from .handler.operator_handler import OperatorHandler
from .handler.identifier_handler import IdentifierHandler
from .token_types import TokenType

class Lexer:
    """Main Lexer class to tokenize source code."""

    def __init__(self):
        """Initialize all token handlers."""
        

        self.handlers = [
            WhiteSpaceHandler(),
            CommentHandler(),
            NumberHandler(),
            StringHandler(),
            OperatorHandler(),
            IdentifierHandler(),
        ]

    def tokenize(self, source):
        """Tokenizes the input source code and returns a list of tokens."""
        state = LexerState(source)

        while state.has_more_chars():
            # print(f"Processing: '{state.current_char}' at {state.position.index}")  # Debug info
            start_pos = state.position.copy()

            handler_found = False
            for handler in self.handlers:
                if handler.can_handle(state):
                    # print(f"Using handler: {handler.__class__.__name__}")  # Debug info
                    handler.handle(state,start_pos)
                    handler_found = True
                    break

            if not handler_found:
                print(f"Current char: '{state.current_char()}', Position: {state.position.index}, Line: {state.position.line}, Column: {state.position.column}") #debugger

                raise Exception(f"Unexpected character '{state.current_char()}' at {start_pos}")

        return state.tokens
