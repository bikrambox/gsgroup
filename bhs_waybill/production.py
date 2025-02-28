# from waitress import serve
# from app import app  # Import the Flask app
# import os
# from dotenv import load_dotenv
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()

# if __name__ == '__main__':
#     # Log environment variables for debugging
#     logger.info(f"FTP_HOST: {os.getenv('FTP_HOST')}")
#     logger.info(f"FTP_PORT: {os.getenv('FTP_PORT')}")
#     logger.info(f"FTP_USERNAME: {os.getenv('FTP_USERNAME')}")
#     logger.info(f"FTP_PASSWORD: {os.getenv('FTP_PASSWORD')}")
    
#     host = os.getenv('HOST', '0.0.0.0')
#     port = int(os.getenv('PORT', 8000))  # Match your running port
    
#     logger.info(f"Starting BHS Waybill in production mode on {host}:{port}...")
#     serve(app, host=host, port=port)
from waitress import serve
from app import app  # Import the Flask app
import os
from dotenv import load_dotenv
import logging
import sqlite3
import ssl
from waybill_ftp import FTPConnection
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def index_ftp_files(ftp_connection, base_path='/Reports/ELON_data/Nomeco_environments/PROD_internally'):
    """Index all files in the FTP server and store in SQLite database."""
    # Create or update indexing status file
    with open('indexing_status.txt', 'w') as f:
        f.write('ongoing')
    
    conn = sqlite3.connect('ftp_index.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files (file_name TEXT, file_path TEXT UNIQUE)''')
    
    try:
        result = ftp_connection.list_dir(base_path)
        if result["status"] == "error":
            logger.error(f"Failed to index FTP files: {result['message']}")
            return
        
        def index_recursive(current_path):
            ftp_connection.ensure_connected()  # Ensure connection is alive
            result = ftp_connection.list_dir(current_path)
            if result["status"] == "error":
                logger.error(f"Error indexing {current_path}: {result['message']}")
                return
            
            for item in result["data"]:
                full_path = item["path"]
                if item["is_dir"]:
                    index_recursive(full_path)
                else:
                    file_name = item["name"]
                    c.execute("INSERT OR REPLACE INTO files (file_name, file_path) VALUES (?, ?)", 
                              (file_name, full_path))
                    logger.info(f"Indexed: {file_name} at {full_path}")
        
        index_recursive(base_path)
        conn.commit()
        logger.info("FTP file indexing completed and saved to ftp_index.db")
        
        # Update indexing status to done
        with open('indexing_status.txt', 'w') as f:
            f.write('done')
    except Exception as e:
        logger.error(f"Error during FTP indexing: {e}")
    finally:
        conn.close()

def start_indexing_in_background(ftp_connection):
    """Start indexing in a background thread."""
    indexing_thread = threading.Thread(target=index_ftp_files, args=(ftp_connection,), daemon=True)
    indexing_thread.start()
    logger.info("Started FTP file indexing in the background")

@app.route('/api/indexing_status', methods=['GET'])
def get_indexing_status():
    """Return the current indexing status."""
    try:
        with open('indexing_status.txt', 'r') as f:
            status = f.read().strip()
        return jsonify({"status": status})
    except Exception as e:
        logger.error(f"Error reading indexing status: {e}")
        return jsonify({"status": "ongoing"}), 500

if __name__ == '__main__':
    # Log environment variables for debugging
    logger.info(f"FTP_HOST: {os.getenv('FTP_HOST')}")
    logger.info(f"FTP_PORT: {os.getenv('PORT', 21)}")
    logger.info(f"FTP_USERNAME: {os.getenv('FTP_USERNAME')}")
    logger.info(f"FTP_PASSWORD: {os.getenv('FTP_PASSWORD')}")
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5500))  # Match the public port (adjust if different)
    
    logger.info(f"Starting BHS Waybill in production mode on {host}:{port}...")
    
    # Initialize FTP connection
    ftp_connection = FTPConnection()
    
    # Start indexing in the background
    start_indexing_in_background(ftp_connection)
    
    serve(app, host=host, port=port)