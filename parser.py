import ply.yacc as yacc
from lexer import lexer, tokens
from Stack import Stack
from SemanticCube import dicOperandIndexCube, semanticCube, dicOperatorIndexCube, dicReturnValuesCube

#############################
# VARIABLES GLOBALES
#############################

dicDirectorioFunciones = {} # "nombreFuncion" : { "Type": void/TYPE, "dicDirectorioVariables": {}, "ParamCounter": ..., "QuadCounter": ..., "TempCounter": ..., "ParamTypes": [], "Parameters": [] }
# dicDirectorioVariables = "VarName" : { "Type": ..., "Value": ..., "Scope": ..., "Address": ..., "Dimensiones": [ {}, ... ] }

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
dicConstants = {} # { "Address" : address, "Type": constantType } Sirve para almacenar las constantes del programa { "valorConstante" : memoryAddress }
dicConstantsInverted = {} # { "Value" : p[ -1 ], "Type": constantType } Lo mismo que dicConstants pero invertido para la máquina virtual { "memoryAddress" : valorConstante }
methodCall =  "" # Sirve para guardar el nombre de la función a la cual se quiere llamar en METHODCALL
varWithDimensions = "" # Sirve para guardar el id de la variable dimensionada que se está declarando
varDimensionadaLastRead = "" # Sirve para guardar el id de la variable dimensionada que se está leyendo (queriendo acceder a una casilla)
initialValuesForVars = { "int": 0, "float": 0.0, "string": '""', "bool": "False" }
dicArrayBaseAddressHelper = {} # { baseMemoryAddressArray : memoryAddressConstant }

#############################
# RANGOS DE MEMORIA
#############################

# Rangos para variables globales
gIntIndex = 1000
gIntStart = 1000
gIntEnd = 1999
gFloatIndex = 2000
gFloatStart = 2000
gFloatEnd = 2999
gBoolIndex = 3000
gBoolStart = 3000
gBoolEnd = 3999
gStringIndex = 4000
gStringStart = 4000
gStringEnd = 4999

# Rangos para variables locales
lIntIndex = 5000
lIntStart = 5000
lIntEnd = 5999
lFloatIndex = 6000
lFloatStart = 6000
lFloatEnd = 6999
lBoolIndex = 7000
lBoolStart = 7000
lBoolEnd = 7999
lStringIndex = 8000
lStringStart = 8000
lStringEnd = 8999

# Rangos para variables temporales
tIntIndex = 9000
tIntStart = 9000
tIntEnd = 9999
tFloatIndex = 10000
tFloatStart = 10000
tFloatEnd = 10999
tBoolIndex = 11000
tBoolStart = 11000
tBoolEnd = 11999
tStringIndex = 12000
tStringStart = 12000
tStringEnd = 12999

# Rangos para constantes
cIntIndex = 13000
cIntStart = 13000
cIntEnd = 13999
cFloatIndex = 14000
cFloatStart = 14000
cFloatEnd = 14999
cBoolIndex = 15000
cBoolStart = 15000
cBoolEnd = 15999
cStringIndex = 16000
cStringStart = 16000
cStringEnd = 16999


#############################
# REGLAS DE PARSER
#############################

def p_PROGRAM(p):
	"""
	PROGRAM : program void SAVE_TYPE globalFunc START_FUNCTION semicolon PROGRAM_A void SAVE_TYPE start START_FUNCTION FILL_GOTO_MAIN BLOCK END_PROCEDURE PRINTQUADS
	"""


def p_GENERATE_GOTO_MAIN(p):
	"""
	GENERATE_GOTO_MAIN : empty
	"""
	global qQuads, iQuadCounter, sJumps

	quad = [ 'GOTO', '', '', '' ]
	iQuadCounter = iQuadCounter + 1
	qQuads.append( quad )
	sJumps.push( iQuadCounter - 1 )

# Hace lo mismo que p_SOLVE_OPERATION_CONDITIONAL (solo para mantener lógica separada)
def p_FILL_GOTO_MAIN(p):
	"""
	FILL_GOTO_MAIN : empty
	"""
	global sJumps

	end = sJumps.pop()
	fill( end )
	


def p_PROGRAM_A(p):
	"""
	PROGRAM_A : VARS PROGRAM_A
				| GENERATE_GOTO_MAIN PROGRAM_B
	"""

def p_PROGRAM_B(p):
	"""
	PROGRAM_B : METHOD PROGRAM_B
				| empty
	"""




def p_VARS(p):
	"""
	VARS : var TYPE colon VARS_A semicolon VARS_B
	"""

def p_VARS_A(p):
	"""
	VARS_A : id assign VARCTE_AUX_VARS SIMPLE
			| id SAVE_VAR SIMPLE
			| id VALIDATE_NAME_ARRAY lSqrBracket cte_i ACUMULATE_R rSqrBracket LIST CALCULATE_ARRAY LIST_A
			| empty
	"""

def p_VARS_B(p):
	"""
	VARS_B : VARS
			| empty
	"""

def p_SIMPLE(p):
	"""
	SIMPLE : comma VARS_A
			| empty
	"""

def p_LIST(p):
	"""
	LIST : lSqrBracket cte_i ACUMULATE_R rSqrBracket LIST
			| empty
	"""

def p_LIST_A(p):
	"""
	LIST_A : comma VARS_A
		| empty
	"""

# Funcion auxiliar para la declaración de variables
def p_VARCTE_AUX_VARS(p):
	"""
	VARCTE_AUX_VARS : id ISLIST 
		| cte_i PUSH_STACK_OPERANDS_CONSTANT SAVE_ASSIGNED_VAR
		| cte_f PUSH_STACK_OPERANDS_CONSTANT SAVE_ASSIGNED_VAR
		| cte_str PUSH_STACK_OPERANDS_CONSTANT SAVE_ASSIGNED_VAR
		| BOOLEAN_AUX_VARS
	"""

# Funcion auxiliar para la declaración de variables
def p_BOOLEAN_AUX_VARS(p):
	"""
	BOOLEAN_AUX_VARS : False SAVE_ASSIGNED_VAR_BOOL
					| True SAVE_ASSIGNED_VAR_BOOL
	"""


#############################
# ACCIONES SEMANTICAS PARA LEER VARIABLES DIMENSIONADAS
#############################

iCounterDimensions = 0

# Validar nombre del arreglo
def p_VALIDATE_NAME_ARRAY(p):
	"""
	VALIDATE_NAME_ARRAY : empty	
	"""
	global dicDirectorioFunciones, currentFunction, lastReadType, varWithDimensions
	# p[ -1 ] = variable leída


	varWithDimensions = p[ -1 ]
	currentScope = getScope()

	# Validar que arreglo leido no esté previamente declarado
	if p[ -1 ] in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ]:
		imprimirError( 0 )
	else:
		dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -1 ] ] = { "Type": lastReadType, "Value": "", "Scope": currentScope, "Address": "", "Dimensionada" : 1, "Dimensiones" : [ ] }


# Calcular R para la dimensión leída
def p_ACUMULATE_R(p):
	"""
	ACUMULATE_R : empty
	"""
	global dicDirectorioFunciones, currentFunction, lastReadType, iCounterDimensions, varWithDimensions, dicConstantsInverted, dicConstants
	# varWithDimensions = variable leída 
	# p[ -1 ] = tamaño de la dimensión

	# Validar si la constante ya había sido leída previamente
	validateConstant( p[ -1 ] - 1)

	# Conseguir el valor de R acumulada, es 1 para la primera vez
	rAcum = 1
	length = len( dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ varWithDimensions ][ "Dimensiones" ] )
	if length > 0:
		rAcum = dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ varWithDimensions ][ "Dimensiones" ][ length - 1 ][ "R" ]

	# ( LsDim - LiDim + 1 ) * R acumulada
	rAcum = ( p[ -1 ] - 1 - 0  + 1 ) * rAcum
	print("rAcum")
	print(rAcum)

	dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ varWithDimensions ][ "Dimensiones" ].append( { "LiDim" : 0, "LsDim" : p[ -1 ] - 1, "R" : rAcum } )

	iCounterDimensions = iCounterDimensions + 1


# Calcular m para cada dimensión
# Asignar dirección de memoria base al arreglo y ajustar contador de la memoria
def p_CALCULATE_ARRAY(p):
	"""
	CALCULATE_ARRAY : empty
	"""
	global dicDirectorioFunciones, currentFunction, lastReadType, iCounterDimensions, iQuadCounter, qQuads, dicConstants, dicConstantsInverted
	# p[ -7 ] = nombre de arreglo leído


	aux = 1
	for dimension in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -7 ] ][ "Dimensiones" ]:

		mPrevious = -1
		if aux == 1:
			mPrevious = dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -7 ] ][ "Dimensiones" ][ iCounterDimensions - 1 ][ "R" ] # m0
		else:
			mPrevious = dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -7 ] ][ "Dimensiones" ][ aux - 2 ][ "mDim" ]


		LsDim = dimension[ "LsDim" ]
		LiDim = dimension[ "LiDim" ]
		mDim = mPrevious / ( LsDim - LiDim + 1 )

		if aux == iCounterDimensions:
			dimension[ "mDim" ] = 0
		else:
			dimension[ "mDim" ] = mDim

		aux = aux + 1

	iCounterDimensions = 0

	
	# Definir espacio de memoria y scope de arreglo

	# numero de direcciones de memoria que ocupa la variable dimensionada
	m0 = dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -7 ] ][ "Dimensiones" ][ iCounterDimensions - 1 ][ "R" ] 
	varAddress = setAddress( p[ -7 ], m0 )

	# Actualizar campo de memory address en la variable
	dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -7 ] ][ "Address" ] = varAddress

	# Quadruplos de asignación para que la maquina virtual primero haga la asignación y luego la consulta sobre sus valores
	aux = 0
	constAddress = validateConstant( 0 )
	while aux < m0:

		quad = [ "=", constAddress, "", varAddress ]
		varAddress = varAddress + 1
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
		aux = aux + 1


def p_EXPLOG(p):
	"""
	EXPLOG : EXPRESSION EXPLOG_A SOLVE_OPERATION_LOGIC
		| not EXPRESSION EXPLOG_A SOLVE_OPERATION_LOGIC
	"""

def p_EXPLOG_A(p):
	"""
	EXPLOG_A : and EXPLOG
		| or EXPLOG
		| empty
	"""

def p_EXPRESSION(p):
	"""
	EXPRESSION : EXP 
				| EXP EXPRESSION_A EXP SOLVE_OPERATION_RELATIONSHIP
	"""

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

def p_EXP_A(p):
	"""
	EXP_A : plus PUSH_STACK_OPERATORS EXP
		| minus PUSH_STACK_OPERATORS EXP
	"""

def p_TERM(p):
	"""
	TERM : FACTOR SOLVE_OPERATION_TIMES_DIVIDE
		| FACTOR SOLVE_OPERATION_TIMES_DIVIDE TERM_A 
	"""

def p_TERM_A(p):
	"""
	TERM_A : times PUSH_STACK_OPERATORS TERM
			| divide PUSH_STACK_OPERATORS TERM
	"""

def p_FACTOR(p):
	"""
	FACTOR : lParenthesis PUSH_STACK_OPERATORS EXPLOG rParenthesis POP_STACK_OPERATORS
			| VARCONSTAUX
	"""

# Define numeros y accesos a indices de arreglos (sin string y boolean de VARCTE)
def p_VARCONSTAUX(p):
	"""
	VARCONSTAUX : id PUSH_STACK_OPERANDS ISLIST 
				| cte_i PUSH_STACK_OPERANDS_CONSTANT
				| cte_f PUSH_STACK_OPERANDS_CONSTANT
				| BOOLEAN
	"""

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
	ASSIGNMENT : id PUSH_STACK_OPERANDS ISLIST assign PUSH_STACK_OPERATORS ASSIGNMENT_A
	"""

def p_ASSIGNMENT_A(p):
	"""
	ASSIGNMENT_A : EXPLOG SOLVE_OPERATION_ASSIGNMENT semicolon
				| METHODCALL SOLVE_OPERATION_ASSIGNMENT
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


#############################
# ACCIONES SEMANTICAS PARA ACCEDER VARIABLES DIMENSIONADAS
#############################

def p_ISLIST(p):
	"""
	ISLIST : lSqrBracket EXP VALIDATE_INDEX rSqrBracket ISLIST
			| empty SOLVE_OFFSETS
	"""


iDimensionCounter = 1 # valor default. Ayuda a seguir track de en que dimensión estamos para las variables dimensionadas
lastReadIndex = -1 # valor default. Esta variable ayuda a la función p_SOLVE_OFFSETS a recordar el último índice leído


# Generar cuadruplo para validar indice dentro de rango de variable dimensionada
# Generar cuadruplo opcional para multiplicar Sn * Mn
def p_VALIDATE_INDEX(p):
	"""
	VALIDATE_INDEX : empty
	"""
	global sOperands, iQuadCounter, qQuads, currentFunction, dicDirectorioFunciones, varDimensionadaLastRead, iDimensionCounter, lastReadIndex, dicConstants
	# p[ -4 ] = nombre de arreglo


	# Esta variable ayuda a la función p_SOLVE_OFFSETS a recordar el último índice leído
	lastReadIndex = sOperands.top()

	# Conseguir toda la info de la variable dimensionada
	varDim = ""	
	if varDimensionadaLastRead in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ]:
		varDim = dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ varDimensionadaLastRead ]
	else:
		varDim = dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ][ varDimensionadaLastRead ]

	# TODO: convertir las constantes de los rangos a direcciones
	LiDim = varDim[ "Dimensiones" ][ iDimensionCounter - 1 ][ "LiDim" ]
	LsDim = varDim[ "Dimensiones" ][ iDimensionCounter - 1 ][ "LsDim" ]
	quad = [ "VER", sOperands.top(), dicConstants[ LiDim ][ "Address" ], dicConstants[ LsDim ][ "Address" ] ]
	iQuadCounter = iQuadCounter + 1
	qQuads.append( quad )

	# Calcular todas las multiplicaciones Sn * Mn (Dependiendo de cuantas dimensiones tenga la variable)
	dimensiones = len( varDim[ "Dimensiones" ] )
	if( iDimensionCounter < dimensiones ): # Significa que todavia falta de procesar al menos una dimensión más
		

		# Conseguir dirección de memoria para constante mDim
		mDim = varDim[ "Dimensiones" ][ iDimensionCounter - 1 ][ "mDim" ]
		if mDim not in dicConstants:
			# Consigues una dirección de memoria para la constante y la insertas en los diccionarios de constantes globales
			constAddress = setConstAddress( "int" )
			dicConstants[ mDim ] = { "Address" : constAddress, "Type": "int" }
			dicConstantsInverted[ constAddress ] = { "Value" : mDim, "Type": "int" }


		# Generar cuadruplo para Sn * Mn
		temporal = setTempAddress( varDim[ "Type" ] )
		Sn = sOperands.pop()
		quad = [ "*", Sn, dicConstants[ mDim ][ "Address" ], temporal ]
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
		sOperands.push( temporal )

		# Para manejar el cubo, se tienen que sumar las multiplicaciones de Sn * Mn + Sn * Mn
		#if iDimensionCounter >= 2:
		#	temporal = setTempAddress( varDim[ "Type" ] )
		#	aux = sOperands.pop()
		#	aux2 = sOperands.pop()
		#	quad = [ "+", aux, aux2, temporal ]
		#	iQuadCounter = iQuadCounter + 1
		#	qQuads.append( quad )
		#	sOperands.push( temporal )

	iDimensionCounter = iDimensionCounter + 1


# Sumar -k y dirección Base de la variable dimensionada
def p_SOLVE_OFFSETS(p):
	"""
	SOLVE_OFFSETS : empty
	"""
	global iQuadCounter, qQuads, sOperands, dicDirectorioFunciones, varDimensionadaLastRead, currentFunction, iDimensionCounter, lastReadIndex, dicArrayBaseAddressHelper


	# TODO arreglar esto con reglas gramaticales
	# Nacada para poder asignar variables
	if p[-2] == None:
		return
	
	varDim = ""	
	if varDimensionadaLastRead in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ]:
		varDim = dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ varDimensionadaLastRead ]
	else:
		varDim = dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ][ varDimensionadaLastRead ]


	if iDimensionCounter - 1 > 1: # Se tiene que sumar Sn-1 * Mn-1 + Sn

		temporal = setTempAddress( varDim[ "Type" ] )
		# Generar cuadruplo para Sn-1 * Mn-1 + Sn
		sOperands.pop()
		aux = sOperands.pop()
		quad = [ "+", aux, lastReadIndex, temporal ]
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
		sOperands.push( temporal )

	length = len( varDim[ "Dimensiones" ] )

	# Cuadruplo para sumar dirección base 
	# Se tiene que poner un identificador para indicar que el temporal es un apuntador a un contenido TODO
	temporal = setTempAddress( varDim[ "Type" ] )

	constAddress = -1
	if varDim[ "Address" ] not in dicArrayBaseAddressHelper:
		# Consigues una dirección de memoria para la constante y la insertas en los diccionarios de constantes globales
		constAddress = setConstAddress( "int" )
		dicConstants[ constAddress ] = { "Address" : varDim[ "Address" ], "Type": "int" }
		dicConstantsInverted[ constAddress ] = { "Value" : varDim[ "Address" ], "Type": "int" }
		dicArrayBaseAddressHelper[ varDim[ "Address" ] ] = constAddress
	else:
		constAddress = dicArrayBaseAddressHelper[ varDim[ "Address" ] ]	

	quad = [ "+", sOperands.pop(), constAddress , temporal ]
	iQuadCounter = iQuadCounter + 1
	qQuads.append( quad )
	sOperands.push( temporal + 500000 )

	# Reset de variables auxiliares
	iDimensionCounter = 1
	lastReadIndex = -1


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
		| cte_i PUSH_STACK_OPERANDS_CONSTANT
		| cte_f PUSH_STACK_OPERANDS_CONSTANT
		| cte_str PUSH_STACK_OPERANDS_CONSTANT
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
	PARAMS : TYPE id SAVE_PARAM SAVE_PARAM_TYPE INCREMENT_PARAM_COUNTER PARAMS_A 
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
	METHODCALL : id VALIDATE_FUNCTION_NAME ERA lParenthesis METHODCALL_A METHODCALL_B rParenthesis semicolon VALIDATE_METHOD_CALL
	"""

def p_METHODCALL_A(p):
	"""
	METHODCALL_A : EXP VALIDATE_PARAMETER 
					| empty
	"""

def p_METHODCALL_B(p):
	"""
	METHODCALL_B : comma EXP VALIDATE_PARAMETER METHODCALL_B
				| empty
	"""

def p_RETURN(p):
	"""
	RETURN : return EXPLOG GENERATE_QUAD_RETURN semicolon
	"""

def p_GENERATE_QUAD_RETURN(p):
	"""
	GENERATE_QUAD_RETURN : empty
	"""
	global iQuadCounter, qQuads, sOperands

	# Quadruplo de asignación para que la maquina virtual primero haga la asignación y luego la consulta sobre sus valores
	quad = [ "RET", "", "", sOperands.top() ]
	iQuadCounter = iQuadCounter + 1
	qQuads.append( quad )


def p_BOOLEAN(p):
	"""
	BOOLEAN : False PUSH_STACK_OPERANDS_CONSTANT
			| True PUSH_STACK_OPERANDS_CONSTANT
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
	elif error == 8:
		print( "Error: Se quiere asignar una constante de diferente tipo de dato a la variable" )
	elif error == 9:
		print( "Error: No se puede dividir entre 0" )
	elif error == 10:
		print( "Error de rangos en arreglo" )


	exit(1)


#############################
# ACCIONES SEMANTICAS DE VARIABLES 
#############################

# Guarda la función en el directorio de funciones
def p_START_FUNCTION(p):
	"""
	START_FUNCTION : empty
	"""
	global currentFunction, dicDirectorioFunciones, iTemporalVariableCounter

	currentFunction = p[ -1 ]
	iTemporalVariableCounter = 0

	# Validar que la función no esté previamente declarada
	if currentFunction not in dicDirectorioFunciones:
		dicDirectorioFunciones[ currentFunction ]  = { "Type": lastReadType, "dicDirectorioVariables": {}, "ParamCounter": 0, "QuadCounter": 0, "TempCounter": 0, "ParamTypes": [ ], "Parameters" : [ ] }
	else:
		imprimirError( 5 )


# Guarda el último tipo de variable leido en una variable global lastReadType
def p_SAVE_TYPE(p):
	"""
	SAVE_TYPE : empty
	"""
	global lastReadType
	lastReadType = p[-1]
	

# Lógica para variables que son declaradas sin asignarles un valor, entonces se deben inicializar con un valor default
# Guardar nombre de variable, tipo, scope y dirección de memoria en directorio de variables de la función
def p_SAVE_VAR(p):
	"""
	SAVE_VAR : empty
	"""
	global dicDirectorioFunciones, currentFunction, lastReadType
	# p[ -1 ] = variable leída


	# Validar que variable leida no esté previamente declarada
	if p[ -1 ] in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ]:
		imprimirError( 0 )
	else:
		# Le mando la variable leida y un valor de -1 que indica que la variable no fue inicializada
		saveVarHelper( p[ -1 ], -1 )


# Lógica para variables que son declaradas y asignadas un valor 
# Guardar nombre de variable, tipo, scope y dirección de memoria en directorio de variables de la función
# Guardar constante en diccionario de constantes
# Para este paso ya se tiene la constante en el diccionario de constantes, su tipo de datos en el stack de tipos y su dirección de memoria asignada en el stack de operandos
# Se tiene que validar que la constante sea del mismo tipo de dato que la variable
def p_SAVE_ASSIGNED_VAR(p):
	"""
	SAVE_ASSIGNED_VAR : empty
	"""
	global dicDirectorioFunciones, currentFunction, lastReadType
	# p[ -2 ] = constante leida
	# p[ -4 ] = variable a la cual se le asigna la constante


	# Validar que variable leida no esté previamente declarada
	if p[ -4 ] in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ]:
		imprimirError( 0 )
	else:
		# Validar que el valor de la constante coincida con el tipo de dato de la variable
		# conseguir el tipo de dato de la constante
		if type( p[ -2 ] ) is int:
			constantType = 'int'
		elif type( p[ -2 ] ) is float:
			constantType = 'float'
		elif type( p[ -2 ] ) is str:
			constantType = 'string'

		if constantType != lastReadType:
			imprimirError( 8 )
		else:
			# Le mando la variable leida y el valor de la constante, lo cual indica que la variable si fue inicializada
			saveVarHelper( p[ -4 ], p[ -2 ] )


def p_SAVE_ASSIGNED_VAR_BOOL(p):
	"""
	SAVE_ASSIGNED_VAR_BOOL : empty
	"""
	global dicDirectorioFunciones, currentFunction, lastReadType
	# p[ -1 ] = constante leida
	# p[ -3 ] = variable a la cual se le asigna la constante


	# Validar que variable leida no esté previamente declarada
	if p[ -3 ] in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ]:
		imprimirError( 0 )
	else:
		# Validar que el valor de la constante coincida con el tipo de dato de la variable

		constantType = ""
		print("aaaaa")
		print(p[ -1 ])
		print(p[ -3 ])
		# conseguir el tipo de dato de la constante
		if type( p[ -1 ] ) is int:
			constantType = 'int'
		elif type( p[ -1 ] ) is float:
			constantType = 'float'
		elif type( p[ -1 ] ) is str:
			aux = p[ -1 ]
			if aux == "True" or aux == "False":
				constantType = 'bool'
			else:
				constantType = 'string'
			print("string")

		if constantType != lastReadType:
			imprimirError( 8 )
		else:
			# Le mando la variable leida y el valor de la constante, lo cual indica que la variable si fue inicializada
			saveVarHelper( p[ -3 ], p[ -1 ] )


# Sirve para guardar los parametros de una función
# No tengo que validar que estos parametros estén previamente declarados
# Estos parametros van a ser locales a la función
# Cuando se hace la llamada a la función y se pasan argumentos es cuando tengo que validar que las variables existan ( si se pasan variables )
# Los parametros los tengo que guardar en una lista, así como sus tipos están guardados (mismo orden)
def p_SAVE_PARAM(p):
	"""
	SAVE_PARAM : empty
	"""
	global dicDirectorioFunciones, currentFunction, lastReadType
	

	currentScope = getScope()

	# Se agrega el parametro a la lista de parametros de la función
	dicDirectorioFunciones[ currentFunction ][ "Parameters" ].append( p[ -1 ] )

	dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -1 ] ] = { "Type": lastReadType, "Value": "", "Scope": currentScope, "Address": "",  "Dimensionada": 0 }

	varAddress = setAddress( p[ -1 ], 1 )

	# Actualizar campo de memory address en la variable
	dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -1 ] ][ "Address" ] = varAddress

	# TODO: ¿ talvez ni siquiera tengo que inicializar los parametros ?
	# p[ -1 ] = variable leída
	#saveVarHelper( p[ -1 ], -1 )


# Lógica que comparten las funciones de p_SAVE_VAR y p_SAVE_ASSIGNED_VAR
# Se guarda una variable ya sea con un valor default inicial o bien con el valor que le asignaron
# Se genera cuadruplo de asignación en ambos casos para que la máquina virtual primero asigne y luego lea
def saveVarHelper( varRead, constantValue ):

	global initialValuesForVars, lastReadType, dicConstants, dicConstantsInverted, dicDirectorioFunciones, currentFunction, qQuads, iQuadCounter
	

	currentScope = getScope()
	constValue = -1 # Guarda el valor de la constante (puede ser el valor default generado o bien el que recibe como parametro)

	if constantValue == -1: # Se necesita generar un valor inicial default para la variable
		# Conseguir valor default según el tipo de dato que se esté manejando
		# Este valor es una constante
		constValue = initialValuesForVars.get( lastReadType )
	else: # El valor de la constante se recibe como parametro 
		constValue = constantValue

	validateConstant( constValue )

	dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ varRead ] = {"Type": lastReadType, "Value": constValue, "Scope": currentScope, "Address": "", "Dimensionada": 0 }

	# Definir espacio de memoria y scope de variable
	# Esto tiene que ir despues de insertar la variable en dicDirectorioFunciones porque se hace una consulta a su tipo de dato
	varAddress = setAddress( varRead, 1 )

	# Actualizar campo de memory address en la variable
	dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ varRead ][ "Address" ] = varAddress

	# Quadruplo de asignación para que la maquina virtual primero haga la asignación y luego la consulta sobre sus valores
	quad = [ "=", dicConstants[ constValue ][ "Address" ], "", varAddress ]
	iQuadCounter = iQuadCounter + 1
	qQuads.append( quad )


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
	global iQuadCounter, currentFunction, dicDirectorioFunciones
	dicDirectorioFunciones[ currentFunction ][ "QuadCounter" ] = iQuadCounter


# Acciones en la terminación de una función
# Reset de contadores para rangos de memoria
def p_END_PROCEDURE(p):
	"""
	END_PROCEDURE : empty
	"""
	global qQuads, iQuadCounter, iTemporalVariableCounter, dicDirectorioFunciones, currentFunction


	quad = [ "ENDPROC", "", "", "" ]
	qQuads.append( quad )
	iQuadCounter = iQuadCounter + 1

	dicDirectorioFunciones[ currentFunction ][ "TempCounter" ] = iTemporalVariableCounter

	resetTempAndLocalVars()
	iTemporalVariableCounter = 0


# Guardar el tipo de dato del parametro leido de la función
def p_SAVE_PARAM_TYPE(p):
	"""
	SAVE_PARAM_TYPE : empty
	"""
	global dicDirectorioFunciones, currentFunction, lastReadType
	dicDirectorioFunciones[ currentFunction ][ "ParamTypes" ].append( lastReadType )


# Valida que el nombre de la función a la que se está llamando haya sido previamente declarada
def p_VALIDATE_FUNCTION_NAME(p):
	"""
	VALIDATE_FUNCTION_NAME : empty
	"""
	global dicDirectorioFunciones, methodCall
	# p[ -1 ] = function name


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
    global qQuads, iQuadCounter, currentFunction, qQuadRecursiveCalls, dicDirectorioFunciones


    # p[ -2 ] =  nombre de la función a la que se está llamando
    quad = [ "ERA", p[ -2 ], dicDirectorioFunciones[ p[ -2 ] ][ "ParamCounter" ], dicDirectorioFunciones[ p[ -2 ] ][ "TempCounter" ] ]

    # Validar si es una llamada recursiva
    if( currentFunction == p[ -2 ] ):
        qQuadRecursiveCalls.append( iQuadCounter );

    qQuads.append(quad);
    iQuadCounter = iQuadCounter + 1;


# Se lee el argumento y se valida contra la lista de tipos de parametros de la función a la que se quiere llamar
def p_VALIDATE_PARAMETER(p):
	"""
	VALIDATE_PARAMETER : empty
	"""
	global sOperands, sTypes, iParametersCounter, qQuads, iQuadCounter, dicDirectorioFunciones, methodCall

	argument = sOperands.pop()
	argumentType = sTypes.pop()

	if iParametersCounter < len( dicDirectorioFunciones[ methodCall ][ "Parameters" ] ):
		# ParamTypes es una lista de tipos de los parametros de la función
		if argumentType != dicDirectorioFunciones[ methodCall ][ "ParamTypes" ][ iParametersCounter ]:
			imprimirError( 4 )
		else:
			paramName = dicDirectorioFunciones[ methodCall ][ "Parameters" ][ iParametersCounter ]
			quad = [ "PARAMETER", argument, '', dicDirectorioFunciones[ methodCall ][ "dicDirectorioVariables" ][ paramName ][ "Address" ] ]
			iParametersCounter = iParametersCounter + 1
			iQuadCounter = iQuadCounter + 1
			qQuads.append( quad )
	else:
		imprimirError( 7 )


# Se valida que el número de argumentos coincida con el número de parametros de la función
# Se manejan los valores de retorno de las funciones
def p_VALIDATE_METHOD_CALL(p):
	"""
	VALIDATE_METHOD_CALL : empty
	"""
	global iParametersCounter, dicDirectorioFunciones, qQuads, iQuadCounter, methodCall, iTemporalVariableCounter, sOperands


	if iParametersCounter != dicDirectorioFunciones[ methodCall ][ "ParamCounter" ]:
		imprimirError( 7 )
	else:
		quad = [ "GOSUB", methodCall, '', dicDirectorioFunciones[ methodCall ][ "QuadCounter" ] ]
		qQuads.append( quad )
		iQuadCounter = iQuadCounter + 1

	if dicDirectorioFunciones[ methodCall ][ "Type" ] != "void":

		# Definir espacio de memoria de variable temporal
		address = setTempAddress( dicDirectorioFunciones[ methodCall ][ "Type" ] )
		quad = [ "=", methodCall, '',  address ]
		qQuads.append( quad )
		iQuadCounter = iQuadCounter + 1
		sOperands.push(address)
		iTemporalVariableCounter = iTemporalVariableCounter + 1

	iParametersCounter = 0


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
	global sOperands, dicDirectorioFunciones, varDimensionadaLastRead, dicConstants, dicConstantsInverted


	# Validar que la variable leida haya sido previamente declarada, que exista en el diccionario de variables de la función
	if p[ -1 ] in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ]:
		# Validar si es una variable dimensionada o no
		if dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -1 ] ][ "Dimensionada" ] == 1:
			varDimensionadaLastRead = p[ -1 ]
			return
		
		# Conseguir la dirección de memoria de variable previamente guardada en directorio
		address = dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -1 ] ][ "Address" ]
		sOperands.push( address )
		sTypes.push( dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[ -1 ] ][ "Type" ] )
	elif p[-1] in dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ]:

		# Validar si es una variable dimensionada o no
		if dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ][ p[ -1 ] ][ "Dimensionada" ] == 1:
			varDimensionadaLastRead = p[ -1 ]
			return

		# Conseguir la dirección de memoria de variable previamente guardada en directorio
		address = dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ][ p[ -1 ] ][ "Address" ]
		sOperands.push( address )
		sTypes.push( dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ][ p[-1] ][ "Type" ] )
	else:
		imprimirError(3)


# Funciona igual que PUSH_STACK_OPERANDS, solo que aquí manejamos constantes
# Se agrega la constante al diccionario global de constantes
def p_PUSH_STACK_OPERANDS_CONSTANT(p):
	"""
	PUSH_STACK_OPERANDS_CONSTANT : empty
	"""

	global sOperands, sTypes, dicConstants, dicConstantsInverted


	constantType = ""
	# Si la constante no existe, se debe asignar una dirección de memoria
	# También se debe agregar a la pila de operandos y a la pila de tipos la info correspondiente
	if p[ -1 ] not in dicConstants:
		print("yujhuuuu")
		print(p[ -1 ])

		# conseguir el tipo de dato de la constante
		if type( p[ -1 ] ) is int:
			constantType = 'int'
		elif type( p[ -1 ] ) is float:
			constantType = 'float'
		elif type( p[ -1 ] ) is str:
			print("string")
			constantType = 'string'
		elif type( p[ -1 ] ) is bool:
			print("bool")
			constantType = 'bool'

		
		address = setConstAddress( constantType )
		print(address)
		dicConstants[ p[ -1 ] ] = { "Address" : address, "Type": constantType }
		dicConstantsInverted[ address ] = { "Value" : p[ -1 ], "Type": constantType }
		sOperands.push( address )
		sTypes.push( constantType )
	else:
		sOperands.push( dicConstants[ p[ -1 ] ][ "Address" ] ) # Se hace push del memory address de la constante
		sTypes.push( dicConstants[ p[ -1 ] ][ "Type" ] ) # Se hace push del tipo de dato de la constante


# Insertar operador en stack de operadores
def p_PUSH_STACK_OPERATORS(p):
	"""
	PUSH_STACK_OPERATORS : empty
	"""
	global sOperators
	sOperators.push( p[-1] )
	

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

	global sOperands, sOperators, sTypes, qQuads, iQuadCounter, iTemporalVariableCounter, dicDirectorioFunciones, currentFunction
	

	rightOperand = sOperands.pop()
	rightType = sTypes.pop()

	leftOperand = sOperands.pop()
	leftType = sTypes.pop()

	operator = sOperators.pop()

	# Esta es una variable temporal
	resultType = semanticCube[ dicOperandIndexCube[ leftType ] ][ dicOperandIndexCube[ rightType ] ][ dicOperatorIndexCube[ operator ] ]

	if resultType != 0: # 0 = error en subo semantico
		result = 'result' # es un valor dummy por mientras, solo para ver que se generen los quads

		currentScope = getScope()

		dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ "t" + str(iTemporalVariableCounter) ] = {"Type": dicReturnValuesCube[ resultType ], "Value": "", "Scope": currentScope, "Address": "" }

		# Definir espacio de memoria de variable temporal
		address = setTempAddress( dicReturnValuesCube[ resultType ] )

		# Actualizar campo de memory address en la variable
		dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ "t" + str(iTemporalVariableCounter) ][ "Address" ] = address

		iTemporalVariableCounter = iTemporalVariableCounter + 1
		quad = [ operator, leftOperand, rightOperand, address ]
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
		sOperands.push( address )
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

	global sOperands, sOperators, sTypes, qQuads, iQuadCounter


	rightOperand = sOperands.pop()
	rightType = sTypes.pop()

	leftOperand = sOperands.pop()
	leftType = sTypes.pop()

	operator = sOperators.pop()

	resultType = semanticCube[ dicOperandIndexCube[ leftType ] ][ dicOperandIndexCube[ rightType ] ][ dicOperatorIndexCube[ operator ] ]

	if resultType != 0: # 0 = error en subo semantico

		quad = [ operator, rightOperand, '', leftOperand]
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
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

	global iQuadCounter, qQuads

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
	global sTypes, sOperands, sJumps, iQuadCounter, qQuads


	expType = sTypes.pop()

	print("exptypes")
	print(expType)
	print("sOperands")
	print(sOperands.top())

	if expType == 'bool':
		result = sOperands.pop()

		quad = [ 'GOTOF', result, '', '' ]
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
		sOperands.push( result )
		sJumps.push( iQuadCounter - 1 )
	else:
		imprimirError( 4 )


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
	global sJumps, iQuadCounter, qQuads

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
	global sJumps, iQuadCounter
	sJumps.push( iQuadCounter )


#############################
# ACCIONES SEMANTICAS DE CICLOS
#############################

# Resuelve cuadruplo con salto pendiente para whiles anidados
def fillAux( end ):

	global iQuadCounter, qQuads

	aux = qQuads[ end ] # Cuadruplo con salto pendiente
	aux[ 3 ] = iQuadCounter + 1 # Llenar cuadruplo con el siguiente cuadruplo a ejecutar
	qQuads[ end ] = aux # Reemplazar breadcrumb por cuadruplo con salto a fin de ciclo

lastJumpAux = -1
# Resuelve cuadruplos con saltos pendientes para el while
# Resuelve los saltos de regreso a la expresión y el salto que indica el final del loop
def p_SOLVE_OPERATION_PRE_CONDITIONAL_LOOP(p):
	"""
	SOLVE_OPERATION_PRE_CONDITIONAL_LOOP : empty
	"""
	global sJumps, iQuadCounter, qQuads, lastJumpAux

	#if qQuads[ len( qQuads ) - 1 ][ 0 ] == 'GOTO':
	#	print("AAHAHHAHAHAHAHAHAH")
	#	fillAux( lastJumpAux )

	lastJumpAux = sJumps.top()
	end = sJumps.pop()
	returnTo = sJumps.pop()

	quad = [ 'GOTO', '', '', returnTo ] 
	iQuadCounter = iQuadCounter + 1
	qQuads.append( quad )

	fill( end )


# Resuelve cuadruplo con salto pendiente para el do while
# Resuelve el salto de regreso a la ejecución de los statements del do while (en caso de que sea verdadera la expresión)
def p_SOLVE_OPERATION_POST_CONDITIONAL_LOOP(p):
	"""
	SOLVE_OPERATION_POST_CONDITIONAL_LOOP : empty
	"""
	global sJumps, sOperands, iQuadCounter, qQuads


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
	global qQuads, iQuadCounter, sOperands


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
# MANEJO DE MEMORIA
#############################


# Asignar memoria a variable
# Se busca primero en el directorio de variables de la función global y si no está entonces se confirma que es una variable local
# Regresa la dirección de memoria asignada a la variable
def setAddress( varName, totalMemoryAddresses ):

	global currentFunction, gIntIndex, gFloatIndex, gBoolIndex, gStringIndex, lIntIndex, lFloatIndex, lBoolIndex, lStringIndex

	if varName in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ] and currentFunction != "globalFunc": # Es una variable local
		typeVar = dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ varName ][ "Type" ]
		return setAddressHelper( typeVar, totalMemoryAddresses, lIntIndex, lFloatIndex, lBoolIndex, lStringIndex, "local" ) 
	else: # Es una variable global
		typeVar = dicDirectorioFunciones[ "globalFunc" ][ "dicDirectorioVariables" ][ varName ][ "Type" ]
		return setAddressHelper( typeVar, totalMemoryAddresses, gIntIndex, gFloatIndex, gBoolIndex, gStringIndex, "global" ) 


# Asignar memoria a variable global/local
# Incrementa el contador del rango para la memoria global/local
def setAddressHelper( varType, totalMemoryAddresses, IntIndex, FloatIndex, BoolIndex, StringIndex, scope ):

	global currentFunction, gIntIndex, gFloatIndex, gBoolIndex, gStringIndex, lIntIndex, lFloatIndex, lBoolIndex, lStringIndex, tIntIndex, tFloatIndex, tBoolIndex, tStringIndex

	addressAsigned = None

	if varType == "int":
		addressAsigned = IntIndex
		if scope == "global":
			gIntIndex += totalMemoryAddresses
		else:
			lIntIndex += totalMemoryAddresses
	elif varType == "float":
		addressAsigned = FloatIndex
		if scope == "global":
			gFloatIndex += totalMemoryAddresses
		else:
			lFloatIndex += totalMemoryAddresses
	elif varType == "bool":
		addressAsigned = BoolIndex
		if scope == "global":
			gBoolIndex += totalMemoryAddresses
		else:
			lBoolIndex += totalMemoryAddresses
	elif varType == "string":
		addressAsigned = StringIndex
		if scope == "global":
			gStringIndex += totalMemoryAddresses
		else:
			lStringIndex += totalMemoryAddresses

	return addressAsigned


# Asignar memoria a variable temporal
# Incrementa el contador del rango para la memoria temporal
def setTempAddress( varType ):

	global tIntIndex, tFloatIndex, tBoolIndex, tStringIndex

	addressAsigned = None

	if varType == "int":
		addressAsigned = tIntIndex
		tIntIndex += 1
	elif varType == "float":
		addressAsigned = tFloatIndex
		tFloatIndex += 1
	elif varType == "bool":
		addressAsigned = tBoolIndex
		tBoolIndex += 1
	elif varType == "string":
		addressAsigned = tStringIndex
		tStringIndex += 1

	return addressAsigned


# Validar si la constante es nueva para el programa, en dicho caso guardarla en diccionario de constantes
def validateConstant( constantVal ):

	global dicConstants, dicConstantsInverted, lastReadType

	constAddress = -1 # Valor default

	if constantVal not in dicConstants:

		# Consigues una dirección de memoria para la constante y la insertas en los diccionarios de constantes globales
		constAddress = setConstAddress( lastReadType )
		dicConstants[ constantVal ] = { "Address" : constAddress, "Type": lastReadType }
		dicConstantsInverted[ constAddress ] = { "Value" : constantVal, "Type": lastReadType }
	else:
		constAddress = dicConstants[ constantVal ][ "Address" ]

	return constAddress


# Asignar memoria a constante
# Incrementa el contador del rango para la memoria de constantes
def setConstAddress( varType ):

	global cIntIndex, cFloatIndex, cBoolIndex, cStringIndex

	addressAsigned = None

	if varType == "int":
		addressAsigned = cIntIndex
		cIntIndex += 1
	elif varType == "float":
		addressAsigned = cFloatIndex
		cFloatIndex += 1
	elif varType == "bool":
		addressAsigned = cBoolIndex
		cBoolIndex += 1
	elif varType == "string":
		addressAsigned = cStringIndex
		cStringIndex += 1

	return addressAsigned


# Reset a los contadores de los rangos de las memorias 
# Cada función tiene su propio rango de memoria local
def resetTempAndLocalVars():

	global lIntIndex, lFloatIndex, lBoolIndex, lStringIndex, tIntIndex, tFloatIndex, tBoolIndex, tStringIndex

	lIntIndex = 5000
	lFloatIndex = 6000
	lBoolIndex = 7000
	lStringIndex = 8000
	tIntIndex = 9000
	tFloatIndex = 10000
	tBoolIndex = 11000
	tStringIndex = 12000


parser = yacc.yacc()