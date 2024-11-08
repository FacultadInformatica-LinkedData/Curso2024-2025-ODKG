# app.py
from flask import Flask, render_template
from flask_cors import CORS 
from back import api  # Import the blueprint from back.py

app = Flask(__name__)
CORS(app)  # Enable CORS in the app

# Register the blueprint in the application
app.register_blueprint(api)

# Route to serve the main HTML file (frontend)
@app.route('/')
def index():
    return render_template('index.html')

# Run the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
