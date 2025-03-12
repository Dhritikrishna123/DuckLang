from src.lexer import Lexer
from src.parser.main_parser import MainParser
from src.interpreter import Interpreter
from src.utils.debug import debug, DebugLevel
import sys

def execute_program(source_code):
    # Enable debug output
    debug.level = DebugLevel.DEBUG
    
    # Create instances
    lexer = Lexer()
    tokens = lexer.tokenize(source_code)
    parser = MainParser(tokens)
    ast = parser.parse()
    
    if ast:
        # Execute the program
        interpreter = Interpreter(debug_mode=True)
        try:
            interpreter.interpret(ast)
        except Exception as e:
            print(f"Runtime Error: {str(e)}")
    else:
        print("Parsing Error: Could not generate AST")

def main():
    # Get filename from command line argument or default to program.duck
    filename = sys.argv[1] if len(sys.argv) > 1 else 'program.duck'
    
    try:
        with open(filename, 'r') as file:
            source_code = file.read()
            execute_program(source_code)
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}' file")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
