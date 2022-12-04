class Code:
    def __init__(self):
        #dest 
        self.null0 = "000"
        self.M = "001"
        self.D = "010"
        self.MD = "011"
        self.A = "100"
        self.AM = "101"
        self.AD = "110"
        self.AMD = "111"
        
        #jump 
        self.null = "000"
        self.JGT = "001"
        self.JEQ = "010"
        self.JGE = "011"
        self.JLT = "100"
        self.JNE = "101"
        self.JLE = "110"
        self.JMP = "111"

     

        

       
    def dest(self,symbol):
        if symbol == "null0":
            return self.null0
        elif symbol == "M":
            return self.M
        elif symbol == "D":
            return self.D
        elif symbol == "MD":
            return self.MD
        elif symbol == "A":
            return self.A
        elif symbol == "AM":
            return self.AM
        elif symbol == "AD":
            return self.AD
        elif symbol == "AMD":
            return self.AMD

    def jump(self,symbol):
        if symbol == "null":
            return self.null
        elif symbol == "JGT":
            return self.JGT
        elif symbol == "JEQ":
            return self.JEQ
        elif symbol == "JGE":
            return self.JGE
        elif symbol == "JLT":
            return self.JLT
        elif symbol == "JNE":
            return self.JNE
        elif symbol == "JMP":
            return self.JMP
        elif symbol == "JLE":
            return self.JLE

    def comp(self,symbol):
        if symbol == "0":
            return "0101010"
        elif symbol == "1":
            return "0111111"
        elif symbol == "-1":
            return "0111010"
        elif symbol == "D":
            return "0001100"
        elif symbol == "A":
            return "0110000"
        elif symbol == "M":
            return "1110000"
        elif symbol == "!D":
            return "0001101"
        elif symbol == "!A":
            return "0110001"
        elif symbol == "!M":
            return "1110001"
        elif symbol == "-D":
            return "0001111"
        elif symbol == "-A":
            return "0110011"
        elif symbol == "-M":
            return "1110011"
        elif symbol == "D+1":
            return "0011111"
        elif symbol == "A+1":
            return "0110111"
        elif symbol == "M+1":
            return "1110111"
        elif symbol == "D-1":
            return "0001110"
        elif symbol == "A-1":
            return  "0110010"
        elif symbol == "M-1":
            return  "1110010"
        elif symbol == "D+A":
            return  "0000010"
        elif symbol == "D+M":
            return  "1000010"
        elif symbol == "D-A":
            return  "0010011"
        elif symbol == "D-M":
            return  "1010011"
        elif symbol == "A-D":
            return  "0000111"
        elif symbol == "M-D":
            return  "1000111"
        elif symbol == "D&A":
            return  "0000000"
        elif symbol == "D&M":
            return  "1000000"
        elif symbol == "D|A":
            return  "0010101"
        elif symbol == "D|M":
            return  "1010101"

 
