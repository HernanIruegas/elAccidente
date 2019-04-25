import ply.yacc as yacc
from lexer import lexer, tokens
from Stack import Stack
from SemanticCube import dicOperandIndexCube, semanticCube, dicOperatorIndexCube, dicReturnValuesCube

#############################
# VARIABLES GLOBALES
#############################

dicDirectorioFunciones = {} # "nombreFuncion" : { "Type": void/TYPE, "dicDirectorioVariables": {}, "ParamCounter": ..., "QuadCounter": ..., "TempCounter": ..., ParamTypes: [] }
# dicDirectorioVariables = "VarName" : { "Type": ..., "Value": ..., "Scope": ..., "Address": ...}

lastReadType = "" # Sirve para conocer el tipo de dato más recientemente leído ( de funciones y de variables )
currentFunction = "" # Sirve para conocer el nombre de la función más recientemente leida

sOperators = Stack() # Pila de operadores
sOperands = Stack() # Pila de operandos
sTypes = Stack() # Pila de tipos
sJumps = Stack() # Pila de saltos
qQuads = [] # Lista de quadruplos
qQuadRecursiveCalls = [] # Lista de cuadruplos de llamadas recursivas
iQuadCounter = 0 # Contador de cuadruplos, apunta al siguiente
iTemporalVariableCounter = 0 # Contador de variables temporales para los cuadruplos
iParametersCounter = 0 # Contador para saber cuántos parametros tiene una función (se usa cuando se lee la declaración de una función) y también sirve como indice para la lista de tipos ParamTypes de la función
dicConstants = {} # Sirve para almacenar las constantes del programa { "valorConstante" : memoryAddress }
dicConstantsInverted = {} # Lo mismo que dicConstants pero invertido para la máquina virtual { "memoryAddress" : valorConstante }
methodCall =  "" # Sirve para guardar el nombre de la función a la cual se quiere llamar en METHODCALL

#############################
# RANGOS DE MEMORIA
#############################

# Rangos para variables globales
index_gInt = 1000
gIntStart = 1000
gIntEnd = 1999
index_gFloat = 2000
gFloatStart = 2000
gFloatEnd = 2999
index_gBool = 3000
gBoolStart = 3000
gBoolEnd = 3999
index_gString = 4000
gStringStart = 4000
gStringEnd = 4999

# Rangos para variables locales
index_lInt = 5000
lIntStart = 5000
lIntEnd = 5999
index_lFloat = 6000
lFloatStart = 6000
lFloatEnd = 6999
index_lBool = 7000
lBoolStart = 7000
lBoolEnd = 7999
index_lString = 8000
lStringStart = 8000
lStringEnd = 8999

# Rangos para variables temporales
index_tInt = 9000
tIntStart = 9000
tIntEnd = 9999
index_tFloat = 10000
tFloatStart = 10000
tFloatEnd = 10999
index_tBool = 11000
tBoolStart = 11000
tBoolEnd = 11999
index_tString = 12000
tStringStart = 12000
tStringEnd = 12999

# Rangos para constantes
index_cInt = 13000
cIntStart = 13000
cIntEnd = 13999
index_cFloat = 14000
cFloatStart = 14000
cFloatEnd = 14999
index_cBool = 15000
cBoolStart = 15000
cBoolEnd = 15999
index_cString = 16000
cStringStart = 16000
cStringEnd = 16999


#############################
# REGLAS DE PARSER
#############################

def p_PROGRAM(p):
	"""
	PROGRAM : program void SAVE_TYPE globalFunc START_FUNCTION semicolon PROGRAM_A void SAVE_TYPE start START_FUNCTION BLOCK PRINTQUADS
	"""

def p_PROGRAM_A(p):
	"""
	PROGRAM_A : VARS PROGRAM_A
			| METHOD PROGRAM_B
			| empty
	"""

def p_PROGRAM_B(p):
	"""
	PROGRAM_B : METHOD PROGRAM_B
			| empty
	"""

def p_VARS(p):
	"""
	VARS : var VARS_A
	"""

def p_VARS_A(p):
	"""
	VARS_A : TYPE colon VARS_B semicolon VARS_C
	"""

def p_VARS_B(p):
	"""
	VARS_B : SIMPLE
		| LIST
	"""

def p_VARS_C(p):
	"""
	VARS_C : VARS_A
			| empty
	"""

def p_SIMPLE(p):
	"""
	SIMPLE : id SAVE_VAR SIMPLE_A
	"""

def p_SIMPLE_A(p):
	"""
	SIMPLE_A : comma SIMPLE
			| empty
	"""

def p_LIST(p):
	"""
	LIST : id lSqrBracket VARCONSTAUX rSqrBracket SAVE_ARRAY LIST_A
	"""

def p_LIST_A(p):
	"""
	LIST_A : comma LIST
		| empty
	"""

def p_EXPLOG(p):
	"""
	EXPLOG : EXPRESSION EXPLOG_A SOLVE_OPERATION_LOGIC
		| not EXPRESSION EXPLOG_A SOLVE_OPERATION_LOGIC
	"""
	#print("p_EXPLOG")

def p_EXPLOG_A(p):
	"""
	EXPLOG_A : and EXPLOG
		| or EXPLOG
		| empty
	"""
	#print("p_EXPLOG_A")

def p_EXPRESSION(p):
	"""
	EXPRESSION : EXP 
				| EXP EXPRESSION_A EXP SOLVE_OPERATION_RELATIONSHIP
	"""
	#print("EXPRESSION")

def p_EXPRESSION_A(p):
	"""
	EXPRESSION_A : greater PUSH_STACK_OPERATORS
				| lessThan PUSH_STACK_OPERATORS
				| greaterEquals PUSH_STACK_OPERATORS
				| lessThanEquals PUSH_STACK_OPERATORS
				| equals PUSH_STACK_OPERATORS
				| notEquals PUSH_STACK_OPERATORS
	"""

def p_EXP(p):
	"""
	EXP : TERM SOLVE_OPERATION_SUM_MINUS
		| TERM SOLVE_OPERATION_SUM_MINUS EXP_A 
	"""
	#print("EXP")

def p_EXP_A(p):
	"""
	EXP_A : plus PUSH_STACK_OPERATORS EXP
		| minus PUSH_STACK_OPERATORS EXP
	"""
	#print("EXP_A")

def p_TERM(p):
	"""
	TERM : FACTOR SOLVE_OPERATION_TIMES_DIVIDE
		| FACTOR SOLVE_OPERATION_TIMES_DIVIDE TERM_A 
	"""
	#print("TERM")

def p_TERM_A(p):
	"""
	TERM_A : times PUSH_STACK_OPERATORS TERM
			| divide PUSH_STACK_OPERATORS TERM
	"""
	#print("TERM_A")

def p_FACTOR(p):
	"""
	FACTOR : lParenthesis PUSH_STACK_OPERATORS EXPLOG rParenthesis POP_STACK_OPERATORS
			| VARCONSTAUX
	"""
	#print("FACTOR")

# Define numeros y accesos a indices de arreglos (sin string y boolean de VARCTE)
def p_VARCONSTAUX(p):
	"""
	VARCONSTAUX : id PUSH_STACK_OPERANDS ISLIST 
		| cte_i PUSH_STACK_OPERANDS_CONSTANT
		| cte_f PUSH_STACK_OPERANDS_CONSTANT
	"""
	#print("VARCONSTAUX")

def p_TYPE(p):
	"""
	TYPE : int SAVE_TYPE
		| float SAVE_TYPE
		| string SAVE_TYPE
		| bool SAVE_TYPE
	"""

def p_BLOCK(p):
	"""
	BLOCK : lCurlyBracket BLOCK_A rCurlyBracket
	"""

def p_BLOCK_A(p):
	"""
	BLOCK_A : STATEMENT BLOCK_A
			| empty
	"""

def p_STATEMENT(p):
	"""
	STATEMENT : ASSIGNMENT
			| CONDITION
			| WRITE
			| PRE_CONDITIONAL_LOOP
			| POST_CONDITIONAL_LOOP
			| METHODCALL
			| READ
			| STATMETHODS
			| RETURN 
	"""

def p_ASSIGNMENT(p):
	"""
	ASSIGNMENT : id PUSH_STACK_OPERANDS ISLIST assign PUSH_STACK_OPERATORS EXPLOG SOLVE_OPERATION_ASSIGNMENT semicolon 
	"""

def p_READ(p):
	"""
	READ : scan lParenthesis VARCTE READ_A rParenthesis
	"""

def p_READ_A(p):
	"""
	READ_A : comma
		| empty
	"""

def p_ISLIST(p):
	"""
	ISLIST : lSqrBracket EXP rSqrBracket
			| empty 
	"""

def p_TYPEMETHOD(p):
	"""
	TYPEMETHOD : TYPE
			| void SAVE_TYPE
	"""

def p_CONDITION(p):
	"""
	CONDITION : if lParenthesis EXPLOG rParenthesis GENERATE_GOTOF_CONDITIONAL BLOCK CONDITION_A SOLVE_OPERATION_CONDITIONAL
	"""

def p_CONDITION_A(p):
	"""
	CONDITION_A : else GENERATE_GOTO_CONDITIONAL BLOCK
				| empty
	"""

def p_WRITE(p):
	"""
	WRITE : print lParenthesis EXPRESSION GENERATE_QUAD_PRINT WRITE_A rParenthesis semicolon
	"""

def p_WRITE_A(p):
	"""
	WRITE_A : comma EXPRESSION GENERATE_QUAD_PRINT WRITE_A
		| empty
	"""

def p_VARCTE(p):
	"""
	VARCTE : id ISLIST 
		| cte_i 
		| cte_f 
		| cte_str 
		| BOOLEAN
	"""

def p_METHOD(p):
	"""
	METHOD : func TYPEMETHOD id START_FUNCTION lParenthesis METHOD_A SAVE_COUNTER_PARAM rParenthesis SAVE_COUNTER_QUAD BLOCK END_PROCEDURE
	"""

def p_METHOD_A(p):
	"""
	METHOD_A : PARAMS
			| empty		
	"""

def p_PARAMS(p):
	"""
	PARAMS : TYPE id SAVE_VAR SAVE_PARAM_TYPE INCREMENT_PARAM_COUNTER PARAMS_A 
	"""

def p_PARAMS_A(p):
	"""
	PARAMS_A : comma PARAMS
		| empty
	"""

def p_PRE_CONDITIONAL_LOOP(p):
	"""
	PRE_CONDITIONAL_LOOP : while PUSH_STACK_JUMPS lParenthesis EXPLOG rParenthesis GENERATE_GOTOF_CONDITIONAL BLOCK SOLVE_OPERATION_PRE_CONDITIONAL_LOOP
	"""

def p_POST_CONDITIONAL_LOOP(p):
	"""
	POST_CONDITIONAL_LOOP : do PUSH_STACK_JUMPS BLOCK while lParenthesis EXPLOG rParenthesis SOLVE_OPERATION_POST_CONDITIONAL_LOOP
	"""

def p_METHODCALL(p):
	"""
	METHODCALL : id VALIDATE_FUNCTION_NAME ERA lParenthesis EXP VALIDATE_PARAMETER METHODCALL_A rParenthesis semicolon VALIDATE_METHOD_CALL
	"""

def p_METHODCALL_A(p):
	"""
	METHODCALL_A : comma EXP
				| empty
	"""

def p_RETURN(p):
	"""
	RETURN : return EXPLOG semicolon
	"""

def p_BOOLEAN(p):
	"""
	BOOLEAN : FALSE
			| TRUE
	"""

def p_STATMETHODS(p):
	"""
	STATMETHODS : ORDINARY_LEAST_SQUARES
				| LASSO
				| RIDGE
				| K_MEANS
				| MINI_BATCH_MEANS
				| TIME_SERIES_SPLIT
				| MEAN_ABSOLUTE_ERROR
				| MEAN_SQUARED_ERROR
				| MEDIAN_ABSOLUTE_ERROR
				| MEAN
				| MODE
				| MEDIAN
				| PROBABILITY
				| FREQUENCY
				| VARIANCE
				| STANDARD_DEVIATION
				| SKEWNESS
				| KURTOSI
	"""

def p_ORDINARY_LEAST_SQUARES(p):
	"""
	ORDINARY_LEAST_SQUARES : ols lParenthesis id comma id comma BOOLEAN comma BOOLEAN comma VARCONSTAUX comma BOOLEAN rParenthesis semicolon
	"""

def p_LASSO(p):
	"""
	LASSO : las lParenthesis id comma id comma VARCONSTAUX comma BOOLEAN comma BOOLEAN comma VARCONSTAUX comma BOOLEAN comma BOOLEAN comma BOOLEAN comma VARCONSTAUX comma string comma float comma BOOLEAN rParenthesis semicolon
	"""

def p_RIDGE(p):
	"""
	RIDGE : rid lParenthesis id comma id comma VARCONSTAUX comma BOOLEAN comma BOOLEAN comma BOOLEAN comma VARCONSTAUX comma VARCONSTAUX comma string comma VARCONSTAUX rParenthesis semicolon
	"""

def p_K_MEANS(p):
	"""
	K_MEANS : kmeans lParenthesis VARCONSTAUX comma string comma VARCONSTAUX comma VARCONSTAUX comma VARCONSTAUX comma string comma VARCONSTAUX comma VARCONSTAUX comma BOOLEAN comma VARCONSTAUX comma string rParenthesis semicolon
	"""

def p_MINI_BATCH_MEANS(p):
	"""
	MINI_BATCH_MEANS : mbm lParenthesis VARCONSTAUX comma string comma VARCONSTAUX comma VARCONSTAUX comma BOOLEAN comma BOOLEAN comma VARCONSTAUX comma VARCONSTAUX comma VARCONSTAUX comma VARCONSTAUX comma VARCONSTAUX comma VARCONSTAUX rParenthesis semicolon 
	"""

def p_TIME_SERIES_SPLIT(p):
	"""
	TIME_SERIES_SPLIT : tseries lParenthesis VARCONSTAUX comma VARCONSTAUX rParenthesis semicolon 
	"""

def p_MEAN_ABSOLUTE_ERROR(p):
	"""
	MEAN_ABSOLUTE_ERROR : mean_abs_err lParenthesis id comma id rParenthesis semicolon
	"""

def p_MEAN_SQUARED_ERROR(p):
	"""
	MEAN_SQUARED_ERROR : mean_sqr_err lParenthesis id comma id rParenthesis semicolon 
	"""

def p_MEDIAN_ABSOLUTE_ERROR(p):
	"""
	MEDIAN_ABSOLUTE_ERROR : median_abs_err lParenthesis id comma id rParenthesis semicolon 
	"""

def p_MEAN(p):
	"""
	MEAN : mean lParenthesis id MEAN_A rParenthesis semicolon
	"""

def p_MEAN_A(p):
	"""
	MEAN_A : comma id MEAN_A
		| empty
	"""

def p_MODE(p):
	"""
	MODE : mode lParenthesis id MODE_A rParenthesis semicolon
	"""

def p_MODE_A(p):
	"""
	MODE_A : comma id MODE_A
		| empty
	"""

def p_MEDIAN(p):
	"""
	MEDIAN : median lParenthesis id MEDIAN_A rParenthesis semicolon
	"""

def p_MEDIAN_A(p):
	"""
	MEDIAN_A : comma id MEDIAN_A
		| empty
	"""

def p_PROBABILITY(p):
	"""
	PROBABILITY : prob lParenthesis id PROBABILITY_A rParenthesis semicolon
	"""

def p_PROBABILITY_A(p):
	"""
	PROBABILITY_A : comma id PROBABILITY_A
		| empty
	"""

def p_FREQUENCY(p):
	"""
	FREQUENCY : freq lParenthesis id FREQUENCY_A rParenthesis semicolon
	"""

def p_FREQUENCY_A(p):
	"""
	FREQUENCY_A : comma id FREQUENCY_A
		| empty
	"""

def p_VARIANCE(p):
	"""
	VARIANCE : variance lParenthesis id VARIANCE_A rParenthesis semicolon
	"""

def p_VARIANCE_A(p):
	"""
	VARIANCE_A : comma id VARIANCE_A
		| empty
	"""

def p_STANDARD_DEVIATION(p):
	"""
	STANDARD_DEVIATION : stddev lParenthesis id STANDARD_DEVIATION_A rParenthesis semicolon
	"""

def p_STANDARD_DEVIATION_A(p):
	"""
	STANDARD_DEVIATION_A : comma id STANDARD_DEVIATION_A
		| empty
	"""

def p_SKEWNESS(p):
	"""
	SKEWNESS : skew lParenthesis id SKEWNESS_A rParenthesis semicolon
	"""

def p_SKEWNESS_A(p):
	"""
	SKEWNESS_A : comma id SKEWNESS_A
		| empty
	"""

def p_KURTOSI(p):
	"""
	KURTOSI : kurt  lParenthesis id KURTOSI_A rParenthesis semicolon
	"""

def p_KURTOSI_A(p):
	"""
	KURTOSI_A : comma id KURTOSI_A
		| empty
	"""

def p_empty(p):
    """
    empty :
    """

def p_error(p):
    print("Syntax error at '%s'" % p)

    exit(1)


# Función manejadora de errores
def imprimirError(error):
	if error == 0:
		print( "Error: Variable Duplicada" )
	elif error == 1:
		print( "Error: Arreglo Duplicado" )
	elif error == 2:
		print( "Error: Operación invalida" )
	elif error == 3:
		print( "Error: Variable sin declarar" )
	elif error == 4:
		print( "Error: Type-mismatch" )
	elif error == 5:
		print( "Error: Función duplicada" )
	elif error == 6:
		print( "Error: Función no declarada previamente" )
	elif error == 7:
		print( "Error: Número de argumentos no equivale a número de parametros" )

	exit(1)


#############################
# ACCIONES SEMANTICAS 
#############################

# Guarda la función en el directorio de funciones
def p_START_FUNCTION(p):
	"""
	START_FUNCTION : empty
	"""
	global currentFunction 
	global dicDirectorioFunciones

	currentFunction = p[ -1 ]

	# Validar que la función no esté previamente declarada
	if currentFunction not in dicDirectorioFunciones:
		dicDirectorioFunciones[ currentFunction ]  = { "Type": lastReadType, "dicDirectorioVariables": {}, "ParamCounter": 0, "QuadCounter": 0, "TempCounter": 0, "ParamTypes": [ ] }
	else:
		imprimirError( 5 )


# Guarda el último tipo de variable leido en una variable global lastReadType
def p_SAVE_TYPE(p):
	"""
	SAVE_TYPE : empty
	"""
	global lastReadType
	print(p[-1])
	print(currentFunction)
	lastReadType = p[-1]
	

# Guardar nombre de variable, tipo, scope y dirección de memoria en directorio de variables de la función
def p_SAVE_VAR(p):
	"""
	SAVE_VAR : empty
	"""
	global dicDirectorioFunciones
	global currentFunction
	global lastReadType

	# Validar que variable leida no esté previamente declarada
	if p[-1] in dicDirectorioFunciones[currentFunction]["dicDirectorioVariables"]:
		imprimirError(0)
	else:

		currentScope = getScope()
		
		#print("currentScope")
		#print(currentScope)
		#print(p[-1])
		#print( "currentFunction" )
		#print( currentFunction )
		dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[-1] ] = {"Type": lastReadType, "Value": "", "Scope": currentScope, "Address": "" }

		# Definir espacio de memoria y scope de variable
		address = set_address( p[-1] )

		# Actualizar campo de memory address en la variable
		dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[-1] ][ "Address" ] = address


# Todavia no se debe hacer nada de arreglos (esperar a elda)
def p_SAVE_ARRAY(p): 
	"""
	SAVE_ARRAY : empty
	"""
	global dicDirectorioFunciones
	global currentFunction
	global lastReadType

	# Validar que arreglo leido no esté previamente declarado
	if p[-4] in dicDirectorioFunciones[currentFunction]["dicDirectorioVariables"]:
	    imprimirError(1)
	else:
	    dicDirectorioFunciones[currentFunction]["dicDirectorioVariables"][ p[-4] ] = {"Type": lastReadType, "Value": p[-2]}


#############################
# ACCIONES SEMANTICAS DE FUNCIONES
#############################


# Guarda el tipo de parametro en la lista de tipos de parametros de la función
# Incrementa el contador de parametros
def p_INCREMENT_PARAM_COUNTER(p):
	"""
	INCREMENT_PARAM_COUNTER : empty
	"""
	global iParametersCounter

	iParametersCounter =  iParametersCounter + 1


# Guardar el número de parametros de la función
# Hacer reset del contador de parametros para una función
def p_SAVE_COUNTER_PARAM(p):
	"""
	SAVE_COUNTER_PARAM : empty
	"""
	global iParametersCounter

	dicDirectorioFunciones[currentFunction][ "ParamCounter" ] = iParametersCounter
	iParametersCounter = 0


# Guardar contador de quadruplos en propiedades de la función
# Sirve como breadcrumb para cuando se llame a la función desde otro lado del programa, para saber donde empieza su ejecución
def p_SAVE_COUNTER_QUAD(p):
	"""
	SAVE_COUNTER_QUAD : empty
	"""

	global iQuadCounter
	global currentFunction
	global dicDirectorioFunciones

	dicDirectorioFunciones[currentFunction][ "QuadCounter" ] = iQuadCounter


# Acciones en la terminación de una función
# Reset de contadores para rangos de memoria
def p_END_PROCEDURE(p):
	"""
	END_PROCEDURE : empty
	"""
	global qQuads
	global iQuadCounter

	quad = [ "ENDPROC", "", "", "" ]
	qQuads.append( quad )
	iQuadCounter = iQuadCounter + 1

	reset_local_vars()


# Guardar el tipo de dato del parametro leido de la función
def p_SAVE_PARAM_TYPE(p):
	"""
	SAVE_PARAM_TYPE : empty
	"""
	global dicDirectorioFunciones
	global currentFunction
	global lastReadType

	print( "WAAAAAAAAAA" )
	print(currentFunction)
	dicDirectorioFunciones[ currentFunction ][ "ParamTypes" ].append( lastReadType )


# Valida que el nombre de la función a la que se está llamando haya sido previamente declarada
def p_VALIDATE_FUNCTION_NAME(p):
	"""
	VALIDATE_FUNCTION_NAME : empty
	"""
	global dicDirectorioFunciones
	global methodCall

	if p[ -1 ] not in dicDirectorioFunciones:
		imprimirError( 6 )
	else:
		methodCall = p[ -1 ]


# Generar accion ERA
# Manejar recursividad en funciones
def p_ERA(p):
    """
    ERA : empty
    """
    global qQuads;
    global iQuadCounter;
    global currentFunction;
    global qQuadRecursiveCalls;
    global dicDirectorioFunciones

    #print( "p[ -2 ]" )
    #print( p[ -2 ] )
    #print( "ParamCounter")
    #print( dicDirectorioFunciones[ p[ -2 ] ][ "ParamCounter" ] )
    #print( "TempCounter" )
    #print( dicDirectorioFunciones[ p[ -2 ] ][ "TempCounter" ] )

    # p[ -2 ] =  nombre de la función a la que se está llamando
    quad = [ "ERA", p[ -2 ], dicDirectorioFunciones[ p[ -2 ] ][ "ParamCounter" ], dicDirectorioFunciones[ p[ -2 ] ][ "TempCounter" ] ]

    # Validar si es una llamada recursiva
    if(currentFunction == p[ -2 ]):
        qQuadRecursiveCalls.append( iQuadCounter );

    qQuads.append(quad);
    iQuadCounter = iQuadCounter + 1;


# Se lee el argumento y se valida contra la lista de tipos de parametros de la función a la que se quiere llamar
def p_VALIDATE_PARAMETER(p):
    """
    VALIDATE_PARAMETER : empty
    """
    global sOperands
    global sTypes
    global iParametersCounter
    global qQuads
    global iQuadCounter
    global dicDirectorioFunciones
    global methodCall

    argument = sOperands.pop()
    argumentType = sTypes.pop()

    print( "iParametersCounter")
    print( iParametersCounter )
    print( "paramtypes" )
    print( currentFunction)
    print( dicDirectorioFunciones[ methodCall ][ "ParamTypes" ] )

    if argumentType != dicDirectorioFunciones[ methodCall ][ "ParamTypes" ][ iParametersCounter ]:
    	imprimirError( 4 )
    else:
    	iParametersCounter = iParametersCounter + 1
    	quad = [ "PARAMETER", argument, '', iParametersCounter ]
    	iQuadCounter = iQuadCounter + 1
    	qQuads.append( quad )


# Se valida que el número de argumentos coincida con el número de parametros de la función
# Se manejan los valores de retorno de las funciones
def p_VALIDATE_METHOD_CALL(p):
	"""
	VALIDATE_METHOD_CALL : empty
	"""
	global iParametersCounter
	global dicDirectorioFunciones
	global qQuads
	global iQuadCounter

	if iParametersCounter != dicDirectorioFunciones[ methodCall ][ "ParamCounter" ]:
		imprimirError( 7 )
	else:
		quad = [ "GOSUB", currentFunction, '', "dirección de memoria pendiente" ]
		qQuads.append( quad )
		iQuadCounter = iQuadCounter + 1

	iParametersCounter = 0

	# Falta manejar cosas para cuando la función tiene valor de retorno
	# empieza en línea 1711 en apollo


#############################
# ACCIONES SEMANTICAS DE EXPRESIONES
#############################

# Insertar operando en stack de operandos y su tipo en stack de tipos
# Necesitas consultar el tipo de la variable con el diccionario de variables de la función
# Si no se encuentra en la función actual, tienes que buscar en la función global
def p_PUSH_STACK_OPERANDS(p):
	"""
	PUSH_STACK_OPERANDS : empty
	"""
	global sOperands
	global dicDirectorioFunciones

	# Validar que la variable leida haya sido previamente declarada, que exista en el diccionario de variables de la función
	if p[-1] in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ]:

		# Conseguir la dirección de memoria de variable previamente guardada en directorio
		address = dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -1 ] ][ "Address" ] 

		sOperands.push( address )
		print(str(sOperands.top())+ " PUSH_STACK_OPERANDS")
		print(p[-1])
		sTypes.push( dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -1 ] ][ "Type" ] )
	elif p[-1] in dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ]:

		# Conseguir la dirección de memoria de variable previamente guardada en directorio
		address = dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ][ p[ -1 ] ][ "Address" ] 
		sOperands.push( address )
		print(str(sOperands.top())+ " PUSH_STACK_OPERANDS")
		print(p[-1])
		sTypes.push( dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ][ p[-1] ][ "Type" ] )
	else:
		imprimirError(3)


# Funciona igual que PUSH_STACK_OPERANDS, solo que aquí manejamos constantes
# Se agrega la constante al diccionario global de constantes
def p_PUSH_STACK_OPERANDS_CONSTANT(p):
	"""
	PUSH_STACK_OPERANDS_CONSTANT : empty
	"""

	global sOperands
	global dicConstants
	global dicConstantsInverted

	constantType = ""
	# Si la constante no existe, se debe asignar una dirección de memoria
	# También se debe agregar a la pila de operandos y a la pila de tipos la info correspondiente
	if p[ -1 ] not in dicConstants:

		# conseguir el tipo de dato de la constante
		if type( p[ -1 ] ) is int:
			constantType = 'int'
		elif type( p[ -1 ] ) is float:
			constantType = 'float'

		print( "constantType" )
		print( constantType )
		print( p[ -1 ] )

		address = set_address_const( constantType )
		dicConstants[ p[ -1 ] ] = { "Address" : address, "Type": constantType }
		dicConstantsInverted[ address ] = p[ -1 ]
		sOperands.push( address )
		sTypes.push( constantType )
	else:
		sOperands.push( dicConstants[ p[ -1 ] ][ "Address" ] ) # Se hace push del memory address
		sTypes.push( dicConstants[ p[ -1 ] ][ "Type" ] )


# Insertar operador en stack de operadores
def p_PUSH_STACK_OPERATORS(p):
	"""
	PUSH_STACK_OPERATORS : empty
	"""
	global sOperators
	sOperators.push( p[-1] )
	print(str(sOperators.top())+ " PUSH_STACK_OPERATORS")
	

# Se ejecuta cuando se topa con un closing parenthesis ')'
# Genera cuadruplos hasta encontrar el opening parenthesis '('
def p_POP_STACK_OPERATORS(p):
	"""
	POP_STACK_OPERATORS : empty
	"""

	# Generar cuadruplos con los operadores pendientes
	# Hasta encontrarte con el fondo falso
	while( sOperators.top() != '(' ):
		solveOperationHelper()

	sOperators.pop() # Eliminar el fondo falso de la pila de operadores


# Código compartido para función de SOLVE_OPERATION
def solveOperationHelper():

	global sOperands
	global sOperators
	global sTypes
	global qQuads
	global iQuadCounter
	global iTemporalVariableCounter # para contar vars temporales creadas (solucion por mientras)
	global dicDirectorioFunciones
	global currentFunction

	rightOperand = sOperands.pop()
	#print("rightOperand")
	#print(rightOperand)
	rightType = sTypes.pop()

	leftOperand = sOperands.pop()
	#print("leftOperand")
	#print(leftOperand)
	leftType = sTypes.pop()

	operator = sOperators.pop()
	#print("operator")
	#print(operator)

	# Esta es una variable temporal
	resultType = semanticCube[ dicOperandIndexCube[ leftType ] ][ dicOperandIndexCube[ rightType ] ][ dicOperatorIndexCube[ operator ] ]

	if resultType != 0: # 0 = error en subo semantico
		result = 'result' # es un valor dummy por mientras, solo para ver que se generen los quads

		currentScope = getScope()

		dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ "t" + str(iTemporalVariableCounter) ] = {"Type": dicReturnValuesCube[ resultType ], "Value": "", "Scope": currentScope, "Address": "" }

		# Definir espacio de memoria de variable temporal
		address = set_address_temp( dicReturnValuesCube[ resultType ] )

		# Actualizar campo de memory address en la variable
		dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ "t" + str(iTemporalVariableCounter) ][ "Address" ] = address

		iTemporalVariableCounter = iTemporalVariableCounter + 1
		quad = [ operator, leftOperand, rightOperand, address ]
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
		sOperands.push( address )
		print(str(sOperands.top())+ " solveOperationHelper")
		sTypes.push( dicReturnValuesCube[ resultType ] )
	else:
		imprimirError(2)


# Función helper para determinar el scope de una variable/constante
def getScope():

	global currentFunction

	if currentFunction == "globalFunc":
		return "global"
	else:
		return "local"


# Resuelve operación de operadores '+' y '-'
# Se consulta el cubo semántico para saber si la operación es valida
def p_SOLVE_OPERATION_SUM_MINUS(p):
	"""
	SOLVE_OPERATION_SUM_MINUS : empty
	"""
	#print("+ || -")
	global sOperators

	if sOperators.size() > 0:
		if sOperators.top() == '+' or sOperators.top() == '-':
			solveOperationHelper()


# Resuelve operación de operadores '*' y '/'
# Se consulta el cubo semántico para saber si la operación es valida
def p_SOLVE_OPERATION_TIMES_DIVIDE(p):
	"""
	SOLVE_OPERATION_TIMES_DIVIDE : empty
	"""
	#print("* || /")
	global sOperators

	if sOperators.size() > 0:
		if sOperators.top() == '*' or sOperators.top() == '/':
			solveOperationHelper()


# Resuelve operación de operadores relacionales
# Se consulta el cubo semántico para saber si la operación es valida
def p_SOLVE_OPERATION_RELATIONSHIP(p):
	"""
	SOLVE_OPERATION_RELATIONSHIP : empty
	"""
	global sOperators

	if sOperators.size() > 0:
		if sOperators.top() == '>' or sOperators.top() == '<' or sOperators.top() == '>=' or sOperators.top() == '<=' or sOperators.top() == '==' or sOperators.top() == '!=':
			solveOperationHelper()


# Resuelve operación de operadores lógicos
# Se consulta el cubo semántico para saber si la operación es valida
def p_SOLVE_OPERATION_LOGIC(p):
	"""
	SOLVE_OPERATION_LOGIC : empty
	"""
	global sOperators

	if sOperators.size() > 0:
		if sOperators.top() == 'and' or sOperators.top() == 'or' or sOperators.top() == 'not':
			solveOperationHelper()


# Genera cuadruplo para la asignación
def solveOperationHelperAssignment():
	global sOperands
	global sOperators
	global sTypes
	global qQuads
	global iQuadCounter

	rightOperand = sOperands.pop()
	rightType = sTypes.pop()

	leftOperand = sOperands.pop()
	leftType = sTypes.pop()

	operator = sOperators.pop()

	resultType = semanticCube[ dicOperandIndexCube[ leftType ] ][ dicOperandIndexCube[ rightType ] ][ dicOperatorIndexCube[ operator ] ]

	if resultType != 0: # 0 = error en subo semantico
		#result <- AVAIL.next() No sabemos que es pero viene en la hoja
		#result = 'result' # es un valor dummy por mientras, solo para ver que se generen los quads
		quad = [ operator, rightOperand, '', leftOperand ]
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
		#sOperands.push( result + str(iQuadCounter) )
		#print(str(sOperands.top())+ " solveOperationHelper")
		#print("sTypes: " + str(resultType) )
		#sTypes.push( dicReturnValuesCube[ resultType ] )
	else:
		imprimirError(2)


# Indica que se tiene que generar cuadruplo para una asignación
# Utiliza otra función helper porque su cuadruplo es distinto al que genera la función de SOLVE_OPERATION
# El cuadruplo de la asignación solo debe tener 2 espacios llenos, no 4 como el de las operaciones
def p_SOLVE_OPERATION_ASSIGNMENT(p):
	"""
	SOLVE_OPERATION_ASSIGNMENT : empty
	"""
	global sOperators

	if sOperators.size() > 0:
		if sOperators.top() == '=':
			solveOperationHelperAssignment()


# Resuelve cuadruplo con salto pendiente
def fill( end ):
	global iQuadCounter
	global qQuads

	aux = qQuads[ end ] # Cuadruplo con salto pendiente
	aux[ 3 ] = iQuadCounter # Llenar cuadruplo con el siguiente cuadruplo a ejecutar
	qQuads[ end ] = aux # Reemplazar breadcrumb por cuadruplo con salto a fin de ciclo


#############################
# ACCIONES SEMANTICAS DE ESTATUTOS DE DECISIÓN
#############################

# Genera cuadruplo con salto pendiente después de haber leido un if condicional
def p_GENERATE_GOTOF_CONDITIONAL(p):
	"""
	GENERATE_GOTOF_CONDITIONAL : empty
	"""

	global sTypes
	global sOperands
	global sJumps
	global iQuadCounter
	global qQuads

	expType = sTypes.pop()

	if expType == 'bool':
		result = sOperands.pop()

		quad = [ 'GotoF', result, '', '' ]
		print("iQuadCounter_goto_F")
		print(iQuadCounter)
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
		sOperands.push( result )
		sJumps.push( iQuadCounter - 1 )
		print(str(sOperands.top()) +" solveOperationHelper")
	else:
		imprimirError(4)


# Indica el fin de un if condicional y resuelve su cuadruplo con el salto pendiente
def p_SOLVE_OPERATION_CONDITIONAL(p):
	"""
	SOLVE_OPERATION_CONDITIONAL : empty
	"""
	global sJumps

	end = sJumps.pop()
	fill( end )


# Indica el salto que tiene que hacer la condición en caso de que el bloque verdadero se cumpla (para que no entre al else)
def p_GENERATE_GOTO_CONDITIONAL(p):
	"""
	GENERATE_GOTO_CONDITIONAL : empty
	"""

	global sJumps
	global iQuadCounter
	global qQuads

	quad = [ 'GOTO', '', '', '' ]
	iQuadCounter = iQuadCounter + 1
	qQuads.append( quad )


	false = sJumps.pop()
	sJumps.push( iQuadCounter - 1 )
	fill( false )


# Inserta en la pila de saltos el cuadruplo breadcrumb para regresar a evaluar la expresión 
# El contador debe apuntar al cuadruplo donde se evalua la expresión del while
def p_PUSH_STACK_JUMPS(p):
	"""
	PUSH_STACK_JUMPS : empty
	"""
	global sJumps
	global iQuadCounter

	sJumps.push( iQuadCounter )


#############################
# ACCIONES SEMANTICAS DE CICLOS
#############################

# Resuelve cuadruplos con saltos pendientes para el while
# Resuelve los saltos de regreso a la expresión y el salto que indica el final del loop
def p_SOLVE_OPERATION_PRE_CONDITIONAL_LOOP(p):
	"""
	SOLVE_OPERATION_PRE_CONDITIONAL_LOOP : empty
	"""

	global sJumps
	global iQuadCounter
	global qQuads

	end = sJumps.pop()
	print("end")
	print(end)
	returnTo = sJumps.pop()
	print("returnTo")
	print(returnTo)

	quad = [ 'GOTO', '', '', returnTo ] 
	iQuadCounter = iQuadCounter + 1
	print("iQuadCounter")
	print(iQuadCounter)
	qQuads.append( quad )

	fill( end )


# Resuelve cuadruplo con salto pendiente para el do while
# Resuelve el salto de regreso a la ejecución de los statements del do while (en caso de que sea verdadera la expresión)
def p_SOLVE_OPERATION_POST_CONDITIONAL_LOOP(p):
	"""
	SOLVE_OPERATION_POST_CONDITIONAL_LOOP : empty
	"""
	global sJumps
	global sOperands
	global iQuadCounter
	global qQuads

	result = sOperands.pop()
	returnTo = sJumps.pop()

	quad = [ 'GOTOT', result, '', returnTo ] 
	iQuadCounter = iQuadCounter + 1
	qQuads.append( quad )


#############################
# ACCIONES SEMANTICAS GENERALES PARA VISUALIZACIÓN Y GENERACIÓN DE QUADRUPLOS
#############################

# Genera le cuadruplo para los prints
# Utiliza a la pila de operandos para obtener el resultado de la expresión que va a imprimir el print
def p_GENERATE_QUAD_PRINT(p):
	"""
	GENERATE_QUAD_PRINT : empty
	"""

	global qQuads
	global iQuadCounter
	global sOperands

	result = sOperands.pop()

	quad = [ 'PRINT', '', '', result ] 
	iQuadCounter = iQuadCounter + 1
	qQuads.append( quad )


# Helper para saber los cuadruplos que se generan
def p_PRINTQUADS(p):
	"""
	PRINTQUADS : empty
	"""

	global qQuads
	cont = 0
	for i in qQuads:
		print( str(cont) + ": " + str(i) )
		cont = cont + 1;


#############################
# ACCIONES MEMORIA
#############################


# Asignar memoria a variable
# Se busca primero en el directorio de variables de la función global y si no está entonces se confirma que es una variable local
# Regresa la dirección de memoria asignada a la variable
def set_address( varName ):

	global currentFunction

	if varName in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ] and currentFunction != "globalFunc": # Es una variable local
		return set_address_local( dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ varName ][ "Type" ] ) # Le pasamos el tipo de la variable
	else: # Es una variable global
		return set_address_global( dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ][ varName ][ "Type" ] ) # Le pasamos el tipo de la variable


# Asignar memoria a variable global
# Incrementa el contador del rango para la memoria global
def set_address_global( varType ):

	global index_gInt
	global index_gFloat
	global index_gBool
	global index_gString

	assigned_address = None

	if varType == "int":
		assigned_address = index_gInt
		index_gInt += 1
	elif varType == "float":
		assigned_address = index_gFloat
		index_gFloat += 1
	elif varType == "bool":
		assigned_address = index_gBool
		index_gBool += 1
	elif varType == "string":
		assigned_address = index_gString
		index_gString += 1


	print("assigned_address")
	print(assigned_address)
	return assigned_address


# Asignar memoria a variable local
# Incrementa el contador del rango para la memoria local
def set_address_local( varType ):

	global index_lInt
	global index_lFloat
	global index_lBool
	global index_lString

	assigned_address = None

	if varType == "int":
		assigned_address = index_lInt
		index_lInt += 1
	elif varType == "float":
		assigned_address = index_lFloat
		index_lFloat += 1
	elif varType == "bool":
		assigned_address = index_lBool
		index_lBool += 1
	elif varType == "string":
		assigned_address = index_lString
		index_lString += 1

	print("assigned_address")
	print(assigned_address)
	return assigned_address


# Asignar memoria a variable temporal
# Incrementa el contador del rango para la memoria temporal
def set_address_temp( varType ):

	global index_tInt
	global index_tFloat
	global index_tBool
	global index_tString

	assigned_address = None

	if varType == "int":
		assigned_address = index_tInt
		index_tInt += 1
	elif varType == "float":
		assigned_address = index_tFloat
		index_tFloat += 1
	elif varType == "bool":
		assigned_address = index_tBool
		index_tBool += 1
	elif varType == "string":
		assigned_address = index_tString
		index_tString += 1

	print("assigned_address")
	print(assigned_address)
	return assigned_address


# Asignar memoria a constante
# Incrementa el contador del rango para la memoria de constantes
def set_address_const( varType ):

	global index_cInt
	global index_cFloat
	global index_cBool
	global index_cString

	assigned_address = None

	if varType == "int":
		assigned_address = index_cInt
		index_cInt += 1
	elif varType == "float":
		assigned_address = index_cFloat
		index_cFloat += 1
	elif varType == "bool":
		assigned_address = index_cBool
		index_cBool += 1
	elif varType == "string":
		assigned_address = index_cString
		index_cString += 1

	print("assigned_address")
	print(assigned_address)
	return assigned_address


# Reset a los contadores de los rangos de las memorias 
# Cada función tiene su propio rango de memoria local
def reset_local_vars():

	global index_lInt
	global index_lFloat
	global index_lBool
	global index_lString
	global index_tInt
	global index_tFloat
	global index_tBool
	global index_tString

	index_lInt = 5000
	index_lFloat = 6000
	index_lBool = 7000
	index_lString = 8000
	index_tInt = 9000
	index_tFloat = 10000
	index_tBool = 11000
	index_tString = 12000


parser = yacc.yacc()




