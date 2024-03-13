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

    elif node_type == 'variable_declaration':
        # Add variable information to the symbol table
        var_type = node[1]
        var_name = node[2]
        symbol_table[var_name] = {'type': var_type}

    # Add more semantic analysis rules for other language constructs


# Integrate semantic analysis into the parser
def parse_and_analyze(program):
    ast = parser.parse(program)
    analyze_semantics(ast)
    return ast
