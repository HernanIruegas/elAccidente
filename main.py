import sys
from parser import parser, yacc, qQuads, dicConstants, dicConstantsInverted
from VirtualMachine import readQuads

if __name__ == "__main__":

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, "r")
            data = f.read()
            f.close()
            yacc.parse(data, tracking=True)
            #print( dicConstantsInverted )
            readQuads( qQuads, dicConstantsInverted)
        except EOFError:
            print("EOFError")
    else:
        print("File missing")

        {4: {'Address': 13000, 'Type': 'int'}, 1: {'Address': 13001, 'Type': 'int'}, 2: {'Address': 13002, 'Type': 'int'}}
