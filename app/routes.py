from flask import Blueprint, request, jsonify
from threading import Thread
from model import generate_text

routes = Blueprint('routes', __name__)

def handle_generate_request(data, response_container):
    prompt = data.get("prompt", "")
    max_tokens = data.get("max_tokens", None)
    temperature = data.get("temperature", None)
    
    if not prompt:
        response_container["response"] = {"error": "No prompt provided"}, 400
    else:
        response = generate_text(prompt, max_tokens, temperature)
        response_container["response"] = {"response": response}

@routes.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    response_container = {}
    thread = Thread(target=handle_generate_request, args=(data, response_container))
    thread.start()
    thread.join()  # Wait for the thread to finish
    return jsonify(response_container["response"])

@routes.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"})
