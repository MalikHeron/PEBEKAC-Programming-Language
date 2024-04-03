import os
import unittest

from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer


class CodeGeneration(unittest.TestCase):
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
            """,
            "test_prime_number_checker": """
                fun main() {
                    int num = 10;
                    boolean isPrime = true;
                    for (int i = 2; i <= num / 2; i += 1) {
                        if (num % i == 0) {
                            isPrime = false;
                            break;
                        }
                    }
                    if (isPrime) {
                        print("The number is prime");
                    } else {
                        print("The number is not prime");
                    }
                }

                main();
            """,
            "test_fibonacci_series": """
                fun main() {
                    int num = 10;
                    int a = 0;
                    int b = 1;
                    for (int i = 0; i < num; i +=1 ) {
                        print(a);
                        int temp = a;
                        a = b;
                        b = temp + b;
                    }
                }

                main();
            """,
            "test_scopes": """
                fun void main() {
                    int a = 10;
                    doubleArray x = [2.5, 3.5];
                    
                    if (a == 10) {
                        a = 20;
                        print(a); // prints 20
                    }
                    print(a); // prints 10
                }

                main();
            """,
            "test_assignment_inside": """
                fun void main() {
                    int a = 10;
                    doubleArray x = [2.5, 3.5];
                    a = 20;
                    print(a); // prints 20
                }
                
                int a = 5;
                
                main();            
            """,
            "test_assignment_outside": """
                int a = 5;
                a = 2;
                
                fun void main() {
                    int a = 10;
                    doubleArray x = [2.5, 3.5];
                    print(a); // prints 10
                }
                
                print(a); // prints 5
                
                main();
            """,
            "test_function_call": """
                fun void printSum(int a, int b) {
                    print(a + b);
                }
                
                list x = {1, "hello"};
                x = 5;
                
                fun void main() {
                    int x = 10;
                    int b = 20;
                    printSum(x, b);
                    
                    fun void prints(int a, int b) {
                        a = 5;
                        b = 2;
                    }
                    
                    prints(x, b);
                }
                
                main();
            """,
            "test_function_call_with_return": """
                int p = 5;
                fun void main() {
                    int a = 10;
                    int b = 20;
                    
                    fun int sum(int a, int b) {
                        int x = 5;
                        x = 2;
                        p = 5;
                        return a + b;
                    }
                    
                    print(sum(a, b));
                }
                
                int a = 10;
                a = 2;
                
                main();
            """,

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

    def test_prime_number_checker(self):
        self.run_test_case("test_prime_number_checker", self.test_cases["test_prime_number_checker"])

    def test_fibonacci_series(self):
        self.run_test_case("test_fibonacci_series", self.test_cases["test_fibonacci_series"])

    def test_scopes(self):
        self.run_test_case("test_scopes", self.test_cases["test_scopes"])

    def test_assignment_inside(self):
        self.run_test_case("test_assignment_inside", self.test_cases["test_assignment_inside"])

    def test_assignment_outside(self):
        self.run_test_case("test_assignment_outside", self.test_cases["test_assignment_outside"])

    def test_function_call(self):
        self.run_test_case("test_function_call", self.test_cases["test_function_call"])

    def test_function_call_with_return(self):
        self.run_test_case("test_function_call_with_return", self.test_cases["test_function_call_with_return"])


if __name__ == '__main__':
    unittest.main()
