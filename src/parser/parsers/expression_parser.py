from ...lexer.token_types import TokenType
from ..ast import BinaryOpNode
from .literal_parser import LiteralNode
from .variable_parser import VariableNode
from .unaryOperator_parser import UnaryOpNode

class ExpressionParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.debug_mode = True

    def debug(self, message):
        if self.debug_mode:
            print(f"[ExpressionParser DEBUG] {message}")

    def parse(self):
        start_pos = self.current
        self.debug(f"Starting parse with {len(self.tokens)} tokens")
        
        try:
            expr = self.parse_expression()
            consumed = self.current
            
            self.debug(f"Parsed expression: {expr}")
            self.debug(f"Tokens consumed: {consumed - start_pos}")
            
            return expr, consumed - start_pos
        except Exception as e:
            self.debug(f"Parsing Error: {e}")
            return None, 0

    def parse_expression(self):
        self.debug("Parsing main expression")
        return self.parse_binary_operation()

    def parse_binary_operation(self):
        self.debug("Parsing binary operation")
        left = self.parse_term()

        while self.match(TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.previous()
            self.debug(f"Found binary operator: {operator.token_type}")
            
            # Skip whitespace before right operand
            while not self.is_at_end() and self.current_token().token_type == TokenType.WHITESPACE:
                self.advance()
            
            right = self.parse_term()
            left = BinaryOpNode(left, operator.token_type, right)

        return left

    def parse_term(self):
        self.debug("Parsing term")
        # Skip any whitespace
        while not self.is_at_end() and self.current_token().token_type == TokenType.WHITESPACE:
            self.advance()

        if self.match(TokenType.LEFT_PAREN):
            self.debug("Found left parenthesis")
            
            # Skip whitespace after left paren
            while not self.is_at_end() and self.current_token().token_type == TokenType.WHITESPACE:
                self.advance()

            expr = self.parse_expression()
            
            # Skip whitespace before right paren
            while not self.is_at_end() and self.current_token().token_type == TokenType.WHITESPACE:
                self.advance()

            # More robust right parenthesis checking
            if not self.check(TokenType.RIGHT_PAREN):
                self.debug(f"Current token: {self.current_token().token_type}")
                raise SyntaxError("Expected closing parenthesis")
            
            self.advance()  # Consume right parenthesis
            
            self.debug("Completed parenthesized expression")
            return expr

        if self.match(TokenType.MINUS, TokenType.NOT):
            operator = self.previous()
            self.debug(f"Found unary operator: {operator.token_type}")
            right = self.parse_term()
            return UnaryOpNode(operator.token_type, right)

        # Improved literal and identifier parsing
        if self.match(TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING, TokenType.BOOLEAN):
            value = self.previous().value
            self.debug(f"Found literal: {value}")
            return LiteralNode(value)

        if self.match(TokenType.IDENTIFIER):
            identifier = self.previous().value
            self.debug(f"Found identifier: {identifier}")
            return VariableNode(identifier)

        current_token = self.current_token()
        raise SyntaxError(f"Unexpected token in term: {current_token.token_type} with value '{current_token.value}'")

    def match(self, *token_types):
        if self.check(*token_types):
            self.advance()
            return True
        return False

    def check(self, *token_types):
        if self.is_at_end():
            return False
        return self.current_token().token_type in token_types

    def advance(self):
        if not self.is_at_end():
            self.current += 1

    def current_token(self):
        if self.is_at_end():
            raise SyntaxError("Unexpected end of tokens")
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def is_at_end(self):
        return self.current >= len(self.tokens)