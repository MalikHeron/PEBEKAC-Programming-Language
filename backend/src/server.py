import io
import sys

from flask import Flask, request, jsonify
from flask_cors import CORS

from code_generator import generate_code
from semantic_analyzer import parse_and_analyze

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable to store user inputs
user_input_queue = []
# Global variable to track whether the program should stop
stop_program = False


@app.route('/compile_code', methods=['POST'])
def generate_and_execute_code():
    try:
        global stop_program  # Access the global variable

        # Reset the stop flag for each new request
        stop_program = False

        # Read the program code from the request
        program_code = request.json.get('program_code')

        # Parse and analyze the program
        ast_with_semantics = parse_and_analyze(program_code)

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
            return jsonify({'output': error_message, 'execution_complete': False}), 500
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


@app.route('/provide_input', methods=['POST'])
def provide_input():
    try:
        # Read the input from the request
        user_input = request.json.get('input')
        # Append the user input to the global list
        user_input_queue.append(user_input)
        return jsonify({'message': 'Input received successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_input', methods=['GET'])
def get_input():
    try:
        # Check if there are pending user inputs
        if user_input_queue:
            # Pop the first user input from the queue
            input_value = user_input_queue.pop(0)
            return jsonify({'input': input_value})
        else:
            # Return an empty response if no inputs are available
            return jsonify({'input': None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
