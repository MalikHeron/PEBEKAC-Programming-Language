from flask import Flask, request, jsonify
from flask_cors import CORS
from code_generator import generate_code
from semantic_analyzer import parse_and_analyze
import sys
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/compile_code', methods=['POST'])
def generate_and_execute_code():
    # Read the program code from the request
    program_code = request.json.get('program_code')

    # Parse and analyze the program
    ast_with_semantics = parse_and_analyze(program_code)

    # Generate Python code with semantics
    python_code_with_semantics = generate_code(ast_with_semantics)

    print(python_code_with_semantics)
    # Capture standard output and standard error
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        # Execute the generated Python code
        exec(python_code_with_semantics)
        # Get the captured output
        output = sys.stdout.getvalue()
        # Reset standard output and standard error
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return jsonify({'output': output})
    except Exception as e:
        # Get the captured error message
        error_message = str(e)
        # Reset standard output and standard error
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return jsonify({'error': error_message}), 500


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
