TOKENS = {
    "LeftParen": "LeftParen",
    "RightParen": "RightParen",
    "LeftBrace": "LeftBrace",
    "RightBrace": "RightBrace",
    "LeftBracket": "LeftBracket",
    "RightBracket": "RightBracket",
    "Comma": "Comma",
    "Dot": "Dot",
    "Colon": "Colon",
    "Minus": "Minus",
    "Plus": "Plus",
    "Slash": "Slash",
    "Star": "Star",
    "BangEqual": "BangEqual",
    "Equal": "Equal",
    "Keyword": "Keyword",
    "Identifier": "Identifier",
    "Number": "Number",
    "String": "String",
    "EOF": "EOF"
}

class Token:
    def __init__(kind, value, content, line, column):
        self.type = kind # From TOKENS
        self.value = value
        self.content = content
        self.line = line
        self.column = column
    def __str__(self):
        return self.value
    def __repr__(self):
        return self.value

class Lexer:
    def __init__(self,program):
        self.program = program
        self.tokens = []
        self.current = 0
        self.line = 1
        self.column = 0
    
    def error(msg):
        raise SuperscriptError("Oh no! We've got an error on line " + str(self.line) + " column " + str(self.column) + ": " + msg)
    
    def scanTokens(self):
        while self.peek != "\0":
            self.scanToken()
        self.tokens.append(Token("EOF", None, None, self.line, self.column))
        return self.tokens

    def peek(self):
        if self.current >= len(self.program):
            return "\0"
        return self.program[self.current]

    def advance(self):
        if self.current >= len(self.program):
            return "\0"
        self.current += 1
        self.column += 1
        return self.program[self.current]

    def addToken(self, kind, value, content):
        self.tokens.append(Token(kind, value, content, self.line, self.column))

    def scanToken(self):
        char = self.advance()
        match char:
            case "(":
                self.tokens.append(Token(TOKENS["LeftParen"], char, char, self.line, self.column))
            case ")":
                self.tokens.append(Token(TOKENS["RightParen"], char, char, self.line, self.column))
            case "{":
                self.tokens.append(Token(TOKENS["LeftBrace"], char, char, self.line, self.column))
            case "}":
                self.tokens.append(Token(TOKENS["RightBrace"], char, char, self.line, self.column))
            case "[":
                self.tokens.append(Token(TOKENS["LeftBracket"], char, char, self.line, self.column))
            case "]":
                self.tokens.append(Token(TOKENS["RightBracket"], char, char, self.line, self.column))
            case ",":
                self.tokens.append(Token(TOKENS["Comma"], char, char, self.line, self.column))
            case ".":
                self.tokens.append(Token(TOKENS["Dot"], char, char, self.line, self.column))
            case ":":
                self.tokens.append(Token(TOKENS["Colon"], char, char, self.line, self.column))
            case "-":
                self.tokens.append(Token(TOKENS["Minus"], char, char, self.line, self.column))
            case "+":
                self.tokens.append(Token(TOKENS["Plus"], char, char, self.line, self.column))
            case "/":
                self.tokens.append(Token(TOKENS["Slash"], char, char, self.line, self.column))
            case "*":
                self.tokens.append(Token(TOKENS["Star"], char, char, self.line, self.column))
            case "!=":
                self.tokens.append(Token(TOKENS["BangEqual"], char, char, self.line, self.column))
            case "=":
                self.tokens.append(Token(TOKENS["Equal"], char, char, self.line, self.column))
            case "\"":
                pass # TODO: strings
            case "\n":
                self.line += 1
                self.column = 0          
