# -----------------------------------------------------------------------------
# example.py
#
# Example of using PLY To parse the following simple grammar.
#
#   expression : term PLUS term
#              | term MINUS term
#              | term
#
#   term       : factor TIMES factor
#              | factor DIVIDE factor
#              | factor
#
#   factor     : NUMBER
#              | NAME
#              | PLUS factor
#              | MINUS factor
#              | LPAREN expression RPAREN
#
# -----------------------------------------------------------------------------

from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer

# All tokens must be named in advance.
tokens = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'ASSIGN',
          'NAME', 'NUMBER', 'MOD', 'EQUAL', 'NOTEQUAL', 'LESSTHAN', 'GREATERTHAN', 'LESSTHANEQUAL',
          'GREATERTHANEQUAL', 'AND', 'OR', 'NOT', 'IF', 'ELSE', 'WHILE', 'FOR', 'RETURN', 'PRINT', 'INPUT', 'FUNCTION',
          'CLASS', 'NEW', 'NULL', 'TRUE', 'FALSE', 'COMMA', 'SEMICOLON', 'COLON', 'DOT', 'LBRACE', 'RBRACE', 'LBRACKET',
          'RBRACKET', 'ARROW', 'ASSIGN', 'INCREMENT', 'DECREMENT', 'POW', 'BACKSLASH', 'SLASH', 'APOSTROPHE', 'AT',
          'HASH', 'DOUBLEQUOTE', 'UNDERSCORE', 'PIPE', 'PLUSASSIGN', 'MINUSASSIGN', 'TIMESASSIGN', 'DIVIDEASSIGN',
          'MODASSIGN')

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_MOD = r'%'
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_LESSTHANEQUAL = r'<='
t_GREATERTHANEQUAL = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_FOR = r'for'
t_RETURN = r'return'
t_PRINT = r'print'
t_INPUT = r'input'
t_FUNCTION = r'fun'
t_CLASS = r'class'
t_NEW = r'new'
t_NULL = r'null'
t_TRUE = r'true'
t_FALSE = r'false'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_DOT = r'\.'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ASSIGN = r'='
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_POW = r'\*\*'
t_AT = r'@'
t_HASH = r'\#'
t_BACKSLASH = r'\\'
t_SLASH = r'/'
t_APOSTROPHE = r'\''
t_DOUBLEQUOTE = r'\"'
t_UNDERSCORE = r'_'
t_PIPE = r'\|'
t_PLUSASSIGN = r'\+='
t_MINUSASSIGN = r'-='
t_TIMESASSIGN = r'\*='
t_DIVIDEASSIGN = r'/='
t_MODASSIGN = r'%='

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


# Ignored token with an action associated with it
def t_ignore_newline(t):
    r"""\n+"""
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
def p_expression(p):
    """
    expression : term PLUS term
               | term MINUS term
               | term EQUAL term
               | term NOTEQUAL term
               | term LESSTHAN term
               | term GREATERTHAN term
               | term LESSTHANEQUAL term
               | term GREATERTHANEQUAL term
               | term AND term
               | term OR term
    """
    # p is a sequence that represents rule contents.
    #
    # expression : term PLUS term
    #   p[0]     : p[1] p[2] p[3]
    #
    p[0] = ('binop', p[2], p[1], p[3])


def p_expression_term(p):
    """
    expression : term
    """
    p[0] = p[1]


def p_term(p):
    """
    term : factor TIMES factor
         | factor DIVIDE factor
         | factor MOD factor
         | factor ASSIGN factor
         | factor EQUAL factor
         | factor NOTEQUAL factor
         | factor LESSTHAN factor
         | factor GREATERTHAN factor
         | factor LESSTHANEQUAL factor
         | factor GREATERTHANEQUAL factor
         | factor AND factor
         | factor OR factor
    """
    p[0] = ('binop', p[2], p[1], p[3])


def p_term_factor(p):
    """
    term : factor
    """
    p[0] = p[1]


def p_factor_number(p):
    """
    factor : NUMBER
    """
    p[0] = ('number', p[1])


def p_factor_name(p):
    """
    factor : NAME
    """
    p[0] = ('name', p[1])


def p_factor_unary(p):
    """
    factor : PLUS factor
           | MINUS factor
           | NOT factor
           | ASSIGN factor
           | INCREMENT factor
           | DECREMENT factor
           | EQUAL factor
           | NOTEQUAL factor
           | LESSTHAN factor
           | GREATERTHAN factor
           | LESSTHANEQUAL factor
           | GREATERTHANEQUAL factor
           | AND factor
           | OR factor
    """
    p[0] = ('unary', p[1], p[2])


def p_factor_grouped(p):
    """
    factor : LPAREN expression RPAREN
    """
    p[0] = ('grouped', p[2])


def p_error(p):
    print(f'Syntax error at {p.value!r}')


# Build the parser
parser = yacc()

# Parse an expression
ast = parser.parse('(3 + 5) = 8')
print(ast)
