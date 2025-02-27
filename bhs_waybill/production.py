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


from waitress import serve
from app import app
from waybill_ftp import FTPConnection  # Import FTPConnection
import os
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Global FTP connection instance
ftp_connection = FTPConnection()

def initialize_ftp():
    """Initialize FTP connection at startup"""
    result = ftp_connection.connect()
    logger.info(f"FTP Status at startup: {result['message']}")
    return result

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5500))
    
    logger.info(f"Starting BHS Waybill in production mode on {host}:{port}...")
    initialize_ftp()  # Connect to FTP once at startup
    serve(app, host=host, port=port)