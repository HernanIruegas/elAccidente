tokenToCode = {
    # Operaciones
    "+": 0,
    "-": 1,
    "*": 2,
    "/": 3,
    # Asignación
    "=": 4,

    # Relacionales
    ">" : 5,
    "<" : 6,
    "<=" : 7,
    ">=" : 8,

    # Lógicos
    "==" : 9,
    "!=" : 10,
    "&&" : 11,
    "||" : 12,
    "!" : 13,

    # Jumps and special keywords
    "GOTO": 14,
    "GOTOF": 15,
    "GOTOT": 16,
    "GOSUB": 17,
    "ERA": 18,
    "PARAMETER": 19,
    "ENDPROC": 20,
    "RET": 21
}


codeToToken = {
    # Operaciones
    0: "+",
    1: "-",
    2: "*",
    3: "/",
    # Asignación
    4: "=",

    # Relacionales
    5: ">",
    6: "<",
    7: "<=",
    8: ">=",

    # Lógicos
    9: "==",
    10: "!=",
    11: "&&",
    12: "||",
    13: "!",

    # Jumps and special keywords
    14: "GOTO",
    15: "GOTOF",
    16: "GOTOT",
    17: "GOSUB",
    18: "ERA",
    19: "PARAMETER",
    20: "ENDPROC",
    21: "RET"
}

typeToCode = {"bool": 1, "str": 2, "double": 3, "error": 4, "int": 5, "void": 6}

codeToType = {1: "bool", 2: "str", 3: "double", 4: "error", 5: "int", 6: "void"}

#type_to_init_value = {"bool": "False", "str": '""', "double": "0.0", "int": "0"}

scopeToCode = {"global": 1, "local": 2}

codeToScope = {1: "global", 2: "local"}