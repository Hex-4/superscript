from stdlib import SuperError

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
    "GreaterThan": "GreaterThan",
    "LessThan": "LessThan",
    "Gte": "Gte",
    "Lte": "Lte",
    "PlusPlus": "PlusPlus",
    "Keyword": "Keyword",
    "Identifier": "Identifier",
    "Number": "Number",
    "String": "String",
    "EOF": "EOF"
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
    "takes": "takes",
    "return": "return",
    "call": "call",
    "with": "with",

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
        raise SuperError("Whoops! I found an error on line " + str(self.line) + ", column " + str(self.column) + ": " + msg)
    
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

    def match(char, self):
        if self.peek == char: return self.advance()
        return False

    def isChar(self, char):
        return (char >= "a" and char <= "z") or (char >= "A" and char <= "Z") or (char == "_")

    def isNumber(self, char):
        return char >= "0" and char <= "9"

    def isAlphanumeric(self, char):
        return self.isChar(char) or self.isNumber(char)

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
                if self.match("+"):
                    self.tokens.append(Token(TOKENS["PlusPlus"], "++", "++", self.line, self.column))
                self.tokens.append(Token(TOKENS["Plus"], char, char, self.line, self.column))

            case "/":
                self.tokens.append(Token(TOKENS["Slash"], char, char, self.line, self.column))
            case "*":
                self.tokens.append(Token(TOKENS["Star"], char, char, self.line, self.column))

            case "!":
                if self.match("="):
                    self.tokens.append(Token(TOKENS["BangEqual"], "!=", "!=", self.line, self.column))
            case ">":
                if self.match("="):
                    self.tokens.append(Token(TOKENS["Gte"], ">=", ">=", self.line, self.column))
                else: self.tokens.append(Token(TOKENS["GreaterThan"], char, char, self.line, self.column))
            case "<":
                if self.match("="):
                    self.tokens.append(Token(TOKENS["Lte"], "<=", "<=", self.line, self.column))
                
                else: self.tokens.append(Token(TOKENS["LessThan"], char, char, self.line, self.column))
            case "=":
                self.tokens.append(Token(TOKENS["Equal"], char, char, self.line, self.column))
            
            case "?":
                while self.peek != "\n" and self.peek != "\0":
                    self.advance()

            case " ":
                pass
            case "\r":
                pass
            case "/n":
                self.line = line + 1
                self.column = 0
            

            case "\"":
                string = []
                
                while self.peek != char:
                    string.append(self.advance())
                    if self.peek == "\0":
                        self.error("I couldn't find a matching end quote. Check your code to see if you missed one.")
                self.advance()
                string = string.join("")
                return self.tokens.append(Token(TOKENS["String"], string, string, self.line, self.column))
            case "\n":
                self.line += 1
                self.column = 0
            case _:
                if self.isNumber(char):
                    number = [char]
                    while (self.isNumber(self.peek)) or (self.peek == "." and not "." in number):
                        number.append(self.advance())

                    number = number.join("")
                    return self.tokens.append(Token(TOKENS["Number"], number, float(number), self.line, self.column))
                elif self.isChar(char):
                    identifier = [char]
                    while self.isAlphanumeric(self.peek()):
                        identifier.append(self.advance())

                    identifier = identifier.join("")
                    if identifier in KEYWORDS:
                        return self.tokens.append(Token(TOKENS["Keyword"], identifier, KEYWORDS[identifier], self.line, self.column))
                    elif identifier == "true" or identifier == "false":
                        return self.tokens.append(Token(TOKENS["Boolean"], identifier, identifier == "true", self.line, self.column))
                    else:
                        return self.tokens.append(Token(TOKENS["Identifier"], identifier, identifier, self.line, self.column))
                
                else:
                    self.error("I don't recognize this character: " + char + "Is this possibly a typo?")
                
