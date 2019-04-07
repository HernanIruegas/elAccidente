import ply.lex as lex

# Reserved Keywords (there should be no grammatical rules for these)

reserved = {
    
    # Code Related and Decision Making
    'program' : 'program',
    'globalFunc' : 'globalFunc',
    'start' : 'start',
    'var' : 'var',
    'scan' : 'scan',
    'print': 'print',
    'func' : 'func',
    'while' : 'while',
    'if' : 'if',
    'else' : 'else',
    'void' : 'void',
    'return' : 'return',
    'and' : 'and',
    'or' : 'or',

    # Data Types
    'int' : 'int',
    'float' : 'float',
    'string' : 'string',
    'bool' : 'bool',
    'TRUE' : 'TRUE',
    'FALSE' : 'FALSE',

    #Special Functions
    'ols' : 'ols',
    'las' : 'las',
    'rid' : 'rid',
    'kmeans' : 'kmeans',
    'mbm' : 'mbm',
    'tseries' : 'tseries',
    'mean_abs_err' : 'mean_abs_err',
    'mean_sqr_err' : 'mean_sqr_err',
    'median_abs_err' : 'median_abs_err',
    'mean' : 'mean',
    'mode' : 'mode',
    'median' : 'median',
    'prob' : 'prob',
    'freq' : 'freq',
    'variance' : 'variance',
    'stddev' : 'stddev',
    'skew' : 'skew',
    'kurt' : 'kurt'

 }

# Token List

tokens = [
    'id',
    'semicolon',
    'colon',
    'comma',
    'lSqrBracket',
    'rSqrBracket',
    'greater',
    'lessThan',
    'greaterEquals',
    'lessThanEquals',
    'assign',
    'equals',
    'notEquals',
    'not',
    'minus',
    'times',
    'divide',
    'plus',
    'lParenthesis',
    'rParenthesis',
    'lCurlyBracket',
    'rCurlyBracket',
    'cte_str',
    'cte_i',
    'cte_f'
] + list(reserved.values())


# Regular Expressions for simple tokens (no action needed)

t_semicolon = r'\;'
t_colon = r'\:'
t_comma = r'\,'
t_lSqrBracket = r'\['
t_rSqrBracket = r'\]'
t_lParenthesis = r'\('
t_rParenthesis = r'\)'
t_lCurlyBracket = r'\{'
t_rCurlyBracket = r'\}'


# Token rules specified as a functions (action needed)

def t_id(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    t.type = reserved.get(t.value, "id")
    return t

def t_greater(t):
    r'\>'
    return t

def t_lessThan(t):
    r'\<'
    return t

def t_greaterEquals(t):
    r'\>\='
    return t

def t_equals(t):
    r'\=\='
    return t

def t_notEquals(t):
    r'\!\='
    return t

def t_lessThanEquals(t):
    r'\<\='
    return t

def t_not(t):
    r'\!'
    return t

def t_plus(t):
    r'\+'
    return t

def t_minus(t):
    r'\-'
    return t

def t_times(t):
    r'\*'
    return t

def t_divide(t):
    r'\/'
    return t

def t_assign(t):
    r'\='
    return t
    
def t_cte_str(t):
    r'\".*\"'
    t.value = str(t.value)
    return t

def t_cte_i(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_cte_f(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


t_ignore = "\t\r "
def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")

# Error handling rule
def t_error(t):
 print("Illegal character '%s'" % t.value[0])
 t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
#data = '''
#3 + 4 * 10
#+ -20 *2
#'''

# Give the lexer some input
#lexer.input(data)

# Tokenize
#while True:
# tok = lexer.token()
# if not tok: 
#     break      # No more input
# print(tok)