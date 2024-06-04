import sys
from lexer import *
from tok import *
from emitter import *

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer: Lexer, emitter: Emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.identInt = set()   # All int variables seen so far
        self.identFloat = set() # All float variables seen so far
        self.identStr = set()   # All string variables seen so far

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
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void) {")

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # Parse all the statements in the program
        while not self.checkToken(TokenType.EOF):
            self.statement()
        
        self.emitter.enderLine("return 0;")
        self.emitter.enderLine("}")
        
    
    def statement(self) -> None:
        # "RIZZ" (print) (expression | string)
        if self.checkToken(TokenType.RIZZ):
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                # Simple string, so print it.
                self.emitter.emitLine("printf(" + self.curToken.text[:-1] + "\\n\");")   # [:-1] to remove the quotation mark
                self.nextToken()
            
            # If identifier, check which identifier it is
            elif self.checkToken(TokenType.IDENT):
                if self.curToken.text in self.identFloat:
                    self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                    self.expression()
                    self.emitter.emitLine("));")
                elif self.curToken.text in self.identInt:
                    self.emitter.emit("printf(\"%" + "d\\n\", (int)(")
                    self.expression()
                    self.emitter.emitLine("));")
                elif self.curToken.text in self.identStr:
                    self.emitter.emitLine("printf(" + self.curToken.text)
                else:
                    self.abort("Need to intialize identifier before printing")

            # Else it is an expression
            else:
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")
        
        elif self.checkToken(TokenType.IDENT):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.match(TokenType.EQ)
            self.emitter.emit(" = ")
            self.expression()
            self.emitter.emitLine(";")
        
        # "IS" comparison "CHAT" nl {statement} "THANKS CHAT" nl
        elif self.checkToken(TokenType.IS):
            self.emitter.emit("if (")
            self.nextToken()
            self.comparison()
            self.emitter.emit(")")
            self.match(TokenType.CHAT)
            self.emitter.emitLine("{")

            self.nl()

            while not self.checkToken(TokenType.THANKS):
                self.statement()
            
            self.match(TokenType.THANKS)
            self.match(TokenType.CHAT)
            self.emitter.emitLine("}")
        
        # "ONLY IN OHIO" comparison nl {statement nl} "SUS" nl
        elif self.checkToken(TokenType.ONLY):
            self.nextToken()
            self.match(TokenType.IN)
            self.match(TokenType.OHIO)
            self.emitter.emit("while (")
            self.comparison()
            self.emitter.emitLine(") {")
            self.nl()

            while not self.checkToken(TokenType.SUS):
                self.statement()
        
            self.match(TokenType.SUS)
            self.emitter.emitLine("}")
        

        # "ALLOW IT" ident "=" expression
        elif self.checkToken(TokenType.ALLOW):
            self.nextToken()
            self.match(TokenType.IT)
            varName = self.curToken.text
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)


            # Find and determine what type the variable is and intialize the variable if not initalized
            if self.checkToken(TokenType.INTEGER):
                self.intializeVariable("int", varName)
                self.emitter.emit(varName + " = ")
                self.expression()
            
            elif self.checkToken(TokenType.FLOAT):
                self.intializeVariable("float", varName)
                self.emitter.emit(varName + " = ")
                self.expression()

            # Strings have a character limit of 256
            elif self.checkToken(TokenType.STRING):
                self.intializeVariable("string", varName)
                self.emitter.emit("strcpy(" + varName + ", " + self.curToken.text + ")")
                self.emitter.enderLine("free(" + varName +");")
                self.nextToken()

            elif self.checkToken(TokenType.IDENT):
                if self.curToken.text in self.identFloat:
                    self.intializeVariable("float", varName)
                elif self.curToken.text in self.identInt:
                    self.intializeVariable("int", varName)
                self.emitter.emit(varName + " = ")
                self.expression()
           
            else:
                self.abort("Could not recognize variable type")

            self.emitter.emitLine(";")

        # "SKIBIDI" ident; input must initialize variable to determine type
        elif self.checkToken(TokenType.SKIBIDI):
            self.nextToken()

            # ensures the variable is the correct type, 
            if self.checkToken(TokenType.IDENT):
                if self.curToken.text in self.identFloat:
                    # Emit scanf but also validate the input. If invalid, set the variable to 0 and clear the input.
                    self.emitter.emitLine("if(0 == scanf(\"%" + "f\", &" + self.curToken.text + ")) {")
                    self.emitter.emitLine(self.curToken.text + " = 0;")
                    self.emitter.emit("scanf(\"%")
                    self.emitter.emitLine("*s\");")
                    self.emitter.emitLine("}")

                elif self.curToken.text in self.identInt:
                    self.emitter.emitLine("if(0 == scanf(\"%" + "d\", &" + self.curToken.text + ")) {")
                    self.emitter.emitLine(self.curToken.text + " = 0;")
                    self.emitter.emit("scanf(\"%")
                    self.emitter.emitLine("*s\");")
                    self.emitter.emitLine("}")
                
                elif self.curToken.text in self.identStr:
                    self.emitter.emitLine("if(0 == scanf(\"%" + "s\", " + self.curToken.text + ")) {")
                    self.emitter.emitLine(self.curToken.text + " = 0;")
                    self.emitter.emit("scanf(\"%")
                    self.emitter.emitLine("*s\");")
                    self.emitter.emitLine("}")
                
                else:
                    self.abort("Expected an initalized variable for SKIBIDI")
            else:
                self.abort("Expected an initalized variable for SKIBIDI")
            self.nextToken()


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
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.term()
    
    # term ::= unary {( "/" | "*" ) unary}
    def term(self) -> None:
        print("TERM")

        self.unary()
        # Can have 0 or more *// expressions
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()
    
    def unary(self) -> None:
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        self.primary()
    
    # primary ::= number | ident
    def primary(self) -> None:

        if self.checkToken(TokenType.INTEGER) or self.checkToken(TokenType.FLOAT): 
            self.emitter.emit(self.curToken.text)
            self.nextToken()

        elif self.checkToken(TokenType.IDENT):
            # Ensure the variable already exists.
            if self.curToken.text not in self.identInt and self.curToken.text not in self.identFloat:
                print(self.identInt, self.identFloat)
                self.abort("Referencing variable before assignment: " + self.curToken.text)

            self.emitter.emit(self.curToken.text)
            self.nextToken()
        else:
            # Error!
            self.abort("Unexpected token at " + self.curToken.text)

    def comparison(self) -> None:
        print("COMPARISON")
        self.expression()

        # Must have one comparison operator and another expression
        if self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()

        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()
        
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()
    
    def isComparisonOperator(self) -> bool:
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)
    
    def intializeVariable(self, varType: str, varName: str) -> None:
        # check if ident exists in symbol table. if not declare it
        if self.curToken.text not in self.identFloat or self.curToken.text not in self.identInt or self.curToken.text not in self.identStr:
            if varType == "string":
                self.identStr.add(varName)
                self.emitter.headerLine("char *" + varName + " = malloc(256);")
            elif varType == "int":
                self.identInt.add(varName)
                self.emitter.headerLine(varType + " " + varName + ";")
            else:
                self.identFloat.add(varName)
                self.emitter.headerLine(varType + " " + varName + ";")