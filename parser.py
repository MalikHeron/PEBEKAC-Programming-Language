from ply.yacc import yacc


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
    stmt : fun_declaration
         | variable_declaration
         | assignment
         | print_stmt
         | len_stmt SEMICOLON
         | control_structure
         | function_call SEMICOLON
         | return_stmt
         | break_stmt
         | comment stmt
         | empty
    """
    p[0] = p[1]


def p_fun_declaration(p):
    """
       fun_declaration : FUN return_type identifier LPAREN params RPAREN LBRACE stmt_list RBRACE
                       | FUN identifier LPAREN params RPAREN LBRACE stmt_list RBRACE
    """
    if len(p) == 10:
        # Accounting for return type specification
        p[0] = ('fun_declaration', p[2], p[3], p[5], p[8])
    else:
        p[0] = ('fun_declaration', p[2], p[4], p[7])


def p_params(p):
    """
    params : param
           | empty
    """
    p[0] = ('params', p[1])


def p_param(p):
    """
    param : general_type identifier COMMA param
          | general_type identifier
          | list_type identifier COMMA param
          | list_type identifier
          | array_type identifier COMMA param
          | array_type identifier
          | empty
    """
    if len(p) == 5:
        p[0] = ('param', p[1], p[2], p[4])
    elif len(p) == 3:
        p[0] = ('param', p[1], p[2])
    else:
        p[0] = ('param', p[1])


def p_len_stmt(p):
    """
    len_stmt : LEN LPAREN identifier RPAREN
    """
    p[0] = ('len_stmt', p[3])


def p_print_stmt(p):
    """
    print_stmt : PRINT LPAREN expression RPAREN SEMICOLON
                | PRINT LPAREN expression COMMA function_call COMMA expression RPAREN SEMICOLON
                | PRINT LPAREN expression COMMA function_call RPAREN SEMICOLON
                | PRINT LPAREN function_call RPAREN SEMICOLON
    """
    if len(p) == 6:
        p[0] = ('print_stmt', p[3])
    elif len(p) == 8:
        p[0] = ('print_stmt', p[3], p[5])
    elif len(p) == 7:
        p[0] = ('print_stmt', p[3], p[5])
    else:
        p[0] = ('print_stmt', p[2])


def p_function_call(p):
    """
    function_call : identifier LPAREN arg_list RPAREN
    """
    p[0] = ('function_call', p[1], p[3])


def p_arg_list(p):
    """
    arg_list : expression COMMA arg_list
             | expression
             | empty
    """
    if len(p) == 4:
        p[0] = ('arg_list', p[1], p[3])
    else:
        p[0] = ('arg_list', p[1])


def p_return_stmt(p):
    """
    return_stmt : RETURN expression SEMICOLON
    """
    p[0] = ('return_stmt', p[2])


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
               | general_type identifier ASSIGN NULL SEMICOLON
               | general_type identifier ASSIGN function_call SEMICOLON
               | list_type identifier ASSIGN NULL SEMICOLON
               | list_type identifier ASSIGN function_call SEMICOLON
               | list_type identifier ASSIGN LBRACKET expression RBRACKET SEMICOLON
               | list_type identifier LBRACKET digit RBRACKET ASSIGN function_call SEMICOLON
               | list_type identifier LBRACKET digit RBRACKET ASSIGN NULL SEMICOLON
               | list_type identifier LBRACKET digit RBRACKET ASSIGN expression SEMICOLON
               | array_type identifier ASSIGN NULL SEMICOLON
               | array_type identifier ASSIGN function_call SEMICOLON
               | array_type identifier LBRACKET digit RBRACKET ASSIGN NULL SEMICOLON
               | array_type identifier LBRACKET digit RBRACKET ASSIGN expression SEMICOLON
               | array_type identifier LBRACKET digit RBRACKET ASSIGN function_call SEMICOLON
               | array_type identifier ASSIGN LBRACE expression RBRACE SEMICOLON
               | identifier assignment_sign expression SEMICOLON
               | identifier assignment_sign function_call SEMICOLON
               | identifier ASSIGN NULL SEMICOLON
               | identifier ASSIGN len_stmt SEMICOLON
    """
    if len(p) == 5:
        p[0] = ('assignment', p[1], p[2], p[3])  # identifier, sign, value
    elif len(p) == 6:
        p[0] = ('assignment', p[1], p[2], p[4])
    elif len(p) == 8:
        if p[7][0] == 'function_call':
            p[0] = ('assignment', p[1], p[2], p[7])
        else:
            p[0] = ('assignment', p[1], p[2], p[5])
    elif len(p) == 9:
        p[0] = ('assignment', p[1], p[2], p[7])


def p_control_structure(p):
    """
    control_structure : if_stmt
                      | for_stmt
                      | while_stmt
    """
    p[0] = ('control_structure', p[1])


def p_break_stmt(p):
    """
    break_stmt : BREAK SEMICOLON
    """
    p[0] = (f'{p[1]}_stmt',)


def p_comment(p):
    """
    comment : COMMENT
    """
    p[0] = ('comment', p[1])


def p_return_type(p):
    """
    return_type : general_type
                | array_type
                | list_type
                | VOID
    """
    p[0] = ('return_type', p[1])


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
       for_stmt : FOR LPAREN variable_declaration expression SEMICOLON expression RPAREN LBRACE stmt_list RBRACE
                | FOR LPAREN assignment expression SEMICOLON expression RPAREN LBRACE stmt_list RBRACE
    """
    p[0] = ('for_stmt', p[3], p[4], p[6], p[9])


def p_while_stmt(p):
    """
    while_stmt : WHILE LPAREN expression RPAREN LBRACE stmt_list RBRACE
    """
    p[0] = ('while_stmt', p[3], p[6])


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
               | expression COMMA expression
               | expression POW expression
               | expression PLUSASSIGN expression
               | expression MINUSASSIGN expression
               | expression TIMESASSIGN expression
               | expression DIVIDEASSIGN expression
               | expression MODASSIGN expression
               | LPAREN expression RPAREN
               | NOT expression
               | identifier
               | digit
               | string
               | boolean
               | array_access
               | function_call
               | len_stmt
               | NULL
    """

    left = p[1]
    right = p[3] if len(p) > 3 else None
    operator = p[2] if len(p) > 3 else None

    if operator in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULUS', 'POW', 'TIMESASSIGN', 'PLUSASSIGN', 'MINUSASSIGN',
                    'DIVIDEASSIGN', 'MODASSIGN']:
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


def p_assignment_sign(p):
    """
    assignment_sign : ASSIGN
                    | DIVIDEASSIGN
                    | MINUSASSIGN
                    | MODASSIGN
                    | PLUSASSIGN
                    | TIMESASSIGN
    """
    p[0] = ('assignment_sign', p[1])


def p_digit(p):
    """
    digit : NUMBER
          | FLOAT
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


def p_string_literal(p):
    """
    string : STRING_LITERAL
    """
    p[0] = ('string_literal', p[1])


def p_array_access(p):
    """
    array_access : identifier LBRACKET expression RBRACKET
    """
    p[0] = ('array_access', p[1], p[3])


def p_empty(p):
    """
    empty :
    """
    p[0] = 'empty'


def p_error(p):
    print(p)
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}' on line {p.lineno}, position {p.lexpos}")
    else:
        raise SyntaxError("Syntax error at EOF")


# Create the parser object
yaccBuilder = yacc
