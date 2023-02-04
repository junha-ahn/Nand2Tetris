class Writer:
    def __init__(self, file_name, isPrint = False):
        self.isPrint = isPrint
        if not isPrint:
            self.file = open(f'{file_name}' , 'w')
        pass

    def write(self, s):
        if self.isPrint:
            print(s)
        else:
            self.file.write(s + '\n')
    def writeTag(self, type, s):
        self.write(f"<{type}> {s} </{type}>")
        
    def close(self):
        if not self.isPrint:
            self.file.close()