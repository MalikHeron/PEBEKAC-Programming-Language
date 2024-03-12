from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# Keywords
reserved = {
    'class': 'CLASS',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL',
    'return': 'RETURN',
    'print': 'PRINT',
    'input': 'INPUT',
    'fun': 'FUN',
    'new': 'NEW',
    'import': 'IMPORT',
    'int': 'INT',
    'float': 'FLOAT',
    'double': 'DOUBLE',
    'boolean': 'BOOLEAN',
    'string': 'STRING',
    'intArray': 'INTARRAY',
    'floatArray': 'FLOATARRAY',
    'stringArray': 'STRINGARRAY',
    'doubleArray': 'DOUBLEARRAY',
    'intList': 'INTLIST',
    'floatList': 'FLOATLIST',
    'stringList': 'STRINGLIST',
    'doubleList': 'DOUBLELIST',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'break': 'BREAK',
    'params': 'PARAMS'
}

# All tokens must be named in advance.
tokens = list(reserved.values()) + [
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LPAREN', 'RPAREN', 'ASSIGN',
    'IDENTIFIER', 'STRING_LITERAL', 'NUMBER', 'MODULUS', 'EQUAL', 'NOTEQUAL', 'LESSTHAN', 'GREATERTHAN',
    'LESSTHANEQUAL', 'GREATERTHANEQUAL', 'AND', 'OR', 'NOT', 'SEMICOLON',
    'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COMMA', 'DOT',
    'ARROW', 'INCREMENT', 'DECREMENT', 'POW', 'BACKSLASH', 'SLASH', 'APOSTROPHE', 'AT',
    'HASH', 'DOUBLEQUOTE', 'PIPE', 'PLUSASSIGN', 'MINUSASSIGN', 'TIMESASSIGN', 'DIVIDEASSIGN',
    'MODASSIGN', 'COLON', 'QUESTION'
]

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_MODULUS = r'%'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_LESSTHANEQUAL = r'<='
t_GREATERTHANEQUAL = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_SEMICOLON = r';'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_DOT = r'\.'
t_COLON = r':'
t_ASSIGN = r'='
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_POW = r'\*\*'
t_AT = r'@'
t_HASH = r'\#'
t_QUESTION = r'\?'
t_BACKSLASH = r'\\'
t_SLASH = r'/'
t_APOSTROPHE = r'\''
t_DOUBLEQUOTE = r'\"'
t_PIPE = r'\|'
t_PLUSASSIGN = r'\+='
t_MINUSASSIGN = r'-='
t_TIMESASSIGN = r'\*='
t_DIVIDEASSIGN = r'/='
t_MODASSIGN = r'%='

# Ignored characters
t_ignore = ' \t'


# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING_LITERAL(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # Remove the quotation marks
    return t


# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)


# Build the lexer object
lexer = lex()


# --- Parser

# Write functions for each grammar rule which is
# specified in the docstring.
def p_program(p):
    """
    program : stmt_list
    """
    p[0] = ('program', p[1])


def p_stmt_list(p):
    """
    stmt_list : stmt stmt_list
              | empty
    """
    p[0] = ('stmt_list', p[1])


def p_stmt(p):
    """
    stmt : class_declaration
         | fun_declaration
         | import_declaration
         | assignment
         | variable_declaration
         | print_stmt
         | control_structure
         | empty
    """
    p[0] = ('stmt', p[1])


def p_class_declaration(p):
    """
    class_declaration : CLASS IDENTIFIER LBRACE stmt_list RBRACE
    """
    p[0] = ('class_declaration', p[2], p[4])


def p_fun_declaration(p):
    """
    fun_declaration : FUN IDENTIFIER LPAREN params RPAREN LBRACE stmt_list RBRACE
    """
    p[0] = ('fun_declaration', p[2], p[4], p[7])


def p_params(p):
    """
    params : general_type IDENTIFIER COMMA params
           | general_type IDENTIFIER
           | empty
    """
    if len(p) == 5:
        p[0] = ('params', p[1], p[2], p[4])
    elif len(p) == 3:
        p[0] = ('params', p[1], p[2])
    else:
        p[0] = ('params', p[1])


def p_import_declaration(p):
    """
    import_declaration : IMPORT STRING_LITERAL
    """
    p[0] = ('import_declaration', p[2])


def p_variable_declaration(p):
    """
    variable_declaration : general_type IDENTIFIER SEMICOLON
                         | list_type IDENTIFIER LBRACKET RBRACKET SEMICOLON
                         | array_type IDENTIFIER LBRACE RBRACE SEMICOLON
    """
    p[0] = ('variable_declaration', p[1], p[2])


def p_assignment(p):
    """
    assignment : general_type IDENTIFIER ASSIGN expression SEMICOLON
               | list_type IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression SEMICOLON
               | array_type IDENTIFIER LBRACE expression RBRACE ASSIGN expression SEMICOLON
    """
    p[0] = ('assignment', p[1], p[2], p[4])


def p_print_stmt(p):
    """
    print_stmt : PRINT LPAREN expression RPAREN SEMICOLON
    """
    p[0] = ('print_stmt', p[3])


def p_control_structure(p):
    """
    control_structure : if_stmt
                      | for_stmt
                      | while_stmt
                      | switch_stmt
    """
    p[0] = ('control_structure', p[1])


def p_if_stmt(p):
    """
    if_stmt : IF LPAREN expression RPAREN LBRACE stmt_list RBRACE
            | IF LPAREN expression RPAREN LBRACE stmt_list RBRACE ELSE LBRACE stmt_list RBRACE
            | expression QUESTION expression COLON expression SEMICOLON
    """
    if len(p) == 12:
        p[0] = ('if_stmt', p[3], p[6], p[10])
    elif len(p) == 8:
        p[0] = ('if_stmt', p[3], p[6])
    elif len(p) == 7:
        p[0] = ('if_stmt', p[1], p[3], p[5])


def p_for_stmt(p):
    """
    for_stmt : FOR LPAREN assignment SEMICOLON expression SEMICOLON expression RPAREN LBRACE stmt_list RBRACE
    """
    p[0] = ('for_stmt', p[3], p[5], p[7], p[10])


def p_while_stmt(p):
    """
    while_stmt : WHILE LPAREN expression RPAREN LBRACE stmt_list RBRACE
    """
    p[0] = ('while_stmt', p[3], p[6])


def p_switch_stmt(p):
    """
    switch_stmt : SWITCH LPAREN expression RPAREN LBRACE case_stmts default_stmt RBRACE
    """
    p[0] = ('switch_stmt', p[3], p[6], p[7])


def p_case_stmts(p):
    """
    case_stmts : CASE expression COLON stmt_list case_stmts
               | empty
    """
    p[0] = ('case_stmts', p[2], p[4], p[5])


def p_default_stmt(p):
    """
    default_stmt : DEFAULT COLON stmt_list
                 | empty
    """
    p[0] = ('default_stmt', p[3])


def p_expression(p):
    """
    expression : expression PLUS expression
               | expression MINUS expression
               | expression MULTIPLY expression
               | expression DIVIDE expression
               | expression MODULUS expression
               | expression AND expression
               | expression OR expression
               | expression EQUAL expression
               | expression NOTEQUAL expression
               | expression LESSTHAN expression
               | expression GREATERTHAN expression
               | expression LESSTHANEQUAL expression
               | expression GREATERTHANEQUAL expression
               | expression INCREMENT
               | expression DECREMENT
               | expression POW expression
               | NOT expression
               | LPAREN expression RPAREN
               | IDENTIFIER
               | digit
               | STRING_LITERAL
               | boolean
               | IDENTIFIER LBRACKET expression RBRACKET
               | IDENTIFIER LBRACE expression RBRACE
    """
    if len(p) == 5:
        p[0] = ('expression', p[1], p[3])
    elif len(p) == 4:
        p[0] = ('expression', p[1], p[2], p[3])
    if len(p) == 3:
        p[0] = ('expression', p[1], p[2])
    else:
        p[0] = ('expression', p[1])


def p_digit(p):
    """
    digit : NUMBER
    """
    p[0] = ('digit', p[1])


def p_boolean(p):
    """
    boolean : TRUE
            | FALSE
    """
    p[0] = ('boolean', p[1])


def p_general_type(p):
    """
    general_type : INT
                 | FLOAT
                 | DOUBLE
                 | STRING
                 | BOOLEAN
                 | IDENTIFIER
    """
    p[0] = ('general_type', p[1])


def p_array_type(p):
    """
    array_type : INTARRAY
               | FLOATARRAY
               | STRINGARRAY
               | DOUBLEARRAY
    """
    p[0] = ('array_type', p[1])


def p_list_type(p):
    """
    list_type : INTLIST
              | FLOATLIST
              | STRINGLIST
              | DOUBLELIST
    """
    p[0] = ('list_type', p[1])


def p_empty(p):
    """
    empty :
    """
    p[0] = ('empty',)


def p_error(p):
    print(f'Syntax error at {p.value!r}')


# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('if (true) {}')
print(ast)
