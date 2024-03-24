def generate_code(node):
    node_type = node[0]

    if node_type == 'program':
        return generate_code(node[1])

    elif node_type == 'stmt_list':
        return '\n'.join(generate_code(stmt) for stmt in node[1:])

    elif node_type == 'class_declaration':
        class_name = node[1]
        stmts = generate_code(node[2])
        return f'class {class_name}:\n{indent(stmts)}'

    elif node_type == 'fun_declaration':
        fun_name = node[1][1]
        params = generate_code(node[2])
        stmts = generate_code(node[3])
        return f'def {fun_name}({params}):\n{indent(stmts)}'

    elif node_type == 'params':
        if len(node) == 2:
            return ''
        else:
            return ', '.join(generate_code(param) for param in node[1])

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
        if node[1][0] == 'general_type' or node[1][0] == 'list_type' or node[1][0] == 'array_type':
            var_name = node[2][1]
            expr = generate_code(node[3])
            return f'{var_name} = {expr}'  # Correct assignment syntax
        else:
            var_name = node[1][1]
            expr = generate_code(node[2])
            return f'{var_name} = {expr}'

    elif node_type == 'print_stmt':
        expr = generate_code(node[1])  # Extract expression node directly
        return f'print({expr})'

    elif node_type == 'control_structure':
        return generate_code(node[1])

    elif node_type == 'if_stmt':
        condition = generate_code(node[1])
        if_body = generate_code(node[2])
        else_body = generate_code(node[3]) if len(node) > 3 else ''
        return f'if {condition}:\n{indent(if_body)}' + (f'\nelse:\n{indent(else_body)}' if else_body else '')

    elif node_type == 'while_stmt':
        condition = generate_code(node[1])
        loop_body = generate_code(node[2])
        return f'while {condition}:\n{indent(loop_body)}'

    elif node_type == 'for_stmt':
        init = generate_code(node[1])
        condition = generate_code(node[2])
        increment = generate_code(node[3])
        loop_body = generate_code(node[4])
        return f'{init}\nwhile {condition}:\n{indent(loop_body)}\n  {increment}'

    elif node_type == 'switch_stmt':
        expression = generate_code(node[1])
        case_stmts = generate_code(node[2])
        default_stmt = generate_code(node[3])
        return f'switch {expression}:\n{indent(case_stmts)}\n{indent(default_stmt)}'

    elif node_type == 'case_stmts':
        if len(node) == 2:
            return generate_code(node[1])
        else:
            return generate_code(node[1]) + '\n' + generate_code(node[2])

    elif node_type == 'default_stmt':
        return generate_code(node[1])

    elif node_type == 'digit':
        return str(node[1])

    elif node_type == 'identifier':
        return node[1]

    elif node_type == 'string_literal':
        return f'"{node[1]}"'

    elif node_type == 'boolean':
        return str(node[1]).lower()

    elif node_type == 'expression':
        if len(node) == 2:
            return generate_code(node[1])

        elif len(node) == 3:
            op = node[1]
            right = generate_code(node[2])
            return f'{op} {right}'
        elif len(node) == 4:
            left = generate_code(node[1])
            op = node[2]
            right = generate_code(node[3])
            if op == '+':
                # Check if either operand is a string
                if isinstance(left, str) or isinstance(right, str):
                    # Convert both operands to strings before concatenation
                    return f'str({left}) + str({right})'
                else:
                    return f'{left} + {right}'
            else:
                return f'{left} {op} {right}'
        elif len(node) == 1:
            return str(node[0])

    elif node_type == 'function_call':
        fun_name = node[1]
        args = generate_code(node[2])
        return f'{fun_name}({args})'

    elif node_type == 'args':
        if len(node) == 2:
            return generate_code(node[1])
        else:
            return generate_code(node[1]) + ', ' + generate_code(node[2])

    elif node_type == 'return_stmt':
        return f'return {generate_code(node[1])}'

    elif node_type == 'comment':
        comment_text = node[1]
        return f'{comment_text}'

    elif node_type == 'empty':
        return ''

    else:
        return f'Unknown node type: {node_type}'


def indent(code):
    return '\n'.join('    ' + line for line in code.split('\n'))
