# Define your semantic analysis functions and symbol table here...

# Integrate semantic analysis into the parser...
from yacc import parser

# Define a symbol table to store information about variables and functions
symbol_table = {}

# Define a stack to manage scopes
scope_stack = []


def push_scope():
    # Push a new scope onto the stack
    scope_stack.append({})


def pop_scope():
    # Pop the current scope from the stack
    scope_stack.pop()


def declare_symbol(name, symbol_type):
    # Declare a symbol in the current scope
    scope_stack[-1][name] = symbol_type


def lookup_symbol(name):
    # Look up a symbol in all scopes, starting from the current scope and moving outward
    for scope in reversed(scope_stack):
        if name in scope:
            return scope[name]
    return None


# Now, modify your semantic analysis functions to use these scope management functions.
# For example, when entering a function or class declaration, push a new scope, and when exiting, pop the scope.
# When declaring a variable, use the declare_symbol function.
# When looking up a variable, use the lookup_symbol function.

# Define a function for semantic analysis
def analyze_semantics(node):
    node_type = node[0]

    if node_type == 'program':
        # Perform semantic analysis for the entire program
        push_scope()
        analyze_semantics(node[1])
        pop_scope()

    elif node_type == 'stmt_list':
        # Analyze each statement in the statement list
        for stmt in node[1:]:
            analyze_semantics(stmt)

    elif node_type == 'class_declaration':
        # Add class information to the symbol table
        class_name = node[1]
        if lookup_symbol(class_name):
            raise Exception(f"Error: Class {class_name} already defined")
        else:
            declare_symbol(class_name, {'type': 'class'})

        # Analyze statements inside the class declaration
        push_scope()
        analyze_semantics(node[2])
        pop_scope()


    elif node_type == 'fun_declaration':
        # Add function information to the symbol table
        fun_name = node[2][1] if node[1] else node[1][
            1]  # Extract the actual function name from the identifier non-terminal

        params = node[3] if node[1] else node[2]

        if lookup_symbol(fun_name):
            raise Exception(f"Error: Function {fun_name} already defined")
        else:
            fun_type = node[1][1] if node[1] else None  # Extract the return type if it exists
            declare_symbol(fun_name, {'type': 'function', 'return_type': fun_type, 'params': params})

        # Analyze statements inside the function declaration
        push_scope()

        # First analyze all declarations and initializations
        for stmt in node[4] if node[1] else node[3]:

            if stmt[0] in ['variable_declaration', 'assignment']:
                analyze_semantics(stmt)

        # Then analyze other statements
        for stmt in node[4] if node[1] else node[3]:

            if stmt[0] not in ['variable_declaration', 'assignment']:
                analyze_semantics(stmt)

        pop_scope()

    elif node_type == 'params':
        # Analyze each parameter in the parameter list
        for param in node[1:]:
            analyze_semantics(param)

        # Check if there are multiple parameters with the same name and datatype
        param_names = [param[1] for param in node[1:]]
        param_types = [param[0] for param in node[1:]]
        if len(param_names) != len(set(param_names)) or len(param_types) != len(set(param_types)):
            raise Exception("Error: Function has multiple parameters with the same name and datatype")

    elif node_type == 'import_declaration':
        # Add import information to the symbol table
        module_name = node[1]
        symbol_table[module_name] = {'type': 'module'}

    elif node_type == 'variable_declaration':
        # Extract variable information
        var_type = node[1]
        var_name = node[2][1]  # Extract the actual variable name from the identifier non-terminal

        # Check if the variable is already declared
        if lookup_symbol(var_name):
            raise Exception(f"Error: Variable {var_name} already declared")
        else:
            # Add variable to the symbol table
            declare_symbol(var_name, {'type': var_type})

        # If the variable has an initialization value, analyze it
        if len(node) == 4:
            init_value = node[3]
            # First add the variable to the symbol table, then analyze the initialization
            analyze_semantics(('assignment', var_type, var_name, init_value))

    elif node_type == 'assignment':
        # Check if the variable being assigned is declared
        var_name = node[2][1]  # Extract the actual variable name from the identifier non-terminal
        if not lookup_symbol(var_name):
            raise Exception(f"Error: Variable {var_name} not declared")

        # Check if the assigned value matches the type of the variable
        assigned_value = node[3]
        var_type = lookup_symbol(var_name)['type']
        if isinstance(assigned_value, str) and var_type != 'string':
            raise Exception(f"Error: Type mismatch. Expected {var_type}, got string")
        elif isinstance(assigned_value, int) and var_type != 'int':
            raise Exception(f"Error: Type mismatch. Expected {var_type}, got int")
        elif isinstance(assigned_value, float) and (var_type != 'float' and var_type != 'double'):
            raise Exception(f"Error: Type mismatch. Expected {var_type}, got float")
        elif isinstance(assigned_value, bool) and var_type != 'boolean':
            raise Exception(f"Error: Type mismatch. Expected {var_type}, got boolean")
        elif not isinstance(assigned_value, (str, int, float, bool)) and var_type == 'string':
            raise Exception(f"Error: Type mismatch. Expected {var_type}, got non-string")

    elif node_type == 'if_stmt':
        # Analyze the condition expression
        analyze_semantics(node[1])

        # Analyze statements in the if block
        push_scope()
        analyze_semantics(node[2])
        pop_scope()

        # If there's an else block, analyze its statements too
        if len(node) == 4:
            push_scope()
            analyze_semantics(node[3])
            pop_scope()

    elif node_type == 'while_stmt':
        # Analyze the condition expression
        analyze_semantics(node[1])

        # Analyze statements in the while loop body
        push_scope()
        analyze_semantics(node[2])
        pop_scope()

    elif node_type == 'for_stmt':
        # Check if initial assignment, condition, and increment are valid...
        init_type = get_assignment_type(node[1])
        cond_type = get_expression_type(node[2])
        incr_type = get_expression_type(node[3])
        if init_type is None or cond_type != 'boolean' or incr_type is None:
            raise ValueError(
                f"Invalid for statement: init_type={init_type}, cond_type={cond_type}, incr_type={incr_type}")

            # Check if the variable in the initial assignment is not used in the condition and increment
        init_var = node[1][2][1]  # Extract the variable name from the initial assignment
        if not (init_var in str(node[2]) and init_var in str(node[3])):
            raise ValueError(
                f"Variable {init_var} in the initial assignment is not used correctly in the condition and increment")

        # Analyze statements in the for block
        push_scope()
        analyze_semantics(node[1])  # Analyze the initialization part in the new scope
        analyze_semantics(node[2])  # Analyze the loop body in the new scope
        pop_scope()

    elif node_type == 'class_method':
        # Analyze statements inside the method
        push_scope()
        analyze_semantics(node[2])
        pop_scope()

    elif node_type == 'print_stmt':
        # Analyze expression(s) in print statement
        for expr in node[1:]:
            analyze_semantics(expr)

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

    elif node_type == 'fun_call':
        fun_name = node[1][1]  # Extract the actual function name from the identifier non-terminal
        args = node[2]

        # Check if the function is declared
        fun_info = lookup_symbol(fun_name)
        if not fun_info or fun_info['type'] != 'function':
            raise Exception(f"Error: Function {fun_name} not declared")

        # Check if the function is a method of the correct class
        if 'class' in fun_info and (not args or lookup_symbol(args[0])['type'] != fun_info['class']):
            raise Exception(f"Error: Method {fun_name} called on an instance of the wrong class")

        # Check if the function is from an imported module and used correctly
        if 'module' in fun_info and not args:
            raise Exception(f"Error: Function {fun_name} from module {fun_info['module']} used incorrectly")

        # Check if the number and types of arguments match the function declaration
        declared_params = fun_info['params']
        if len(args) != len(declared_params):
            raise Exception(f"Error: Incorrect number of arguments for function {fun_name}")
        for arg, declared_param in zip(args, declared_params):
            if get_expression_type(arg) != declared_param['type']:
                raise Exception(f"Error: Incorrect type of argument for function {fun_name}")

    elif node_type == 'return_stmt':
        expr = node[1]

        # Check if the return statement is inside a function
        if 'function' not in [info['type'] for info in reversed(scope_stack)]:
            raise Exception("Error: Return statement not inside a function")

        # Check if the type of the returned expression matches the function's return type
        fun_info = next(info for info in reversed(scope_stack) if info['type'] == 'function')
        if get_expression_type(expr) != fun_info['return_type']:
            raise Exception("Error: Return type does not match function's return type")

    elif node_type == 'break_continue_stmt':
        stmt_type = node[1]

        # Check if the break or continue statement is inside a loop
        if 'loop' not in [info['type'] for info in reversed(scope_stack)]:
            raise Exception(f"Error: {stmt_type} statement not inside a loop")

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
    print(ast)
    analyze_semantics(ast)
    return ast

# ... rest of your code ...
