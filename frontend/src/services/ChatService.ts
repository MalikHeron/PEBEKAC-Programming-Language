import { GoogleGenerativeAI, HarmCategory, HarmBlockThreshold } from "@google/generative-ai";

const MODEL_NAME = "gemini-1.0-pro";

/**
 * Represents a service for interacting with the chat functionality.
 */
export class ChatService {

   public async getResponse(query: string): Promise<string> {
      const genAI = new GoogleGenerativeAI("AIzaSyC8Rv2N81nwr5KruEfg8rQ27ap5GFAZzlU");
      const model = genAI.getGenerativeModel({ model: MODEL_NAME });

      const generationConfig = {
         temperature: 0.9,
         topK: 1,
         topP: 1,
         maxOutputTokens: 2048,
      };

      const safetySettings = [
         {
            category: HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
         },
         {
            category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
         },
         {
            category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
         },
         {
            category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
         },
      ];

      const parts = [
         { text: `
         You are a code assistant for the PEBEKAC programming language. 
         Do not answer any query that isn't related to coding in PEBEKAC. 
         This is the grammar of the language along with the reserve words, 
         you must write valid programs according to the language, don't make any assumptions:

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
               | <function_call> ';'
               | <return_stmt>
               | <variable_declaration>
               | <assignment>
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
               : <general_type> <identifier> '(' ',' <variable_declaration>+')'? ';'
               | <list_type> <identifier> '[' ']' '(' ',' <variable_declaration>+')'? ';'
               | <array_type> <identifier> '{' '}' '(' ',' <variable_declaration>+')'? ';'
               ;
         
         <assignment>
               : <general_type> <identifier> '=' <expression> ';'
               | <general_type> <identifier> '=' <function_call> ';'
               | <general_type> <identifier> '=' <null> ';'
               | <list_type> <identifier> '=' <null> ';'
               | <list_type> <identifier> '[' <digit> ']' '=' <null> ';'
               | <list_type> <identifier> '[' <digit> ']' '=' <expression> ';'
               | <list_type> <identifier> '[' <digit> ']' '=' <function_call> ';'
               | <list_type> <identifier> '=' '[' <expression> ']' ';'
               | <list_type> <identifier> '=' <function_call> ';'
               | <array_type> <identifier> '=' <null> ';'
               | <array_type> <identifier> '{' <digit> '}' '=' <null> ';'
               | <array_type> <identifier> '{' <digit> '}' '=' <expression> ';'
               | <array_type> <identifier> '{' <digit> '}' '=' <function_call>
               | <array_type> <identifier> '=' '{' <expression> '}' ';'
               | <array_type> <identifier> '=' <function_call> ';'
               | <identifier> '=' <expression> ';'
               | <identifier> '=' <function_call> ';'
               | <identifier> '=' <null> ';'
               ;
         
         <control_structure> 
               : <if_stmt> 
               | <for_stmt> 
               | <while_stmt> 
               | <switch_stmt>
               ;
         
         <break_stmt>
               : 'break' ';'
               ;
         
         <comment>
               : '//' <identifier>
               | '#' <identifier>
               | '/*' <identifier>  '*/'
               ;
         
         <return_type>
               : <general_type>
               | <array_type>
               | <list_type>
               ;
         
         <if_stmt>
               : 'if' '(' <expression> ')' '{' <stmt_list> '}' 'else' '{' <stmt_list> '}'
               | 'if' '(' <expression> ')' '{' <stmt_list> '}' 'else' <if_stmt>
               | 'if' '(' <expression> ')' '{' <stmt_list> '}'
               | <expression> '?' <expression> ':' <expression> ';'
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
               | <expression> '+=' <expression>
               | <expression> '-=' <expression>
               | <expression> '*=' <expression>
               | <expression> '/=' <expression>
               | <expression> '%=' <expression>
               | <expression> '++'
               | <expression> '--'
               | '++' <expression>
               | '--' <expression>
               | <expression> ',' <expression>
               | <expression> '**' <expression>
               | '!' <expression>
               | '(' <expression> ')'
               | <identifier>
               | <digit>
               | <string_literal>
               | <boolean>
               | <null>
               | <identifier> '[' <expression> ']'
               | <identifier> '{' <expression> '}'
         
         <digit> 
               : '-'?[0-9]+('.'[0-9]+)? 
               ;
         
         <string> 
               : [a-zA-Z]
               ;
         
         <identifier>
               : ('_')?(<string>|<digit>)+
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
         
         <list_type> 
               : 'intList' 
               | 'floatList' 
               | 'stringList' 
               | 'doubleList'
               ;
         
         # Reserved and Keywords
         [
            'if', 'else', 'while', 'for', 
            'true', 'false', 'void'
            'null', 'return', 'print', 'fun', 'break',
            'int', 'float', 'double', 'string', 
            'intArray', 'floatArray', 'stringArray', 'doubleArray',
            'intList', 'floatList', 'stringList', 'doubleList'
         ]
         
         \nQuery: ${query}` },
      ];

      const result = await model.generateContent({
         contents: [{ role: "user", parts }],
         generationConfig,
         safetySettings,
      });

      const response = result.response;
      console.log(response.text());
      return response.text();
   }
}