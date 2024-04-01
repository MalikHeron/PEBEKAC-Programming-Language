import unittest

from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer


class TestCodeGeneration(unittest.TestCase):
    def setUp(self):
        # Define multiple program codes
        self.program_codes = [
            """
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
               }
               return n * factorial(n - 1);
            }

            print(factorial(5));
            """
        ]

    def test_code_generation_and_execution(self):
      self.exceptions = []  # List to store exceptions
      for i, program_code in enumerate(self.program_codes, start=1):
         try:
               # Parse and analyze the program
               ast_with_semantics = SemanticAnalyzer().parse_and_analyze(program_code)

               # Generate Python code with semantics
               python_code_with_semantics = generate_code(ast_with_semantics)

               # Save the generated Python code to a file
               with open(f'generated_code-{i}.py', 'w') as file:
                  file.write(python_code_with_semantics)

               exec(open(f'generated_code-{i}.py').read(), globals())
         except Exception as e:
               self.exceptions.append(str(e))  # Convert the exception to a string before appending
               continue  # Skip to the next program code

      # If there were any exceptions, fail the test
      if self.exceptions:
         error_messages = "\n".join(self.exceptions)  # Now this should work
         self.fail("Errors during code generation, analysis or execution:\n{}".format(error_messages))



if __name__ == '__main__':
    unittest.main()
