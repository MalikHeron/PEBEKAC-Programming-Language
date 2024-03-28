from code_generator import generate_code
from semantic_analyzer import parse_and_analyze

# Read the program code from a file or define it here...
program_code = """  
     int i_number = null; # Language int null assignment outside function
     float f_number = null; # Language float  null assignment outside function
     double d_number = null; # Language double null assignment outside function
     string s_number = null; # Language string null assignment outside function
     
     i_number = 1; # Language int acceptance outside function
     f_number = 1.12; # Language float acceptance outside function
     d_number = 1.13; # Language double acceptance outside function
     s_number = "1.14"; # Language string acceptance outside function
     
     #printing single values outside function
     print(i_number); 
     print(f_number); 
     print(d_number);
     print(s_number); 
     
    
     fun add(int a, int b){
        print (a + b);
     }

    fun main() { 
        int graph = null;
        fun add(int a, int c, int s) {
            return a + s + c;
        }

        fun int subtract(int d, int e, int f ) {
          #return add(d, e, f) - e - f;  # still not possible on this branch
        }

        fun void test() {
         print("Testing void return type");
        }
      
        test();
        
        int a = 500;
        int c = 6;
        int b = 7;
        a += 4;
        int values = add(a, c, b);

        print(add(a, c, b)); 

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
