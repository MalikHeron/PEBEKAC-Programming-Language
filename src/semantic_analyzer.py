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
        fun_name = node[1][1]  # Extract the actual function name from the identifier non-terminal
        params = node[2]

        if lookup_symbol(fun_name):
            raise Exception(f"Error: Function {fun_name} already defined")
        else:
            declare_symbol(fun_name, {'type': 'function', 'params': params})

        # Analyze statements inside the function declaration
        push_scope()

        # First analyze all declarations and initializations
        for stmt in node[3]:
            if stmt[0] in ['variable_declaration', 'assignment']:
                analyze_semantics(stmt)

        # Then analyze other statements
        for stmt in node[3]:
            if stmt[0] not in ['variable_declaration', 'assignment']:
                analyze_semantics(stmt)

        pop_scope()

    elif node_type == 'params':
        # Analyze each parameter in the parameter list
        for param in node[1:]:
            analyze_semantics(param)

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

    elif node_type == 'class_method':
        # Analyze statements inside the method
        push_scope()
        analyze_semantics(node[2])
        pop_scope()

    elif node_type == 'print_stmt':
        # Analyze expression(s) in print statement
        for expr in node[1:]:
            analyze_semantics(expr)

    # Add more semantic analysis rules for other language constructs


# Integrate semantic analysis into the parser
def parse_and_analyze(program):
    ast = parser.parse(program)
    print(ast)
    analyze_semantics(ast)
    return ast

# ... rest of your code ...
