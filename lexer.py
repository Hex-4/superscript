from stdlib import SuperError

TOKEN_KINDS = {
    "LeftParen": "LeftParen",
    "RightParen": "RightParen",
    "LeftBrace": "LeftBrace",
    "RightBrace": "RightBrace",
    "Comma": "Comma",
    "Dot": "Dot",
    "Minus": "Minus",
    "Plus": "Plus",
    "Slash": "Slash",
    "Star": "Star",
    "BangEqual": "BangEqual",
    "Greater": "Greater",
    "GreaterEqual": "GreaterEqual",
    "Less": "Less",
    "LessEqual": "LessEqual",
    "Equal": "Equal",
    "Identifier": "Identifier",
    "String": "String",
    "Number": "Number",
    "PlusPlus": "PlusPlus"
}

KEYWORDS = {
    "expose": "expose",
    "use": "use",
    "from": "from",
    "define": "define",
    "as": "as",
    "is": "is",
    "loop": "loop",
    "over": "over",
    "if": "if",
    "current": "current",
    "return": "return",
    "call": "call",
    "with": "with",
}

class Token:
    def __init__(self, kind, content, value, line, col):
        self.kind = kind
        self.content = content
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return self.value

class Lexer:
    def __init__(self, program):
        self.program = program
        self.line = 1
        self.current = 0
        self.col = 0

    def error(self, msg):
        raise SuperError(f"")
