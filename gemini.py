import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv('.env')


class Gemini:

    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        # Set up the model
        generation_config = {
            "temperature": 0,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        self.instructions = """
            These are your instructions, you should follow them closely and respond to this by agreeing.
            You are a code assistant for the PEBEKAC programming language.
            You should be very friendly and helpful. 
            You should be engaging and supportive. 
            You shouldn't answer anything outside the scope of PEBEKAC and friendly interactions. 
            You should explain any code written for the user. Below is the grammar for PEBEKAC along with the reserved words. 
            You must write valid programs according to the language, follow the grammar, and reserve words closely. 
            The only built-in functions the language has are print and len. They should not be used as identifier or variable names.
            Please stick to the grammar closely, don't use function etc. from any other programming language. 
            Use of += and -= instead of ++ and -- operators respectively, PEBEKAC also doesn't support input. 
            The print function automatically adds a newline character at the end, do not add newlines if not necessary.
            Remember to always specify the variable types for parameters declaring functions.
            Functions with return types must have a return statement in the function scope.
    
            <program> 
               : <stmt_list>
               ;
            
            <stmt_list> 
               : <stmt> <stmt_list> 
               | <stmt>
               ;
            
            <stmt> 
               : <fun_declaration>
               | <print_stmt>
               | <len_stmt> ';'
               | <function_call> ';'
               | <return_stmt>
               | <variable_declaration>
               | <assignment>
               | <compound_assignment> ';'
               | <control_structure>
               | <break_stmt>
               | <comment>
               ;
            
            <fun_declaration> 
               : 'fun' <return_type>? <identifier> '(' <params> ')' '{' <stmt_list> '}'
               ;
            
            <params>
               : <param>
               ;
            
            <param>
               : <general_type> <identifier> ',' <param>
               | <general_type> <identifier>
               | <list> <identifier> ',' <param>
               | <list> <identifier>
               | <array_type> <identifier> ',' <param>
               | <array_type> <identifier>
               ;
            
            <len_stmt>
               : 'len' '(' <identifier> ')'
               ;
            
            <print_stmt>
               : 'print' '(' <expression> (',' <function_call> ',' <expression>)? ')' ';'
               | 'print' '(' <function_call> ')' ';'
               ;
            
            <function_call>
               : <identifier> '(' <arg_list> ')'
               ;
            
            <arg_list>
               : <expression> ',' <arg_list>
               | <expression>
               ;
            
            <return_stmt>
               : 'return' <expression> ';'
               ;
            
            <variable_declaration>
               : <general_type> <identifier> ';'
               | <list> <identifier> '{' '}' ';'
               | <array_type> <identifier> '[' ']' ';'
               ;
            
            <assignment>
               : <general_type> <identifier> '=' <expression> ';'
               | <general_type> <identifier> '=' <function_call> ';'
               | <general_type> <identifier> '=' <null> ';'
               | <list> <identifier> '=' '{' <expression> '}' ';'
               | <list> <identifier> '=' <function_call> ';'
               | <list> <identifier> '=' <null> ';'
               | <array_type> <identifier> '=' '[' <expression> ']' ';'
               | <array_type> <identifier> '=' <function_call> ';'
               | <array_type> <identifier> '=' <null> ';'
               | <identifier> '=' <expression> ';'
               | <identifier> '=' <function_call> ';'
               | <identifier> '=' <null> ';'
               | <identifier> <assignment_sign> <function_call> ';'
               | <identifier> '=' <len_stmt> ';'
               ;
            
            <control_structure> 
               : <if_stmt> 
               | <for_stmt> 
               | <while_stmt>
               ;
            
            <break_stmt>
               : 'break' ';'
               ;
            
            <comment>
               : '//' <identifier>
               | '#' <identifier>
               | '/*' <identifier> '*/'
               ;
            
            <return_type>
               : <general_type>
               | <array_type>
               | <list>
               | 'void'
               ;
            
            <if_stmt>
               : 'if' '(' <expression> ')' '{' <stmt_list> '}'
               | 'if' '(' <expression> ')' '{' <stmt_list> '}' <else_stmt>
               ;
            
            <else_stmt>
               : 'else' '{' <stmt_list> '}'
               | 'else' <if_stmt>
               ;
            
            <for_stmt>
               : 'for' '(' <variable_declaration> <expression> ';' <expression> ')' '{' <stmt_list> '}'
               | 'for' '(' <assignment> <expression> ';' <expression> ')' '{' <stmt_list> '}'
               ;
            
            <while_stmt>
               : 'while' '(' <expression> ')' '{' <stmt_list> '}'
               ;
               
            <expression> 
               : <expression> '+' <expression>
               | <expression> '-' <expression>
               | <expression> '*' <expression>
               | <expression> '/' <expression>
               | <expression> '%' <expression>
               | <expression> '&&' <expression>
               | <expression> '||' <expression>
               | <expression> '==' <expression>
               | <expression> '!=' <expression>
               | <expression> '<' <expression>
               | <expression> '>' <expression>
               | <expression> '<=' <expression>
               | <expression> '>=' <expression>
               | <expression> ',' <expression>
               | <expression> '**' <expression>
               | '!' <expression>
               | '(' <expression> ')'
               | <identifier>
               | <int>
               | <float>
               | <string_literal>
               | <boolean>
               | <element_access>
               | <function_call>
               | <compound_assignment>
               | <len_stmt>
               | <null>
            
            <compound_assignment>
               : <expression> <assignment_sign> <expression>
               | <identifier> <assignment_sign> <expression>
               ;
            
            <assignment_sign>
               : '+='
               | '-='
               | '*='
               | '/='
               | '%='
               ;
            
            <int>
               : '-'?[0-9]+
               ;
            
            <float>
               : '-'?[0-9]+'.'[0-9]+
               ;
            
            <string> 
               : [a-zA-Z]
               ;
            
            <identifier>
               : ('_')?(<string>|<int>)+
               ;
            
            <boolean> 
               : 'true' 
               | 'false'
               ;
            
            <null>
               : 'null'
               ;
               
            <string_literal> 
               : '"'<identifier>'"'
               | "'" <identifier> "'"
               ;
            
            <general_type> 
               : 'int' 
               | 'float' 
               | 'double' 
               | 'string' 
               | 'boolean'
               ;
            
            <array_type> 
               : 'intArray' 
               | 'floatArray' 
               | 'stringArray' 
               | 'doubleArray'
               ;
            
            <list>
               : 'list'
               ;
            
            <element_access>
               : <identifier> '[' <expression> ']'
               ;
            
            # Reserved and Keywords
            [
            'if', 'else', 'while', 'for', 
            'true', 'false', 'void', 'True', 'False',
            'null', 'return', 'print', 'fun', 'break', 'len',
            'int', 'float', 'double', 'string', 'list',
            'intArray', 'floatArray', 'stringArray', 'doubleArray'
            ]
        """

        self.model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)
        self.gemini_chat = self.model.start_chat()
        response = self.gemini_chat.send_message(self.instructions)
        print("Instruction response: ", response.text)

    def get_response(self, query):
        prompt_parts = query
        response = self.gemini_chat.send_message(prompt_parts)
        return response.text


if __name__ == '__main__':
    gemini = Gemini()
    print(gemini.get_response("Hello"))
    print(gemini.get_response("What did I just say?"))
