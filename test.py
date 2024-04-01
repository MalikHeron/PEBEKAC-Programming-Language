import unittest

from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer


class TestCodeGeneration(unittest.TestCase):
    def setUp(self):
        # Define multiple program codes
        self.program_codes = [
            """  
            # Program code 1
            # Check if two strings are the same
fun boolean stringEquals(string string1, string string2) {
    return string1 == string2;
}

// main function
fun main() {
    // call the equals function to compare the two strings
    if (stringEquals("Hello", "hello")) {
        print("The strings are equal");
    } else {
        print("The strings are not equal");
    }
}

main();
            """,
            """  
            fun int factorial(int n) {
    if (n == 0) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

print(factorial(5));
            """
        ]

    def test_code_generation_and_execution(self):
        for program_code in self.program_codes:
            # Parse and analyze the program
            ast_with_semantics = SemanticAnalyzer().parse_and_analyze(program_code)

            # Generate Python code with semantics
            python_code_with_semantics = generate_code(ast_with_semantics)

            # Save the generated Python code to a file
            with open('generated_code.py', 'w') as file:
                file.write(python_code_with_semantics)

            # Execute the generated Python code
            try:
                exec(open('generated_code.py').read())
            except Exception as e:
                self.fail("Error executing generated code: {}".format(e))


if __name__ == '__main__':
    unittest.main()
