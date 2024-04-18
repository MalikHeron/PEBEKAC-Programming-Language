import os
import binascii
import io
import sys
import threading
import time
import secrets

from datetime import datetime, timedelta
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session

from code_generator import generate_code
from semantic_analyzer import SemanticAnalyzer
from gemini import Gemini

app = Flask(__name__, static_folder='frontend/dist/', static_url_path='/')
app.secret_key = secrets.token_hex(32)
CORS(app)  # Enable CORS for all routes

# Configure Flask Session
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

# Global variables to track whether the program should stop and the timeout period
stop_program = False
timeout_period = 5  # Timeout period in seconds

# Locks to synchronize access to stop_program and timeout_period
stop_lock = threading.Lock()
timeout_lock = threading.Lock()

# Dictionary to store chatbot instances
chatbots = {}


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


@app.route('/start_gemini', methods=['POST'])
def start_gemini():
    # Create a new instance of the Gemini chatbot for this session
    if 'user_id' not in session:
        # Generate a unique ID for each user
        session['user_id'] = binascii.b2a_hex(os.urandom(15)).decode('utf-8')
    user_id = session['user_id']
    chatbots[user_id] = {'gemini': Gemini(), 'last_active': datetime.now()}
    return jsonify({'response': user_id})


@app.route('/get_response', methods=['POST'])
def get_response():
    query = request.json.get('query')
    user_id = request.json.get('userId')
    if user_id and user_id in chatbots:
        gemini = chatbots[user_id]['gemini']
        # Update the last active time
        chatbots[user_id]['last_active'] = datetime.now()
        return jsonify({'response': gemini.get_response(query)})
    else:
        return jsonify({'error': 'No chatbot instance found for this session. Start a new chatbot instance.'})


# Run a background task to clear inactive chatbot instances
def clear_inactive_chatbots():
    while True:
        for user_id, data in list(chatbots.items()):
            if datetime.now() - data['last_active'] > timedelta(minutes=30):  # 30 minutes timeout
                del chatbots[user_id]
        time.sleep(86400)  # Check every 24 hours


clear_thread = threading.Thread(target=clear_inactive_chatbots)
clear_thread.start()

if __name__ == '__main__':
    app.run()
