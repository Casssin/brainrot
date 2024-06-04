# keeps track of code and outputs the code into c
class Emitter:
    def __init__(self, fullPath) -> None:
        self.fullPath = fullPath
        self.header = ""
        self.code = ""
        self.ender = ""
    
    def emit(self, code: str) -> None:
        self.code += code
    
    def emitLine(self, code: str) -> None:
        self.code += code + '\n'
    
    def headerLine(self, code: str) -> None:
        self.header += code + '\n'

    def enderLine(self, code: str) -> None:
        self.ender += code + '\n'
    
    def writeFile(self):
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code + self.ender) 