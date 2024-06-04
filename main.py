from lexer import *
from parse import *
from tok import *
from emitter import *

def main():
    print("Brainrot Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    # Initialize the lexer and parser.
    lexer = Lexer(source)
    emitter = Emitter("compiled/out.c")
    parser = Parser(lexer, emitter)

    parser.program() # Start the parser.
    emitter.writeFile() # writes the file
    print("Parsing completed.")

main()