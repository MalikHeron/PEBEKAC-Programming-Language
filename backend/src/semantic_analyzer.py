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


# Define functions to manage the symbol table and scope stack
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

    elif node_type == 'class_declaration':
        # Add class information to the symbol table
        class_name = node[1]
        if lookup_symbol(class_name):
            raise Exception(f"Error: Class {class_name} already defined")
        else:
            declare_symbol(class_name, {'type': 'class'})
            print(f'added to symbol_table: {class_name}')

        # Analyze statements inside the class declaration
        push_scope()
        analyze_semantics(node[2])
        pop_scope()

    elif node_type == 'fun_declaration':
        # Add function information to the symbol table
        fun_name = None
        params = None

        if len(node) == 4:
            fun_name = node[1][1]  # Extract the actual function name from the identifier non-terminal
            print(f'fun_name: {fun_name}')
            params = node[2]
            print(f'params: {params}')
        elif len(node) == 5:
            print(f'Node Values now: {node[3]}')
            fun_name = node[2][1]  # Extract the actual function name from the identifier non-terminal
            print(f'fun_name: {fun_name}')
            params = node[3]
            print(f'params: {params}')

        if lookup_symbol(fun_name):
            raise Exception(f"Error: Function {fun_name} already defined")
        else:
            declare_symbol(fun_name, {'type': 'function', 'params': params})
            print(f'added to symbol_table: {fun_name}')

        # Analyze statements inside the function declaration
        push_scope()
        is_in_function(True)
        pop_scope()
        is_in_function(False)

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
        var_type = node[1][1]
        print(f'var_type: {var_type}')
        var_name = node[2][1]  # Extract the actual variable name from the identifier non-terminal
        print(f'var_name: {var_name}')
        # Check if the variable is already declared
        if lookup_symbol(var_name):
            raise Exception(f"Error: Variable {var_name} already declared")
        else:
            # Add variable to the symbol table
            declare_symbol(var_name, {'type': var_type})
            print(f'added to symbol_table: {var_name}')

        # If the variable has an initialization value, analyze it
        if len(node) == 4:
            init_value = node[3]
            # First add the variable to the symbol table, then analyze the initialization
            analyze_semantics(('assignment', var_type, var_name, init_value))

    elif node_type == 'assignment':
        global assigned_value
        if node[1][0] == 'general_type' or node[1][0] == 'list_type' or node[1][0] == 'array_type':
            # Check if the variable being assigned is declared
            var_name = node[2][1]  # Extract the actual variable name from the identifier non-terminal
            print(f'assignment var_name: {var_name}')
            # Check if the assigned value matches the type of the variable

            if node[3][0] == 'function_call':
                print(f'assigned_value is a: {node[3][0]}')
                analyze_semantics(node[3])

            assigned_value = node[3][1][1]
            print(f'assigned_value: {assigned_value}')
            # Extract variable information
            var_type = node[1][1]
            print(f'assigned var_type: {var_type}')

            if not lookup_symbol(var_name):
                # Add variable to the symbol table
                declare_symbol(var_name, {'type': var_type})
            elif lookup_symbol(var_name):
                raise Exception(f"Error: Variable {var_name} already declared")
        else:
            # Extract variable information
            var_type = lookup_symbol(node[1][1])['type']

            # Check if the variable being assigned is declared
            var_name = node[1][1]  # Extract the actual variable name from the identifier non-terminal
            print(f'assignment var_name: {var_name}')

            if not lookup_symbol(var_name):
                raise Exception(f"Error: Variable {var_name} not declared")
            elif lookup_symbol(var_name):
                # Check if the assigned value matches the type of the variable
                if node[2][0] == 'function_call':
                    print(f'assigned_value is a: {node[3][0]}')
                    analyze_semantics(node[2])

                assigned_value = node[2][1][1]
                print(f'assigned_value: {assigned_value}')
                var_type = lookup_symbol(var_name)['type']
                print(f'assigned var_type: {var_type}')

        if len(node) == 3 and node[2][0] == 'function_call' or len(node) == 4 and node[3][0] == 'function_call':
            pass  # allow the return type checking to be done by python compiler
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

    elif node_type == 'control_structure':
        # Analyze the control structure
        analyze_semantics(node[1])

    elif node_type == 'if_stmt' or node_type == 'while_stmt':
        # Analyze the condition expression
        if len(node[1]) == 2:
            # Analyze the condition expression
            expression_type = node[1][1][0]
            var = node[1][1][1]
            print(f'expression_type: {expression_type}')
            print(f'var: {var}')
            if expression_type == 'identifier' and not lookup_symbol(var):
                raise Exception(f"Error: Variable {var} not declared")
        else:
            # Analyze the condition expression
            expression_type = node[1][1][1][0]
            var = node[1][1][1][1]
            print(f'expression_type: {expression_type}')
            print(f'var: {var}')
            if expression_type == 'identifier' and not lookup_symbol(var):
                raise Exception(f"Error: Variable {var} not declared")
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

    # elif node_type == 'class_method':
    #     # Analyze statements inside the method
    #     push_scope()
    #     analyze_semantics(node[2])
    #     pop_scope()

    elif node_type == 'print_stmt':
        # Analyze expression(s) in print statement
        for expr in node[1:]:
            analyze_semantics(expr)

        # Check if expression is valid...
        expr_type = get_expression_type(node[1])
        if expr_type is None:
            raise ValueError(f"Invalid expression in print statement: {node[1]}")

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
        print(f'fun_call: {fun_name}')
        print(f'arg_list: {arg_list}')
        print(f'Number of arguments: {num_args}')

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
            print(f'params: {params}')
            print(f'Number of params: {num_params}')
            if num_args != num_params:
                raise Exception(
                    f"Error: Number of arguments in function call ({num_args}) does not match the number of "
                    f"parameters in function declaration ({num_params})")
        # Analyze statements inside the function declaration
        push_scope()

    elif node_type == 'input_stmt':
        var_name = node[1][1]  # Extract the actual variable name from the identifier non-terminal
        prompt = node[2][1] # Extract the prompt from the input statement
        print(f'input var_name: {var_name}')

        # Check if the variable being assigned is declared
        if not lookup_symbol(var_name):
            raise Exception(f"Error: Variable {var_name} not declared")

        # check if prompt is a string
        if isinstance(prompt, str):
            raise Exception(f"Error: Prompt must be a string")



    elif node_type == 'return_stmt':
        print(f'return: {node[1]}')

        if in_function is False:
            raise Exception(f" Values may only be returned from a function")

        # TODO Check if the type of the returned expression matches the function's return type
        analyze_semantics(node[1])

    elif node_type == 'break_stmt':
        if in_loop is False:
            raise Exception("Error: break statement not inside loop or switch")
        else:
            print(f'break: {node[1]}')

    # Add more semantic analysis rules for other language construct


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


# Add more semantic analysis rules for other language constructs


# Integrate semantic analysis into the parser
def parse_and_analyze(program):
    ast = parser.parse(program)
    print(ast)
    # Reset the symbol table and scope stack before each analysis
    reset_symbol_table_and_scope_stack()
    analyze_semantics(ast)
    return ast