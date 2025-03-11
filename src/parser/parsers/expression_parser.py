from ...lexer.token_types import TokenType
from ..ast import (
    BinaryOpNode,
    UnaryOpNode,
    LiteralNode,
    VariableNode,
    ArrayNode,
    ArrayAccessNode,
    AssignmentNode,
    FunctionCallNode
)
from .base_expression_parser import BaseExpressionParser
from ...utils.debug import debug, DebugLevel

class ExpressionParser(BaseExpressionParser):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.component_name = "ExpressionParser"

    def parse(self):
        """Parse an expression and return the AST node and number of tokens consumed."""
        start_pos = self.current
        
        self.skip_whitespace()
        expr = self.parse_assignment()
        consumed = self.current - start_pos
        
        if expr:
            debug.info(self.component_name, f"Parsed expression: {expr}")
            debug.debug(self.component_name, f"Tokens consumed: {consumed}")
            return expr, consumed
        else:
            debug.error(self.component_name, "Failed to parse expression")
            return None, 0

    def parse_assignment(self):
        """Parse an assignment expression."""
        self.skip_whitespace()
        left = self.parse_logical()
        
        if not left:
            return None
        
        self.skip_whitespace()
        if self.match(TokenType.ASSIGN):
            if isinstance(left, VariableNode):
                value = self.parse_assignment()
                if not value:
                    debug.error(self.component_name, "Expected value after '='")
                    return None
                debug.debug(self.component_name, f"Parsed assignment: {left.name} = {value}")
                return AssignmentNode(left.name, value)
            elif isinstance(left, ArrayAccessNode):
                value = self.parse_assignment()
                if not value:
                    debug.error(self.component_name, "Expected value after '='")
                    return None
                debug.debug(self.component_name, f"Parsed array assignment: {left} = {value}")
                return AssignmentNode(left, value)
            else:
                debug.error(self.component_name, f"Invalid assignment target: {left}")
                return None
        
        return left

    def parse_logical(self):
        """Parse logical operators (and, or)."""
        self.skip_whitespace()
        expr = self.parse_equality()
        
        if not expr:
            return None
        
        while True:
            self.skip_whitespace()
            if not self.match(TokenType.AND, TokenType.OR):
                break
            operator = self.previous().token_type
            right = self.parse_equality()
            if not right:
                debug.error(self.component_name, f"Expected expression after {operator}")
                return None
            expr = BinaryOpNode(expr, operator, right)
            debug.debug(self.component_name, f"Parsed logical expression: {expr}")
        
        return expr

    def parse_equality(self):
        """Parse equality expressions (==, !=)."""
        self.skip_whitespace()
        expr = self.parse_comparison()
        
        if not expr:
            return None
        
        while True:
            self.skip_whitespace()
            if not self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
                break
            operator = self.previous().token_type
            right = self.parse_comparison()
            if not right:
                debug.error(self.component_name, f"Expected expression after {operator}")
                return None
            expr = BinaryOpNode(expr, operator, right)
            debug.debug(self.component_name, f"Parsed equality expression: {expr}")
        
        return expr

    def parse_comparison(self):
        """Parse comparison expressions (<, >, <=, >=)."""
        self.skip_whitespace()
        expr = self.parse_term()
        
        if not expr:
            return None
        
        while True:
            self.skip_whitespace()
            if not self.match(
                TokenType.LESS_THAN, TokenType.GREATER_THAN,
                TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL
            ):
                break
            operator = self.previous().token_type
            right = self.parse_term()
            if not right:
                debug.error(self.component_name, f"Expected expression after {operator}")
                return None
            expr = BinaryOpNode(expr, operator, right)
            debug.debug(self.component_name, f"Parsed comparison expression: {expr}")
        
        return expr

    def parse_term(self):
        """Parse terms (addition and subtraction)."""
        self.skip_whitespace()
        expr = self.parse_factor()
        
        if not expr:
            return None
        
        while True:
            self.skip_whitespace()
            if not self.match(TokenType.PLUS, TokenType.MINUS):
                break
            operator = self.previous().token_type
            right = self.parse_factor()
            if not right:
                debug.error(self.component_name, f"Expected expression after {operator}")
                return None
            expr = BinaryOpNode(expr, operator, right)
            debug.debug(self.component_name, f"Parsed term: {expr}")
        
        return expr

    def parse_factor(self):
        """Parse factors (multiplication and division)."""
        self.skip_whitespace()
        expr = self.parse_unary()
        
        if not expr:
            return None
        
        while True:
            self.skip_whitespace()
            if not self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
                break
            operator = self.previous().token_type
            right = self.parse_unary()
            if not right:
                debug.error(self.component_name, f"Expected expression after {operator}")
                return None
            expr = BinaryOpNode(expr, operator, right)
            debug.debug(self.component_name, f"Parsed factor: {expr}")
        
        return expr

    def parse_unary(self):
        """Parse unary expressions (-, not)."""
        self.skip_whitespace()
        if self.match(TokenType.MINUS, TokenType.NOT):
            operator = self.previous().token_type
            right = self.parse_unary()
            if not right:
                debug.error(self.component_name, "Expected expression after unary operator")
                return None
            expr = UnaryOpNode(operator, right)
            debug.debug(self.component_name, f"Parsed unary expression: {expr}")
            return expr
        
        return self.parse_call()

    def parse_call(self):
        """Parse function calls and array access."""
        self.skip_whitespace()
        expr = self.parse_primary()
        
        if not expr:
            return None
        
        while True:
            self.skip_whitespace()
            if self.match(TokenType.LEFT_PAREN):
                # Function call
                if not isinstance(expr, VariableNode):
                    debug.error(self.component_name, "Can only call functions")
                    return None
                
                arguments = []
                if not self.check(TokenType.RIGHT_PAREN):
                    while True:
                        arg = self.parse_assignment()
                        if not arg:
                            debug.error(self.component_name, "Expected argument")
                            return None
                        arguments.append(arg)
                        if not self.match(TokenType.COMMA):
                            break
                
                if not self.match(TokenType.RIGHT_PAREN):
                    debug.error(self.component_name, "Expected ')' after arguments")
                    return None
                expr = FunctionCallNode(expr.name, arguments)
                debug.debug(self.component_name, f"Parsed function call: {expr}")
            elif self.match(TokenType.LEFT_BRACKET):
                # Array access
                index = self.parse_assignment()
                if not index:
                    debug.error(self.component_name, "Expected index expression")
                    return None
                if not self.match(TokenType.RIGHT_BRACKET):
                    debug.error(self.component_name, "Expected ']' after index")
                    return None
                expr = ArrayAccessNode(expr, index)
                debug.debug(self.component_name, f"Parsed array access: {expr}")
            else:
                break
        
        return expr

    def parse_primary(self):
        """Parse primary expressions (literals, variables, parentheses, arrays)."""
        self.skip_whitespace()
        
        if self.match(TokenType.INTEGER):
            value = int(self.previous().value)
            expr = LiteralNode(value)
            debug.debug(self.component_name, f"Parsed literal: {expr}")
            return expr
            
        if self.match(TokenType.STRING):
            value = str(self.previous().value)
            expr = LiteralNode(value)
            debug.debug(self.component_name, f"Parsed literal: {expr}")
            return expr
            
        if self.match(TokenType.BOOLEAN):
            value = self.previous().value
            expr = LiteralNode(value)
            debug.debug(self.component_name, f"Parsed literal: {expr}")
            return expr
            
        if self.match(TokenType.IDENTIFIER):
            name = self.previous().value
            expr = VariableNode(name)
            debug.debug(self.component_name, f"Parsed variable: {expr}")
            return expr
            
        if self.match(TokenType.LEFT_PAREN):
            expr = self.parse_assignment()
            if not expr:
                debug.error(self.component_name, "Expected expression after '('")
                return None
            if not self.match(TokenType.RIGHT_PAREN):
                debug.error(self.component_name, "Expected ')' after expression")
                return None
            return expr
            
        if self.match(TokenType.LEFT_BRACKET):
            elements = []
            if not self.check(TokenType.RIGHT_BRACKET):
                while True:
                    element = self.parse_assignment()
                    if not element:
                        debug.error(self.component_name, "Expected array element")
                        return None
                    elements.append(element)
                    if not self.match(TokenType.COMMA):
                        break
            
            if not self.match(TokenType.RIGHT_BRACKET):
                debug.error(self.component_name, "Expected ']' after array elements")
                return None
            expr = ArrayNode(elements)
            debug.debug(self.component_name, f"Parsed array: {expr}")
            return expr
        
        debug.error(self.component_name, f"Unexpected token: {self.peek()}")
        return None

    def skip_whitespace(self):
        """Skip whitespace tokens."""
        while self.check(TokenType.WHITESPACE, TokenType.NEWLINE):
            self.advance()

    def consume(self, expected_type, error_message):
        """Consume a token of the expected type or raise an error."""
        self.skip_whitespace()
        if self.check(expected_type):
            token = self.advance()
            debug.debug(self.component_name, f"Consumed token: {token}")
            return token
        current = self.current_token()
        debug.error(self.component_name, f"{error_message} - got {current.token_type} instead")
        raise SyntaxError(f"{error_message} at token {current}")

    def match(self, *token_types):
        """Match current token against given types."""
        self.skip_whitespace()
        for token_type in token_types:
            if self.check(token_type):
                token = self.advance()
                debug.debug(self.component_name, f"Matched token: {token}")
                return True
        return False

    def check(self, *token_types):
        """Check if current token is of given type."""
        if self.is_at_end():
            return False
        return self.current_token().token_type in token_types