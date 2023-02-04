import sys, os
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter

def getFileList(name):
    if name.endswith('.jack'):
        return [name]
    else:
        files = os.listdir(os.path.abspath(name))
        return list(map(lambda e: f'{name}/{e}', files)) 

def getFileName(file_location, noPath = False):
    fname = file_location
    if noPath and file_location.find('/') >= 0:
        fname = "".join(file_location.split('/')[-1])

    if fname.endswith('.jack'):
        return fname.replace('.jack', '')
    else:
        return fname


file_location = sys.argv[1]

files = getFileList(file_location)

for filename in files:
    if filename.endswith('.jack'):
        compile = CompilationEngine(
            getFileName(filename), 
            JackTokenizer(filename), 
            VMWriter(getFileName(filename))
        )
        compile.CompileClass()