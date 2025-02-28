from flask import Flask, render_template, jsonify, request, Response, send_file
from flask_cors import CORS
from waybill_ftp import FTPConnection  # Updated import
import logging
import os
from dotenv import load_dotenv
import io
import sqlite3
import time

# Load environment variables before anything else
load_dotenv()

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Enable CORS for all routes, ensuring HTTPS and cross-browser compatibility
CORS(app, resources={r"/api/*": {"origins": ["https://vps1139.basicserver.io:42030"], "allow_headers": ["Content-Type"]}})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global FTPS connection instance
ftp_connection = FTPConnection()

def initialize_ftp():
    """Initialize FTPS connection at startup and retry on failure"""
    max_retries = 3
    for attempt in range(max_retries):
        result = ftp_connection.connect()
        if result["status"] == "success":
            logger.info(f"FTPS Status at startup: {result['message']}")
            return result
        logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {result['message']}")
        time.sleep(5)  # Wait before retrying
    logger.error("Failed to initialize FTPS connection after all retries")
    return {"status": "error", "message": "Failed to connect to FTPS server"}

# Initialize FTPS when the app starts
initialize_ftp()

@app.route('/')
def index():
    logger.info("Serving SPA index page")
    return render_template('index.html')

@app.route('/api/ftp/status', methods=['GET'])
def ftp_status():
    logger.info("API request for FTPS status")
    result = ftp_connection.get_status()
    if result["status"] == "error":
        ftp_connection.connect()  # Attempt to reconnect
    return jsonify(result)

@app.route('/api/ftp/list', methods=['GET'])
def ftp_list():
    logger.info("API request to list FTPS directory with path: %s", request.args.get('path', '/Reports/ELON_data/Nomeco_environments/PROD_internally'))
    path = request.args.get('path', '/Reports/ELON_data/Nomeco_environments/PROD_internally')
    result = ftp_connection.list_dir(path)
    if result["status"] == "error" and "Not connected" in result["message"]:
        ftp_connection.connect()  # Attempt to reconnect
        result = ftp_connection.list_dir(path)
    return jsonify(result)

@app.route('/api/ftp/navigate', methods=['GET'])
def ftp_navigate():
    logger.info("API request to navigate FTPS directory with path: %s", request.args.get('path', ''))
    path = request.args.get('path', '')
    result = ftp_connection.list_dir(path)
    if result["status"] == "error" and "Not connected" in result["message"]:
        ftp_connection.connect()  # Attempt to reconnect
        result = ftp_connection.list_dir(path)
    return jsonify(result)

@app.route('/api/ftp/download/<path:file_path>', methods=['GET'])
def ftp_download(file_path):
    logger.info(f"API request to download file: {file_path}")
    try:
        # Decode the URL-encoded path
        decoded_path = file_path.replace('%2F', '/')
        result = ftp_connection.get_file(decoded_path)
        if result["status"] == "error":
            if "Not connected" in result["message"]:
                ftp_connection.connect()  # Attempt to reconnect
                result = ftp_connection.get_file(decoded_path)
            if result["status"] == "error":
                logger.error(f"Failed to download file {file_path}: {result['message']}")
                return jsonify(result), 404
        
        # Determine file type and return as downloadable file over HTTPS
        filename = decoded_path.split('/')[-1]
        if file_path.endswith(('.pdf', '.csv', '.txt')):
            logger.info(f"Successfully downloaded file: {filename}")
            return Response(
                result["data"],
                mimetype={
                    '.pdf': 'application/pdf',
                    '.csv': 'text/csv',
                    '.txt': 'text/plain'
                }[file_path[-4:]],
                headers={'Content-Disposition': f'attachment; filename="{filename}"'}
            )
        else:
            logger.error(f"Unsupported file type for {filename}")
            return jsonify({"status": "error", "message": "Unsupported file type"}), 400
    except Exception as e:
        logger.error(f"Error downloading file {file_path}: {e}")
        return jsonify({"status": "error", "message": f"Failed to download file: {e}"}), 500

@app.route('/api/ftp/index', methods=['GET'])
def get_ftp_index():
    logger.info("Serving FTP index database as JSON")
    try:
        conn = sqlite3.connect('ftp_index.db')
        c = conn.cursor()
        c.execute("SELECT file_name, file_path FROM files")
        rows = c.fetchall()
        data = [{"file_name": row[0], "file_path": row[1]} for row in rows]
        conn.close()
        logger.info("Successfully served FTP index as JSON with %d records", len(data))
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error serving FTP index database as JSON: {e}")
        return jsonify({"status": "error", "message": f"Failed to serve FTP index: {e}"}), 500

@app.route('/api/indexing_status', methods=['GET'])
def get_indexing_status():
    """Return the current indexing status."""
    logger.info("API request for indexing status")
    try:
        with open('indexing_status.txt', 'r') as f:
            status = f.read().strip()
        logger.info(f"Indexing status returned: {status}")
        return jsonify({"status": status})
    except Exception as e:
        logger.error(f"Error reading indexing status: {e}")
        return jsonify({"status": "ongoing"}), 500

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == '__main__':
    # This will only be used in development
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5500))
    app.run(debug=True, host=host, port=port, ssl_context=None)  # Remove SSL context for local testing