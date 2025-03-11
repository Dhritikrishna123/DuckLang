from src.lexer import Lexer
from src.parser.main_parser import MainParser
from src.interpreter import Interpreter
from src.utils.debug import debug, DebugLevel

def execute_program(source_code):
    # Disable all debug output
    debug.level = DebugLevel.OFF
    
    # Create instances
    lexer = Lexer()
    tokens = lexer.tokenize(source_code)
    parser = MainParser(tokens)
    ast = parser.parse()
    
    if ast:
        # Execute the program
        interpreter = Interpreter(debug_mode=False)
        try:
            interpreter.interpret(ast)
        except Exception as e:
            print(f"Runtime Error: {str(e)}")
    else:
        print("Parsing Error: Could not generate AST")

def main():
    # Read from program.duck file
    try:
        with open('program.duck', 'r') as file:
            source_code = file.read()
            execute_program(source_code)
    except FileNotFoundError:
        print("Error: Could not find 'program.duck' file")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
