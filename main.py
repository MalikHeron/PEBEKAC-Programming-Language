from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer

# Read the program code from a file or define it here...
program_code = """  
fun float area_of_circle(float radius) {
  return 3.14 * radius * radius;
}

fun main() {
  float radius = 5.0;
  float area = area_of_circle(radius);
  print("The area of the circle is ", area);
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
