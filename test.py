import os
import unittest

from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer


class TestCodeGeneration(unittest.TestCase):
    def setUp(self):
        # Ensure the test_runs directory exists
        self.output_dir = "test_runs"
        os.makedirs(self.output_dir, exist_ok=True)

        # Define test cases as a dictionary {test_name: code}
        self.test_cases = {
            "test_string_equality": """
                fun boolean stringEquals(string string1, string string2) {
                    return string1 == string2;
                }

                fun main() {
                    if (stringEquals("Hello", "hello")) {
                        print("The strings are equal");
                    } else {
                        print("The strings are not equal");
                    }
                }

                main();
                """,
            "test_factorial": """
                fun int factorial(int n) {
                    if (n == 0) {
                        return 1;
                    }
                    return n * factorial(n - 1);
                }

                print(factorial(5));
                """
        }

    def run_test_case(self, test_name, test_code):
        try:
            # Parse and analyze the program
            ast_with_semantics = SemanticAnalyzer().parse_and_analyze(test_code)

            # Generate Python code with semantics
            python_code_with_semantics = generate_code(ast_with_semantics)

            # Specify the file path within the test_runs directory
            file_path = os.path.join(self.output_dir, f'{test_name}.py')

            # Save the generated Python code to a file in the specified directory
            with open(file_path, 'w') as file:
                file.write(python_code_with_semantics)

            # Execute the generated Python code
            exec(open(file_path).read(), globals())
        except Exception as e:
            self.fail(f"{test_name} failed with error: {e}")

    def test_string_equality(self):
        self.run_test_case("test_string_equality", self.test_cases["test_string_equality"])

    def test_factorial(self):
        self.run_test_case("test_factorial", self.test_cases["test_factorial"])


if __name__ == '__main__':
    unittest.main()
