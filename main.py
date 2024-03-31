from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer

# Read the program code from a file or define it here...
program_code = """  
fun stringList caesarCypher(string text, int shift) {
    stringList result = null;
    for (int i = 0; i < len(text); i += 1) {
        string c = text[i];
        if (c >= "a" && c <= "z") {
            c = (c - "a" + shift) % 26 + "a";
        } else if (c >= "A" && c <= "Z") {
            c = (c - "A" + shift) % 26 + "A";
        }
        result = result + c;
    }
    return result;
}
"""

# Parse and analyze the program
ast_with_semantics = SemanticAnalyzer().parse_and_analyze(program_code)

# Generate Python code with semantics
python_code_with_semantics = generate_code(ast_with_semantics)
print(python_code_with_semantics)

# Save the generated Python code to a file
with open('generated_code.py', 'w') as file:
    file.write(python_code_with_semantics)

# Execute the generated Python code
try:
    exec(open('generated_code.py').read())
except Exception as e:
    print("Error executing generated code:", e)
else:
    print("Generated code executed successfully!")
