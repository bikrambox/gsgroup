from waitress import serve
from app import app  # Import the Flask app
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    # Log environment variables for debugging
    logger.info(f"FTP_HOST: {os.getenv('FTP_HOST')}")
    logger.info(f"FTP_PORT: {os.getenv('FTP_PORT')}")
    logger.info(f"FTP_USERNAME: {os.getenv('FTP_USERNAME')}")
    logger.info(f"FTP_PASSWORD: {os.getenv('FTP_PASSWORD')}")
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))  # Match your running port
    
    logger.info(f"Starting BHS Waybill in production mode on {host}:{port}...")
    serve(app, host=host, port=port)