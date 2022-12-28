import os

class Parser:

    C_ARITHEMTIC = 'C_ARITHEMTIC'
    C_PUSH = 'C_PUSH'
    C_POP = 'C_POP'

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
        else:
            print("(parser.py commandType method) error this command is not define  >>  ", command)
        

    def arg1(self):
        arg1 = self.files[self.counter]
        

        if self.commandType() == self.C_ARITHEMTIC:
            return arg1[0] 
        elif self.commandType() == self.C_PUSH:
            return arg1[1]
        elif self.commandType() == self.C_POP:
            return arg1[1]
         
    


    def arg2(self):
        arg2 = self.files[self.counter]
        
        if self.commandType() == self.C_PUSH:
            return arg2[2]
        elif self.commandType() == self.C_POP:
            return arg2[2]


  
