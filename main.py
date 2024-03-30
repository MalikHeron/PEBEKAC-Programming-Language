from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer

# Read the program code from a file or define it here...
program_code = """  
fun boolean isPalindrome(string str) {
  int length = len(str);
  int i = 0;
  int j = length - 1;
  while (i < j) {
    if (str[i] != str[j]) {
      return false;
    }
    i = i + 1;
    j = j - 1;
  }
  return true;
}

fun main() {
  string str = "racecar";
  if (isPalindrome(str)) {
    print("The string is a palindrome.");
  } else {
    print("The string is not a palindrome.");
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
