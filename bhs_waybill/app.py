from flask import Flask, render_template, jsonify, request, Response, send_file
from flask_cors import CORS
from waybill_ftp import FTPConnection  # Updated import
import logging
import os
from dotenv import load_dotenv
import io
import sqlite3
import time
import threading

# Load environment variables before anything else
load_dotenv()

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Enable CORS for all routes, ensuring HTTPS and cross-browser compatibility
CORS(app, resources={r"/api/*": {
    "origins": ["https://vps1139.basicserver.io:42030", "https://vps1139.basicserver.io", "http://localhost:8000", "*"],
    "allow_headers": ["Content-Type", "Authorization"],
    "methods": ["GET", "POST", "OPTIONS", "HEAD"],
    "supports_credentials": True
}})

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)



# Configure logging to output to terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to terminal
        logging.FileHandler('app.log')  # Optional: Output to file
    ]
)
logger = logging.getLogger(__name__)



# Force HTTPS globally
app.config['PREFER_HTTPS'] = True

# Global FTPS connection instance
ftp_connection = FTPConnection()

def initialize_ftp():
    """Initialize FTPS connection at startup and retry on failure"""
    max_retries = 3
    for attempt in range(max_retries):
        result = ftp_connection.connect()
        if result["status"] == "success":
            logger.info(f"FTPS Status at startup (Windows FTP): {result['message']}")
            return result
        logger.error(f"Attempt {attempt + 1}/{max_retries} failed (Windows FTP): {result['message']}")
        time.sleep(5)  # Wait before retrying
    logger.error("Failed to initialize FTPS connection after all retries (Windows FTP)")
    return {"status": "error", "message": "Failed to connect to FTPS server"}

# Initialize FTPS when the app starts
initialize_ftp()

@app.before_request
def before_request():
    """Detect if the request is coming through a proxy (e.g., Nginx) and force HTTPS unconditionally."""
    forwarded_proto = request.headers.get('X-Forwarded-Proto')
    current_scheme = request.environ.get('wsgi.url_scheme', 'http')
    logger.info(f"Before request - X-Forwarded-Proto: {forwarded_proto}, Current Scheme: {current_scheme}")
    
    # Force HTTPS unconditionally, ignoring X-Forwarded-Proto if it’s None or missing
    request.environ['wsgi.url_scheme'] = 'https'
    logger.info("Forcing HTTPS scheme unconditionally for all requests (Windows FTP)")

@app.route('/')
def index():
    logger.info("Serving SPA index page over HTTPS (Windows FTP)")
    return render_template('index.html')

@app.route('/api/ftp/status', methods=['GET'])
def ftp_status():
    logger.info("API request for FTPS status over HTTPS (Windows FTP)")
    result = ftp_connection.get_status()
    if result["status"] == "error":
        ftp_connection.connect()  # Attempt to reconnect
    return jsonify(result)

@app.route('/api/ftp/list', methods=['GET'])
def ftp_list():
    logger.info("API request to list FTPS directory with path: %s over HTTPS (Windows FTP)", request.args.get('path', '/Reports/ELON_data/Nomeco_environments/PROD_internally'))
    path = request.args.get('path', '/Reports/ELON_data/Nomeco_environments/PROD_internally')
    result = ftp_connection.list_dir(path)
    if result["status"] == "error" and "Not connected" in result["message"]:
        ftp_connection.connect()  # Attempt to reconnect
        result = ftp_connection.list_dir(path)
    return jsonify(result)

@app.route('/api/ftp/navigate', methods=['GET'])
def ftp_navigate():
    logger.info("API request to navigate FTPS directory with path: %s over HTTPS (Windows FTP)", request.args.get('path', ''))
    path = request.args.get('path', '')
    result = ftp_connection.list_dir(path)
    if result["status"] == "error" and "Not connected" in result["message"]:
        ftp_connection.connect()  # Attempt to reconnect
        result = ftp_connection.list_dir(path)
    return jsonify(result)

@app.route('/api/ftp/download/<path:file_path>', methods=['GET'])
def ftp_download(file_path):
    logger.info(f"API request to download file: {file_path} over HTTPS (Windows FTP)")
    try:
        # Decode the URL-encoded path
        decoded_path = file_path.replace('%2F', '/')
        logger.info(f"Decoding file path (Windows FTP): {decoded_path}")
        logger.info("Testing logger III output in app.py")
        
        # Use the new FTP direct download function
        result = ftp_connection.direct_ftp_download(decoded_path)
        if result["status"] == "error":
            logger.error(f"Failed to download file {file_path} over HTTPS (Windows FTP): {result['message']}")
            return jsonify(result), 404
        
        # Determine file type and return as downloadable file over HTTPS with hardcoded URL
        filename = decoded_path.split('/')[-1]
        if file_path.endswith(('.pdf', '.csv', '.txt')):
            logger.info(f"Successfully downloaded file: {filename} over HTTPS (Windows FTP)")
            # Hardcode the HTTPS URL in the response, ensuring all headers use HTTPS with port
            hardcoded_url = f"https://vps1139.basicserver.io:42030/api/ftp/download/{file_path}"
            
            # Set the Content-Type based on file extension
            content_type = {
                '.pdf': 'application/pdf',
                '.csv': 'text/csv',
                '.txt': 'text/plain'
            }[file_path[-4:]]
            
            # Create a response with the file data
            response = Response(
                result["data"],
                mimetype=content_type,
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type',
                }
            )
            
            # Explicitly set the Location header to include the port
            response.headers['Location'] = hardcoded_url
            response.headers['Content-Location'] = hardcoded_url
            logger.info("Testing logger II output in app.py")
            
            return response
        else:
            logger.error(f"Unsupported file type for {filename} over HTTPS (Windows FTP)")
            return jsonify({"status": "error", "message": "Unsupported file type"}), 400
    except Exception as e:
        logger.error(f"Error downloading file {file_path} over HTTPS (Windows FTP): {e}")
        return jsonify({"status": "error", "message": f"Failed to download file over HTTPS (Windows FTP): {e}"}), 500

@app.route('/api/ftp/index', methods=['GET'])
def get_ftp_index():
    logger.info("Serving FTP index database as JSON over HTTPS (Windows FTP)")
    try:
        # Check if database indexing is done
        with open('database_indexing_status.txt', 'r') as f:
            db_status = f.read().strip()
        if db_status != 'done':
            logger.info("Database indexing not complete, returning ongoing status for JSON over HTTPS (Windows FTP)")
            return jsonify({"status": "ongoing", "message": "Database indexing in progress over HTTPS (Windows FTP)"})

        # Simulate JSON indexing (assuming it happens after database indexing)
        with open('json_indexing_status.txt', 'w') as f:
            f.write('ongoing')
        logger.info("JSON indexing status set to 'ongoing' over HTTPS (Windows FTP) in json_indexing_status.txt")

        conn = sqlite3.connect('ftp_index.db')
        c = conn.cursor()
        c.execute("SELECT file_name, file_path FROM files")
        rows = c.fetchall()
        data = [{"file_name": row[0], "file_path": row[1]} for row in rows]
        conn.close()
        
        # Update JSON indexing status to done after processing
        with open('json_indexing_status.txt', 'w') as f:
            f.write('done')
        logger.info("JSON indexing status set to 'done' over HTTPS (Windows FTP) in json_indexing_status.txt")
        logger.info("Successfully served FTP index as JSON over HTTPS (Windows FTP) with %d records", len(data))
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error serving FTP index database as JSON over HTTPS (Windows FTP): {e}")
        return jsonify({"status": "error", "message": f"Failed to serve FTP index over HTTPS (Windows FTP): {e}"}), 500

@app.route('/api/indexing_status', methods=['GET'])
def get_indexing_status():
    """Return the current indexing statuses for database and JSON over HTTPS."""
    logger.info("API request for indexing status over HTTPS (Windows FTP)")
    try:
        with open('database_indexing_status.txt', 'r') as f:
            db_status = f.read().strip()
        with open('json_indexing_status.txt', 'r') as f:
            json_status = f.read().strip()
        logger.info(f"Indexing statuses returned over HTTPS (Windows FTP): Database: {db_status}, JSON: {json_status}")
        return jsonify({"database_status": db_status, "json_status": json_status})
    except Exception as e:
        logger.error(f"Error reading indexing status over HTTPS (Windows FTP): {e}")
        return jsonify({"database_status": "ongoing", "json_status": "ongoing"}), 500

@app.route('/favicon.ico')
def favicon():
    logger.info("Serving favicon over HTTPS (Windows FTP)")
    return app.send_static_file('favicon.ico')

if __name__ == '__main__':
    # This will only be used in development
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    logger.info(f"Starting BHS Waybill in production mode on {os.getenv('HOST')}:{os.getenv('PORT')}")
    app.run(debug=True, host=host, port=port, ssl_context=None)  # Remove SSL context for local testing