from lexer import *
from parser import *


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.scope_stack = []
        self.assigned_value = None
        self.in_loop = False
        self.in_function = False

    def is_in_function(self, boolean):
        self.in_function = boolean

    def looping(self, value):
        self.in_loop = value

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
                self.analyze_semantics(stmt, function_name=function_name)

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
                return_type = node[1][1][1]
                params = node[3]

            # print('fun_name:', fun_name, 'return_type:', return_type, 'params:', params)

            if self.lookup_symbol(fun_name):
                if len(self.scope_stack) > 1:
                    if self.scope_stack[1][fun_name]['params'] == params:
                        raise Exception(f"Error: Function {fun_name} already defined")
            else:
                self.push_scope(function_name=fun_name, return_type=return_type)
                self.declare_symbol(fun_name, {'type': 'function', 'return_type': return_type, 'params': params})

            # Analyze parameters
            self.analyze_semantics(params, function_name=fun_name)

            # Analyze statements inside the function declaration
            self.push_scope(function_name=fun_name, return_type=return_type)
            self.is_in_function(True)
            self.analyze_semantics(node[-1],
                                   function_name=fun_name)  # Changed to analyze last part of the function declaration
            self.pop_scope()
            self.is_in_function(False)

            # Check if the function has a return type but no return statement
            if return_type != 'void' and return_type != 'o':
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
                    f"Error: Parameter {param_name} already declared in {function_name}")
            else:
                # Add parameter to the symbol table
                self.declare_symbol(param_name, {'function_name': function_name, 'type': param_type})

            if len(node) > 3:
                self.analyze_semantics(node[3], function_name=function_name)

        elif node_type == 'variable_declaration':
            # Extract variable information
            var_type = node[1][1]
            var_name = node[2][1]  # Extract the actual variable name from the identifier non-terminal

            # Check if the variable is already declared
            if self.lookup_symbol(var_name) and self.lookup_symbol(var_name)['function_name'] == function_name:
                raise Exception(f"Error: Identifier {var_name} already declared")
            else:
                if var_type == 'list':
                    var_type = ['int', 'float', 'double', 'string']
                # Add variable to the symbol table
                self.declare_symbol(var_name, {'function_name': function_name, 'type': var_type})

            # If the variable has an initialization value, analyze it
            if len(node) == 4:
                init_value = node[3]
                # First add the variable to the symbol table, then analyze the initialization
                self.analyze_semantics(('assignment', var_type, var_name, init_value), function_name=function_name)

        elif node_type == 'assignment':
            # print('assignment_node:', node)
            assigned_value, assignment_type = None, None
            if node[1][0] == 'general_type' or node[1][0] == 'list' or node[1][0] == 'array_type':
                if node[1][0] == 'general_type':
                    # Check if the variable being assigned is declared
                    var_name = node[2][1]  # Extract the actual variable name from the identifier non-terminal
                    var_type = node[1][1]
                    if node[3][0] == 'function_call':
                        # print('assigned_value is a: ', node[3])
                        self.analyze_semantics(node[3], function_name=function_name)
                        fun_type = self.get_expression_type(node[3], function_name=function_name)
                        # print('fun_type:', fun_type)
                        if fun_type != var_type:
                            raise Exception(f"Error: Type mismatch. Expected {var_type}, got {fun_type}")
                    elif node[3][0] == 'expression':
                        # print('assigned_value is: ', node[3][1][1])
                        self.analyze_semantics(node[3], function_name=function_name)
                        assigned_value = node[3][1][1]
                    elif node[3][0] == 'assignment_sign':
                        # print('node:', node)
                        assignment_type = node[2]
                    elif node[3] == 'null':
                        assigned_value = node[3]
                    else:
                        # print('assigned_value_else:', node[3][1][1])
                        assigned_value = node[3][1]

                    # Extract variable information
                    # print('assignment var_name: ', var_name)
                    # print('assigned_value: ', assigned_value)
                    # print('assigned var_type: ', var_type)

                    if not self.lookup_symbol(var_name):
                        # Add variable to the symbol table
                        self.declare_symbol(var_name, {'function_name': function_name, 'type': var_type})
                    elif self.lookup_symbol(var_name) and self.lookup_symbol(var_name)['function_name'] != function_name:
                        # Add variable to the symbol table
                        self.declare_symbol(var_name, {'function_name': function_name, 'type': var_type})
                    elif self.lookup_symbol(var_name) and self.lookup_symbol(var_name)['function_name'] == function_name:
                        raise Exception(f"Error: Identifier {var_name} already declared")
                else:
                    var_name = node[2][1]
                    var_type = self.get_expression_type(node[1][1], function_name=function_name)
                    var_type_check = var_type

                    # print('var_name: ', var_name)
                    # print('var_type: ', var_type)
                    # print('node: ', node)

                    if var_type == 'intArray':
                        var_type_check = 'int'
                    elif var_type == 'floatArray':
                        var_type_check = 'float'
                    elif var_type == 'stringArray':
                        var_type_check = 'string'
                    elif var_type == 'doubleArray':
                        var_type_check = 'double'
                    elif var_type == 'list':
                        var_type_check = ['int', 'float', 'double', 'string']

                    # print('var_type: ', var_type)

                    def process_values(values):
                        # print('values:', values)
                        if values[0] == 'expression':
                            """
                            if len(values) >= 4:
                                print('assigned_value is: ', values[1][1][1])
                                print('assigned_type is: ', values[1][1][0])
                            else:
                                print('assigned_value is: ', values[1][1])
                                print('assigned_type is: ', values[1][0])
                            """
                            self.analyze_semantics(values, function_name=function_name)
                            value_type = self.get_expression_type(values[1], function_name=function_name)
                            # print('value_type:', value_type)
                            if value_type != var_type_check:
                                if var_type_check == ['int', 'float', 'double',
                                                      'string'] and value_type in var_type_check:
                                    pass
                                elif var_type == 'doubleArray' and value_type == 'float':
                                    pass
                                else:
                                    if var_type_check == ['int', 'float', 'double', 'string']:
                                        raise Exception(f"Error: Type mismatch. Expected list, got {value_type}")
                                    raise Exception(f"Error: Type mismatch. Expected {var_type}, got {value_type}")
                            if len(values) >= 4:
                                process_values(values[3])

                    # Process the values
                    process_values(node[3])

                    if not self.lookup_symbol(var_name):
                        # Add variable to the symbol table
                        # print('var_type: ', var_type)
                        self.declare_symbol(var_name, {'function_name': function_name, 'type': var_type})
                    elif self.lookup_symbol(var_name) and self.lookup_symbol(var_name)['function_name'] == function_name:
                        raise Exception(f"Error: Identifier {var_name} already declared")
            else:
                # Extract variable information
                self.get_expression_type(node[1], function_name=function_name)
                var_type = self.lookup_symbol(node[1][1])['type']
                var_name = node[1][1]  # Extract the actual variable name from the identifier non-terminal
                var_type_check = var_type
                # print('assignment var_name: ', var_name)
                # print('assignment var_type: ', var_type)
                # print('node: ', node[3][0])

                if var_type == 'intArray':
                    var_type_check = 'int'
                elif var_type == 'floatArray':
                    var_type_check = 'float'
                elif var_type == 'stringArray':
                    var_type_check = 'string'
                elif var_type == 'doubleArray':
                    var_type_check = 'double'
                elif var_type == 'list':
                    var_type_check = ['int', 'float', 'double', 'string']

                # print('var_type: ', var_type)

                # Check if the variable being assigned is declared
                if not self.lookup_symbol(var_name):
                    raise Exception(f"Error: Identifier {var_name} not declared")
                elif self.lookup_symbol(var_name) and self.lookup_symbol(var_name)['function_name'] != function_name:
                    raise Exception(f"Error: Identifier {var_name} not declared")
                elif self.lookup_symbol(var_name):
                    def process_values(values):
                        # print('values:', values)
                        if values[0] == 'expression':
                            """
                            if len(values) >= 4:
                                print('greater than 4, len(values):', len(values))
                                print('assigned_value is: ', values[1][1][1])
                                print('assigned_type is: ', values[1][1][0])
                            else:
                                print('less than 4, len(values):', len(values))
                                print('assigned_value is: ', values[1][1])
                                print('assigned_type is: ', values[1][0])
                            """
                            self.analyze_semantics(values, function_name=function_name)
                            value_type = self.get_expression_type(values[1], function_name=function_name)
                            # print('value_type:', value_type)
                            if value_type != var_type_check:
                                if var_type_check == ['int', 'float', 'double',
                                                      'string'] and value_type in var_type_check:
                                    pass
                                else:
                                    if var_type_check == ['int', 'float', 'double', 'string']:
                                        raise Exception(f"Error: Type mismatch. Expected list, got {value_type}")
                                    raise Exception(
                                        f"Error: Type mismatch. Expected {var_type_check}, got {value_type}")
                        if values[0] == 'function_call':
                            # print('assigned_value is a: ', node[3])
                            self.analyze_semantics(node[3], function_name=function_name)
                            fun_type = self.get_expression_type(node[3], function_name=function_name)
                            # print('fun_type:', fun_type)
                            if fun_type != var_type_check:
                                raise Exception(f"Error: Type mismatch. Expected {var_type_check}, got {fun_type}")

                        if len(values) == 2:
                            if len(values[1]) > 2:
                                process_values(values[1][3])
                        elif len(values) == 4:
                            process_values(values[3])

                    # Process the values
                    process_values(node[3])

            # Check if the assigned value matches the type of the variable
            if node[3][0] == 'function_call':
                pass  # Allow the return type checking to be done by python compiler
            elif node[3][1][0] == 'element_access':
                # print('array_node:', node[3][1])
                self.analyze_semantics(node[3][1], function_name=function_name)
                assigned_value = self.get_expression_type(node[3][1], function_name=function_name)
                # print('assigned_value:', assigned_value)
                # print('var_type:', var_type)
                if assigned_value != var_type:
                    if var_type != 'boolean' and assigned_value == 'list':
                        return
                    if ((var_type == 'int' and assigned_value == 'intArray')
                            or (var_type == 'float' and assigned_value == 'floatArray')
                            or (var_type == 'string' and assigned_value == 'stringArray')
                            or (var_type == 'double' and assigned_value == 'doubleArray')):
                        return
                    raise Exception(f"Error: Type mismatch. Expected {var_type}, got {assigned_value}")
            elif assigned_value == 'null':
                pass
            else:
                # print('node_else:', node[3])
                # print('assigned_value:', assigned_value, 'var_type:', var_type)
                if self.lookup_symbol(assigned_value):
                    if self.lookup_symbol(assigned_value)['type'] == var_type:
                        return
                if isinstance(assigned_value, str) and var_type != 'string':
                    if assigned_value.capitalize() == 'True' or assigned_value.capitalize() == 'False':
                        if var_type == 'boolean':
                            return
                        else:
                            raise Exception(f"Error: Type mismatch. Expected {var_type}, got boolean")
                    raise Exception(f"Error: Type mismatch. Expected {var_type}, got string")
                elif isinstance(assigned_value, int) and var_type != 'int':
                    raise Exception(f"Error: Type mismatch. Expected {var_type}, got int")
                elif isinstance(assigned_value, float) and (var_type != 'float' and var_type != 'double'):
                    raise Exception(f"Error: Type mismatch. Expected {var_type}, got float")
                elif not isinstance(assigned_value, (str, int, float, bool)) and var_type == 'string':
                    raise Exception(f"Error: Type mismatch. Expected {var_type}, got non-string")
                elif assignment_type is not None and assignment_type != 'ASSIGN' and var_type == 'string':
                    raise Exception(f"Error: Invalid assignment on type {var_type}")

        elif node_type == 'expression':
            # print('expression_node:', node):
            self.analyze_semantics(node[1], function_name=function_name)
            # Handle expression nodes
            self.get_expression_type(node[1], function_name=function_name)  # Analyze left operand

            if len(node) == 4:  # Binary operation
                operator = node[2]
                self.analyze_semantics(operator, function_name=function_name)  # Analyze operator
                self.analyze_semantics(node[3], function_name=function_name)  # Analyze right operand

        elif node_type == 'control_structure':
            # Analyze the control structure
            self.analyze_semantics(node[1], function_name=function_name)

        elif node_type == 'if_stmt':
            # print('node:', node)
            # Analyze the condition expression
            self.analyze_semantics(node[1], function_name=function_name)

            # Analyze statements in the if block
            self.push_scope(function_name=function_name)
            self.analyze_semantics(node[2], function_name=function_name)
            self.pop_scope()

            # If there's an else block, analyze its statements too
            if node_type == 'if_stmt' and len(node) > 3:
                # print('if_node:', node[3])
                self.push_scope(function_name=function_name)
                self.analyze_semantics(node[3], function_name=function_name)
                self.pop_scope()

        elif node_type == 'else_stmt':
            # print('else_node:', node[1][0])
            if node[1][0] == 'if_stmt' or node[1][0] == 'stmt_list':
                # Analyze the statements in the else block
                self.push_scope(function_name=function_name)
                self.analyze_semantics(node[1], function_name=function_name)
                self.pop_scope()

                # Check if the else_if block is followed by an else statement
                if node[1][0] == 'if_stmt' and not len(node[1]) > 3:
                    raise Exception("Error: nested if statement not followed by a else block")

        elif node_type == 'while_stmt':
            # ('node:', node)
            # Analyze the condition expression
            self.analyze_semantics(node[1], function_name=function_name)

            # Analyze statements in the while loop body
            self.push_scope(function_name=function_name)
            self.looping(True)
            self.analyze_semantics(node[2], function_name=function_name)
            self.looping(False)
            self.pop_scope()

        elif node_type == 'for_stmt':
            # Analyze Assignment expression
            self.analyze_semantics(node[1], function_name=function_name)
            self.analyze_semantics(node[2], function_name=function_name)
            self.analyze_semantics(node[3], function_name=function_name)

            # Analyze statements in the for loop body
            self.push_scope(function_name=function_name)
            self.looping(True)
            self.analyze_semantics(node[4], function_name=function_name)
            self.looping(False)
            self.pop_scope()

        elif node_type == 'print_stmt':
            # Analyze expression(s) in print statement
            for expr in node[1:]:
                self.analyze_semantics(expr, function_name=function_name)

        elif node_type == 'len_stmt':
            # Analyze expression(s) in print statement
            for expr in node[1:]:
                # print('expr:', expr)
                # Check if the expression is an identifier
                if expr[0] == 'function_call':
                    # Analyze the function call expression
                    self.analyze_semantics(expr, function_name=function_name)

            # Check the type of the expression
            expr_type = self.get_expression_type(node[1], function_name=function_name)

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

                # Retrieve parameter types from the function declaration
                params = fun_info['params']
                # print('arg_list:', arg_list)
                param_list = params[1]
                # print('param_list:', param_list)

                arg_types = []  # List to store the types of arguments
                param_types = []  # List to store the types of parameters

                def check_arg_type(list_arg):
                    # Check if the types of arguments match the types of parameters
                    for arg in list_arg[1:]:
                        # print('arg:', arg)
                        if arg[0] == 'expression':
                            if arg[1][0] == 'function_call':
                                check_arg_type(arg[1])
                                self.analyze_semantics(arg[1], function_name=function_name)
                            elif arg[1][0] == 'identifier':
                                # print('function_name:', function_name)
                                # print('next_arg:', self.lookup_symbol(arg[1][1]))
                                # print('scope_stack len:', len(self.scope_stack))
                                if len(self.scope_stack[-1]) > 1:
                                    # print('scope_stack[-1]:', self.scope_stack[-1])
                                    if (self.lookup_symbol(arg[1][1])
                                            and self.lookup_symbol(arg[1][1])['function_name'] != function_name):
                                        if (self.lookup_symbol(arg[1][1])['function_name']
                                                != self.scope_stack[-2]['function_name']):
                                            raise Exception(
                                                f"Error: Identifier {arg[1][1]} already exists in outer scope")
                                        if (self.lookup_symbol(arg[1][1])
                                                and self.scope_stack[-2]['function_name'] == function_name):
                                            raise Exception(f"Error: Argument {arg[1][1]} already declared")
                                    if (self.lookup_symbol(arg[1][1])
                                            and self.lookup_symbol(arg[1][1])['function_name'] != function_name):
                                        raise Exception(f"Error: Identifier {arg[1][1]} not declared")
                                    if not self.lookup_symbol(arg[1][1]):
                                        raise Exception(f"Error: Argument {arg[1][1]} not declared")
                            else:
                                arg_types.append(self.get_expression_type(arg[1], function_name=function_name))
                        if arg[0] == 'function_call':
                            arg_types.append(self.get_expression_type(arg[1], function_name=function_name))
                        if arg[0] == 'arg_list':
                            check_arg_type(arg)
                        # print('arg_types:', arg_types)

                def check_param_type(list_param):
                    # Check if the types of parameters
                    for param_ in list_param[1:]:
                        # print('param:', param_)
                        if param_[0] == 'general_type':
                            param_types.append(self.get_expression_type(param_[1], function_name=function_name))
                        if param_[0] == 'function_call':
                            param_types.append(self.get_expression_type(param_[1], function_name=function_name))
                        if param_[0] == 'param':
                            check_param_type(param_)
                        # print('param_types:', param_types)

                check_arg_type(arg_list)  # Check the types of arguments
                check_param_type(param_list)  # Check the types of parameters

                # Check the types of arguments and parameters
                for arg_type, param_type in zip(arg_types[0:], param_types[0:]):
                    if arg_type != param_type:
                        raise Exception(f"Error: Type mismatch in function call. Expected {param_type}, got {arg_type}")

        elif node_type == 'return_stmt':
            # First, find out the current function's name from the scope stack
            # print('scope_stack:', self.scope_stack[-2])
            # print('node:', node)
            self.get_expression_type(node[1], function_name=function_name)

            if function_name is not None:
                current_function_name = function_name
                expected_return_type = self.lookup_symbol(current_function_name)['return_type']
            elif len(self.scope_stack[-1]) > 1:
                current_function_name = self.scope_stack[-1]['function_name']
                expected_return_type = self.scope_stack[-1]['return_type']
                # print('scope_stack:', self.scope_stack[-1])
            elif len(self.scope_stack[-2]) == 1:
                current_function_name = self.scope_stack[-2]['function_name']
                expected_return_type = self.scope_stack[-2]['return_type']
                # print('scope_stack:', self.scope_stack[-2])
            else:
                return

            # Find the function's expected return type
            # function_info = self.lookup_symbol(current_function_name)
            # print('function_info:', function_info)
            # Then, check the type of the return expression
            return_expr_type = self.get_expression_type(node[1], function_name=function_name)

            if isinstance(return_expr_type, dict):
                return_expr_type = return_expr_type['type']

            # print('return_expr_type:', return_expr_type, 'expected_return_type:', expected_return_type)

            if return_expr_type != expected_return_type:
                raise Exception(
                    f"Return type mismatch in function {current_function_name}: "
                    f"Expected {'void' if expected_return_type == 'o' else expected_return_type}, got {return_expr_type}"
                )

        elif node_type == 'compound_assignment':
            # print('node:', node)
            # Analyze the expression to increment
            self.analyze_semantics(node[1], function_name=function_name)
            self.analyze_semantics(node[3], function_name=function_name)

            if len(node) > 4:
                # print('node:', node[1][1])
                # Ensure the expression to increment is an identifier
                if node[1][1] != 'identifier':
                    raise TypeError(f"Invalid operation: Increment operator cannot be applied to a {node[1][1][0]}")
            else:
                # print('node:', node[1][0])
                # Ensure the expression to increment is an identifier
                if node[1][0] != 'identifier':
                    raise TypeError(f"Invalid operation: Increment operator cannot be applied to a {node[1][1][0]}")

            # Ensure the types match
            self.get_expression_type(node, function_name=function_name)

        elif node_type == 'break_stmt':
            if self.in_loop is False:
                raise Exception("Error: break statement not inside a loop")

        elif node_type == 'element_access':
            # Analyze the identifier to ensure it's defined
            # print('node:', node)
            array_name = node[1][1]
            array_info = self.lookup_symbol(array_name)

            if not array_info:
                raise NameError(f"Array {array_name} is not defined")

            # Analyze the index expression
            self.analyze_semantics(node[2], function_name=function_name)

            # Ensure the index expression evaluates to an integer
            index_type = self.get_expression_type(node[2], function_name=function_name)
            if index_type != 'int':
                raise TypeError(f"Array index must be an integer, got {index_type}")

    def get_expression_type(self, expr, function_name):
        # Determine the type of expression.
        if isinstance(expr, tuple):
            expr_type = expr[0]
        else:
            expr_type = expr

        # print('expr_type:', expr_type, ', expr:', expr)

        if expr_type == 'expression':
            if len(expr) >= 4:
                # print('binary_expr:', expr)
                # print('left_operand:', expr[1], 'operator:', expr[2], 'right_operand:', expr[3])
                # Binary operation
                self.analyze_semantics(expr[1], function_name=function_name)
                self.analyze_semantics(expr[3], function_name=function_name)
                operator = expr[2]
                right_operand_type = self.get_expression_type(expr[3],
                                                              function_name=function_name)  # Analyze right operand
                left_operand_type = self.get_expression_type(expr[1],
                                                             function_name=function_name)  # Analyze left operand
                # print('right_operand_type:', right_operand_type, 'left_operand_type:', left_operand_type)
                # Check if the types of the operands match
                if right_operand_type != left_operand_type:
                    return get_type("binary operation", left_operand_type, right_operand_type)
                elif (operator == '-' or operator == '*' or operator == '/' or operator == '%'
                      or operator == '-=' or operator == '*=' or operator == '/=' or operator == '%='):
                    if right_operand_type == 'string' or left_operand_type == 'string':
                        raise TypeError(f"Invalid operation: {operator} on string")
                elif (operator == '==' or operator == '!=' or operator == '<' or operator == '<='
                      or operator == '>' or operator == '>='):
                    return 'boolean'
                return right_operand_type
            self.analyze_semantics(expr, function_name=function_name)  # Analyze right operand
            return self.get_expression_type(expr[1], function_name=function_name)

        if expr_type == 'compound_assignment':
            # print('expr:', expr)
            # Binary operation
            self.analyze_semantics(expr[1], function_name=function_name)
            self.analyze_semantics(expr[3], function_name=function_name)
            operator = expr[2][1]
            right_operand_type = self.get_expression_type(expr[3], function_name=function_name)  # Analyze right operand
            left_operand_type = self.get_expression_type(expr[1], function_name=function_name)  # Analyze left operand
            # print('right_operand_type:', right_operand_type, 'operator:', operator,
            #      'left_operand_type:', left_operand_type)
            # Check if the types of the operands match
            if right_operand_type != left_operand_type:
                get_type("compound assignment", left_operand_type, right_operand_type)
            elif operator == '-=' or operator == '*=' or operator == '/=' or operator == '%=':
                if left_operand_type == 'string':
                    raise TypeError(f"Invalid operation: {operator} on string")
            return left_operand_type

        elif expr_type == 'element_access':
            # print('expr:', expr)
            # Analyze the identifier to ensure it's defined
            array_name = expr[1][1]
            array_info = self.lookup_symbol(array_name)
            if array_info:
                # print('array_info:', array_info)
                return array_info['type']
            raise NameError(f"Array {array_name} is not defined")

        elif expr_type == 'identifier':
            # Look up the identifier in the symbol table
            identifier = expr[1]
            if self.lookup_symbol(identifier):
                # print('identifier:', self.lookup_symbol(identifier)['type'])
                if self.lookup_symbol(identifier)['type'] == 'int':
                    return 'int'
                elif self.lookup_symbol(identifier)['type'] == 'float':
                    return 'float'
                elif self.lookup_symbol(identifier)['type'] == 'double':
                    return 'double'
                return self.lookup_symbol(identifier)['type']
            else:
                raise NameError(f"Identifier {identifier} is not defined")

        elif expr_type == 'function_call':
            # Look up the function in the symbol table
            fun_name = expr[1][1]
            fun_info = self.lookup_symbol(fun_name)
            expr_type = expr[2][1][1][0]
            # print('fun_name:', fun_name)
            # print('call:', expr)
            # print('type:', expr_type)
            if fun_info:
                # Check if the function has a return type
                # print('expr:', expr[2][1][1])
                if expr[0] == 'function_call':
                    # print('expr_call:', expr)
                    self.analyze_semantics(expr, function_name=function_name)
                    # print('fun_info:', fun_info['return_type'])
                    return fun_info['return_type']
                if expr_type == 'expression' or expr_type == 'identifier' or expr_type == 'function_call':
                    if expr_type == 'expression':
                        if len(expr[2][1][1]) > 2:
                            expr_type = self.get_expression_type(expr[2][1][1], function_name=function_name)
                            if expr_type == 'identifier':
                                # print('expr_type:', self.lookup_symbol(expr))
                                expr_type = self.lookup_symbol([2][1])
                        else:
                            expr_type = self.get_expression_type(expr[2][1], function_name=function_name)
                            if expr_type == 'identifier':
                                # print('expr_type:', self.lookup_symbol(expr))
                                expr_type = self.lookup_symbol([2][1])
                    if expr_type == 'identifier':
                        # print('expr:', expr[2][1][1][1])
                        # print('expr_type:', self.lookup_symbol(expr[2][1][1][1])['type'])
                        expr_type = self.lookup_symbol(expr[2][1][1][1])['type']
                    if expr_type == 'function_call':
                        # print('expr_call:', expr[2][1][1][1])
                        expr_type = self.get_expression_type(expr[2][1][1], function_name=function_name)
                if expr_type != fun_info['return_type']:
                    # print('return_type:', expr_type)
                    raise Exception(
                        f"Return type mismatch in function {fun_name}: Expected "
                        f"{'void' if fun_info['return_type'] == 'o' else fun_info['return_type']}, got {expr_type}")
                return fun_info['return_type']
            else:
                raise NameError(f"Function {fun_name} is not defined")

        elif expr_type == 'len_stmt':
            return 'int'

        elif expr_type == 'int':
            return 'int'

        elif expr_type == 'float':
            return 'float'

        elif expr_type == 'double':
            return 'double'

        elif expr_type == 'boolean':
            return 'boolean'

        elif expr_type == 'string' or expr_type == 'string_literal':
            return 'string'

        elif expr_type == 'list':
            return 'list'

        elif expr_type == 'intArray':
            return 'intArray'

        elif expr_type == 'floatArray':
            return 'floatArray'

        elif expr_type == 'doubleArray':
            return 'doubleArray'

        elif expr_type == 'stringArray':
            return 'stringArray'

        elif (expr_type == '==' or expr_type == '!=' or expr_type == '<'
              or expr_type == '<=' or expr_type == '>' or expr_type == '>='):
            return 'boolean'

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


def get_type(op_type, left_operand_type, right_operand_type):
    if ((left_operand_type == 'int' and right_operand_type == 'float')
            or (left_operand_type == 'float' and right_operand_type == 'int')):
        return 'float'
    elif ((left_operand_type == 'int' and right_operand_type == 'double')
          or (left_operand_type == 'double' and right_operand_type == 'int')):
        return 'double'
    elif ((left_operand_type == 'float' and right_operand_type == 'double')
          or (left_operand_type == 'double' and right_operand_type == 'float')):
        return 'double'
    elif ((left_operand_type == 'int' and right_operand_type == 'intArray')
          or (left_operand_type == 'intArray' and right_operand_type == 'int')):
        return 'int'
    elif ((left_operand_type == 'float' and right_operand_type == 'floatArray')
          or (left_operand_type == 'floatArray' and right_operand_type == 'float')):
        return 'float'
    elif ((left_operand_type == 'double' and right_operand_type == 'doubleArray')
          or (left_operand_type == 'doubleArray' and right_operand_type == 'double')):
        return 'double'
    elif ((left_operand_type == 'string' and right_operand_type == 'stringArray')
          or (left_operand_type == 'stringArray' and right_operand_type == 'string')):
        return 'string'
    elif ((left_operand_type != 'boolean' and right_operand_type == 'list')
          or (left_operand_type == 'list' and right_operand_type != 'boolean')):
        return 'int' or 'float' or 'double' or 'string'
    raise TypeError(f"Type mismatch in {op_type}: {left_operand_type} and {right_operand_type}")
