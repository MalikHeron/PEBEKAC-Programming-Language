from lexer import *
from parser import *


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.scope_stack = []
        self.assigned_value = None
        self.in_loop = False
        self.in_function = False
        self.expr = None

    def is_in_function(self, boolean):
        self.in_function = boolean

    def looping(self, value):
        self.in_loop = value

    # Modify self.push_scope() and self.pop_scope() functions to include the current function name
    def push_scope(self, function_name=None, return_type=None):
        if function_name and return_type:
            self.scope_stack.append({'function_name': function_name, 'return_type': return_type})
            return
        # Push a new scope onto the stack
        self.scope_stack.append({})

    def pop_scope(self):
        # Pop the current scope from the stack
        self.scope_stack.pop()

    def declare_symbol(self, name, symbol_type):
        # Declare a symbol in the current scope
        self.scope_stack[-1][name] = symbol_type

    def lookup_symbol(self, name):
        # Look up a symbol in all scopes, starting from the current scope and moving outward
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        return None

    # Define functions to manage the symbol table and scope stack
    def reset_symbol_table_and_scope_stack(self):
        self.symbol_table = {}
        self.scope_stack = []

    # Define a function for semantic analysis
    def analyze_semantics(self, node, function_name=None):
        node_type = node[0]

        if node_type == 'program':
            # Perform semantic analysis for the entire program
            self.push_scope()
            self.analyze_semantics(node[1])
            self.pop_scope()

        elif node_type == 'stmt_list':
            # Analyze each statement in the statement list
            for stmt in node[1:]:
                self.analyze_semantics(stmt)

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

            if self.lookup_symbol(fun_name):
                if len(self.scope_stack) > 1:
                    if self.scope_stack[1][fun_name]['params'] == params:
                        raise Exception(f"Error: Function {fun_name} already defined")
            else:
                self.push_scope(function_name=fun_name, return_type=return_type[1])
                self.declare_symbol(fun_name, {'type': 'function', 'return_type': return_type, 'params': params})

            # Analyze parameters
            self.analyze_semantics(params, function_name=fun_name)

            # Analyze statements inside the function declaration
            self.push_scope(function_name=fun_name, return_type=return_type[1])
            self.is_in_function(True)
            self.analyze_semantics(node[-1],
                                   function_name=fun_name)  # Changed to analyze last part of the function declaration
            self.pop_scope()
            self.is_in_function(False)

            # Check if the function has a return type but no return statement
            if return_type != 'void':
                if not self.has_return_statement(node[-1]):
                    raise Exception(f"Error: Function {fun_name} has a return type but no return statement")

        elif node_type == 'params':
            # Analyze each parameter in the parameter list
            for param in node[1:]:
                self.analyze_semantics(param, function_name=function_name)

        elif node_type == 'param':
            # Extract parameter information
            param_type = node[1][1]
            param_name = node[2][1]

            # print('function_name:', function_name, 'param:', node, 'param_type:', param_type, 'param_name:', param_name)

            # Check if the parameter is already declared
            if self.lookup_symbol(param_name) and self.lookup_symbol(param_name)['function_name'] == function_name:
                raise Exception(
                    f"Error: Parameter {param_name} already declared in previous declaration of function {function_name}")
            else:
                # Add parameter to the symbol table
                self.declare_symbol(param_name, {'function_name': function_name, 'type': param_type})

            if len(node) > 3:
                self.analyze_semantics(node[3])

        elif node_type == 'variable_declaration':
            # Extract variable information
            var_type = node[1][1]
            var_name = node[2][1]  # Extract the actual variable name from the identifier non-terminal

            # Check if the variable is already declared
            if self.lookup_symbol(var_name):
                raise Exception(f"Error: Variable {var_name} already declared")
            else:
                # Add variable to the symbol table
                self.declare_symbol(var_name, {'type': var_type})

            # If the variable has an initialization value, analyze it
            if len(node) == 4:
                init_value = node[3]
                # First add the variable to the symbol table, then analyze the initialization
                self.analyze_semantics(('assignment', var_type, var_name, init_value))

        elif node_type == 'assignment':
            assigned_value, assignment_type = None, None
            if node[1][0] == 'general_type' or node[1][0] == 'list_type' or node[1][0] == 'array_type':
                # Check if the variable being assigned is declared
                var_name = node[2][1]  # Extract the actual variable name from the identifier non-terminal
                var_type = node[1][1]
                if node[3][0] == 'function_call':
                    # print('assigned_value is a: ', node[3][0])
                    self.analyze_semantics(node[3])
                elif node[3] == 'null':
                    assigned_value = node[3]
                else:
                    assigned_value = node[3][1][1]

                # Extract variable information
                # print('assignment var_name: ', var_name)
                # print('assigned_value: ', assigned_value)
                # print('assigned var_type: ', var_type)

                if not self.lookup_symbol(var_name):
                    # Add variable to the symbol table
                    self.declare_symbol(var_name, {'type': var_type})
                elif self.lookup_symbol(var_name) and len(self.lookup_symbol(var_name)) == 1:
                    raise Exception(f"Error: Variable {var_name} already declared")
            else:
                # Extract variable information
                var_type = self.lookup_symbol(node[1][1])['type']
                var_name = node[1][1]  # Extract the actual variable name from the identifier non-terminal
                # print('assignment var_name: ', var_name)
                # print('node: ', node)

                # Check if the variable being assigned is declared
                if not self.lookup_symbol(var_name):
                    raise Exception(f"Error: Variable {var_name} not declared")
                elif self.lookup_symbol(var_name):
                    # Check if the assigned value matches the type of the variable
                    if node[3][0] == 'function_call':
                        # print('assigned_value is a: ', node[3][0])
                        self.analyze_semantics(node[3])
                    elif node[3] == 'null':
                        assigned_value = node[3]
                    elif node[2] == 'assignment_sign':
                        assignment_type = node[2]
                    else:
                        assigned_value = node[3][1][1]
                    # print('assigned_value: ', assigned_value)
                    var_type = self.lookup_symbol(var_name)['type']
                    # print('assigned var_type: ', var_type)

            # Check if the assigned value matches the type of the variable
            if node[3][0] == 'function_call':
                pass  # Allow the return type checking to be done by python compiler
            elif assigned_value == 'null':
                pass
            else:
                # print('assigned_value:', assigned_value, 'var_type:', var_type)
                if self.lookup_symbol(assigned_value):
                    if self.lookup_symbol(assigned_value)['type'] == var_type:
                        return
                if isinstance(assigned_value, str) and var_type != 'string':
                    raise Exception(f"Error: Type mismatch. Expected {var_type}, got string")
                elif isinstance(assigned_value, int) and var_type != 'int':
                    raise Exception(f"Error: Type mismatch. Expected {var_type}, got int")
                elif isinstance(assigned_value, float) and (var_type != 'float' and var_type != 'double'):
                    raise Exception(f"Error: Type mismatch. Expected {var_type}, got float")
                elif isinstance(assigned_value, bool) and var_type != 'boolean':
                    raise Exception(f"Error: Type mismatch. Expected {var_type}, got boolean")
                # elif not isinstance(assigned_value, (str, int, float, bool)) and var_type == 'string':
                #    raise Exception(f"Error: Type mismatch. Expected {var_type}, got non-string")
                elif assignment_type is not None and assignment_type != 'ASSIGN' and var_type == 'string':
                    raise Exception(f"Error: Invalid assignment on type {var_type}")

        elif node_type == 'expression':
            # Handle expression nodes
            self.get_expression_type(node[1])  # Analyze left operand

            if len(node) == 4:  # Binary operation
                operator = node[2]
                self.analyze_semantics(operator)  # Analyze operator
                self.analyze_semantics(node[3])  # Analyze right operand

        elif node_type == 'control_structure':
            # Analyze the control structure
            self.analyze_semantics(node[1])

        elif node_type == 'if_stmt':
            # Analyze the condition expression
            self.analyze_semantics(node[1])

            # Analyze statements in the if block
            self.push_scope(function_name=function_name)
            self.analyze_semantics(node[2], function_name=function_name)
            self.pop_scope()

            # If there's an else block, analyze its statements too
            if node_type == 'if_stmt' and len(node) == 4:
                # print('node:', node)
                self.push_scope(function_name=function_name)
                self.analyze_semantics(node[3], function_name=function_name)
                self.pop_scope()

        elif node_type == 'while_stmt':
            # Analyze the condition expression
            self.analyze_semantics(node[1])

            # Analyze statements in the while loop body
            self.push_scope(function_name=function_name)
            self.looping(True)
            self.analyze_semantics(node[2], function_name=function_name)
            self.looping(False)
            self.pop_scope()

        elif node_type == 'for_stmt':
            # Analyze Assignment expression
            self.analyze_semantics(node[1])
            self.analyze_semantics(node[2])
            self.analyze_semantics(node[3])

            # Analyze statements in the for loop body
            self.push_scope(function_name=function_name)
            self.looping(True)
            self.analyze_semantics(node[4], function_name=function_name)
            self.looping(False)
            self.pop_scope()

        elif node_type == 'print_stmt':
            # Analyze expression(s) in print statement
            for expr in node[1:]:
                self.analyze_semantics(expr)

        elif node_type == 'len_stmt':
            # Analyze expression(s) in print statement
            for expr in node[1:]:
                print('expr:', expr)
                # Check if the expression is an identifier
                if expr[0] == 'function_call':
                    # Analyze the function call expression
                    self.analyze_semantics(expr)

            # Check the type of the expression
            expr_type = self.get_expression_type(node[1])

            # Check if expression is valid...
            if expr_type is None:
                raise ValueError(f"Invalid expression in print statement: {node}")

        elif node_type == 'function_call':
            fun_name = node[1][1]  # Extract the actual function name from the identifier non-terminal
            arg_list = node[2]
            fun_info = self.lookup_symbol(fun_name)

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
                    # print('param_node[0]:', param_node[0])
                    if isinstance(param_node, tuple) and param_node[0] == 'params':
                        # print('If param_node:', param_node)
                        if param_node[1] == 'empty':
                            # print('empty')
                            return 0
                        else:
                            # print('param_node[1]:', param_node[1])
                            # print(len(param_node[1]))
                            # If the node is a 'params' node, count the identifier and recursively count the rest of the
                            # parameters
                            return 1 + count_params(param_node[1][3]) if len(param_node[1]) > 3 else 1
                    elif isinstance(param_node, tuple) and param_node[0] == 'param':
                        # print('ELse param_node:', param_node)
                        if param_node[1] == 'empty':
                            # print('empty')
                            return 0
                        else:
                            # print('param_node[0]:', param_node[0])
                            # print(len(param_node))
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
            print('scope_stack:', self.scope_stack[-2])

            if function_name is not None:
                current_function_name = function_name
                expected_return_type = self.lookup_symbol(current_function_name)['return_type']
            elif len(self.scope_stack[-1]) > 1:
                current_function_name = self.scope_stack[-1]['function_name']
                expected_return_type = self.scope_stack[-1]['return_type']
            else:
                current_function_name = self.scope_stack[-2]['function_name']
                expected_return_type = self.scope_stack[-2]['return_type']

            # Find the function's expected return type
            # function_info = self.lookup_symbol(current_function_name)
            # print('function_info:', function_info)
            # Then, check the type of the return expression
            return_expr_type = self.get_expression_type(node[1])

            if isinstance(return_expr_type, dict):
                return_expr_type = return_expr_type['type']

            # print('return_expr_type:', return_expr_type, 'expected_return_type:', expected_return_type)

            if return_expr_type != expected_return_type:
                raise Exception(
                    f"Return type mismatch in function {current_function_name}: Expected {'void' if expected_return_type == 'o' else expected_return_type}, got {return_expr_type}"
                )

        elif node_type == 'break_stmt':
            if self.in_loop is False:
                raise Exception("Error: break statement not inside loop or switch")

        elif node_type == 'array_access':
            # Analyze the identifier to ensure it's defined
            array_name = node[1]
            array_info = self.lookup_symbol(array_name)

            if not array_info:
                raise NameError(f"Array {array_name} is not defined")

            # Analyze the index expression
            self.analyze_semantics(node[2])

            # Ensure the index expression evaluates to an integer
            index_type = self.get_expression_type(node[2])
            if index_type != 'int':
                raise TypeError(f"Array index must be an integer, got {index_type}")

            # Add the type information for the array element to the current node
            element_type = array_info['type'][:-5]  # Remove the 'ARRAY' suffix
            node.append({'type': element_type})

    def get_expression_type(self, expr):
        # Determine the type of expression.
        if isinstance(expr, tuple):
            expr_type = expr[0]
        else:
            expr_type = expr

        # print('expr_type:', expr_type, ', expr:', expr)

        if expr_type == 'expression':
            if len(expr) == 4:
                # print('expr:', expr)
                # Binary operation
                self.analyze_semantics(expr[1])
                self.analyze_semantics(expr[3])
                return self.get_expression_type(expr[2])
            self.analyze_semantics(expr)  # Analyze right operand
            return self.get_expression_type(expr[1])

        elif expr_type == 'digit':
            return 'int' or 'float'

        elif expr_type == 'boolean':
            return 'boolean'

        elif expr_type == 'string' or expr_type == 'string_literal':
            return 'string'

        elif expr_type == 'identifier':
            # Look up the identifier in the symbol table
            identifier = expr[1]
            if self.lookup_symbol(identifier):
                return self.lookup_symbol(identifier)
            else:
                raise NameError(f"Identifier {identifier} is not defined")

        elif expr_type == 'function_call':
            # Look up the function in the symbol table
            fun_name = expr[1][1]
            fun_info = self.lookup_symbol(fun_name)
            if fun_info:
                return fun_info
            else:
                raise NameError(f"Function {fun_name} is not defined")

        elif expr_type == 'len_stmt':
            return 'int'

        elif expr_type == '==' or expr_type == '!=' or expr_type == '<' or expr_type == '<=' or expr_type == '>' or expr_type == '>=':
            return 'boolean'

        elif expr_type == '+' or expr_type == '-' or expr_type == '*' or expr_type == '/':
            return 'int' or 'float' or 'double' or 'string'

        else:
            pass

    def has_return_statement(self, node):
        # Base case: if the node is a return statement, return True
        if node[0] == 'return_stmt':
            return True

        # If the node is a statement list, iterate through its elements
        if node[0] == 'stmt_list':
            for sub_node in node[1:]:
                # Recursively check each sub-node
                if self.has_return_statement(sub_node):
                    return True

        # If the node is a control structure, check its body
        if node[0] == 'control_structure':
            return self.has_return_statement(node[1])

        # If none of the above conditions are met, return False
        return False

    # Counts number of arguments in a function declaration
    def count_params(self, param_node):
        if isinstance(param_node, tuple) and param_node[0] == 'params':
            if param_node[1] == 'empty':
                return 0
            else:
                # If the node is a 'params' node, count the identifier and recursively count the rest of the
                # parameters
                return 1 + self.count_params(param_node[3]) if len(param_node) > 3 else 1

    # Counts number of arguments in a function call
    def count_args(self, arg_node):
        if isinstance(arg_node, tuple) and arg_node[0] == 'arg_list':
            if arg_node[1] == 'empty':
                return 0
            else:
                return sum(self.count_args(arg) for arg in arg_node[1:])
        else:
            return 1

    # Integrate semantic analysis into the parser
    def parse_and_analyze(self, program):
        # Create a new parser instance for each request
        lexBuilder()
        parser = yaccBuilder()
        # Parse the program
        ast = parser.parse(program)
        print(ast)
        # Reset the symbol table and scope stack before each analysis
        self.reset_symbol_table_and_scope_stack()
        self.analyze_semantics(ast)
        return ast
