import ply.yacc as yacc
from lexer import lexer, tokens

dicDirectorioFunciones = {} # "nombreFuncion" : { "tipo": void/TYPE/null, "dirDirectorioVariables": {} }
# dirDirectorioVariables = "nombreVariable" : { }
lastReadType = ""


# VarConstAux puro numero y acceder a arreglo

def p_PROGRAM(p):
	"""
	PROGRAM : program globalFunc START_GLOBAL_FUNCTION semicolon PROGRAM_A start BLOCK
	"""
	for item in p:
		print(item)

def p_PROGRAM_A(p):
	"""
	PROGRAM_A : VARS PROGRAM_A
			| METHOD PROGRAM_A
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
	SIMPLE : id SAVE_VAR_TYPE SIMPLE_A
	"""

def p_SIMPLE_A(p):
	"""
	SIMPLE_A : comma SIMPLE
			| empty
	"""

def p_LIST(p):
	"""
	LIST : id lSqrBracket VARCONSTAUX rSqrBracket LIST_A
	"""

def p_LIST_A(p):
	"""
	LIST_A : comma LIST
		| empty
	"""

def p_EXPLOG(p):
	"""
	EXPLOG : EXPRESSION EXPLOG_A
		| not EXPRESSION EXPLOG_A
	"""

def p_EXPLOG_A(p):
	"""
	EXPLOG_A : and EXPLOG
		| or EXPLOG
		| empty
	"""

def p_EXPRESSION(p):
	"""
	EXPRESSION : EXP EXPRESSION_A EXP
	"""

def p_EXPRESSION_A(p):
	"""
	EXPRESSION_A : greater 
				| lessThan
				| greaterEquals
				| lessThanEquals
				| equals
				| notEquals
	"""

def p_EXP(p):
	"""
	EXP : TERM EXP_A
	"""

def p_EXP_A(p):
	"""
	EXP_A : plus EXP
		| minus EXP
		| empty
	"""

def p_TERM(p):
	"""
	TERM : FACTOR TERM_A
	"""

def p_TERM_A(p):
	"""
	TERM_A : times TERM
			| divide TERM
			| empty
	"""

def p_FACTOR(p):
	"""
	FACTOR : lParenthesis EXPLOG rParenthesis
			| VARCONSTAUX
	"""

# Define numeros y accesos a indices de arreglos (sin string y boolean de VARCTE)
def p_VARCONSTAUX(p):
	"""
	VARCONSTAUX : id ISLIST 
		| cte_i 
		| cte_f 
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
	BLOCK_A : STATEMENT
			| empty
	"""

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

def p_ASSIGNMENT(p):
	"""
	ASSIGNMENT : id ISLIST equals EXPRESSION semicolon 
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
			| void 
	"""

def p_CONDITION(p):
	"""
	CONDITION : if lParenthesis EXPLOG rParenthesis BLOCK CONDITION_A semicolon
	"""

def p_CONDITION_A(p):
	"""
	CONDITION_A : else BLOCK
				| empty
	"""

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

def p_START_GLOBAL_FUNCTION(p):
	"""
	START_GLOBAL_FUNCTION : empty
	"""
	dicDirectorioFunciones[ "globalFunc" ]  = { "tipo": "null", "dirDirectorioVariables": {} }

def p_SAVE_TYPE(p):
	"""
	SAVE_TYPE : empty
	"""
	lastReadType = str( p.type )
	

def p_SAVE_VAR_TYPE(p):
	"""
	SAVE_VAR_TYPE : empty
	"""

	# Validar que la variable no haya sido previamente declarada
	#if( p.var in dicDirectorioFunciones[ p.nombreFunc ][ "dirDirectorioVariables" ] ):
	#	print( "ERROR: Variable previamente declarada" )
		# exit

	# Diferenciar entre variable simple y lista
	#if len( p ) == 1:
	#	dicDirectorioFunciones[ "globalFunc" ][ "dirDirectorioVariables" ][ p.id ] = { "type": lastReadType }
	#else:
	#	dicDirectorioFunciones[ "globalFunc" ][ "dirDirectorioVariables" ][ p.id ] = { "type": lastReadType, "tamaño": p.tamaño }

parser = yacc.yacc()
 
 
 
 
 
 
























