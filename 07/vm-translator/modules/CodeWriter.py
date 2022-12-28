import os


class CodeWriter:
    
    C_ARITHEMTIC = 'C_ARITHEMTIC'
    C_PUSH = 'C_PUSH'
    C_POP = 'C_POP'


    ARGUMENT = 'argument'
    LOCAL = 'local'
    STATIC = 'static'
    CONSTANT = 'constant'
    THIS = 'this'
    THAT = 'that'
    POINTER = 'pointer'
    TEMP = 'temp'


    SEGMENT_MEMORY = {
        ARGUMENT:'ARG',
        LOCAL:'LCL',
        THIS:'THIS',
        THAT:'THAT',
        CONSTANT:'SP'
    }
 

    OPERATOR_SYMBOL = {
        '=':'JEQ',
        '>':'JGT',
        '<':'JLT'
    }


    def __init__(self , file):
        self.file_name = file
        self.file = open(f'{self.file_name}.asm' , 'w')
        self.jump_flag = 0
   
           
    def setFileName(self , filename):
        self.vmfilename = filename


    def _fileWrite(self, s):
        self.file.write(s + '\n')


    def writerArithmetic(self , command):

        if command == 'add':
            self._arithmeticBinary()
            self._fileWrite("M=M+D")

        elif command == 'sub':
            self._arithmeticBinary()
            self._fileWrite('M=M-D')

        elif command == 'and':
            self._arithmeticBinary()
            self._fileWrite('M=M&D')

        elif command == 'or':
            self._arithmeticBinary()
            self._fileWrite('M=M|D')  

        elif command == 'eq':
            self._arithmeticCompare('JNE')
            self.jump_flag+=1
            
        elif command == 'gt':
            self._arithmeticCompare('JLE')
            self.jump_flag+=1
            
        elif command == 'lt':
            self._arithmeticCompare('JGE') 
            self.jump_flag+=1    

        elif command == 'neg':
            self._fileWrite('D=0')
            self._fileWrite('@SP')
            self._fileWrite('A=M-1')
            self._fileWrite('M=D-M')
      
        elif command == 'not':
            self._fileWrite('@SP')
            self._fileWrite('A=M-1')
            self._fileWrite('M=!M')
        
            
    def WritePushPop(self , command , segment , index):

        if command == 'push':
            if segment == self.CONSTANT:
                self._fileWrite(f'@{index}')
                self._fileWrite('D=A')
                self._fileWrite('@SP')
                self._fileWrite('A=M')
                self._fileWrite('M=D')
                self._fileWrite('@SP')
                self._fileWrite('M=M+1')
                
            elif segment in [self.ARGUMENT, self.LOCAL, self.THIS, self.THAT]:
                self._push(self.SEGMENT_MEMORY[segment],index,False)
            
            elif segment == self.POINTER:

                if int(index) == 0:
                    self._push(self.SEGMENT_MEMORY[self.THIS],index,True)

                elif int(index) == 1:
                    self._push(self.SEGMENT_MEMORY[self.THAT],index,True)

            elif segment == self.TEMP:
                self._push('R5',int(index)+5,False)

            elif segment == self.STATIC:
                self._push(f'{self.vmfilename}.{index}',index,True)

        if command == 'pop':
        
            if segment in [self.ARGUMENT, self.LOCAL, self.THIS, self.THAT]:
                self._pop(self.SEGMENT_MEMORY[segment], index, False)

            elif segment == self.POINTER:
                if int(index) == 0:
                    self._pop(self.SEGMENT_MEMORY[self.THIS], index, True)
    
                elif int(index) == 1:
                    self._pop(self.SEGMENT_MEMORY[self.THAT], index, True)

                else:
                    print('error')

            elif segment == self.TEMP:
                self._pop("R5",int(index)+5,False)
            
            elif segment == self.STATIC:
                self._pop(f'{self.vmfilename}.{index}',index,True)
    
             
    def _arithmeticBinary(self):
        self._fileWrite('@SP')
        self._fileWrite('AM=M-1')
        self._fileWrite('D=M')
        self._fileWrite('A=A-1')


    def _arithmeticCompare(self, type):
        self._fileWrite('@SP')
        self._fileWrite('AM=M-1')
        self._fileWrite('D=M')
        self._fileWrite('A=A-1')
        self._fileWrite('D=M-D')
        self._fileWrite(f'@FALSE{self.jump_flag}')
        self._fileWrite(f'D;{type}')
        self._fileWrite('@SP')
        self._fileWrite('A=M-1')
        self._fileWrite('M=-1')
        self._fileWrite(f'@CONTINUE{self.jump_flag}')
        self._fileWrite('0;JMP')
        self._fileWrite(f'(FALSE{self.jump_flag})')
        self._fileWrite('@SP')
        self._fileWrite('A=M-1')
        self._fileWrite('M=0')
        self._fileWrite(f'(CONTINUE{self.jump_flag})')
 

    def _push(self,seg,index,isPointer):
        self._fileWrite(f'@{seg}')
        self._fileWrite('D=M')

        if not isPointer:
            self._fileWrite(f'@{index}')
            self._fileWrite('A=D+A')
            self._fileWrite('D=M')
            
        self._fileWrite('@SP')
        self._fileWrite('A=M')
        self._fileWrite('M=D')
        self._fileWrite('@SP')
        self._fileWrite('M=M+1')

    def _pop(self,seg,index,isPointer):
        self._fileWrite(f'@{seg}')
        
        if isPointer:
            self._fileWrite('D=A')
        else:
            self._fileWrite('D=M')
            self._fileWrite(f'@{index}')
            self._fileWrite('D=D+A')

        self._fileWrite('@R13')
        self._fileWrite('M=D')
        self._fileWrite('@SP')
        self._fileWrite('AM=M-1')
        self._fileWrite('D=M')
        self._fileWrite('@R13')
        self._fileWrite('A=M')
        self._fileWrite('M=D')

    def Close(self):
        self.file.close()