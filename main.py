import sys
from parser import parser, yacc, qQuads, dicConstants, dicConstantsInverted, dicDirectorioFunciones
from VirtualMachine import readQuads

if __name__ == "__main__":

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, "r")
            data = f.read()
            f.close()
            yacc.parse(data, tracking=True)
            # print("dicConstantsInverted")
            # print( dicConstantsInverted )
            #print("dicDirectorioFunciones")
            #print( dicDirectorioFunciones )
            # Se pasa el queue de quads y el diccionario de todas las constantes encontradas en el codigo fuente
            readQuads( qQuads, dicConstantsInverted, dicConstants ) 
        except EOFError:
            print("EOFError")
    else:
        print("File missing")
