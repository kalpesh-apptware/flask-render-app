# Importing necessary modules
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os
import json

# Creating a Flask application instance
app = Flask(__name__)
CORS(app)

# Defining a route for the home page
@app.route('/')
def home():
    return render_template('Home.html')

# Defining a route for an about page
@app.route('/about')
def about():
    return render_template('about.html')

# Running the application
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
