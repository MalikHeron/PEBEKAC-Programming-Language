import io
import sys

from flask import (Flask, request, jsonify)
from flask_cors import CORS

from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer

app = Flask(__name__, static_folder='frontend/dist/', static_url_path='/')
CORS(app)  # Enable CORS for all routes

# Global variable to track whether the program should stop
stop_program = False


@app.route('/')
def index():
    print('Request for index page received')
    return app.send_static_file('index.html')


@app.route('/compile_code', methods=['POST'])
def generate_and_execute_code():
    try:
        global stop_program  # Access the global variable
        # Create new instances of parse_and_analyze and generate_code for each request
        semantic_analyzer = SemanticAnalyzer()

        # Reset the stop flag for each new request
        stop_program = False

        # Read the program code from the request
        program_code = request.json.get('program_code')

        # Parse and analyze the program
        ast_with_semantics = semantic_analyzer.parse_and_analyze(program_code)

        # Generate Python code with semantics
        python_code_with_semantics = generate_code(ast_with_semantics)

        # Capture standard output and standard error
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        try:
            # Execute the generated Python code
            # Pass stop_program to the execution environment
            exec(python_code_with_semantics, {'stop_program': stop_program})
            # Get the captured output
            output = sys.stdout.getvalue()
            # Reset standard output and standard error
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            # Indicate execution complete
            return jsonify({'output': output, 'execution_complete': True})
        except Exception as e:
            # Get the captured error message
            error_message = str(e)
            # Reset standard output and standard error
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            return jsonify({'output': error_message, 'execution_complete': False})
    except Exception as e:
        # Get the captured error message
        error_message = str(e)
        # Reset standard output and standard error
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return jsonify({'output': error_message, 'execution_complete': False})


@app.route('/stop_execution', methods=['POST'])
def stop_execution():
    global stop_program  # Access the global variable
    stop_program = True  # Set the stop flag to True
    return jsonify({'message': 'Execution stopped successfully'})


if __name__ == '__main__':
    app.run()
