from RuntimeMemory import RuntimeMemory
from Stack import Stack
from parser import imprimirError

instructionPointer = 0 # Apunta al siguiente quad a resolver
dicGlobalConstMemory = {} # Recibe el diccionario de constantes invertidas resultado de cuando se compila el código fuente
dicConstants = {}
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

    #print("memoryAddress")
    #print(memoryAddress)
    if memoryAddress >= gMemory.gIntStart and memoryAddress <= gMemory.gStringEnd: # Rango global
        return gMemory.getValueFromAddressHelper( memoryAddress )
    elif memoryAddress >= sMemories.top().lIntStart and memoryAddress <= sMemories.top().lStringEnd: # Rango local
        return sMemories.top().getValueFromAddressHelper( memoryAddress ) 
    elif memoryAddress >= sMemories.top().tIntStart and memoryAddress <= sMemories.top().tStringEnd:
        return sMemories.top().getValueFromAddressHelper( memoryAddress )
    elif memoryAddress >= 500000:
        return sMemories.top().getValueFromAddressHelper( sMemories.top().getValueFromAddressHelper( memoryAddress - 500000 ) )
    else:  # Rango de constantes
        return dicGlobalConstMemory[ memoryAddress ][ "Value" ] 


# Determinar si una dirección de memoria pertenece a un rango global, local, temporal o constante
# Asignar un valor a esa dirección de memoria
def setValueToAddress( value, memoryAddress ):
    global sMemories

    if memoryAddress >= gMemory.gIntStart and memoryAddress <= gMemory.gStringEnd: # Rango global
        gMemory.setValueToAddressHelper( value, memoryAddress )
    elif memoryAddress >= sMemories.top().lIntStart and memoryAddress <= sMemories.top().lStringEnd: # Rango local
        sMemories.top().setValueToAddressHelper( value, memoryAddress ) 
    elif memoryAddress >= sMemories.top().tIntStart and memoryAddress <= sMemories.top().tStringEnd:
        sMemories.top().setValueToAddressHelper( value, memoryAddress )
    elif memoryAddress >= 500000:
        aux = sMemories.top().getValueFromAddressHelper( memoryAddress - 500000 )
        sMemories.top().setValueToAddressHelper( value, aux )



#############################
# FIN LOGICA PARA MANEJO DE DIRECCIONES DE MEMORIA
#############################


# Empezar proceso de leer quads del queue
# Esta es la función que se ejcuta primero en el main.py
def readQuads( qQuads, globalConstMemory, dicConstantsAux ):

    global dicGlobalConstMemory, instructionPointer, dicConstants

    dicGlobalConstMemory = globalConstMemory
    dicConstants = dicConstantsAux
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

    global instructionPointer, currentFunctionName, dicConstants, dicGlobalConstMemory
    print( quad[ 0 ] )

    # Se hace el assign primero para que cualquier variable esté inicializada antes de ir a conseguir su valor (para cuestiones de operaciones de expresiones)
    if quad[ 0 ] == "=":
        # Validar si recibo el nombre de una función y no un memory address
        # En caso de recibir el nombre de la función, significa que tengo que asignarle lo que regresa esa función a una variable global
        if type( quad[ 1 ] ) is not int:
            setValueToAddress( currentFunctionName, quad[ 3 ] )
            return
        # Conseguir valor desde la memoria
        # Para el caso de variables inicializadas por default, se inicializan con constantes ya existentes en el diccionario de constantes
        resultVal = getValueFromAddress( quad[ 1 ] )
        #print("assign")
        #print(resultVal)
        # Asignar la constante default a la variable inicializada por default
        setValueToAddress( resultVal, quad[ 3 ] )
        return
    # Resolver operación de saltos
    elif quad[ 0 ] == "GOTO":
        # GOTO, "", "", destination
        # Hacer que instructionPointer apunte a un nuevo cuadruplo
        # Se hace el -1 porque despues de asignar instructionPointer se regresa a función readQuads y se incrementa instructionPointer + 1
        instructionPointer = quad[ 3 ] - 1
        return
    elif quad[ 0 ] == "GOTOF":
        # GOTOF, condition, "", destination
        condition = getValueFromAddress( quad[ 1 ] )
        if not condition:
            instructionPointer = quad[ 3 ] - 1
        return
    elif quad[ 0 ] == "GOTOT":
        # GOTOT, condition, "", destination
        condition = getValueFromAddress(quad[ 1 ])
        if condition:
            instructionPointer = quad[ 3 ] - 1
        return
    elif quad[ 0 ] == "ERA":
        # Crear nueva instancia de memoria y hacer push al stack de memorias
        memory = RuntimeMemory( "local", -1 )
        sMemories.push( memory )
        return
    elif quad[ 0 ] == "RET":
        # Validar si la única memoria que queda en el stack es la global
        # En este caso y toparse con un return, se debe apuntar instructionPointer al final del programa
        if sMemories.top().scope == "global":
            instructionPointer = len( qQuads ) - 1
            return

        # Guardar en variable global lo que la función debe de retornar
        resultVal = getValueFromAddress( quad[ 3 ] )
        currentFunctionName = resultVal

        # Actualizar instructionPointer al siguiente cuadruplo que viene despues de haber hecho la llamada a la función
        instructionPointer = sMemories.top().returnQuad - 1
        # Quitar la memoria del stack (ya se termino de trabajar con ella)
        sMemories.pop()
        return
    elif quad[ 0 ] == "ENDPROC":
        if( sMemories.top().scope != "global" ):
            # Actualizar instructionPointer al siguiente cuadruplo que viene despues de haber hecho la llamada a la función
            instructionPointer = sMemories.top().returnQuad - 1
            # Quitar la memoria del stack (ya se termino de trabajar con ella)
            sMemories.pop()
        return
    elif quad[ 0 ] == "GOSUB":
        # Poner un recordatorio a stack nuevamente creado de que cuadruplo se debe ejecutar, una vez que el contexto actual termine de ejecutarse y haga pop del stack
        sMemories.top().returnQuad = instructionPointer + 1
        # Ejecutar nuevo contexto de memoria
        instructionPointer = quad[ 3 ] - 1
        return 
    elif quad[ 0 ] == "PARAMETER":
        # 'PARAMETER', argument, '', parameter
        resultVal = getValueFromAddress( quad[ 1 ] )
        setValueToAddress( resultVal, quad[ 3 ] )
        return
    elif quad[ 0 ] == "PRINT":
        resultVal = getValueFromAddress( quad[ 3 ] )
        #print(quad[ 3 ])
        print("PRINT THIS")
        print( resultVal )
        return
    elif quad[ 0 ] == "VER":
        # Validar que indice esté dentro de rangos de arreglo
        upperLimit = getValueFromAddress( quad[ 3 ] )
        index = getValueFromAddress( quad[ 1 ] )
        if index >= 0 and index <= upperLimit:
            return True
        imprimirError( 10 )

    
    #print("quad[ 1 ]")
    #print(quad[ 1 ])
    #print("quad[ 2 ]")
    #print(quad[ 2 ])

    # Conseguir valores de la memoria
    leftOperand = getValueFromAddress( quad[ 1 ] )
    rightOperand = getValueFromAddress( quad[ 2 ] )


    # Realizar operación

    resultVal = -1 # Variable auxiliar para guardar resultado de una operación
    # Resolver operación aritmética
    if quad[ 0 ] == "+":    
        resultVal = leftOperand + rightOperand
        #print("leftOperand")
        #print(leftOperand)
        #print("rightOperand")
        #print(rightOperand)
        #print(resultVal)        

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
        print("leftOperand")
        print(leftOperand)
        print("rightOperand")
        print(rightOperand)
        print("resultVal")
        print(resultVal)  
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

    #if quad[ 0 ] == "+":
        #print("after")
        #print(quad[ 3 ] )
        #print( getValueFromAddress( quad[ 3 ] ) )
