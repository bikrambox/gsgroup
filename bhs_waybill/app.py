from flask import Flask, render_template, jsonify
from waybill_ftp import FTPConnection
import logging

app = Flask(__name__, 
           static_folder='static',
           template_folder='templates')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ftp = FTPConnection()

@app.route('/')
def index():
    logger.info("Serving SPA index page")
    return render_template('index.html')

@app.route('/api/ftp/connect', methods=['GET'])
def ftp_connect():
    logger.info("API request to connect to FTP")
    result = ftp.connect()
    return jsonify(result)

@app.route('/api/ftp/list', methods=['GET'])
def ftp_list():
    logger.info("API request to list FTP directory")
    result = ftp.list_dir()
    return jsonify(result)

if __name__ == '__main__':
    # This will only be used in development
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5500))
    app.run(debug=True, host=host, port=port)
