# from waitress import serve
# from app import app
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# if __name__ == '__main__':
#     host = os.getenv('HOST', '0.0.0.0')
#     port = int(os.getenv('PORT', 5500))
    
#     print(f"Starting BHS Waybill in production mode on {host}:{port}...")
#     serve(app, host=host, port=port)


from flask import Flask, render_template, jsonify
from waybill_ftp import FTPConnection
import os
from waitress import serve
from app import app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__, 
           static_folder='static',
           template_folder='templates')

# Initialize FTP connection
ftp = FTPConnection()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ftp/connect', methods=['GET'])
def ftp_connect():
    result = ftp.connect()
    return jsonify(result)

@app.route('/api/ftp/list', methods=['GET'])
def ftp_list():
    result = ftp.list_dir()
    return jsonify(result)

# Your other routes here...

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5500))
    
    print(f"Starting BHS Waybill in production mode on {host}:{port}...")
    serve(app, host=host, port=port)

