from stdlib import SuperError
from rich import print


TOKEN_KINDS = {
    "LeftParen": "LeftParen",
    "RightParen": "RightParen",
    "LeftBrace": "LeftBrace",
    "RightBrace": "RightBrace",
    "LeftBracket": "LeftBracket",
    "RightBracket": "RightBracket",
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
    "Boolean": "Boolean",
    "Keyword": "Keyword",
    "PlusPlus": "PlusPlus",
    "EOF": "EOF",
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
        return str(self.value)

class Lexer:
    def __init__(self, program):
        self.program = program
        self.tokens = []
        self.line = 1
        self.current = 0
        self.col = 1

    def error(self, msg):
        msg = str(self.line) + "|" + str(self.col) + "|" + msg
        raise SuperError(msg)

    def scanTokens(self):
        while self.peek() != "\0" or self.peek() != "\x00":
            self.scanToken()
        self.tokens.append(Token(TOKEN_KINDS["EOF"], "\0", "\0", self.line, self.col))
        return self.tokens
    
    def peek(self):
        if self.current >= len(self.program):
            return "\0"
        return self.program[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.program):
            return "\0"
        return self.program[self.current + 1]

    def advance(self):
        if self.current >= len(self.program):
            return "\0"
        self.current += 1
        self.col += 1
        print(self.current)
        try:
            return self.program[self.current]
        except IndexError:
            return "\0"
    

    def scanToken(self):
        
        def match(char):
            if self.peek() == char: return self.advance()
            else: return False

        # Modded helper functions from Arson (easel/languages/arson)
        def is_alphanumeric(char):
            return char != " " and (char.isalpha() or char.isnumeric() or char == "_")

        def string(char):
            text = self.advance()
            
            while self.peek() != char and self.peek() != "\0":
                if self.peek() == "\n":
                    self.line += 1
                text += self.advance()
            if self.peek() == "\0":
                # Reached end of file, but string hasn't been terminated
                raise SuperError(f"Unterminated string: {self.line}")
            self.advance()  # Consume the closing quote
            text = text[:-1]
            self.tokens.append(Token(TOKEN_KINDS["String"], text, text, self.line, self.col))

        def number():
            text = self.peek()
            while self.peek().isnumeric():
                text += self.advance()
            if self.peek() == "." and self.peek_next().isnumeric():
                text += self.advance()
                while self.peek().isnumeric():
                    text += self.advance()
            text = text[:-1]
            self.tokens.append(Token(TOKEN_KINDS["Number"], text, float(text), self.line, self.col))

        def identifier():
            text = self.peek()
            while is_alphanumeric(self.peek()):
                text += self.advance()
            text = text[:-1]
            kind = KEYWORDS.get(text, None)
            if kind is None:
                kind = TOKEN_KINDS["Identifier"]
            self.current -= 1

            self.tokens.append(Token(kind, text, text, self.line, self.col))


        c = self.advance()
        print(self.tokens)
        match(c):
            case "(":
                self.tokens.append(Token(TOKEN_KINDS["LeftParen"], c, c, self.line, self.col))
            case ")":
                self.tokens.append(Token(TOKEN_KINDS["RightParen"], c, c, self.line, self.col))
            case "{":
                self.tokens.append(Token(TOKEN_KINDS["LeftBrace"], c, c, self.line, self.col))
            case "}":
                self.tokens.append(Token(TOKEN_KINDS["RightBrace"], c, c, self.line, self.col))
            case "[":
                self.tokens.append(Token(TOKEN_KINDS["LeftBracket"], c, c, self.line, self.col))
            case "]":
                self.tokens.append(Token(TOKEN_KINDS["RightBracket"], c, c, self.line, self.col))
            case ",":
                self.tokens.append(Token(TOKEN_KINDS["Comma"], c, c, self.line, self.col))
            case ".":
                self.tokens.append(Token(TOKEN_KINDS["Dot"], c, c, self.line, self.col))
            case "-":
                self.tokens.append(Token(TOKEN_KINDS["Minus"], c, c, self.line, self.col))
            case "+":
                if match("+"): self.tokens.append(Token(TOKEN_KINDS["PlusPlus"], c+c, c+c, self.line, self.col))
                else: self.tokens.append(Token(TOKEN_KINDS["Plus"], c, c, self.line, self.col))
            case "/":
                self.tokens.append(Token(TOKEN_KINDS["Slash"], c, c, self.line, self.col))
            case "*":
                self.tokens.append(Token(TOKEN_KINDS["Star"], c, c, self.line, self.col))
            case "\"":
                string("\"")
            case "!":
                if match("="): self.tokens.append(Token(TOKEN_KINDS["BangEqual"], "!=", "!=", self.line, self.col))
            case ">":
                if match("="): self.tokens.append(Token(TOKEN_KINDS["GreaterEqual"], ">=", ">=", self.line, self.col))
                else: self.tokens.append(Token(TOKEN_KINDS["Greater"], ">", ">", self.line, self.col))
            case "<":
                if match("="): self.tokens.append(Token(TOKEN_KINDS["LessEqual"], "<=", "<=", self.line, self.col))
                else: self.tokens.append(Token(TOKEN_KINDS["Less"], "<", "<", self.line, self.col))
            case "=":
                self.tokens.append(Token(TOKEN_KINDS["Equal"], "=", "=", self.line, self.col))
            case "?":
                while self.peek() != "\n" and self.peek() != "\0": self.advance()
            case " " | "\t" | "\r":
                pass
            case "\n":
                self.line += 1
                self.col = 0
            case _:
                if c.isalpha():
                    identifier()
                elif c.isnumeric():
                    number()
                elif c == "\x00":
                    return
                else:
                    raise Exception(f"Unexpected character: {c}")
                    


                


