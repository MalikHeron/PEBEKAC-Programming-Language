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
        fun_name = node[1]
        params = generate_code(node[2])
        stmts = generate_code(node[3])
        return f'def {fun_name}({params}):\n{indent(stmts)}'

    elif node_type == 'params':
        if len(node) == 2:
            return ''
        else:
            return ', '.join(generate_code(param) for param in node[1])

    elif node_type == 'assignment':
        var_name = node[2]
        expr = generate_code(node[3])
        return f'{var_name} = {expr}'  # Correct assignment syntax

    elif node_type == 'print_stmt':
        expr = generate_code(node[1])  # Extract expression node directly
        return f'print({expr})'

    elif node_type == 'expression':
        if len(node) == 2:
            return f'"{node[1]}"'  # Treat literals as string literals
        elif len(node) == 3:
            op = node[1]
            right = generate_code(node[2])
            return f'{op} {right}'
        elif len(node) == 4:
            left = generate_code(node[1])
            op = node[2]
            right = generate_code(node[3])
            return f'{left} {op} {right}'
        elif len(node) == 1:
            return str(node[0])

    elif node_type == 'empty':
        return ''

    else:
        return f'Unknown node type: {node_type}'


def indent(code):
    return '\n'.join('    ' + line for line in code.split('\n'))
