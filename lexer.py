import sys
from tok import *

class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source + '\n' # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.curChar = ''   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.nextChar()

    # Process the next character.
    def nextChar(self) -> None:
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0' # EOF output
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self) -> str:
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]

    # Invalid token found, print error message and exit.
    def abort(self, message: str) -> None:
        sys.exit("Lexing error. " + message)
		
    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self) -> None:
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()
            
    # Skip comments in the code.
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # Return the next token.
    def getToken(self) -> Token:
        self.skipWhitespace()
        self.skipComment()
        token = None

        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g., !=), number, identifier, or keyword then we will process the rest.
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)

        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)

        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)

        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)

        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)

        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)

        elif self.curChar == '=':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)

        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)

        elif self.curChar == '<':
                # Check whether this is token is < or <=
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.LTEQ)
                else:
                    token = Token(self.curChar, TokenType.LT)

        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())

        elif self.curChar.isdigit():
            # Leading character is a digit, so this must be number
            isFloat = False
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            
            if self.peek() == '.':   # Decimal
                isFloat = True
                self.nextChar()

                if not self.peek().isdigit():
                    self.abort("Illegal characters in number")
                
                while self.peek().isdigit():
                    self.nextChar()
            
            tokText = self.source[startPos:self.curPos + 1]
            if isFloat:
                token = Token(tokText, TokenType.FLOAT)
            else:
                token = Token(tokText, TokenType.INTEGER)

        elif self.curChar.isalpha():
            # Leading character is a letter, so must be an identifier or keyword
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            
            # check if token is in list of keywords
            tokText = self.source[startPos : self.curPos + 1]
            keyword = Token.checkIfKeyword(tokText)
    

            if keyword == None:    # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:                  # keyword
                token = Token(tokText, keyword)
        
        elif self.curChar == '\"':
            # leading character is string
            startPos = self.curPos

            while self.peek() != '\"':
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")

                self.nextChar()
            self.nextChar()
            tokText = self.source[startPos : self.curPos + 1]   # Get substring
            token = Token(tokText, TokenType.STRING)

        else:
            self.abort("Unknown token: " + self.curChar)
			
        self.nextChar()
        return token


