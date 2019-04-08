import ply.yacc as yacc
from lexer import lexer, tokens
from Stack import Stack
from SemanticCube import dicOperandIndexCube, semanticCube, dicOperatorIndexCube, dicReturnValuesCube


dicDirectorioFunciones = {} # "nombreFuncion" : { "Type": void/TYPE/null, "dicDirectorioVariables": {} }
# dicDirectorioVariables = "VarName" : { "Type": ..., "Value": ...}

lastReadType = ""
currentFunction = ""

sOperators = Stack()
sOperands = Stack()
sTypes = Stack()
sJumps = Stack()
qQuads = []
iQuadCounter = 0

# VarConstAux puro numero y acceder a arreglo

def p_PROGRAM(p):
	"""
	PROGRAM : program globalFunc START_GLOBAL_FUNCTION semicolon PROGRAM_A start BLOCK PRINTQUADS
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
		| cte_i PUSH_STACK_OPERANDS
		| cte_f PUSH_STACK_OPERANDS
	"""
	#print("VARCONSTAUX")

def p_TYPE(p):
	"""
	TYPE : int SAVE_TYPE
		| float SAVE_TYPE
		| string SAVE_TYPE
		| bool SAVE_TYPE
	"""
# falta que pueda existir varios statements
def p_BLOCK(p):
	"""
	BLOCK : lCurlyBracket BLOCK_A rCurlyBracket
	"""
	# print("p_BLOCK {}".format(p[-1]))

def p_BLOCK_A(p):
	"""
	BLOCK_A : STATEMENT BLOCK_A
			| empty
	"""
	# print("p_BLOCK_A {}".format(p[-1]))

def p_STATEMENT(p):
	"""
	STATEMENT : ASSIGNMENT
			| CONDITION
			| WRITE
			| LOOP
			| METHODCALL
			| READ
			| STATMETHODS
			| RETURN 
	"""
	# print("STATEMENT {}" .format(p[-1]))

def p_ASSIGNMENT(p):
	"""
	ASSIGNMENT : id ISLIST assign EXPLOG semicolon 
	"""
	# print("ASSIGNMENT {}".format(p[-1]))

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
			| void 
	"""

def p_CONDITION(p):
	"""
	CONDITION : if lParenthesis EXPLOG rParenthesis GENERATE_GOTOF_CONDITIONAL BLOCK CONDITION_A SOLVE_OPERATION_CONDITIONAL
	"""
	# if lParenthesis EXPLOG rParenthesis GENERATE_GOTOF_CONDITIONAL BLOCK CONDITION_A SOLVE_OPERATION_CONDITIONAL
	# print("CONDITION {}" .format(p[-1]))

def p_CONDITION_A(p):
	"""
	CONDITION_A : else GENERATE_GOTO_CONDITIONAL BLOCK
				| empty
	"""
	# print("CONDITION_A")


def p_WRITE(p):
	"""
	WRITE : print lParenthesis EXPRESSION WRITE_A rParenthesis semicolon
	"""

def p_WRITE_A(p):
	"""
	WRITE_A : comma EXPRESSION WRITE_A
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
	METHOD : func TYPEMETHOD id lParenthesis PARAMS rParenthesis BLOCK semicolon
	"""

def p_PARAMS(p):
	"""
	PARAMS : EXP PARAMS_A
	"""

def p_PARAMS_A(p):
	"""
	PARAMS_A : comma EXP PARAMS_A
		| empty
	"""

def p_LOOP(p):
	"""
	LOOP : while lParenthesis EXPLOG rParenthesis BLOCK
	"""

def p_METHODCALL(p):
	"""
	METHODCALL : id lParenthesis EXP METHODCALL_A rParenthesis semicolon
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


# ACCIONES SEMANTICAS

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

	exit(1)


# Crea el directorio de funciones y agrega la función global
def p_START_GLOBAL_FUNCTION(p):
	"""
	START_GLOBAL_FUNCTION : empty
	"""
	global currentFunction 
	global dicDirectorioFunciones

	currentFunction = p[ -1 ]
	dicDirectorioFunciones[ currentFunction ]  = { "Type": "null", "dicDirectorioVariables": {} }


# Guarda el último tipo de variable leido en una variable global lastReadType
def p_SAVE_TYPE(p):
	"""
	SAVE_TYPE : empty
	"""
	global lastReadType

	lastReadType = p[-1]
	

# Guardar nombre de variable en directorio de variables de la función
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
	    dicDirectorioFunciones[currentFunction]["dicDirectorioVariables"][ p[-1] ] = {"Type": lastReadType, "Value": ""}


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


# Insertar operando en stack de operandos y su tipo en stack de tipos
# Necesitas consultar el tipo de la variable con el diccioanrio de variables de la función
def p_PUSH_STACK_OPERANDS(p):
	"""
	PUSH_STACK_OPERANDS : empty
	"""
	global sOperands

	# Validar que la variable leida haya sido previamente declarada, que exista en el diccionario de variables de la función
	if p[-1] in dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ]:
		sOperands.push( p[-1] )
		# print(str(sOperands.top())+ " PUSH_STACK_OPERANDS")
		#print("sTypes: " + str( dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[-1] ][ "Type" ] ) )
		sTypes.push( dicDirectorioFunciones[ currentFunction ][ "dicDirectorioVariables" ][ p[-1] ][ "Type" ] )
	else:
		imprimirError(3)


# Insertar operador en stack de operadores
def p_PUSH_STACK_OPERATORS(p):
	"""
	PUSH_STACK_OPERATORS : empty
	"""
	global sOperators
	sOperators.push( p[-1] )
	# print(str(sOperators.top())+ " PUSH_STACK_OPERATORS")
	

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

	rightOperand = sOperands.pop()
	rightType = sTypes.pop()

	leftOperand = sOperands.pop()
	leftType = sTypes.pop()

	operator = sOperators.pop()

	#print("leftType: " + str(leftType))
	#print(dicOperandIndexCube[ leftType ])
	#print("rightType: " + str(rightType))
	#print(dicOperandIndexCube[ rightType ])
	#print("operator: " + str(operator))
	#print(dicOperatorIndexCube[ operator ])

	resultType = semanticCube[ dicOperandIndexCube[ leftType ] ][ dicOperandIndexCube[ rightType ] ][ dicOperatorIndexCube[ operator ] ]

	if resultType != 0: # 0 = error en subo semantico
		#result <- AVAIL.next() No sabemos que es pero viene en la hoja
		result = 'result' # es un valor dummy por mientras, solo para ver que se generen los quads
		quad = [ operator, leftOperand, rightOperand, result + str(iQuadCounter+1) ]
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
		sOperands.push( result + str(iQuadCounter) )
		# print(str(sOperands.top())+ " solveOperationHelper")
		#print("sTypes: " + str(resultType) )
		sTypes.push( dicReturnValuesCube[ resultType ] )
	else:
		imprimirError(2)


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


# Resuelve cuadruplo con salto pendiente
def fill( end ):
	global iQuadCounter
	global qQuads

	aux = qQuads[ end ] # Cuadruplo con salto pendiente
	aux[ 3 ] = iQuadCounter # Llenar cuadruplo con el siguiente cuadruplo a ejecutar
	qQuads[ end ] = aux # Reemplazar breadcrumb por cuadruplo con salto a fin de ciclo


# Genera cuadruplo con salto pendiente después de haber leido un if condicional
def p_GENERATE_GOTOF_CONDITIONAL(p):
	"""
	GENERATE_GOTOF_CONDITIONAL : empty
	"""

	global sTypes
	global sOperands
	global sJumps
	global iQuadCounter

	expType = sTypes.pop()

	if expType == 'bool':
		result = sOperands.pop()

		quad = [ 'GotoF', result, '', '' ]
		iQuadCounter = iQuadCounter + 1
		qQuads.append( quad )
		sOperands.push( result )
		sJumps.push( iQuadCounter - 1 )
		# print(str(sOperands.top()) +" solveOperationHelper")
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


def p_GENERATE_GOTO_CONDITIONAL(p):
	"""
	GENERATE_GOTO_CONDITIONAL : empty
	"""

	global sJumps

	quad = [ 'GOTO', '', '', '' ]
	iQuadCounter = iQuadCounter + 1

	false = sJumps.pop()
	sJumps.push( iQuadCounter - 1 )
	fill( false )


#
def p_PRINTQUADS(p):
	"""
	PRINTQUADS : empty
	"""

	global qQuads

	for i in qQuads:
		print( i )


parser = yacc.yacc()


#while True:
#	try:
#	    s = input('program globalFunc; start{ varuno = 2 * 3; }')
#	except EOFError:
#	    break
#	if not s: continue
#	result = parser.parse(s)
#	print(result)



