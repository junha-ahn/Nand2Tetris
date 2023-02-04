import os

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

class JackTokenizer:
    KEYWORDS = ['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
    SYMBOLS = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']

    KEYWORD = 'keyword'
    SYMBOL = 'symbol'
    INT_CONST = 'int_const'
    STRING_CONST = 'string_const'
    IDENTIFIER = 'identifier'

    TOKEN_TYPES = {
        KEYWORD: 'keyword',
        SYMBOL: 'symbol',
        INT_CONST: 'int_const',
        STRING_CONST: 'string_const',
        IDENTIFIER: 'identifier',
    }

    counter = -1

    def checkStringConstant(self, c):
        return c == '\"'

    def checkIntegerConstant(self, c):
        return int(c) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def checkSymbol(self, c):
        return c in self.SYMBOLS


    def __init__(self,filename):
        files = []
        self.tokens = []
        with open(os.path.abspath(filename),'r') as file:
            for f in file:
                comment = f.find("//")
                if (comment >= 0):
                    f = f[:comment]
                comment=f.find("/**")
                if (comment >= 0):
                    f = f[:comment]
                comment = f.find("/*")
                if (comment >= 0):
                    f = f[:comment]
                if(f.strip().startswith("*")):
                    continue
                if f.strip() != "": files.append(f.strip())
        def checkKeep(s):
            if s in self.KEYWORDS:
                return (self.TOKEN_TYPES[self.KEYWORD], keep)
            if is_integer(s):
                return (self.TOKEN_TYPES[self.INT_CONST], keep)
            return (self.TOKEN_TYPES[self.IDENTIFIER], keep)

        for s in files:
            keep = ""
            i = 0
            while i < len(s):
                if self.checkStringConstant(s[i]) or self.checkSymbol(s[i]) or s[i] == " ":
                    if keep.strip() != "":
                        self.tokens.append(checkKeep(keep))
                        keep = ""

                    if self.checkStringConstant(s[i]):
                        start = i+1
                        end = start + s[start:].index('"')
                        content = s[start:end]
                        i = end
                        self.tokens.append((self.TOKEN_TYPES[self.STRING_CONST], content))
                    elif self.checkSymbol(s[i]):
                        self.tokens.append((self.TOKEN_TYPES[self.SYMBOL], s[i]))

                else:
                    keep += s[i]
                i += 1

    def hasMoreTokens(self):
        return len(self.token) > self.counter + 1
    
    def advance(self):
        self.counter += 1
        return True

    def back(self):
        self.counter -= 1
        return True
    def tokenType(self):
        return self.tokens[self.counter][0]

    def keyword(self):
        return self.tokens[self.counter][1]

    def symbol(self):
         return self.tokens[self.counter][1]

    def identifier(self):
        return self.tokens[self.counter][1]

    def intVal(self):
        return self.tokens[self.counter][1]

    def stringVal(self):
        return self.tokens[self.counter][1]
