def generate_code(node):
    node_type = node[0]

    if node_type == 'program':
        return generate_code(node[1])

    elif node_type == 'stmt_list':
        return '\n'.join(generate_code(stmt) for stmt in node[1:])

    elif node_type == 'fun_declaration':
        if (len(node)) == 5:
            fun_name = node[2][1]
            params = generate_code(node[3])
            stmts = generate_code(node[4])
        else:
            fun_name = node[1][1]
            params = generate_code(node[2])
            stmts = generate_code(node[3])

        return f'def {fun_name}({params}):\n{indent(stmts)}'

    elif node_type == 'params':
        return generate_code(node[1])

    elif node_type == 'param':
        return node[2][1] + ', ' + generate_code(node[3]) if len(node) > 3 else node[2][1]

    elif node_type == 'variable_declaration':
        var_type = generate_code(node[1])
        var_name = node[2][1]
        if var_type.startswith('list') or var_type.endswith('[]'):
            return f'{var_name} = []'  # Initializing an empty list
        elif var_type.endswith('Array'):
            return f'{var_name} = [0] * {var_type[3:-5]}'  # Initializing an array of zeros of given size
        else:
            return f'{var_name} = None'  # Initializing other variables as None

    elif node_type == 'assignment':
        if node[1][0] == 'general_type':
            var_name = node[2][1]
            if node[3] == 'null':
                return f'{var_name} = None'
            else:
                expr = generate_code(node[3])
                return f'{var_name} = {expr}'  # Correct assignment syntax
        elif node[1][0] == 'list' or node[1][0] == 'array_type':
            var_name = node[2][1]
            expr = generate_code(node[3])
            return f'{var_name} = [{expr}]'
        else:
            var_name = node[1][1]
            if node[3] == 'null':
                return f'{var_name} = None'
            elif node[2][0] == 'assignment_sign':
                expr = generate_code(node[3])
                sign = generate_code(node[2])
                return f'{var_name} {sign} {expr}'
            elif node[2][0] == '=':
                expr = generate_code(node[3])
                sign = generate_code(node[2])
                return f'{var_name} {sign} {expr}'
            else:
                expr = generate_code(node[2])
                return f'{var_name} = {expr}'

    elif node_type == 'print_stmt':
        expr = ', '.join(generate_code(expr) for expr in node[1:])
        return f'print({expr})'

    elif node_type == 'len_stmt':
        expr = ', '.join(generate_code(expr) for expr in node[1:])
        return f'len({expr})'

    elif node_type == 'control_structure':
        return generate_code(node[1])

    elif node_type == 'if_stmt':
        condition = generate_code(node[1])
        if_body = generate_code(node[2])
        else_body = generate_code(node[3]) if len(node) > 3 else ''
        return f'if {condition}:\n{indent(if_body)}' + (f'{else_body}' if else_body else '')

    elif node_type == 'else_stmt':
        # print(node)
        if node[1][0] == 'if_stmt':
            if len(node[1]) > 2:
                condition = generate_code(node[1][1])
                if_body = generate_code(node[1][2])
                else_body = generate_code(node[1][3])
                # print('condition: ', condition)
                # print('if_body: ', if_body)
                # print('else_body: ', else_body)
                return f'\nelif {condition}:\n{indent(if_body)}' + (f'{else_body}' if else_body else '')
        else:
            else_body = generate_code(node[1])
            return f'\nelse:\n{indent(else_body)}' if else_body else ''

    elif node_type == 'while_stmt':
        condition = generate_code(node[1])
        loop_body = generate_code(node[2])
        return f'while {condition}:\n{indent(loop_body)}'

    elif node_type == 'for_stmt':
        init = generate_code(node[1])
        condition = generate_code(node[2])
        increment = generate_code(node[3][1])
        loop_body = generate_code(node[4])
        return f'{init}\nwhile {condition}:\n{indent(loop_body)}\n{indent(increment)}'

    elif node_type == 'expression':
        # print(node)
        if node[1] == 'null':
            return 'None'
        if len(node) == 2:
            return generate_code(node[1])
        elif len(node) == 3:
            op = node[1] if node[1][0] != 'assignment_sign' else generate_code(node[1])
            right = generate_code(node[2])
            # print('op:', op, 'right:', right)
            return f'{op} {right}'
        elif len(node) == 4:
            left = generate_code(node[1])
            op = generate_code(node[2])
            right = generate_code(node[3])
            print('left:', left, 'op:', op, 'right:', right)
            return f'{left} {op} {right}'
        elif len(node) == 1:
            return str(node[0])

    elif node_type == 'int':
        return node[1]

    elif node_type == 'float':
        return node[1]

    elif node_type == 'identifier':
        return node[1]

    elif node_type == 'string_literal':
        return f'"{node[1]}"'

    elif node_type == 'boolean':
        return str(node[1]).capitalize()

    elif node_type == 'function_call':
        fun_name = node[1][1]
        args = generate_code(node[2])  # Generate code for all arguments
        return f'{fun_name}({args})'

    elif node_type == 'arg_list':
        if len(node) == 2:
            return generate_code(node[1])
        else:
            return ', '.join(str(generate_code(arg)) for arg in node[1:])

    elif node_type == 'assignment_sign':
        return f'{node[1]}'

    elif node_type == 'compound_assignment':
        # print(node)
        left_expr = generate_code(node[1])
        increment = generate_code(node[2])
        right_expr = generate_code(node[3])
        return f'{left_expr} {increment} {right_expr}'

    elif node_type == 'return_stmt':
        return f'return {generate_code(node[1])}'

    elif node_type == 'break_stmt':
        return 'break'

    elif node_type == 'comment':
        comment_text = node[1]
        return f'{comment_text}'

    elif node_type == 'empty' or node_type == 'e':
        return ''

    elif node_type == 'element_access':
        array_name = generate_code(node[1])
        index = generate_code(node[2])
        return f'{array_name}[{index}]'

    elif node_type == '|':
        return 'or'

    elif node_type == '&':
        return 'and'

    else:
        return f'{node}'


def indent(code):
    return '\n'.join('    ' + line for line in code.split('\n'))
