from ply.lex import lex

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
    'MODASSIGN', 'COLON', 'QUESTION', 'BOOLEAN', 'COMMENT'
]

# States
states = (
    ('comment', 'exclusive'),
)

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
t_ARROW = r'->'

# Ignored characters
t_ignore = ' \t'


# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t


# Defining float Values
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r'true|false'
    t.value = (t.value == 'true')  # Convert the string to a Python boolean
    return t

def t_STRING_LITERAL(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # Remove the quotation marks
    return t



# Start of a comment
def t_comment(t):
    r'//.*|/\*|\#.*'
    if t.value.startswith('/*'):
        t.lexer.comment_text = t.value[2:]  # Save the text of the comment
        t.lexer.begin('comment')
    else:
        t.type = 'COMMENT'
        return t


# Inside a comment
def t_comment_COMMENT(t):
    r'.|\n'
    t.lexer.comment_text += t.value  # Add the text to the comment


# End of a comment
def t_comment_end(t):
    r'\*/'
    t.lexer.lineno += t.value.count('\n')
    t.lexer.begin('INITIAL')
    t.value = t.lexer.comment_text  # Use the accumulated text for the token
    t.type = 'COMMENT'
    return t


# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


def find_column(t):
    line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if line_start < 0:
        line_start = 0
    return (t.lexpos - line_start) + 1


# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]} at line no: {t.lineno} col: {find_column(t)}')
    t.lexer.skip(1)


# Build the lexer object
lexer = lex()
