from waitress import serve
from app import app  # Import the Flask app
import os
from dotenv import load_dotenv
import logging
import sqlite3
from waybill_ftp import FTPConnection
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def index_ftp_files(ftp_connection, base_path='/Reports/ELON_data/Nomeco_environments/PROD_internally'):
    """Index all files in the FTP server and store in SQLite database, minimizing verification for speed."""
    logger.info("Starting FTP file indexing process for base path: %s", base_path)
    
    # Create or update database indexing status file
    with open('database_indexing_status.txt', 'w') as f:
        f.write('ongoing')
    logger.info("Database indexing status set to 'ongoing' in database_indexing_status.txt")
    
    conn = sqlite3.connect('ftp_index.db')
    c = conn.cursor()
    logger.info("Connected to SQLite database 'ftp_index.db'")
    
    c.execute('''CREATE TABLE IF NOT EXISTS files (file_name TEXT, file_path TEXT UNIQUE)''')
    logger.info("Created or verified 'files' table in SQLite database")
    
    try:
        result = ftp_connection.list_dir(base_path)
        if result["status"] == "error":
            logger.error("Failed to list initial directory: %s", result['message'])
            return
        
        logger.info("Successfully listed initial directory: %s", base_path)
        
        def index_recursive(current_path):
            logger.info("Indexing recursive path: %s", current_path)
            ftp_connection.ensure_connected()  # Ensure connection is alive
            result = ftp_connection.list_dir(current_path)
            if result["status"] == "error":
                logger.error("Error indexing path %s: %s", current_path, result['message'])
                return
            
            logger.info("Successfully listed directory: %s", current_path)
            
            for item in result["data"]:
                full_path = item["path"]
                if item["is_dir"]:
                    logger.info("Found directory: %s", full_path)
                    index_recursive(full_path)
                else:
                    file_name = item["name"]
                    logger.info(f"Found file: {file_name} at {full_path} (skipping FTP verification for speed)")
                    c.execute("INSERT OR REPLACE INTO files (file_name, file_path) VALUES (?, ?)", 
                              (file_name, full_path))
                    logger.info("Indexed: %s at %s", file_name, full_path)
        
        index_recursive(base_path)
        conn.commit()
        logger.info("Committed changes to SQLite database")
        logger.info("FTP file indexing completed and saved to ftp_index.db")
        
        # Update database indexing status to done
        with open('database_indexing_status.txt', 'w') as f:
            f.write('done')
        logger.info("Database indexing status set to 'done' in database_indexing_status.txt")
    except Exception as e:
        logger.error("Error during FTP indexing: %s", str(e))
    finally:
        conn.close()
        logger.info("Closed SQLite database connection")

def start_indexing_in_background(ftp_connection):
    """Start indexing in a background thread."""
    logger.info("Starting FTP file indexing in the background")
    indexing_thread = threading.Thread(target=index_ftp_files, args=(ftp_connection,), daemon=True)
    indexing_thread.start()
    logger.info("Indexing thread started with ID: %d", indexing_thread.ident)

if __name__ == '__main__':
    # Log environment variables for debugging
    logger.info(f"FTP_HOST: {os.getenv('FTP_HOST')}")
    logger.info(f"FTP_PORT: {os.getenv('PORT', 21)}")
    logger.info(f"FTP_USERNAME: {os.getenv('FTP_USERNAME')}")
    logger.info(f"FTP_PASSWORD: {os.getenv('FTP_PASSWORD')}")
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))  # Matches your environment
    
    logger.info(f"Starting BHS Waybill in production mode on {host}:{port}...")
    
    # Initialize FTP connection
    ftp_connection = FTPConnection()
    logger.info("Initialized FTP connection")
    
    # Start indexing in the background
    start_indexing_in_background(ftp_connection)
    
    # Serve without SSL context (SSL should be handled by a reverse proxy like Nginx)
    logger.info(f"Starting Flask server with Waitress on port {port} (SSL handled externally)")
    serve(app, host=host, port=port)  # Removed ssl_context