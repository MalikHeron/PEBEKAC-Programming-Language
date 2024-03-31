import io
import sys
import threading
import time

from flask import Flask, request, jsonify
from flask_cors import CORS

from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer

app = Flask(__name__, static_folder='frontend/dist/', static_url_path='/')
CORS(app)  # Enable CORS for all routes

# Global variables to track whether the program should stop and the timeout period
stop_program = False
timeout_period = 5  # Timeout period in seconds

# Locks to synchronize access to stop_program and timeout_period
stop_lock = threading.Lock()
timeout_lock = threading.Lock()


@app.route('/')
def index():
    print('Request for index page received')
    return app.send_static_file('index.html')


@app.route('/compile_code', methods=['POST'])
def generate_and_execute_code():
    try:
        global stop_program  # Access the global variable
        global stop_lock  # Access the global lock
        global timeout_period  # Access the global variable
        global timeout_lock  # Access the global lock

        # Create new instances of parse_and_analyze and generate_code for each request
        semantic_analyzer = SemanticAnalyzer()

        # Reset the stop flag for each new request
        with stop_lock:
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
            # Execute the generated Python code in a separate thread
            # Pass stop_program to the execution environment
            exec_thread = threading.Thread(target=execute_code, args=(python_code_with_semantics,))
            exec_thread.start()

            # Start the timeout countdown
            start_time = time.time()

            # Wait for the execution to finish or until the stop flag is set or timeout occurs
            while exec_thread.is_alive():
                with stop_lock:
                    if stop_program:
                        break
                with timeout_lock:
                    if time.time() - start_time >= timeout_period:
                        # If timeout occurs, set the stop flag to True
                        stop_program = True
                        return jsonify({'output': 'Execution stopped due to timeout.', 'execution_complete': False})
                time.sleep(0.1)  # Check every 0.1 seconds

            # If the execution is still running, stop the thread
            if exec_thread.is_alive():
                exec_thread.join(timeout=1)

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


def execute_code(code):
    global stop_program
    try:
        exec(code, {'stop_program': stop_program})
    except Exception as e:
        print(str(e))


@app.route('/stop_execution', methods=['POST'])
def stop_execution():
    global stop_program  # Access the global variable
    with stop_lock:
        stop_program = True  # Set the stop flag to True
    return jsonify({'message': 'Execution stopped successfully'})


if __name__ == '__main__':
    app.run()
