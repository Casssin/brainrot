import enum
from typing import Optional

class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3
	# Keywords.
	LABEL = 101
	GOTO = 102
	umm = 103
	actually = 104
	LET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111
	based = 112
	cringe = 113
	# Operators.
	EQ = 201  
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211


class Token:
    def __init__(self, tokenText: str, tokenKind: TokenType) -> None:
        self.text = tokenText  # The token's actual text
        self.kind = tokenKind  # The tokentype that this token is classified as
    
    def checkIfKeyword(tokenText: str) -> Optional[bool]:
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        
        return None
