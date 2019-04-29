###### que falta? 
# 1) Manejar contextos locales
# 2) modifcar codigo de getValueFromAddress y setValueToAddress para que manejen el objeto de memoria local y global...tiene que ir antes de acceder a las variables de los rangos de memoria
# TODO'S

from RuntimeMemory import RuntimeMemory
from tokenAndCodeConverter import tokenToCode, codeToToken

instructionPointer = 0 # Apunta al siguiente quad a resolver
dicGlobalConstMemory = {} # Recibe el diccionario de constantes resultado de cuando se compila el código fuente
gMemory = RuntimeMemory( "global" )


#############################
# COMIENZO LOGICA PARA MANEJO DE DIRECCIONES DE MEMORIA
#############################

# Determinar si una dirección de memoria pertenece a un rango global, local, temporal o constante
# No importa el tipo de dato de la dirección, solo con que esté dentro de los rangos anteriormente mencionados
# # Regresa el valor almacenado que representa la dirección de memoria
def getValueFromAddress( memoryAddress ):

    print("memoryAddress")
    print(memoryAddress)
    if memoryAddress >= gMemory.gIntStart and memoryAddress <= gMemory.gStringEnd: # Rango global
        return gMemory.getValueFromAddressHelper( memoryAddress )
    elif memoryAddress >= gMemory.lIntStart and memoryAddress <= gMemory.lStringEnd: # Rango local
        print("local")
        #return l_memory.getValueFromAddressHelper(memoryAddress)  # TODO: current memory context?
    elif memoryAddress >= gMemory.tIntStart and memoryAddress <= gMemory.tStringEnd: 
        print("temporal")
        print(memoryAddress)
        # Rango temporal
        #return getValueFromAddressHelper(
        #    memoryAddress
        #)  # TODO: how to know if temp from local vs global
        
    else:  # Rango de constantes
        print( "getValueFromAddress")
        print( dicGlobalConstMemory[ memoryAddress ][ "Value" ]  )
        return dicGlobalConstMemory[ memoryAddress ][ "Value" ] 


# Determinar si una dirección de memoria pertenece a un rango global, local, temporal o constante
# Asignar un valor a esa dirección de memoria
def setValueToAddress( value, memoryAddress ):

    if memoryAddress >= gMemory.gIntStart and memoryAddress <= gMemory.gStringEnd:
        # Set GLOBAL variable address
        gMemory.setValueToAddressHelper( value, memoryAddress )
    elif memoryAddress >= gMemory.lIntStart and memoryAddress <= gMemory.lStringEnd:
        print(value)
        # Set LOCAL variable address
        #l_memory.gMemory.setValueToAddressHelper(value, memoryAddress)  # TODO: current memory context?
    else:  # temp
        # Set TEMP variable address
        gMemory.setValueToAddressHelper(
            value, memoryAddress
        )  # TODO: how to know if temp from local vs global


#############################
# FIN LOGICA PARA MANEJO DE DIRECCIONES DE MEMORIA
#############################


# Empezar proceso de leer quads del queue
# Esta es la función que se ejcuta primero
def readQuads( qQuads, globalConstMemory ):

    global dicGlobalConstMemory 
    global instructionPointer

    dicGlobalConstMemory = globalConstMemory
    instructionPointer = 0

    # Resolver quad por quad
    while instructionPointer < len( qQuads ):
        solveQuad( qQuads[ instructionPointer ] )
        instructionPointer = instructionPointer + 1

    print(gMemory.intMemory)
    print(gMemory.floatMemory)
    print(gMemory.boolMemory)
    print(gMemory.strMemory)
    print(gMemory.tempMemory)


# quad = token operand1 operand2 operand3 
# Determinar cómo resolver el quad dependiendo de su operador
def solveQuad( quad ):

    global instructionPointer

    if quad[ 0 ] == "=":#tokenToCode.get("="):  # Assign
        # Conseguir valor desde la memoria
        resultVal = getValueFromAddress( quad[ 1 ] )
        # Guardar resultado en memoria
        setValueToAddress(resultVal, quad[ 3 ])
        return

    resultVal = -1 # Variable auxiliar para guardar resultado de una operación

    # Conseguir valores de la memoria
    leftOperand = getValueFromAddress( quad[ 1 ] )
    rightOperand = getValueFromAddress( quad[ 2 ] )


    # Realizar operación

    # Resolver operación aritmética
    if quad[ 0 ] == tokenToCode.get("+"):    # Add
        resultVal = leftOperand + rightOperand
    elif quad[ 0 ] == tokenToCode.get("-"):  # Subtract
        resultVal = leftOperand - rightOperand
    elif quad[ 0 ] == tokenToCode.get("*"):  # Multiply
        resultVal = leftOperand * rightOperand
    elif quad[ 0 ] == tokenToCode.get("/"):  # Divide
        if rightOperand == 0:
            #imprimirError(??) # TODO
            print("imprimirError")
        resultVal = leftOperand / rightOperand
    # Resolver operación relacional
    elif quad[ 0 ] == tokenToCode.get(">="): # Mayor que
        resultVal = leftOperand >= rightOperand
    elif quad[ 0 ] == tokenToCode.get("<="): # Menor que
        resultVal = leftOperand <= rightOperand
    elif quad[ 0 ] == tokenToCode.get(">"): # Mayor
        resultVal = leftOperand > rightOperand
    elif quad[ 0 ] == tokenToCode.get("<"): # Menor
        resultVal = leftOperand < rightOperand
    # Resolver operación lógica
    if quad[ 0 ] == tokenToCode.get("=="): # equals 
        resultVal = leftOperand == rightOperand
    elif quad[ 0 ] == tokenToCode.get("!="): # different
        resultVal = leftOperand != rightOperand
    elif quad[ 0 ] == tokenToCode.get("&&"): # and
        resultVal = leftOperand and rightOperand 
    elif quad[ 0 ] == tokenToCode.get("||"): # or 
        resultVal = leftOperand or rightOperand
    elif quad[ 0 ] == tokenToCode.get("!"): # not
        print("!") 
        #resultVal =  !rightOperand # TODO
    # Resolver operación de saltos
    elif quad[ 0 ] == tokenToCode.get("GOTO"):
        # GOTO, -1, -1, destination
        # Change inst pointer to point to destination quad
        instructionPointer = quad[ 3 ] - 1
    elif quad[ 0 ] == tokenToCode.get("GOTOF"):
        # GOTOF, trigger, -1, destination
        # Get trigger (result of condition)
        trigger = getValueFromAddress(quad[ 1 ])
        # print("TRIGGER ", trigger)
        # Change inst = destination quad IF trigger is FALSE
        if not trigger:
            instructionPointer = quad[ 3 ] - 1
    elif quad[ 0 ] == tokenToCode.get("GOTOT"):
        # GOTOT, trigger, -1, destination
        # Get trigger (result of condition)
        trigger = getValueFromAddress(quad[ 1 ])
        # print("TRIGGER ", trigger)
        # Change inst = destination quad IF trigger is FALSE
        if trigger:
            instructionPointer = quad[ 3 ] - 1
    else:
        return

    # Guardar resultado en memoria
    setValueToAddress(resultVal, quad[ 3 ])



