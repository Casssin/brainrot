from lexer import *
from parse import *
from tok import *

def main():
    print("Brainrot Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    # Initialize the lexer and parser.
    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program() # Start the parser.
    print("Parsing completed.")

main()