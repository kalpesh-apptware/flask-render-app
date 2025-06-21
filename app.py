from flask import Flask, request, jsonify, render_template, abort, send_file
import json
import os
import secrets
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY_FILE = 'api_keys.json'
LAST_JSON_FILE = 'last_output.json'

# Load stored keys
def load_api_keys():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            return json.load(f)
    return []

# Validate API key decorator
def require_api_key(f):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key not in load_api_keys():
            abort(401, description="Unauthorized: Invalid API Key")
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Main page renders index.html
@app.route('/')
def home():
    return render_template('index.html')

# API to generate API key
@app.route('/generate-api-key', methods=['POST'])
def generate_api_key():
    new_key = secrets.token_hex(32)
    keys = load_api_keys()
    keys.append(new_key)
    with open(API_KEY_FILE, 'w') as f:
        json.dump(keys, f, indent=2)
    return jsonify({"api_key": new_key})

# Cogniac submits JSON here
@app.route('/submit-json', methods=['POST'])
@require_api_key
def submit_json():
    try:
        data = request.get_json()
        with open(LAST_JSON_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "success", "message": "JSON received and stored."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Frontend loads latest JSON here
@app.route('/json-view')
def json_view():
    if not os.path.exists(LAST_JSON_FILE):
        return "No data", 404
    with open(LAST_JSON_FILE, 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
