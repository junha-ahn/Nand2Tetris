import sys
from modules import code,parser,symbolTable 

file_location = sys.argv[1]

code = code.Code()
parser = parser.Parser(file_location)
symbolTable = symbolTable.symbolTable()

def append(*args):
    s = ""
    for v in args:
        s += str(v)
    print(s)

def toBinary(s):
    bs = format(int(s), 'b')
    return ("0" * 15)[:(15 - len(bs))] + format(int(s), 'b')

pc = 0
while(parser.hasMoreCommands()): # PASE 1
    parser.advance()
    symbol_type = parser.commandType()
    if symbol_type != parser.L_COMMAND: 
        pc += 1
        continue
    symbolTable.addEntry(parser.symbol(), pc)

parser.reset()
 
while(parser.hasMoreCommands()): # PASE 2
    parser.advance()
    symbol_type = parser.commandType()
    
    #print('>>',parser.files[parser.counter])

    if symbol_type == parser.A_COMMAND:
        if symbolTable.contains(parser.symbol()):
            append(
                "0",
                toBinary(symbolTable.GetAddress(parser.symbol()))
            )
        else:
            if parser.symbol().isnumeric():
                append("0", toBinary(parser.symbol()))
            else:
                symbolTable.addEntry(
                    parser.symbol(), 
                    symbolTable.getNextRAMAddr()
                )
                append(
                    "0",
                    toBinary(symbolTable.GetAddress(parser.symbol()))
                )

    elif symbol_type == parser.C_COMMAND:
        append(
            "111",
            code.comp(parser.comp()),
            code.dest(parser.dest()),
            code.jump(parser.jump())
        )

    
