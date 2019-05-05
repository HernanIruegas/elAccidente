from RuntimeMemory import RuntimeMemory
from Stack import Stack
from parser import imprimirError

instructionPointer = 0 # Apunta al siguiente quad a resolver
dicGlobalConstMemory = {} # Recibe el diccionario de constantes resultado de cuando se compila el código fuente
sMemories = Stack()
gMemory = RuntimeMemory( "global", -1 )
sMemories.push( gMemory )
currentFunctionName = "default"

#############################
# COMIENZO LOGICA PARA MANEJO DE DIRECCIONES DE MEMORIA
#############################

# Determinar si una dirección de memoria pertenece a un rango global, local, temporal o constante
# No importa el tipo de dato de la dirección, solo con que esté dentro de los rangos anteriormente mencionados
# Regresa el valor almacenado que representa la dirección de memoria
def getValueFromAddress( memoryAddress ):

    global sMemories

    print("memoryAddress")
    print(memoryAddress)
    if memoryAddress >= gMemory.gIntStart and memoryAddress <= gMemory.gStringEnd: # Rango global
        return gMemory.getValueFromAddressHelper( memoryAddress )
    elif memoryAddress >= sMemories.top().lIntStart and memoryAddress <= sMemories.top().lStringEnd: # Rango local
        return sMemories.top().getValueFromAddressHelper( memoryAddress ) 
    elif memoryAddress >= sMemories.top().tIntStart and memoryAddress <= sMemories.top().tStringEnd: 
        return sMemories.top().getValueFromAddressHelper( memoryAddress )  
    else:  # Rango de constantes
        return dicGlobalConstMemory[ memoryAddress ][ "Value" ] 


# Determinar si una dirección de memoria pertenece a un rango global, local, temporal o constante
# Asignar un valor a esa dirección de memoria
def setValueToAddress( value, memoryAddress ):
    global sMemories

    if memoryAddress >= gMemory.gIntStart and memoryAddress <= gMemory.gStringEnd:
        gMemory.setValueToAddressHelper( value, memoryAddress )
    elif memoryAddress >= sMemories.top().lIntStart and memoryAddress <= sMemories.top().lStringEnd: 
        sMemories.top().setValueToAddressHelper( value, memoryAddress ) 
    elif memoryAddress >= sMemories.top().tIntStart and memoryAddress <= sMemories.top().tStringEnd:
        sMemories.top().setValueToAddressHelper( value, memoryAddress )


#############################
# FIN LOGICA PARA MANEJO DE DIRECCIONES DE MEMORIA
#############################


# Empezar proceso de leer quads del queue
# Esta es la función que se ejcuta primero en el main.py
def readQuads( qQuads, globalConstMemory ):

    global dicGlobalConstMemory, instructionPointer

    dicGlobalConstMemory = globalConstMemory
    instructionPointer = 0

    # Resolver quad por quad
    while instructionPointer < len( qQuads ):
        solveQuad( qQuads[ instructionPointer ], qQuads )
        instructionPointer = instructionPointer + 1

    print(gMemory.intMemory)
    print(gMemory.floatMemory)
    print(gMemory.boolMemory)
    print(gMemory.strMemory)
    print(gMemory.tempMemory)


# Determinar cómo resolver el quad dependiendo de su operador
def solveQuad( quad, qQuads):

    global instructionPointer, currentFunctionName

    #print("instructionPointer")
    #print(instructionPointer)
    print( quad[ 0 ] )


    # Lo hago primero para que cualquier variable esté inicializada antes de ir a conseguir su valor
    if quad[ 0 ] == "=":

        if type( quad[ 1 ] ) is not int:
            # Guardar resultado en memoria
            setValueToAddress( currentFunctionName, quad[ 3 ] )
            return
        # Conseguir valor desde la memoria
        resultVal = getValueFromAddress( quad[ 1 ] )
        # Guardar resultado en memoria
        setValueToAddress( resultVal, quad[ 3 ] )
        return
    # Resolver operación de saltos
    elif quad[ 0 ] == "GOTO":
        # GOTO, "", "", destination
        # Hacer que instructionPointer apunte a un nuevo cuadruplo
        instructionPointer = quad[ 3 ] - 1
        return
    elif quad[ 0 ] == "GOTOF":
        # GOTOF, trigger, -1, destination
        # Get trigger (result of condition)
        trigger = getValueFromAddress( quad[ 1 ] )
        print("trigger")
        print(trigger)
        if not trigger:
            instructionPointer = quad[ 3 ] - 1
            print("instructionPointer")
            print(instructionPointer)
        return
    elif quad[ 0 ] == "GOTOT":
        # GOTOT, trigger, -1, destination
        # Get trigger (result of condition)
        trigger = getValueFromAddress(quad[ 1 ])
        if trigger:
            instructionPointer = quad[ 3 ] - 1
        return
    elif quad[ 0 ] == "ERA":
        memory = RuntimeMemory( "local", -1 )
        sMemories.push( memory )
        return
    elif quad[ 0 ] == "RET":
        if sMemories.top().scope == "global":
            instructionPointer = len( qQuads ) - 1
            return
        currentFunctionName = quad[ 3 ]
        instructionPointer = sMemories.top().returnQuad - 1
        sMemories.pop()
        return
    elif quad[ 0 ] == "ENDPROC":
        if( sMemories.top().scope != "global" ):
            instructionPointer = sMemories.top().returnQuad - 1
            sMemories.pop()
        return
    elif quad[ 0 ] == "GOSUB":
        sMemories.top().returnQuad = instructionPointer + 1
        instructionPointer = quad[ 3 ] - 1
        return 
    elif quad[ 0 ] == "PARAMETER":
        return
    elif quad[ 0 ] == "PRINT":
        # Conseguir valor desde la memoria
        resultVal = getValueFromAddress( quad[ 3 ] )
        print("PRINT THIS")
        print( resultVal )
        return

    

    # Conseguir valores de la memoria
    leftOperand = getValueFromAddress( quad[ 1 ] )
    rightOperand = getValueFromAddress( quad[ 2 ] )


    # Realizar operación

    resultVal = -1 # Variable auxiliar para guardar resultado de una operación
    # Resolver operación aritmética
    if quad[ 0 ] == "+":    
        resultVal = leftOperand + rightOperand
    elif quad[ 0 ] == "-":  
        resultVal = leftOperand - rightOperand
    elif quad[ 0 ] == "*":  
        resultVal = leftOperand * rightOperand
    elif quad[ 0 ] == "/":
        if rightOperand == 0:
            imprimirError( 9 )
        resultVal = leftOperand / rightOperand
    # Resolver operación relacional
    elif quad[ 0 ] == ">=": 
        resultVal = leftOperand >= rightOperand
    elif quad[ 0 ] == "<=": 
        resultVal = leftOperand <= rightOperand
    elif quad[ 0 ] == ">": 
        resultVal = leftOperand > rightOperand
    elif quad[ 0 ] == "<": 
        resultVal = leftOperand < rightOperand
    # Resolver operación lógica
    elif quad[ 0 ] == "==": 
        resultVal = leftOperand == rightOperand
    elif quad[ 0 ] == "!=": 
        resultVal = leftOperand != rightOperand
    elif quad[ 0 ] == "and": 
        resultVal = leftOperand and rightOperand 
    elif quad[ 0 ] == "or":  
        resultVal = leftOperand or rightOperand
    elif quad[ 0 ] == "!": 
        print("!") 
        #resultVal =  !rightOperand # TODO
    else:
        return

    # Guardar resultado en memoria
    setValueToAddress( resultVal, quad[ 3 ] )



