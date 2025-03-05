from src.lexer import Lexer
from src.parser.main_parser import MainParser

# ========================
# 1. Source Code Input
# ========================
source_code = """
var = 56
x = 3
hello = (var + x)

"""

# ========================
# 2. Lexical Analysis
# ========================
print("\n🔍 [Lexical Analysis]")
lexer = Lexer()
tokens = lexer.tokenize(source_code)

# Detailed Token Information
print("\n📝 Token Details:")
for token in tokens:
    print(f"🔹 {token}")

# Token Table
print("\n📌 Token Table:")

# Define column widths
col_widths = [20, 12, 14, 12, 6, 8]
line_sep = "+" + "+".join(["-" * w for w in col_widths]) + "+"

# Table Header
print(line_sep)
print(f"| {'Type':<20} | {'Value':<12} | {'Start Index':<14} | {'End Index':<12} | {'Line':<6} | {'Column':<8} |")
print(line_sep)

# Token Rows
for token in tokens:
    print(f"| {str(token.token_type):<20} | {str(token.value):<12} | {str(token.start_pos.index):<14} | {str(token.end_pos.index):<12} | {str(token.start_pos.line):<6} | {str(token.start_pos.column):<8} |")

print(line_sep)

# ========================
# 3. Parsing & Symbol Table
# ========================
print("\n🌳 [Parsing]")
try:
    parser = MainParser(tokens)
    ast = parser.parse()

    # Pretty Printed AST
    print("\n🧠 AST Nodes:")
    for statement in ast:
        print(f"🔸 {statement}")

    # Symbol Table Dump
    parser.symbol_table.dump()

    print("\n🎯 Parsing Completed Successfully!")
except SyntaxError as e:
    print(f"❌ Syntax Error: {e}")
except Exception as e:
    print(f"⚠️ Error: {e}")
