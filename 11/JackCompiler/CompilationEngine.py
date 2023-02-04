from JackTokenizer import JackTokenizer
from Writer import Writer
from VMWriter import VMWriter
from SymbolTable import SymbolTable

def checkList(v):
    return hasattr(v, "__len__")

class CompilationEngine:
    OP = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

    def __init__(self, filename, tokenizer, vmWriter):
        self.tokenizer = tokenizer
        self.vmWriter = vmWriter
        self.symbolTable = SymbolTable()
        self.className = ''
        self.subroutineName = ''
        self.lebelIndex = -1

    def getValue(self):
        v = self.tokenizer.keyword()
        tokenType = self.tokenizer.tokenType()
        if tokenType == self.tokenizer.SYMBOL: v = self.tokenizer.symbol()
        if tokenType == self.tokenizer.IDENTIFIER: v = self.tokenizer.identifier()
        if tokenType == self.tokenizer.INT_CONST: v = self.tokenizer.intVal()
        if tokenType == self.tokenizer.STRING_CONST: v = self.tokenizer.stringVal()
        return v
        
    def advance(self, requiredValue = None):
        self.tokenizer.advance()
        return self.getValue()

    def getType(self, requiredValue = None):
        self.tokenizer.advance()
        return self.getValue()

    def nextTokenTypeIs(self, requireType):
        self.advance()
        flag = self.tokenizer.tokenType() == requireType
        self.tokenizer.back()
        return flag
        

    def nextValueIs(self, requiredValue):
        v = self.advance()
        self.tokenizer.back()

        flag = False
        if checkList(requiredValue): 
            flag = v in requiredValue
        else: 
            flag = v == requiredValue

        return flag

    def CompileClass(self):
        self.advance('class')
        self.className = self.advance()
        self.advance('{')
        
        self.CompileClassVarDec()
        self.CompileSubroutine()

        self.advance('}')
        self.vmWriter.close()

    def CompileClassVarDec(self):
        def isClassVarDec():
            return self.nextValueIs(['static', 'field'])

        while isClassVarDec():
            kind = self.advance()  #'static' or 'field'
            type = self.advance()  # var type
            name = self.advance()  # var name
            self.symbolTable.Define(name, type, kind)
            while self.nextValueIs(','):
                self.advance()
                name = self.advance()
                self.symbolTable.Define(name, type, kind)
            self.advance(';')

    def CompileSubroutine(self):
        def isSubroutine():
            return self.nextValueIs(['constructor', 'function', 'method'])
            
        
        while isSubroutine():
            funcType = self.advance(['function', 'method', 'constructor'])
            self.getType() # return type
            self.subroutineName = self.advance() 
            self.symbolTable.startSubroutine()
            self.advance('(')
            self.CompileParameterList(funcType)
            self.advance(')')
            self.CompileSubroutineBody(funcType)
    
    def CompileParameterList(self, funcType):
        def isParameter():
            return self.nextValueIs(['int', 'char', 'boolean'])

        if not isParameter():
            return

        if funcType == "method":
            self.symbolTable.Define("this", "self", 'arg')

        while isParameter():
            type = self.getType()
            name = self.advance()
            self.symbolTable.Define(name, type, 'arg')
            if self.nextValueIs(','):
                self.advance(',')

    def CompileSubroutineBody(self, funcType):
        self.advance('{') 
        self.compileVarDec()

        self.vmWriter.writeFunction(
            f'{self.className}.{self.subroutineName}',
            self.symbolTable.VarCount('var')
        );

        if funcType == "method":
            self.vmWriter.writePush('argument', 0)
            self.vmWriter.writePop('pointer', 0)
        if funcType == 'constructor':
            self.vmWriter.writePush('constant', self.symbolTable.VarCount('field'))
            self.vmWriter.writeCall('Memory.alloc', 1)
            self.vmWriter.writePop('pointer', 0)

        self.compileStatements()
        self.advance('}')

    def compileVarDec(self):
        def isVar():
            return self.nextValueIs('var')

        while isVar():
            kind = self.advance()
            type = self.advance()
            name = self.advance()
        
            self.symbolTable.Define(name, type, kind)
            while self.nextValueIs(','):
                self.advance(',')
                name = self.advance()
                self.symbolTable.Define(name, type, kind)

            self.advance(';')
    
    def compileStatements(self):
        def isStatements():
            return self.nextValueIs(['do', 'let', 'if', 'while', 'return'])
        

        while isStatements():
            if   self.nextValueIs("do"):     self.compileDo()
            elif self.nextValueIs("let"):    self.compileLet()
            elif self.nextValueIs("if"):     self.compileIf()
            elif self.nextValueIs("while"):  self.compileWhile()
            elif self.nextValueIs("return"): self.compileReturn()
    
    def compileIf(self):
        def isIf():
            return self.nextValueIs('if')
        if not isIf(): return False
        
        ifCounter = str(self.symbolTable.ifCounter)
        self.symbolTable.ifCounter += 1
    
        self.advance('if') 
        self.advance('(')
        self.CompileExpression()
        self.advance(')')

        # if not condition: go to endLabel
        self.vmWriter.writeIf('IF_TRUE' + ifCounter)
        self.vmWriter.writeGoto('IF_FALSE' + ifCounter)
        self.vmWriter.writeLabel('IF_TRUE' + ifCounter)

        self.advance('{')
        self.compileStatements()
        self.advance('}')

        if self.nextValueIs('else'):
            self.vmWriter.writeGoto('IF_END' + ifCounter)
            self.vmWriter.writeLabel('IF_FALSE' + ifCounter)
            self.advance('else')
            self.advance('{')
            self.compileStatements()
            self.advance('}')
            self.vmWriter.writeLabel('IF_END' + ifCounter)
        else:
            self.vmWriter.writeLabel('IF_FALSE' + ifCounter)
            

    
    def compileWhile(self):
        def isWhile(): return self.nextValueIs('while')
        if not isWhile(): return False

        whileCounter = str(self.symbolTable.whileCounter)
        self.symbolTable.whileCounter +=1

        self.vmWriter.writeLabel('WHILE_EXP' + whileCounter)

        self.advance('while') 
        self.advance('(')
        self.CompileExpression()
        self.advance(')')

        # if not condition: go to endLabel
        self.vmWriter.writerArithmetic('not')
        self.vmWriter.writeIf('WHILE_END' + whileCounter)

        self.advance('{') 
        self.compileStatements()
        self.advance('}') 

        self.vmWriter.writeGoto('WHILE_EXP' + whileCounter)
        self.vmWriter.writeLabel('WHILE_END' + whileCounter)

    def compileLet(self):
        def isLet():
            return self.nextValueIs('let')

        if not isLet(): return False

        self.advance('let')
        varName = self.advance()
        # if self.nextValueIs('['):
        #     self.advance('[')
        #     self.CompileExpression()
        #     self.advance(']')
        self.advance('=')
        self.CompileExpression()
        self.advance(';')

        self.vmWriter.writePop(
            self.symbolTable.getSegmentByKind(self.symbolTable.KindOf(varName)), 
            self.symbolTable.IndexOf(varName)
        )

    def compileDo(self):
        def isDo():
            return self.nextValueIs('do')
        if not isDo():
            return False

        self.advance('do')
        self.compileSubroutineCall()
        self.vmWriter.writePop('temp', 0)
        self.advance(';')

    def isSubroutineCall(self):
        self.tokenizer.advance()
        flag = self.nextValueIs(['(', '.'])
        self.tokenizer.back()
        return flag

    def compileSubroutineCall(self):
        if not self.isSubroutineCall():
            return False
        firstName = lastName = fullName = ''
        nLocals = 0 
        firstName = self.advance()
        if self.nextValueIs('.'):
            self.advance('.')
            lastName = self.advance()
            t = self.symbolTable.TypeOf(firstName)
            if t is None:
                fullName = firstName + "." + lastName;
            else:
                nLocals = 1
                self.vmWriter.writePush(
                    self.symbolTable.getSegmentByKind(self.symbolTable.KindOf(firstName)), 
                    self.symbolTable.IndexOf(firstName)
                )
                fullName = self.symbolTable.TypeOf(firstName) + "." + lastName
        else:  
            self.vmWriter.writePush('pointer', 0)
            nLocals += 1
            fullName = self.className + '.' + firstName
        self.advance('(')
        nLocals += self.compileExpressionList()
        self.vmWriter.writeCall(fullName, nLocals)
        self.advance(')')

    def compileExpressionList(self):
        counter = 0

        if not self.nextValueIs(')'):
            self.CompileExpression()
            counter += 1
            while self.nextValueIs(','):
                self.advance(',')
                self.CompileExpression()
                counter += 1
        return counter

    def compileReturn(self):
        def isReturn():
            return self.nextValueIs('return')
        if not isReturn(): return False
        self.advance('return')
        returnEmpty = True
        if not self.nextValueIs(';'):
            returnEmpty = False
            self.CompileExpression()
            
        if returnEmpty:
            self.vmWriter.writePush('constant', 0)
        self.vmWriter.writeReturn()
        self.advance(';')

    def CompileExpression(self):
        self.CompileTerm()
        while self.nextValueIs(self.OP):
            op = self.advance()
            self.CompileTerm()
    
            if op == '+':
                self.vmWriter.writerArithmetic('add')
            elif op == '-':
                self.vmWriter.writerArithmetic('sub')
            elif op == '*':
                self.vmWriter.writeCall('Math.multiply', 2)
            elif op == '/':
                self.vmWriter.writeCall('Math.divide', 2)
            elif op == '|':
                self.vmWriter.writerArithmetic('or')
            elif op == '&':
                self.vmWriter.writerArithmetic('and')
            elif op == '=':
                self.vmWriter.writerArithmetic('eq')
            elif op == '<':
                self.vmWriter.writerArithmetic('lt')
            elif op == '>':
                self.vmWriter.writerArithmetic('gt')

    def CompileTerm(self):
        if self.nextTokenTypeIs(self.tokenizer.INT_CONST):
            value = self.advance()
            self.vmWriter.writePush('constant', value)
        elif self.nextValueIs('('):
            self.advance('(') 
            self.CompileExpression()
            self.advance(')')
        elif self.nextTokenTypeIs(self.tokenizer.IDENTIFIER):
            # varName | varName '[' expression ']' | subroutineCall
            name = self.advance()
            if self.nextValueIs(['[']):
                pass
            elif self.nextValueIs(['(', '.']):
                self.tokenizer.back()
                self.compileSubroutineCall()
            else:
                self.vmWriter.writePush(
                    self.symbolTable.getSegmentByKind(self.symbolTable.KindOf(name)), 
                    self.symbolTable.IndexOf(name)
                )
        elif self.nextTokenTypeIs(self.tokenizer.KEYWORD):
            value = self.advance()
            if value == 'this':
                self.vmWriter.writePush('pointer', 0)
            elif value == 'true':
                self.vmWriter.writePush('constant', 0)
                self.vmWriter.writerArithmetic('not')
            elif value == 'false':
                self.vmWriter.writePush('constant', 0)
        elif self.nextValueIs(['-', '~']):
            op = self.advance()
            self.CompileTerm()
            if op == '-': 
                self.vmWriter.writerArithmetic('neg')
            elif op == '~': 
                self.vmWriter.writerArithmetic('not')
        else: 
            print('CompileTerm:: ', self.advance(), self.tokenizer.tokenType())