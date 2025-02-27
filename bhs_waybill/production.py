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

# Configure logging to show in terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def check_ftp_status():
    """Check FTP connection status at startup"""
    ftp = FTPConnection()
    result = ftp.connect()
    logger.info(f"FTP Status: {result['message']}")
    ftp.disconnect()  # Clean up after checking

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5500))
    
    logger.info(f"Starting BHS Waybill in production mode on {host}:{port}...")
    check_ftp_status()  # Check FTP status before serving
    serve(app, host=host, port=port)
