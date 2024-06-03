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
        self.nextToken()

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

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

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
        
        # "IF" comparison "THEN" nl {statement} "ENDIF" nl
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            
            self.match(TokenType.ENDIF)
        
        # "WHILE" comparison "REPEAT" nl {satement nl} "ENDWHILE" nl
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
        
            self.match(TokenType.ENDWHILE)
        
                # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()
            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.match(TokenType.IDENT)

        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            print("STATEMENT-LET")
            self.nextToken()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)

            self.expression()

        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()
            self.match(TokenType.IDENT)

        # This is not a valid statement. Error!
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        # Newline.
        self.nl()
        
    
    # nl ::= '\n' +
    def nl(self) -> None:
        self.match(TokenType.NEWLINE)
        print("NEWLINE")

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

    # expression ::= term {( "-" | "+" ) term}
    def expression(self) -> None:
        print("EXPRESSION")

        self.term()
        # Can have 0 o r more +/- epxressions
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()
    
    # term ::= unary {( "/" | "*" ) unary}
    def term(self) -> None:
        print("TERM")

        self.unary()
        # Can have 0 or more *// expressions
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()
    
    def unary(self) -> None:
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()
    
    def primary(self) -> None:
        print("Primary (" + self.curToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.curToken.text)

    def comparison(self) -> None:
        print("COMPARISON")
        self.expression()

        # Must have one comparison operator and another expression
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)
        
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()
    
    def isComparisonOperator(self) -> bool:
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)