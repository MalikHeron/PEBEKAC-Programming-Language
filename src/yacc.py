from ply.yacc import yacc
from lex import *


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
              | stmt
              | empty
    """
    if len(p) == 3:
        p[0] = ('stmt_list', p[1], p[2])
    elif len(p) == 2:
        p[0] = ('stmt_list', p[1])
    else:
        p[0] = ('stmt_list',)


def p_stmt(p):
    """
    stmt : class_declaration
         | fun_declaration
         | import_declaration
         | assignment
         | variable_declaration
         | print_stmt
         | control_structure
         | return_stmt
         | function_call
         | break_stmt
         | empty
         | comment stmt
    """
    p[0] = p[1]


def p_class_declaration(p):
    """
    class_declaration : CLASS identifier LBRACE stmt_list RBRACE
    """
    p[0] = ('class_declaration', p[2], p[4])


def p_print_stmt(p):
    """
    print_stmt : PRINT LPAREN expression RPAREN SEMICOLON
    """
    p[0] = ('print_stmt', p[3])


def p_fun_declaration(p):
    """
       fun_declaration : general_type FUN identifier LPAREN params RPAREN LBRACE stmt_list RBRACE
                       | FUN identifier LPAREN params RPAREN LBRACE stmt_list RBRACE
    """
    if len(p) == 10:
        # Accounting for return type specification
        p[0] = ('fun_declaration', p[1], p[3], p[5], p[8])
    else:
        p[0] = ('fun_declaration', p[2], p[4], p[7])


def p_function_call(p):
    """
    function_call : identifier LPAREN arg_list RPAREN SEMICOLON
    """
    p[0] = ('function_call', p[1], p[3])


def p_return_stmt(p):
    """
    return_stmt : RETURN expression SEMICOLON
    """
    p[0] = ('return_stmt', p[2])


def p_break_stmt(p):
    """
    break_stmt : BREAK SEMICOLON
    """
    p[0] = (f'{p[1]}_stmt',)


def p_params(p):
    """
    params : general_type identifier COMMA params
           | general_type identifier
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
    variable_declaration : general_type identifier SEMICOLON
                         | list_type identifier LBRACKET RBRACKET SEMICOLON
                         | array_type identifier LBRACE RBRACE SEMICOLON
    """
    p[0] = ('variable_declaration', p[1], p[2])


def p_assignment(p):
    """
    assignment : general_type identifier ASSIGN expression SEMICOLON
               | list_type identifier LBRACKET digit RBRACKET ASSIGN expression SEMICOLON
               | list_type identifier ASSIGN LBRACKET expression RBRACKET SEMICOLON
               | array_type identifier LBRACE digit RBRACE ASSIGN expression SEMICOLON
               | array_type identifier ASSIGN LBRACE expression RBRACE SEMICOLON
               | identifier ASSIGN expression SEMICOLON
    """
    if len(p) == 6:
        p[0] = ('assignment', p[1], p[2], p[4])
    else:
        p[0] = ('assignment', p[1], p[3])


def p_control_structure(p):
    """
    control_structure : if_stmt
                      | for_stmt
                      | while_stmt
                      | switch_stmt
    """
    p[0] = ('control_structure', p[1])


def p_arg_list(p):
    """
    arg_list : expression COMMA arg_list
             | expression
    """
    if len(p) == 4:
        p[0] = ('arg_list', p[1], p[3])
    else:
        p[0] = ('arg_list', p[1])


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
    expression : expression_plus
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
               | expression COMMA expression
               | expression POW expression
               | NOT expression
               | LPAREN expression RPAREN
               | identifier
               | digit
               | string
               | boolean
               | identifier LBRACKET expression RBRACKET
               | identifier LBRACE expression RBRACE
    """

    left = p[1]
    right = p[3] if len(p) > 3 else None
    operator = p[2] if len(p) > 3 else None

    if operator in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULUS', 'POW']:
        # For mathematical operations, check if operands are numerical
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise TypeError("Error: Mathematical operations can only be performed on numerical values")
    elif operator in ['AND', 'OR', 'EQUAL', 'NOTEQUAL', 'LESSTHAN', 'GREATERTHAN', 'LESSTHANEQUAL', 'GREATERTHANEQUAL']:
        # For logical and comparison operations, operands can be of any type
        pass
    elif operator in ['INCREMENT', 'DECREMENT']:
        # For increment and decrement operations, check if operand is numerical
        if not isinstance(left, (int, float)):
            raise TypeError("Error: Increment and decrement operations can only be performed on numerical values")

    if len(p) == 5:
        p[0] = ('expression', p[1], p[3])
    elif len(p) == 4:
        p[0] = ('expression', p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = ('expression', p[1], p[2])
    else:
        p[0] = ('expression', p[1])


def p_expression_plus(p):
    """
    expression_plus : expression PLUS expression
    """
    left = p[1]
    right = p[3]
    if isinstance(left, str) and isinstance(right, str):
        p[0] = left + right
    elif isinstance(left, str) and isinstance(right, (int, float)):
        p[0] = left + str(right)
    elif isinstance(left, (int, float)) and isinstance(right, str):
        p[0] = str(left) + right
    else:
        p[0] = left + right


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
                 | identifier
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


def p_identifier(p):
    """
    identifier : IDENTIFIER
    """
    p[0] = ('identifier', p[1])


def p_comment(p):
    """
    comment : COMMENT
    """
    p[0] = ('comment', p[1])


def p_string_literal(p):
    """
    string : STRING_LITERAL
    """
    p[0] = ('string_literal', p[1])


def p_empty(p):
    """
    empty :
    """
    p[0] = 'empty'


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}, position {p.lexpos}")
    else:
        print("Syntax error at EOF")


# Build the parser
parser = yacc()
