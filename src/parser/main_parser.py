from .parsers.assignment_parser import AssignmentParser
from .parsers.binaryOperator_parser import BinaryOperatorParser
from .parsers.functionCall_parser import FunctionCallParser
from .parsers.if_parser import IfParser
from .parsers.literal_parser import LiteralParser
from .parsers.print_parser import PrintParser
from .parsers.variable_parser import VariableParser
from .parsers.while_parser import WhileParser
from .parsers.return_parser import ReturnParser
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
    WhileNode
)
from src.lexer.token_types import TokenType


class MainParser:
    DEBUG_MODE = True

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.symbol_table = SymbolTable()

    def debug(self, msg):
        if self.DEBUG_MODE:
            print(f"[DEBUG] {msg}")

    def parse(self):
        statements = []
        while not self.is_at_end():
            self.skip_whitespace()
            statement = self.parse_statement()
            if statement:
                self.debug(f"Parsed Statement: {statement}")
                statements.append(statement)

                if isinstance(statement, AssignmentNode):
                    resolved_value = self.resolve_expression(statement.value)  # 🔥 Resolve Expression
                    self.symbol_table.set(statement.name, resolved_value)
                    self.debug(f"Symbol Table Updated: {self.symbol_table}")

                self.consume_optional_separators()
            else:
                self.debug("Skipping Unknown Token")
                self.advance()

        print("[DEBUG] Final Symbol Table:", self.symbol_table)
        return statements

    def resolve_expression(self, expr):
        """ Recursively resolve VariableNode and BinaryOpNode expressions """
        if isinstance(expr, VariableNode):
            value = self.symbol_table.get(expr.name)
            if value is not None:
                self.debug(f"Resolved Variable: {expr.name} -> {value}")
                return value
            return expr  # If the variable is undefined, return the node itself

        elif isinstance(expr, BinaryOpNode):
            expr.left = self.resolve_expression(expr.left)
            expr.right = self.resolve_expression(expr.right)

            if isinstance(expr.left, LiteralNode) and isinstance(expr.right, LiteralNode):
                result = self.evaluate_binary_operation(expr.left, expr.operator, expr.right)
                self.debug(f"Evaluated BinaryOp: {expr.left} {expr.operator} {expr.right} = {result}")
                return result

        return expr

    def evaluate_binary_operation(self, left, operator, right):
        if operator == TokenType.PLUS:
            return LiteralNode(left.value + right.value)
        elif operator == TokenType.MINUS:
            return LiteralNode(left.value - right.value)
        elif operator == TokenType.MULTIPLY:
            return LiteralNode(left.value * right.value)
        elif operator == TokenType.DIVIDE:
            if right.value == 0:
                raise ZeroDivisionError("Division by zero")
            return LiteralNode(left.value / right.value)

        raise ValueError(f"Unknown operator: {operator}")

    def skip_whitespace(self):
        while self.check(TokenType.WHITESPACE, TokenType.NEWLINE):
            self.advance()

    def consume_optional_separators(self):
        while self.check(TokenType.SEMICOLON, TokenType.WHITESPACE, TokenType.NEWLINE):
            self.advance()

    def parse_statement(self):
        self.skip_whitespace()
        if self.is_at_end():
            return None

        token = self.current_token()

        if token.token_type == TokenType.VARIABLE_DECLARE:
            parser = VariableParser(self.tokens[self.current:])
            node, consumed = parser.parse()
            self.current += consumed
            return node

        elif token.token_type == TokenType.IDENTIFIER:
            next_token = self.peek_non_whitespace(1)
            if next_token and next_token.token_type == TokenType.ASSIGN:
                parser = AssignmentParser(self.tokens[self.current:])
                node, consumed = parser.parse()
                self.current += consumed
                return node
            else:
                parser = FunctionCallParser(self.tokens[self.current:])
                node, consumed = parser.parse()
                if node:
                    self.current += consumed
                    return node
                return self.parse_expression()

        elif token.token_type in [TokenType.IF, TokenType.WHILE, TokenType.PRINT_COMMAND, TokenType.RETURN]:
            parser_map = {
                TokenType.IF: IfParser,
                TokenType.WHILE: WhileParser,
                TokenType.PRINT_COMMAND: PrintParser,
                TokenType.RETURN: ReturnParser
            }
            parser = parser_map[token.token_type](self.tokens[self.current:])
            node, consumed = parser.parse()
            self.current += consumed
            return node

        if token.token_type in [TokenType.INTEGER, TokenType.STRING, TokenType.FLOAT]:
            return self.parse_expression()

        self.debug(f"Unexpected Token: {token}")
        return None

    def parse_expression(self):
        try:
            expr_parser = ExpressionParser(self.tokens[self.current:])
            expr, consumed = expr_parser.parse()
            if expr:
                if isinstance(expr, VariableNode):
                    value = self.symbol_table.get(expr.name)
                    if value is not None:
                        expr.value = value
                        self.debug(f"Resolved Variable: {expr.name} -> {value}")
                self.current += consumed
                return expr
        except SyntaxError as e:
            print(f"Expression Parsing Error: {e}")
        return None

    def peek_non_whitespace(self, offset=0):
        index = self.current + offset
        while index < len(self.tokens):
            token = self.tokens[index]
            if token.token_type != TokenType.WHITESPACE:
                return token
            index += 1
        return None

    def consume(self, token_type, message):
        if self.check(token_type):
            token = self.current_token()
            self.advance()
            return token
        raise SyntaxError(message)

    def check(self, *types):
        if self.is_at_end():
            return False
        return self.current_token().token_type in types

    def advance(self):
        if not self.is_at_end():
            self.debug(f"Advance: {self.current_token()}")
            self.current += 1

    def current_token(self):
        if self.is_at_end():
            return None
        return self.tokens[self.current]

    def is_at_end(self):
        return self.current >= len(self.tokens)
