import JackTokenizer

def checkList(v):
    return hasattr(v, "__len__")


class Writer:
    def __init__(self, file_name, isPrint = False):
        self.isPrint = isPrint
        if not isPrint:
            self.file = open(f'{file_name}.xml' , 'w')
        pass

    def write(self, s):
        if self.isPrint:
            print(s)
        else:
            self.file.write(s + '\n')
    def writeTag(self, type, s):
        self.write(f"<{type}> {s} </{type}>")
        
    def close(self):
        self.file.close()

class CompilationEngine:
    OP = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

    def __init__(self, tokenizer: JackTokenizer, filename):
        self.writer = Writer(filename)
        self.tokenizer = tokenizer

    def getValue(self):
        v = self.tokenizer.keyword()
        tokenType = self.tokenizer.tokenType()
        if tokenType == self.tokenizer.SYMBOL: v = self.tokenizer.symbol()
        if tokenType == self.tokenizer.IDENTIFIER: v = self.tokenizer.identifier()
        if tokenType == self.tokenizer.INT_CONST: v = self.tokenizer.intVal()
        if tokenType == self.tokenizer.STRING_CONST: v = self.tokenizer.stringVal()
        return v

    
    def require(self, type, requiredValue):
        v = self.getValue()

        flag = self.tokenizer.tokenType() == type
        if requiredValue is not None:
            if checkList(requiredValue): flag = flag and v in requiredValue
            else: flag = flag and v == requiredValue
        return flag

    def isKeyword(self, requiredValue = None): return self.require(self.tokenizer.KEYWORD, requiredValue)
    def isSymbol(self, requiredValue = None): return self.require(self.tokenizer.SYMBOL, requiredValue)
    def isIdentifier(self, requiredValue = None): return self.require(self.tokenizer.IDENTIFIER, requiredValue)
    def isInt(self, requiredValue = None): return self.require(self.tokenizer.INT_CONST, requiredValue)
    def isString(self, requiredValue = None): return self.require(self.tokenizer.STRING_CONST, requiredValue)
    def isOp(self): return self.isSymbol() and self.tokenizer.symbol() in self.OP

    def __write(self, type, requiredValue):
        if self.require(type, requiredValue):
            self.writeCurrentTagAndNext()
        else:
            v = self.getValue()

            raise Exception(f'required {type}:{requiredValue} but {v}')  
    def writeKeyword(self, requiredValue = None): self.__write(self.tokenizer.KEYWORD, requiredValue)
    def writeSymbol(self, requiredValue = None): self.__write(self.tokenizer.SYMBOL, requiredValue)
    def writeIdentifier(self, requiredValue = None): self.__write(self.tokenizer.IDENTIFIER, requiredValue)
    def writeInt(self, requiredValue = None): self.__write(self.tokenizer.INT_CONST, requiredValue) 
    def writeString(self, requiredValue = None): self.__write(self.tokenizer.STRING_CONST, requiredValue)

    def writeCurrentTagAndNext(self):
        v = self.getValue()
        if v == '<': v = '&lt;'
        if v == '>': v = '&gt;'
        if v == '"': v = '&quot;'
        if v == '&': v = '&amp;'

        token_type = self.tokenizer.tokenType()
        if token_type == self.tokenizer.STRING_CONST: token_type = "stringConstant"
        if token_type == self.tokenizer.INT_CONST: token_type = "integerConstant"
        self.writer.writeTag(token_type, v)
        self.tokenizer.advance()


    def compileType(self):
        # add here: check type 
        self.writeCurrentTagAndNext()

    def CompileClass(self):
        self.writer.write("<class>")
        self.tokenizer.advance()
        self.writeKeyword('class') 
        self.writeIdentifier()  # class name
        self.writeSymbol('{') 

        self.CompileClassVarDec()
        self.CompileSubroutine()
    
        self.writeSymbol('}')
        
        self.writer.write("</class>")
        self.writer.close()

    def CompileClassVarDec(self):
        def isClassVarDec():
            return self.isKeyword(['static', 'field'])

        if not isClassVarDec():
            return False

        while isClassVarDec():
            self.writer.write('<classVarDec>')

            self.writeKeyword(['static', 'field'])
            self.compileType()
            self.writeIdentifier()
            while self.isSymbol(','):
                self.writeSymbol(',')
                self.writeIdentifier()
            self.writeSymbol(';')
            self.writer.write('</classVarDec>')

    def CompileSubroutine(self):
        def isSubroutine():
            return self.isKeyword(['constructor', 'function', 'method'])
    
        if not isSubroutine():
            return 
        

        while isSubroutine():
            self.writer.write('<subroutineDec>')
            self.writeKeyword(['function', 'method', 'constructor'])
            self.compileType()  # type
            self.writeIdentifier()  # Functionname
            self.writeSymbol('(')  
            self.writer.write('<parameterList>')
            self.compileParameterList()
            self.writer.write('</parameterList>')
            self.writeSymbol(')') 
            self.compileSubRoutineBody()
            self.writer.write('</subroutineDec>')


    def compileParameterList(self):
        def isParameter():
            return self.isKeyword(['int', 'char', 'boolean'])

        if not isParameter():
            return
        
        while isParameter():
            self.compileType()  # type
            self.writeIdentifier()  # variable name
            if self.isSymbol(','):
                self.writeSymbol(',')

    def compileSubRoutineBody(self):
        self.writer.write('<subroutineBody>')
        self.writeSymbol('{') 
        self.compileVarDec()
        self.compileStatements()
        self.writeSymbol('}')
        self.writer.write('</subroutineBody>')



    def compileVarDec(self):
        def isVar():
            return self.isKeyword('var')

        if not isVar():
            return
        while isVar():
            self.writer.write('<varDec>')
            self.writeKeyword('var')
            self.compileType()  # type
            self.writeIdentifier()  # varName
        
            while self.isSymbol(','):
                self.writeSymbol(',')
                self.writeIdentifier()  # varName
        
            self.writeSymbol(';')
            self.writer.write('</varDec>')


    def compileStatements(self):
        def callAll():
            return self.compileLet() or self.compileDo() or self.compileIf() or self.compileReturn() or self.compileWhile()
        

        self.writer.write('<statements>')
                
        while callAll():
            continue

        self.writer.write('</statements>')
        return True

    def compileDo(self):
        def checkDo():
            return self.isKeyword('do')
        if not checkDo():
            return False
        self.writer.write('<doStatement>')
        self.writeKeyword('do')
        self.compileSubroutineCall()
        self.writeSymbol(';')
        self.writer.write('</doStatement>')
        return True

    def compileLet(self):
        def checkLet():
            return self.isKeyword('let')

        if not checkLet():
            return False
        self.writer.write('<letStatement>')
        self.writeKeyword('let')
        self.writeIdentifier() # varName
        if self.isSymbol('['):
            self.writeSymbol('[')
            self.CompileExpression()
            self.writeSymbol(']')
        self.writeSymbol('=')
        self.CompileExpression()
        self.writeSymbol(';')
        self.writer.write('</letStatement>')
        return True

    
    def compileWhile(self):
        def checkWhile():
            return self.isKeyword('while')
        if not checkWhile():
            return False
        self.writer.write('<whileStatement>')
        self.writeKeyword('while') 
        self.writeSymbol('(')
        self.CompileExpression()
        self.writeSymbol(')')
        self.writeSymbol('{') 
        self.compileStatements()
        self.writeSymbol('}') 
        self.writer.write('</whileStatement>')
        return True

    def compileReturn(self):
        def checkReturn():
            return self.isKeyword('return')
        if not checkReturn():
            return False
        self.writer.write('<returnStatement>')
        self.writeKeyword('return') 
        if not self.isSymbol(';'):
            self.CompileExpression()
        self.writeSymbol(';')
        self.writer.write('</returnStatement>')
        return True

    def compileIf(self):
        def checkIf():
            return self.isKeyword('if')
        if not checkIf():
            return False
        self.writer.write('<ifStatement>')
        self.writeKeyword('if') 
        self.writeSymbol('(')
        self.CompileExpression()
        self.writeSymbol(')')
        self.writeSymbol('{')
        self.compileStatements()
        self.writeSymbol('}')
        self.writer.write('</ifStatement>')
        return True

    def CompileExpression(self):
        self.writer.write('<expression>')
        self.CompileTerm()
        while self.isOp():
            self.writeSymbol(self.OP)
            self.CompileTerm()

        self.writer.write('</expression>')

    def CompileTerm(self):
        self.writer.write('<term>')
        if self.isInt(): self.writeInt()
        elif self.isString(): self.writeString()
        elif self.isKeyword(): self.writeKeyword()
        elif self.isSubroutineCall(): self.compileSubroutineCall()
        elif self.isIdentifier(): 
            self.writeIdentifier() # varName
            if self.isSymbol('['):
                self.writeSymbol('[')
                self.CompileExpression()
                self.writeSymbol(']')
        elif self.isSymbol('('):
            self.writeSymbol('(')
            self.CompileExpression()
            self.writeSymbol(')')
        elif self.isSymbol(['-', '~']):
            self.writeSymbol(['-', '~'])
            self.CompileTerm()
            
        self.writer.write('</term>')
        return True

    def CompileExpressionList(self):
        self.writer.write('<expressionList>')

        if not self.isSymbol(')'):
            self.CompileExpression()
            while self.isSymbol(','):
                self.writeSymbol(',')
                self.CompileExpression()
        self.writer.write('</expressionList>')
        return True

    def isSubroutineCall(self):
        flag = self.isIdentifier()
        self.tokenizer.advance()
        flag = flag and self.isSymbol(['(', '.'])
        self.tokenizer.back()
        return flag
        
    def compileSubroutineCall(self):
        if not self.isSubroutineCall():
            return False
        self.writeIdentifier()
        if self.tokenizer.symbol() == '.':
            self.writeSymbol('.')
            self.writeIdentifier()
        self.writeSymbol('(')
        self.CompileExpressionList()
        self.writeSymbol(')')
        return True

