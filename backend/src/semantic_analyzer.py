# Define your semantic analysis functions and symbol table here...

# Integrate semantic analysis into the parser...
from yacc import parser

# Define a symbol table to store information about variables and functions
symbol_table = {}

# Define a stack to manage scopes
scope_stack = []

assigned_value = None
in_loop = False
in_function = False


def is_in_function(boolean):
    global in_function
    in_function = boolean


def looping(value):
    global in_loop
    in_loop = value


# Modify push_scope() and pop_scope() functions to include the current function name
def push_scope(function_name=None):
    # Push a new scope onto the stack
    scope_stack.append({'function_name': function_name})


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


# # Define functions to manage the symbol table and scope stack
def reset_symbol_table_and_scope_stack():
    global symbol_table, scope_stack
    symbol_table = {}
    scope_stack = []


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

    elif node_type == 'fun_declaration':
        # Add function information to the symbol table
        fun_name = None
        return_type = None
        params = None

        if len(node) == 4:
            fun_name = node[1][1]  # Extract the actual function name from the identifier non-terminal
            return_type = 'void'
            params = node[2]
        elif len(node) == 5:
            fun_name = node[2][1]  # Extract the actual function name from the identifier non-terminal
            return_type = node[1][1]
            params = node[3]

        if lookup_symbol(fun_name):
            raise Exception(f"Error: Function {fun_name} already defined")
        else:
            declare_symbol(fun_name, {'type': 'function', 'return_type': return_type, 'params': params})

        # Analyze statements inside the function declaration
        push_scope(function_name=fun_name)
        is_in_function(True)
        analyze_semantics(node[-1])  # Changed to analyze last part of the function declaration
        pop_scope()
        is_in_function(False)

        # Check if the function has a return type but no return statement
        if return_type != 'void':
            has_return_stmt = False
            for stmt in node[-1][1:]:
                if stmt[0] == 'return_stmt':
                    has_return_stmt = True
                    break
            if not has_return_stmt:
                raise Exception(f"Error: Function {fun_name} has a return type but no return statement")

    elif node_type == 'params':
        # Analyze each parameter in the parameter list
        for param in node[1:]:
            analyze_semantics(param)

        # Check if there are multiple parameters with the same name and datatype
        param_names = [param[1] for param in node[1:]]
        param_types = [param[0] for param in node[1:]]
        if len(param_names) != len(set(param_names)) or len(param_types) != len(set(param_types)):
            raise Exception("Error: Function has multiple parameters with the same name and datatype")

    elif node_type == 'variable_declaration':
        # Extract variable information
        var_type = node[1][1]
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
        global assigned_value, expr
        if node[1][0] == 'general_type' or node[1][0] == 'list_type' or node[1][0] == 'array_type':
            # Check if the variable being assigned is declared
            var_name = node[2][1]  # Extract the actual variable name from the identifier non-terminal
            var_type = node[1][1]

            if node[3][0] == 'function_call':
                analyze_semantics(node[3])
            elif node[3] == 'null':
                assigned_value = node[3]
            else:
                assigned_value = node[3][1][1]

            # Check if the variable being assigned is declared
            if not lookup_symbol(var_name):
                # Add variable to the symbol table
                declare_symbol(var_name, {'type': var_type})
            elif lookup_symbol(var_name):
                raise Exception(f"Error: Variable {var_name} already declared")
        else:
            # Extract variable information
            var_type = lookup_symbol(node[1][1])['type']
            var_name = node[1][1]  # Extract the actual variable name from the identifier non-terminal

            # Check if the variable being assigned is declared
            if not lookup_symbol(var_name):
                raise Exception(f"Error: Variable {var_name} not declared")
            elif lookup_symbol(var_name):
                # Check if the assigned value matches the type of the variable
                if node[2][0] == 'function_call':
                    analyze_semantics(node[2])
                elif node[2] == 'null':
                    assigned_value = node[2]
                else:
                    assigned_value = node[2][1][1]

        # Check if the assigned value matches the type of the variable
        if len(node) == 3 and node[2][0] == 'function_call' or len(node) == 4 and node[3][0] == 'function_call':
            pass  # Allow the return type checking to be done by python compiler
        elif assigned_value == 'null':
            pass
        else:
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

    elif node_type == 'expression':
        # Handle expression nodes
        get_expression_type(node[1])  # Analyze left operand

        if len(node) == 4:  # Binary operation
            operator = node[2]
            analyze_semantics(operator)  # Analyze operator
            analyze_semantics(node[3])  # Analyze right operand

    elif node_type == 'control_structure':
        # Analyze the control structure
        analyze_semantics(node[1])

    elif node_type == 'if_stmt' or node_type == 'while_stmt':
        # Analyze the condition expression
        analyze_semantics(node[1])

        # Analyze statements in the if block
        push_scope()
        analyze_semantics(node[2])
        pop_scope()

        # If there's an else block, analyze its statements too
        if node_type == 'if_stmt' and len(node) == 4:
            push_scope()
            analyze_semantics(node[3])
            pop_scope()

    elif node_type == 'while_stmt':
        # Analyze the condition expression
        analyze_semantics(node[1])

        # Analyze statements in the while loop body
        push_scope()
        looping(True)
        analyze_semantics(node[2])
        looping(False)
        pop_scope()

    elif node_type == 'for_stmt':
        # Analyze Assignment expression
        analyze_semantics(node[1])
        analyze_semantics(node[2])
        analyze_semantics(node[3])

        # Analyze statements in the for loop body
        push_scope()
        looping(True)
        analyze_semantics(node[4])
        looping(False)
        pop_scope()

    elif node_type == 'print_stmt':
        # Analyze expression(s) in print statement
        for expr in node[1:]:
            # Check if the expression is an identifier
            if expr[0] == 'function_call':
                # Analyze the function call expression
                analyze_semantics(expr)

        # Check the type of the expression
        expr_type = get_expression_type(node[1])

        # Check if expression is valid...
        if expr_type is None:
            raise ValueError(f"Invalid expression in print statement: {expr}")

    elif node_type == 'function_call':
        fun_name = node[1][1]  # Extract the actual function name from the identifier non-terminal
        arg_list = node[2]
        fun_info = lookup_symbol(fun_name)

        # Check if the arguments are expressions
        def count_args(arg_node):
            if isinstance(arg_node, tuple) and arg_node[0] == 'arg_list':
                if arg_node[1] == 'empty':
                    return 0
                else:
                    return sum(count_args(arg) for arg in arg_node[1:])
            else:
                return 1

        num_args = count_args(arg_list)

        if fun_info is None:
            raise Exception(f"Error: Function {fun_name} not defined")
        else:
            params = fun_info['params']

            # Count the number of parameters in the function declaration
            def count_params(param_node):
                if isinstance(param_node, tuple) and param_node[0] == 'params':
                    if param_node[1] == 'empty':
                        return 0
                    else:
                        # If the node is a 'params' node, count the identifier and recursively count the rest of the
                        # parameters
                        return 1 + count_params(param_node[3]) if len(param_node) > 3 else 1

            num_params = count_params(params)
            if num_args != num_params:
                raise Exception(
                    f"Error: Number of arguments in function call ({num_args}) does not match the number of "
                    f"parameters in function declaration ({num_params})")

    elif node_type == 'return_stmt':
        # First, find out the current function's name from the scope stack
        current_function_name = scope_stack[-1]['function_name']

        # Find the function's expected return type
        function_info = lookup_symbol(current_function_name)
        expected_return_type = function_info['return_type'][1]

        # Then, check the type of the return expression
        return_expr_type = get_expression_type(node[1])['type']
        if return_expr_type != expected_return_type:
            raise Exception(
                f"Return type mismatch in function {current_function_name}: Expected {'void' if expected_return_type == 'o' else expected_return_type}, got {return_expr_type}"
            )

    elif node_type == 'break_stmt':
        if in_loop is False:
            raise Exception("Error: break statement not inside loop or switch")

    # Add more semantic analysis rules for other language constructs


def get_expression_type(expr):
    # Determine the type of expression.
    expr_type = expr[0]
    print('expr_type:', expr_type, ', expr:', expr)

    if expr_type == 'expression':
        analyze_semantics(expr)  # Analyze right operand
        return get_expression_type(expr[1])

    elif expr_type == 'digit':
        return 'int' or 'float'

    elif expr_type == 'boolean':
        return 'boolean'

    elif expr_type == 'string' or expr_type == 'string_literal':
        return 'string'

    elif expr_type == 'identifier':
        # Look up the identifier in the symbol table
        identifier = expr[1]
        if lookup_symbol(identifier):
            return lookup_symbol(identifier)
        else:
            raise NameError(f"Identifier {identifier} is not defined")

    elif expr_type == 'function_call':
        # Look up the function in the symbol table
        fun_name = expr[1][1]
        fun_info = lookup_symbol(fun_name)
        if fun_info:
            return fun_info
        else:
            raise NameError(f"Function {fun_name} is not defined")
    else:
        pass


def analyze_expression(expr_node):
    expr_type = expr_node[0]

    if expr_type in ('EQUAL', 'NOTEQUAL', 'LESSTHAN', 'GREATERTHAN', 'LESSTHANEQUAL', 'GREATERTHANEQUAL'):
        # Analyze comparison expressions
        analyze_comparison_expression(expr_node)
    elif expr_type == 'identifier':
        # Look up the identifier in the symbol table
        identifier = expr_node[1]
        if not lookup_symbol(identifier):
            raise NameError(f"Identifier '{identifier}' is not defined")


def analyze_comparison_expression(expr_node):
    # Analyze the operands of the comparison expression
    analyze_semantics(expr_node[1])
    analyze_semantics(expr_node[3])


# Integrate semantic analysis into the parser
def parse_and_analyze(program):
    ast = parser.parse(program)
    print(ast)
    # Reset the symbol table and scope stack before each analysis
    reset_symbol_table_and_scope_stack()
    analyze_semantics(ast)
    return ast
