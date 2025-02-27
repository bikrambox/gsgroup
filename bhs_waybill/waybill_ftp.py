import ftplib
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FTPConnection:
    def __init__(self):
        load_dotenv()
        self.ftp = None
        self.host = os.getenv('FTP_HOST')
        self.port = int(os.getenv('FTP_PORT', 21))
        self.username = os.getenv('FTP_USERNAME')
        self.password = os.getenv('FTP_PASSWORD')
        self.connected = False
        logger.info(f"Initializing FTP connection from bastion host to {self.host}:{self.port}")

    def connect(self):
        if self.connected:
            return {"status": "success", "message": "Already connected"}
        try:
            self.ftp = ftplib.FTP()
            logger.info(f"Attempting connection to {self.host}:{self.port}")
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.username, self.password)
            self.connected = True
            logger.info(f"Successfully connected to FTP server at {self.host}:{self.port}")
            return {
                "status": "success",
                "message": f"Connected to FTP server at {self.host}:{self.port}"
            }
        except ConnectionRefusedError as e:
            self.connected = False
            logger.error(f"Connection refused to {self.host}:{self.port} - {str(e)}")
            return {
                "status": "error",
                "message": f"FTP connection refused: {str(e)}"
            }
        except Exception as e:
            self.connected = False
            logger.error(f"FTP connection failed: {str(e)}")
            return {
                "status": "error",
                "message": f"FTP connection failed: {str(e)}"
            }

    def list_dir(self):
        if not self.connected or not self.ftp:
            logger.warning("Attempted to list directory without active connection")
            return {
                "status": "error",
                "message": "Not connected to FTP server"
            }
        try:
            files = self.ftp.nlst()
            logger.info("Successfully retrieved directory listing")
            return {
                "status": "success",
                "data": files,
                "message": "Directory listing retrieved successfully"
            }
        except Exception as e:
            logger.error(f"Error listing directory: {str(e)}")
            return {
                "status": "error",
                "message": f"Error listing directory: {str(e)}"
            }

    def get_status(self):
        """Return current connection status"""
        if self.connected:
            return {"status": "success", "message": f"Connected to {self.host}:{self.port}"}
        return {"status": "error", "message": "Not connected to FTP server"}

    def disconnect(self):
        if self.connected and self.ftp:
            try:
                self.ftp.quit()
                self.connected = False
                logger.info("FTP connection closed")
                return True
            except Exception as e:
                logger.error(f"Error closing FTP connection: {str(e)}")
                return False
        return True