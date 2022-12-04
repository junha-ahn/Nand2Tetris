class symbolTable:
    ramAddr = 16
    def __init__(self):
        self.hashTable = {}        
        self.predefinedSymbols = ['SP','LCL','ARG','THIS','THAT','R0','R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','R11','R12','R13','R14','R15','SCREEN','KBD']
        self.symbolMemory = [0,1,2,3,4,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16384,24576]

        for i in range(len(self.predefinedSymbols)):
            self.hashTable[self.predefinedSymbols[i]] = self.symbolMemory[i]
        

    def addEntry(self,symbol,address):
        self.hashTable[symbol] = address
    

    def contains(self,symbol):
        if self.hashTable.get(symbol) != None:
            return True
        else:
            return False

    def GetAddress(self,symbol):
        return self.hashTable.get(symbol)
    
    def getNextRAMAddr(self):
        v = self.ramAddr
        self.ramAddr += 1
        return v

