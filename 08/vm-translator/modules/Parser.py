import os

class Parser:

    C_ARITHEMTIC = 'C_ARITHEMTIC'
    C_PUSH = 'C_PUSH'
    C_POP = 'C_POP'
    
    C_LABEL = 'C_LABEL'
    C_GOTO = 'C_GOTO'
    C_IF = 'C_IF'
    C_FUNCTION = 'C_FUNCTION'
    C_RETURN = 'C_RETURN'
    C_CALL = 'C_CALL'

    def __init__(self,file):
        #read file
        self.files = list()
        self.counter = -1
 
        with open(os.path.abspath(file),'r') as file:
            for f in file:
                if f.startswith("//") or f.startswith("\n"):
                    continue
                self.files.append(''.join(f.replace("\n","")).split())                

        
        self.file_length = len(self.files)
         
    def hasMoreCommands(self):
        if self.counter + 1 < self.file_length:
            return True 
        
        return False

    def advance(self):
        self.counter += 1

    def commandType(self):
        command = self.files[self.counter][0]
  
        if command in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return self.C_ARITHEMTIC
        elif command == 'push':
            return self.C_PUSH
        elif command == 'pop':
            return self.C_POP
        elif command == 'label':
            return self.C_LABEL
        elif command == 'goto':
            return self.C_GOTO
        elif command == 'if-goto':
            return self.C_IF
        elif command == 'function':
            return self.C_FUNCTION
        elif command == 'return':
            return self.C_RETURN
        elif command == 'call':
            return self.C_CALL
        else:
            print("(parser.py commandType method) error this command is not define  >>  ", command)
        

    def arg1(self):
        arg1 = self.files[self.counter]
        # print(f'result>>>{arg1}')
        if self.commandType() == self.C_ARITHEMTIC:
            return arg1[0] 
        elif self.commandType() != self.C_RETURN:
            return arg1[1]
        


    def arg2(self):
        arg2 = self.files[self.counter]
        
        if self.commandType() == self.C_PUSH:
            return arg2[2]
        elif self.commandType() == self.C_POP:
            return arg2[2]
        elif self.commandType() == self.C_FUNCTION:
            return arg2[2]
        elif self.commandType() == self.C_CALL:
            return arg2[2]


  
