import sys ,os
from modules import Parser,CodeWriter 

def getFileList(name):
    if name.endswith('.vm'):
        return [name]
    else:
        files = os.listdir(os.path.abspath(name))
        return list(map(lambda e: f'{name}/{e}', files)) 

def getFileName(file_location, noPath = False):
    fname = file_location
    if noPath and file_location.find('/') >= 0:
        fname = "".join(file_location.split('/')[-1])

    if fname.endswith('.vm'):
        return fname.replace('.vm', '')
    else:
        return fname


file_location = sys.argv[1]
files = getFileList(file_location)


codeWriter = CodeWriter.CodeWriter(getFileName(file_location))
if len(files) > 1: codeWriter.writerInit()

for filename in files:
    codeWriter.setFileName(getFileName(filename, True))
    
    parser = Parser.Parser(filename)

    while parser.hasMoreCommands():
        parser.advance()
        command_type = parser.commandType()

        if command_type == parser.C_ARITHEMTIC:
            codeWriter.writerArithmetic(parser.arg1())
        elif command_type == parser.C_PUSH:
            codeWriter.WritePushPop('push' , parser.arg1() , parser.arg2())
        elif command_type == parser.C_POP:
            codeWriter.WritePushPop('pop' , parser.arg1() , parser.arg2())
        elif command_type == parser.C_LABEL:
            codeWriter.writeLabel(parser.arg1())
        elif command_type == parser.C_GOTO:
            codeWriter.writeGoto(parser.arg1())
        elif command_type == parser.C_IF:
            codeWriter.writeIf(parser.arg1())
        elif command_type == parser.C_RETURN:
            codeWriter.writeReturn()
        elif command_type == parser.C_FUNCTION:
            codeWriter.writeFunction(parser.arg1(), parser.arg2())
        elif command_type == parser.C_CALL:
            codeWriter.writeCall(parser.arg1(), parser.arg2())

codeWriter.Close()





