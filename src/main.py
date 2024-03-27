from code_generator import generate_code
from semantic_analyzer import parse_and_analyze

# Read the program code from a file or define it here...
program_code = """  

    int graph;
    fun add(int a, int c, int s) {
        return a + s + c;
    }
    
    
    int fun subtract(int d, int e, int f ) {
        return d - e - f; 
    }
    
    int a = 5;
    int c = 6;
    int b = 7;
    string s = "hello world";
    
    int values = add(a, c, b);
    
    fun main() {     
        int a = 10;
        int b = 5;
        int x = 5;
        string code = "John";
        print("Hello World, my name is ");

        if (x == 10) {
            print("x = 10");
        } else {
            print("x != 10");
        }

        while(x) {
            print("x is not zero");
            break;
        }
        
        print("x = " + 5);
        
         for (int i = 0; i < 10; i++){
            print("x = " + 5);
        }
           
        /*
            This is a comment
            This is a comment
            This is a comment
            This is a comment
            This is a comment
            
            Comment tokens are not saved. Once recognized they are ignore them.
        */   
    }    
"""

# Parse and analyze the program
ast_with_semantics = parse_and_analyze(program_code)

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
