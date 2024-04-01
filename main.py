from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer

# Read the program code from a file or define it here...
program_code = """  
// This is a comment in PEBEKAC

// Declare a variable x with scope within the main function
fun main() {
    int x = 10;
    print("x inside main: ", x);

    if (true) {
        x = 15;

        print("x inside if: ", x);
    }

    print("x inside main after if: ", x);

    fun add(int a, int b) {
        int x = 3;
        print("x inside add: ", x);
    }

    add(3, 2);        
}

// Declare a variable x with scope within the function
fun scopeTest() {
    int x = 20;
    print("x inside scopeTest: ", x);
}

// Call the scopeTest function
scopeTest();
main();

// Print the value of x outside of the function
print("x outside of scope: ", x);
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
