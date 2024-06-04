import enum
from typing import Optional

class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	INTEGER = 1
	FLOAT  = 2
	STRING = 3
	IDENT = 4
	# Keywords.
	#LABEL = 101
	#GOTO = 102
	# SKIBIDI = print
	SKIBIDI = 102
    # RIZZ = input
	RIZZ = 104
	#LET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111
	# based = true
	BASED = 112
	# cringe = false
	CRINGE = 113
	# allow it = LET, aka assigning IDENT
	ON = 114
	GOD = 115
	# only in ohio = while
	ONLY = 116
	IN = 117
	OHIO = 118
	# SUS = endwhile
	SUSSY = 119
    # IS comparison CHAT = IF comparison
	IS = 120
	CHAT = 121
    # THANKS CHAT = ENDIF
	THANKS = 122

	# Operators.
	#EQ = 201  
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
    
    def checkIfKeyword(tokenText: str) -> Optional[TokenType]:
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        
        return None
