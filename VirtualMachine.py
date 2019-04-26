"""
    + : 0,
    - : 1,
    * : 2,
    / : 3,
    = : 4,
"""
arrArithmeticOperators = [ 0, 1, 2, 3, 4 ]


"""
    > : 5,
    < : 6,
    <= : 7,
    >= : 8,
"""
arrRelationalOperators = [ 5, 6, 7, 8 ]

"""
    == : 9,
    != : 10,
    && : 11,
    || : 12,
    ! : 13
"""
arrLogicalOperators = [ 9, 10, 11, 12, 13 ]


"""
    GOTO : ,
    GOTOF : ,
    GOTOT : 
"""
arrJumps = []

instructionPointer = 0 # Apunta al siguiente quad a resolver
const_memory = {} # Recibe el diccionario de constantes de cuando se compila el código fuente


#############################
# COMIENZO LOGICA PARA MANEJO DE DIRECCIONES DE MEMORIA
#############################

# Determinar si una dirección de memoria pertenece a un rango global, local, temporal o constante
# No importa el tipo de dato de la dirección, solo con que esté dentro de los rangos anteriormente mencionados
# # Regresa el valor almacenado que representa la dirección de memoria
def getValueFromAddress( memoryAddress ):

    if memoryAddress >= gIntStart and memoryAddress <= gStringEnd: # Rango global
        return getValueFromAddressHelper( memoryAddress )
    elif memoryAddress >= lIntStart and memoryAddress <= lStringEnd: # Rango local
        return l_memory.getValueFromAddressHelper(memoryAddress)  # TODO: current memory context?
    elif memoryAddress >= tIntStart and memoryAddress <= tStringEnd: # Rango temporal
        #return getValueFromAddressHelper(
        #    memoryAddress
        #)  # TODO: how to know if temp from local vs global
    else:  # Rango de constantes
        return const_memory[ memoryAddress ]


# Determinar si una dirección de memoria pertenece a un rango global, local, temporal o constante
# Asignar un valor a esa dirección de memoria
def setValueToAddress( value, memoryAddress ):

    if memoryAddress >= gIntStart and memoryAddress <= gStringEnd:
        # Set GLOBAL variable address
        setValueToAddressHelper(value, memoryAddress)
    elif memoryAddress >= lIntStart and memoryAddress <= lStringEnd:
        # Set LOCAL variable address
        l_memory.setValueToAddressHelper(value, memoryAddress)  # TODO: current memory context?
    else:  # temp
        # Set TEMP variable address
        setValueToAddressHelper(
            value, memoryAddress
        )  # TODO: how to know if temp from local vs global


#############################
# FIN LOGICA PARA MANEJO DE DIRECCIONES DE MEMORIA
#############################


# Empezar proceso de leer quads del queue
# Esta es la función que se ejcuta primero
def readQuads( qQuads, const_mem ):

    global const_memory 
    global instructionPointer

    const_memory = const_mem
    instructionPointer = 0

    # Resolver quad por quad
    while instructionPointer < len( qQuads ):
        solveQuad( qQuads[ instructionPointer ] )
        instructionPointer = instructionPointer + 1


# Determinar cómo resolver el quad dependiendo de su operador
def solveQuad( quad ):

    global instructionPointer

    resultVal = -1 # Variable auxiliar para guardar resultado de una operación

    # Conseguir valores de la memoria
    leftOperand = getValueFromAddress(quad.operand1)
    rightOperand = getValueFromAddress(quad.operand2)


    # Realizar operación

    # Resolver operación aritmética
    if quad.token == token_to_code.get("+"):    # Add
        resultVal = leftOperand + rightOperand
    elif quad.token == token_to_code.get("-"):  # Subtract
        resultVal = leftOperand - rightOperand
    elif quad.token == token_to_code.get("*"):  # Multiply
        resultVal = leftOperand * rightOperand
    elif quad.token == token_to_code.get("/"):  # Divide
        if rightOperand == 0:
            imprimirError(??)
        resultVal = leftOperand / rightOperand
    elif quad.token == token_to_code.get("="):  # Assign
        # Conseguir valor desde la memoria
        resultVal = getValueFromAddress( quad.operand1 )
    # Resolver operación relacional
    elif quad.token == token_to_code.get(">="): # Mayor que
        resultVal = leftOperand >= rightOperand
    elif quad.token == token_to_code.get("<="): # Menor que
        resultVal = leftOperand <= rightOperand
    elif quad.token == token_to_code.get(">"): # Mayor
        resultVal = leftOperand > rightOperand
    elif quad.token == token_to_code.get("<"): # Menor
        resultVal = leftOperand < rightOperand
    # Resolver operación lógica
    if quad.token == token_to_code.get("equals"): # Es igual a 
        resultVal = leftOperand == rightOperand
    elif quad.token == token_to_code.get("notEquals"): # No es igual a
        resultVal = leftOperand != rightOperand
    elif quad.token == token_to_code.get("and"): # and
        resultVal = leftOperand && rightOperand 
    elif quad.token == token_to_code.get("or"): # or 
        resultVal = leftOperand || rightOperand
    elif quad.token == token_to_code.get("not"): # not 
        #resultVal =  !rightOperand
    # Resolver operación de saltos
    elif quad.token == token_to_code.get("GOTO"):
        # GOTO, -1, -1, destination
        # Change inst pointer to point to destination quad
        instructionPointer = quad.operand3 - 1
    elif quad.token == token_to_code.get("GOTOF"):
        # GOTOF, trigger, -1, destination
        # Get trigger (result of condition)
        trigger = getValueFromAddress(quad.operand1)
        # print("TRIGGER ", trigger)
        # Change inst = destination quad IF trigger is FALSE
        if not trigger:
            instructionPointer = quad.operand3 - 1
    elif quad.token == token_to_code.get("GOTOT"):
        # GOTOT, trigger, -1, destination
        # Get trigger (result of condition)
        trigger = getValueFromAddress(quad.operand1)
        # print("TRIGGER ", trigger)
        # Change inst = destination quad IF trigger is FALSE
        if trigger:
            instructionPointer = quad.operand3 - 1
    else:
        return

    # Guardar resultado en memoria
    setValueToAddress(resultVal, quad.operand3)



