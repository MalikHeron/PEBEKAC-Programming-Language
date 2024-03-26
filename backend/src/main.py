from code_generator import generate_code
from semantic_analyzer import parse_and_analyze

# Read the program code from a file or define it here...
program_code = """  
    fun add(int a, int c, string s) {
        return 0;
    }
    int a = 5;
    int c = 6;
    string s = "hello world";
    add(a, c, s);
    fun main() {     
        int a = 10;
        int b = 5;
        b = "h";
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
        
           
        /*
            I still see your shadows in my room
            Can't take back the love that I gave you
            It's to the point where I love and I hate you
            And I cannot change you, so I must replace you, oh
            Easier said than done, I thought you were the one
            Listenin' to my heart instead of my head
            
            changed my mind about saving tokens for comments, I just throw 
            them away now. Ignore them.
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
