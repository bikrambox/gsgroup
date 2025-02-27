from flask import Flask, render_template
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Production configuration from environment variables
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
app.config['TESTING'] = os.getenv('TESTING', 'False').lower() == 'true'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # This will only be used in development
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5500))
    app.run(host=host, port=port)
