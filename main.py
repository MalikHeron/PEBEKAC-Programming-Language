from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer

# Read the program code from a file or define it here...
program_code = """  
# Check if two strings are the same
fun boolean stringEquals(string string1, string string2) {
    return string1 == string2;
}

// main function
fun main() {
    int a = 5;
    // call the equals function to compare the two strings
    if (stringEquals("Hello", "hello")) {
        print("The strings are equal");
    } else {
        print("The strings are not equal");
    }

    fun sum(float a, float b) {
        print(a + b);
    }
}

main();
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
