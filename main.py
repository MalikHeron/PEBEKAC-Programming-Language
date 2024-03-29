
from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer

# Read the program code from a file or define it here...
program_code = """  
fun int stringLength(stringList str) {
    int count = 0;
    for(int i = 0; str[i] != null; i++) {
        count = count + 1;
    }
    return count;
}

// Assuming a mechanism to initialize a stringList with characters
// This part is abstract, as direct string manipulation isn't detailed in the language spec
stringList myString = ["H", "e", "l", "l", "o"];

// Call the stringLength function and print the result
print(myString);
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
