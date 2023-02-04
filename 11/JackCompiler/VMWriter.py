from Writer import Writer

class VMWriter:
    def __init__(self, filename):
        self.writer = Writer(f'{filename}.vm', False)

    def writePush(self, segment, index):
        self.writer.write(f'push {segment} {index}')

    def writePop(self , segment, index):
        self.writer.write(f'pop {segment} {index}')

    def writerArithmetic(self, command):
        self.writer.write(command)

    def writeLabel(self , label):
        self.writer.write(f'label {label}')

    def writeGoto(self,label):
        self.writer.write(f'goto {label}')

    def writeIf(self, label):
        self.writer.write(f'if-goto {label}')

    def writeCall(self , name , nArgs):
        self.writer.write(f'call {name} {nArgs}')

    def writeFunction(self , name, nLocals):
        self.writer.write(f'function {name} {nLocals}')

    def writeReturn(self):
        self.writer.write('return')
    
    def close(self):
        self.writer.close()