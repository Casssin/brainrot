import sys
from lexer import *
from tok import *

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

    # Return true if the current token matches.
    def checkToken(self, kind: TokenType) -> bool:
        return kind == self.curToken.kind

    # Return true if the next token matches.
    def checkPeek(self, kind: TokenType) -> bool:
        return kind == self.peekToken.kind

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind: TokenType) -> None:
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)

    # Advances the current token.
    def nextToken(self) -> None:
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message: str) -> None:
        sys.exit("Error. " + message)
    
    # Production rules

    # program ::= {statement}
    def program(self) -> None:
        print("PROGRAM")

        # Parse all the statements in the program
        while not self.checkToken(TokenType.EOF):
            self.statement()
    
    def statement(self) -> None:

        # "umm actually" (print) (expression | string)
        if self.checkToken(TokenType.umm) and self.checkPeek(TokenType.actually):
            print("STATEMENT-umm-actually")
            self.nextToken()
            self.nextToken()
            if self.checkToken(TokenType.STRING):
                self.nextToken()
            else:
                self.expression()
        
        self.nl()
    
    # nl ::= '\n' +
    def nl(self) -> None:
        print("NEWLINE")

        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

    def expression(self) -> None:
        pass