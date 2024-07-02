from stdlib import SuperError



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
        return self.value

class Lexer:
    def __init__(self, program):
        self.program = program
        self.tokens = []
        self.line = 1
        self.current = 0
        self.col = 0

    def error(self, msg):
        msg = str(self.line) + "|" + str(self.col) + "|" + msg
        raise SuperError(msg)

    def scanTokens(self):
        while self.peek() != "\0":
            self.scanToken()
        self.tokens.append(Token(TOKEN_KINDS["EOF"], "", "", self.line, self.col))
        return self.tokens
    
    def peek(self):
        if self.current >= len(self.program):
            return "\0"
        return self.program[self.current]

    def advance(self):
        if self.current >= len(self.program):
            return "\0"
        self.current += 1
        self.col += 1
        print(self.current)
        return self.program[self.current]
    

    def scanToken(self):
        
        def match(char):
            if self.peek() == char: return self.advance()
            else: return False
        def isnumber(char):
            return char >= "0" and char <= "9"
        def ischar(char):
            return (char >= "a" and char <= "z") or (char >= "A" and char <= "Z") or char == "_"
        def isalphanumeric(char):
            return ischar(char) or isnumber(char)

        c = self.advance()
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
                string = []
                while self.peek() != "\"":
                    string.append(self.advance())
                    if self.peek() == "\0":
                        self.error("Unterminated string. Did you miss a closing quote?")
                self.advance() # eat the last quote
                string = "".join(string)
                self.tokens.append(Token(TOKEN_KINDS["String"], string, string, self.line, self.col))
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
                if isnumber(c):
                    number = [c]
                    while isnumber(self.peek()) or (self.peek == "." and not "." in number):
                        number.append(self.advance())
                    number = "".join(number)
                    self.tokens.append(Token(TOKEN_KINDS["Number"], number, float(number), self.line, self.col))
                elif ischar(c):
                    identifier = [c]
                    while isalphanumeric(self.peek()): identifier.append(self.advance())
                    identifier = "".join(identifier)
                    for i in KEYWORDS:
                        if i in identifier:
                            self.tokens.append(Token(TOKEN_KINDS["Keyword"], identifier, KEYWORDS[i], self.line, self.col))
                            return
                    if identifier == "true" or identifier == "false":
                        self.tokens.append(Token(TOKEN_KINDS["Boolean"], identifier, identifier == "true", self.line, self.col))
                    else:
                        self.tokens.append(Token(TOKEN_KINDS["Identifier"], identifier, identifier, self.line, self.col))
                else:
                    self.error("Unexpected character: " + c)
                    


                


