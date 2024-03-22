# Define your semantic analysis functions and symbol table here...

# Integrate semantic analysis into the parser...
from yacc import parser

# Define a symbol table to store information about variables and functions
symbol_table = {}


# Define a function for semantic analysis
def analyze_semantics(node):
    node_type = node[0]

    if node_type == 'program':
        # Perform semantic analysis for the entire program
        analyze_semantics(node[1])

    elif node_type == 'stmt_list':
        # Analyze each statement in the statement list
        for stmt in node[1:]:
            analyze_semantics(stmt)

    elif node_type == 'class_declaration':
        # Add class information to the symbol table
        class_name = node[1]
        symbol_table[class_name] = {'type': 'class'}

        # Analyze statements inside the class declaration
        analyze_semantics(node[2])

    elif node_type == 'fun_declaration':
        # Add function information to the symbol table
        fun_name = node[1]
        params = node[2]
        symbol_table[fun_name] = {'type': 'function', 'params': params}

        # Analyze statements inside the function declaration
        analyze_semantics(node[3])

    elif node_type == 'params':
        # Analyze each parameter in the parameter list
        for param in node[1:]:
            analyze_semantics(param)

    elif node_type == 'import_declaration':
        # Add import information to the symbol table
        module_name = node[1]
        symbol_table[module_name] = {'type': 'module'}

    elif node_type == 'variable_declaration':
        # Add variable information to the symbol table
        var_type = node[1]
        var_name = node[2]
        symbol_table[var_name] = {'type': var_type}

    elif node_type == 'assignment':
        var_type = node[1] if is_type(symbol_table, node[1]) else None
        var_name = node[2] if var_type else node[1]
        expr = node[3] if var_type else node[2]

        if var_name in symbol_table:
            # If variable is already in symbol table, check if types match
            existing_type = symbol_table[var_name]['type']

            if var_type and existing_type != var_type:
                raise TypeError(
                    f"Type mismatch: {var_name} is already declared as type {existing_type}, cannot redeclare as {var_type}")
        else:
            # If variable is not in symbol table, add it
            symbol_table[var_name] = {'type': var_type}

        # Check if the type of the expression matches the variable's type
        expr_type = get_expression_type(expr)
        if expr_type != symbol_table[var_name]['type']:
            raise TypeError(
                f"Type mismatch: {var_name} is of type {var_type}, but assigned expression is of type {expr_type}")

    elif node_type == 'print_stmt':
        # Check if expression is valid...
        expr_type = get_expression_type(node[1])
        if expr_type is None:
            raise ValueError(f"Invalid expression in print statement: {node[1]}")

    elif node_type == 'if_stmt':
        # Check if condition is a boolean expression...
        cond_type = get_expression_type(node[1])
        if cond_type != 'boolean':
            raise TypeError(f"Condition in if statement must be a boolean expression, not {cond_type}")

    elif node_type == 'for_stmt':
        # Check if initial assignment, condition, and increment are valid...
        init_type = get_assignment_type(node[1])
        cond_type = get_expression_type(node[2])
        incr_type = get_expression_type(node[3])
        if init_type is None or cond_type != 'boolean' or incr_type is None:
            raise ValueError(
                f"Invalid for statement: init_type={init_type}, cond_type={cond_type}, incr_type={incr_type}")

    # Add more semantic analysis rules for other language construct


def is_type(symbol_table, type_candidate):
    # Check if a given string is a type in the symbol table.
    for symbol, attributes in symbol_table.items():
        if attributes['type'] == type_candidate:
            return True
    return False


def get_expression_type(expr):
    # Determine the type of an expression.
    expr_type = expr[0]

    if expr_type == 'expression':
        # Assuming the type of an expression is the type of its first operand
        return get_expression_type(expr[1])

    elif expr_type == 'digit':
        return 'int' or 'float'

    elif expr_type == 'boolean':
        return 'boolean'

    elif expr_type == 'identifier':
        # Look up the identifier in the symbol table
        identifier = expr[1]
        if identifier in symbol_table:
            return symbol_table[identifier]['type']
        else:
            raise NameError(f"Identifier {identifier} is not defined")
    else:
        pass


def get_assignment_type(assignment):
    """
    Determine the type of an assignment.
    """
    assignment_type = assignment[0]

    if assignment_type == 'assignment':
        var_name = assignment[2]
        if var_name in symbol_table:
            return symbol_table[var_name]['type']
        # else:
        # raise NameError(f"Variable {var_name} is not defined")
    else:
        pass


# Integrate semantic analysis into the parser
def parse_and_analyze(program):
    ast = parser.parse(program)
    analyze_semantics(ast)
    return ast
