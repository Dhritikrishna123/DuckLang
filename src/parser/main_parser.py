from .parsers.expression_parser import ExpressionParser
from .parsers.symbol_table import SymbolTable
from .ast import (
    AssignmentNode,
    BinaryOpNode,
    FunctionCallNode,
    IfNode,
    LiteralNode,
    PrintNode,
    ReturnNode,
    UnaryOpNode,
    VariableNode,
    WhileNode,
    BlockNode,
    ArrayNode,
    ArrayAccessNode,
    FunctionDefNode
)
from src.lexer.token_types import TokenType
from ..utils.debug import debug, DebugLevel

# Turn off debugging by default
debug.level = DebugLevel.OFF

class MainParser:
    DEBUG_MODE = False

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.symbol_table = SymbolTable()
        self.component_name = "MainParser"

    def debug(self, msg):
        if self.DEBUG_MODE:
            print(f"[DEBUG] {msg}")

    def parse(self):
        """Parse the token stream and return an AST."""
        statements = []
        
        while not self.is_at_end():
            debug.debug(self.component_name, f"Current token: {self.current_token()}")
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
            else:
                self.synchronize()
                if not self.is_at_end():
                    self.advance()
        
        return BlockNode(statements)

    def parse_statement(self):
        """Parse a statement."""
        current = self.current_token()
        debug.debug(self.component_name, f"Parsing statement starting with token: {current}")
        
        if current.token_type == TokenType.PRINT_COMMAND:
            return self.parse_print_statement()
        elif current.token_type == TokenType.LEFT_BRACE:
            return self.parse_block()
        elif current.token_type == TokenType.FUNCTION:
            return self.parse_function()
        elif current.token_type == TokenType.RETURN:
            return self.parse_return()
        elif current.token_type == TokenType.IF:
            return self.parse_if()
        elif current.token_type == TokenType.WHILE:
            return self.parse_while()
        elif current.token_type == TokenType.FOR:
            return self.parse_for()
        elif current.token_type == TokenType.BREAK:
            return self.parse_break()
        elif current.token_type == TokenType.CONTINUE:
            return self.parse_continue()
        else:
            return self.parse_expression_statement()

    def parse_print_statement(self):
        """Parse a print statement."""
        self.consume(TokenType.PRINT_COMMAND)
        self.consume(TokenType.LEFT_PAREN)
        
        debug.debug(self.component_name, "Starting expression parse at token: " + str(self.current_token()))
        expr_parser = ExpressionParser(self.tokens[self.current:])
        expr, consumed = expr_parser.parse()
        
        if not expr:
            raise SyntaxError("Expected expression after 'print('")
        
        self.current += consumed
        self.consume(TokenType.RIGHT_PAREN)
        
        return PrintNode(expr)

    def parse_block(self):
        """Parse a block of statements."""
        self.consume(TokenType.LEFT_BRACE)
        statements = []
        
        while not self.is_at_end() and self.current_token().token_type != TokenType.RIGHT_BRACE:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
            else:
                self.synchronize()
                if self.is_at_end() or self.current_token().token_type == TokenType.RIGHT_BRACE:
                    break
                self.advance()
        
        if self.is_at_end():
            raise SyntaxError("Unterminated block")
        
        self.consume(TokenType.RIGHT_BRACE)
        return BlockNode(statements)

    def parse_function(self):
        """Parse a function definition."""
        self.consume(TokenType.FUNCTION)
        name = self.consume(TokenType.IDENTIFIER).value
        
        self.consume(TokenType.LEFT_PAREN)
        parameters = []
        
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                param = self.consume(TokenType.IDENTIFIER).value
                parameters.append(param)
                if not self.match(TokenType.COMMA):
                    break
        
        self.consume(TokenType.RIGHT_PAREN)
        body = self.parse_block()
        
        return FunctionDefNode(name, parameters, body)

    def parse_return(self):
        """Parse a return statement."""
        self.consume(TokenType.RETURN)
        
        if self.check(TokenType.SEMICOLON):
            self.consume(TokenType.SEMICOLON)
            return ReturnNode(None)
        
        expr_parser = ExpressionParser(self.tokens[self.current:])
        expr, consumed = expr_parser.parse()
        self.current += consumed
        
        if self.check(TokenType.SEMICOLON):
            self.consume(TokenType.SEMICOLON)
        
        return ReturnNode(expr)

    def parse_if(self):
        """Parse an if statement."""
        debug.debug(self.component_name, "Parsing if statement")
        self.consume(TokenType.IF)
        
        # Parse condition in parentheses
        self.consume(TokenType.LEFT_PAREN)
        expr_parser = ExpressionParser(self.tokens[self.current:])
        condition, consumed = expr_parser.parse()
        
        if not condition:
            debug.error(self.component_name, "Expected condition after 'if('")
            return None
        
        self.current += consumed
        self.consume(TokenType.RIGHT_PAREN)
        
        # Parse then branch
        then_branch = self.parse_block()
        if not then_branch:
            debug.error(self.component_name, "Expected block after 'if' condition")
            return None
        
        # Parse optional else branch
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.parse_block()
            if not else_branch:
                debug.error(self.component_name, "Expected block after 'else'")
                return None
        
        return IfNode(condition, then_branch, else_branch)

    def parse_while(self):
        """Parse a while statement."""
        self.consume(TokenType.WHILE)
        self.consume(TokenType.LEFT_PAREN)
        
        expr_parser = ExpressionParser(self.tokens[self.current:])
        condition, consumed = expr_parser.parse()
        
        if not condition:
            raise SyntaxError("Expected condition after 'while('")
        
        self.current += consumed
        self.consume(TokenType.RIGHT_PAREN)
        
        body = self.parse_statement()
        return WhileNode(condition, body)

    def parse_for(self):
        """Parse a for statement."""
        self.consume(TokenType.FOR)
        self.consume(TokenType.LEFT_PAREN)
        
        # Initializer
        initializer = None
        if not self.check(TokenType.SEMICOLON):
            expr_parser = ExpressionParser(self.tokens[self.current:])
            initializer, consumed = expr_parser.parse()
            self.current += consumed
        self.consume(TokenType.SEMICOLON)
        
        # Condition
        condition = None
        if not self.check(TokenType.SEMICOLON):
            expr_parser = ExpressionParser(self.tokens[self.current:])
            condition, consumed = expr_parser.parse()
            self.current += consumed
        self.consume(TokenType.SEMICOLON)
        
        # Increment
        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            expr_parser = ExpressionParser(self.tokens[self.current:])
            increment, consumed = expr_parser.parse()
            self.current += consumed
        self.consume(TokenType.RIGHT_PAREN)
        
        body = self.parse_statement()
        return ForNode(initializer, condition, increment, body)

    def parse_break(self):
        """Parse a break statement."""
        self.consume(TokenType.BREAK)
        if self.check(TokenType.SEMICOLON):
            self.consume(TokenType.SEMICOLON)
        return BreakNode()

    def parse_continue(self):
        """Parse a continue statement."""
        self.consume(TokenType.CONTINUE)
        if self.check(TokenType.SEMICOLON):
            self.consume(TokenType.SEMICOLON)
        return ContinueNode()

    def parse_expression_statement(self):
        """Parse an expression statement."""
        debug.debug(self.component_name, f"Starting expression parse at token: {self.current_token()}")
        expr_parser = ExpressionParser(self.tokens[self.current:])
        expr, consumed = expr_parser.parse()
        
        if expr:
            debug.debug(self.component_name, f"Parsed expression: {expr}, consumed {consumed} tokens")
            self.current += consumed
            if self.check(TokenType.SEMICOLON):
                self.consume(TokenType.SEMICOLON)
            return expr
        
        debug.error(self.component_name, "Failed to parse expression statement")
        return None

    def is_at_end(self):
        """Check if we've reached the end of the token stream."""
        return self.current >= len(self.tokens)

    def peek(self):
        """Return the current token without consuming it."""
        if self.is_at_end():
            return None
        return self.tokens[self.current]

    def previous(self):
        """Return the previously consumed token."""
        if self.current == 0:
            return None
        return self.tokens[self.current - 1]

    def advance(self):
        """Consume and return the current token."""
        if not self.is_at_end():
            self.current += 1
            debug.trace(self.component_name, f"Advanced to token: {self.peek()}")
        return self.previous()

    def check(self, *types):
        """Check if the current token is of any of the given types."""
        if self.is_at_end():
            return False
        current_token = self.peek()
        return any(current_token.token_type == t for t in types)

    def match(self, *types):
        """Check if the current token matches any of the given types and consume it if so."""
        for token_type in types:
            if self.check(token_type):
                debug.debug(self.component_name, f"Matched token: {self.peek()}")
                self.advance()
                return True
        return False

    def consume(self, token_type, error_message=None):
        """Consume the current token if it matches the expected type, otherwise raise an error."""
        if self.check(token_type):
            debug.debug(self.component_name, f"Consumed token: {self.peek()}")
            return self.advance()
        if error_message is None:
            error_message = f"Expected {token_type}"
        raise SyntaxError(error_message)

    def current_token(self):
        """Return the current token."""
        if self.is_at_end():
            return None
        return self.tokens[self.current]

    def synchronize(self):
        """Skip tokens until we find a statement boundary."""
        while not self.is_at_end():
            if self.check(TokenType.SEMICOLON):
                self.advance()
                return
            
            current = self.peek()
            if current.token_type in (
                TokenType.FUNCTION,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.FOR,
                TokenType.RETURN,
                TokenType.PRINT_COMMAND
            ):
                return
            
            self.advance()

    def resolve_expression(self, expr):
        """ Recursively resolve VariableNode and BinaryOpNode expressions """
        if isinstance(expr, VariableNode):
            value = self.symbol_table.get(expr.name)
            if value is not None:
                debug.debug(self.component_name, f"Resolved Variable: {expr.name} -> {value}")
                return value
            return expr  # If the variable is undefined, return the node itself

        elif isinstance(expr, BinaryOpNode):
            expr.left = self.resolve_expression(expr.left)
            expr.right = self.resolve_expression(expr.right)

            if isinstance(expr.left, LiteralNode) and isinstance(expr.right, LiteralNode):
                result = expr.evaluate()
                debug.debug(self.component_name, f"Evaluated BinaryOp: {expr.left} {expr.operator} {expr.right} = {result}")
                return result

        elif isinstance(expr, ArrayAccessNode):
            array = self.resolve_expression(expr.array)
            index = self.resolve_expression(expr.index)
            
            # Convert string index to integer if needed
            if isinstance(index, LiteralNode):
                try:
                    idx = int(str(index.value))  # Convert any numeric string to int
                except (ValueError, TypeError):
                    raise TypeError(f"Array index must be an integer, got {type(index.value)}")
            else:
                raise TypeError(f"Array index must be a literal value")

            if isinstance(array, (ArrayNode, LiteralNode)):
                if isinstance(array, ArrayNode):
                    if 0 <= idx < len(array.elements):
                        return array.elements[idx]
                    else:
                        raise IndexError(f"Array index {idx} out of bounds")
                elif isinstance(array.value, list):
                    if 0 <= idx < len(array.value):
                        return LiteralNode(array.value[idx])
                    else:
                        raise IndexError(f"Array index {idx} out of bounds")
            else:
                raise TypeError(f"Cannot index into non-array: {array}")

        elif isinstance(expr, ArrayNode):
            # Resolve each element in the array
            resolved_elements = []
            for element in expr.elements:
                resolved = self.resolve_expression(element)
                if isinstance(resolved, LiteralNode):
                    resolved_elements.append(resolved)
                else:
                    resolved_elements.append(LiteralNode(resolved))
            expr.elements = resolved_elements
            return expr

        return expr

    def evaluate_binary_operation(self, left, operator, right):
        """Evaluate a binary operation using the BinaryOpNode's evaluate method."""
        binary_op = BinaryOpNode(left, operator, right)
        return binary_op.evaluate()

    def consume_optional_separators(self):
        """Consume any optional statement separators (semicolons, whitespace, newlines)."""
        while self.check(TokenType.SEMICOLON, TokenType.WHITESPACE, TokenType.NEWLINE):
            self.advance()
