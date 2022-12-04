import re
import os

class Parser:
    L_COMMAND = "L_COMMAND"
    A_COMMAND = "A_COMMAND"
    C_COMMAND = "C_COMMAND"
    
    def __init__(self,file):
        #read file
        self.files = list()
        self.counter = -1
        
        with open(os.path.abspath(file),'r') as file:
            for f in file:
                s = f.replace(" ","")
                if s.find('//') != -1:
                    s = s[:s.find('//')]
    
                if len(s) == 0 or s.startswith(" ") or s.startswith('\n'):
                    continue
                else:
                    self.files.append(s.strip())
        
        self.file_length = len(self.files)

    def reset(self):
        self.counter = -1

    def hasMoreCommands(self):
        if self.counter + 1 < self.file_length:
            return True
        else:
            return False

    def advance(self):
        self.counter += 1

    def commandType(self):
        if self.files[self.counter].startswith('@'):
            return self.A_COMMAND
        elif self.files[self.counter].startswith('('):
            return self.L_COMMAND
        else:
            return self.C_COMMAND

    def symbol(self):
        return "".join(re.split("[^a-zA-Z|0-9]*",self.files[self.counter]))


    def comp(self):
        symbol = self.files[self.counter].replace(" ","")
        equel = symbol.find("=")
        colon = symbol.find(";")

        if equel != -1:
            return symbol[equel+1:]
     
        elif colon != -1:        
            return symbol[0:colon]
        else:
            return symbol
        

    def dest(self):
        symbol = self.files[self.counter].replace(" ","")
        equel = symbol.find("=")

        if equel != -1:
            return symbol[0:equel]
        else:
            return "null0"


    def jump(self):
        symbol = self.files[self.counter].replace(" ","")
        colon = symbol.find(";")
    
        if colon != -1:
            return symbol[colon+1:]
        else:
            return "null"
 
