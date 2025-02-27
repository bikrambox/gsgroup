import ftplib
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FTPConnection:
    def __init__(self):
        # Load env variables in the class
        load_dotenv()
        self.ftp = None
        self.host = os.getenv('FTP_HOST')
        self.port = int(os.getenv('FTP_PORT'))
        self.username = os.getenv('FTP_USERNAME')  # Single backslash in .env
        self.password = os.getenv('FTP_PASSWORD')
        self.connected = False
        logger.info(f"Initializing FTPS connection from bastion host to {self.host}:{self.port}")
        logger.info(f"Using credentials - Username: '{self.username}', Password: '{self.password}'")

    def connect(self):
        if self.connected:
            return {"status": "success", "message": "Already connected"}
        try:
            self.ftp = ftplib.FTP_TLS()
            logger.info(f"Attempting FTPS connection to {self.host}:{self.port}")
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.username, self.password)
            self.ftp.prot_p()  # Enable protected data connection
            self.connected = True
            logger.info(f"Successfully connected to FTPS server at {self.host}:{self.port}")
            return {
                "status": "success",
                "message": f"Connected to FTPS server at {self.host}:{self.port}"
            }
        except ftplib.error_perm as e:
            self.connected = False
            logger.error(f"FTPS authentication or permission failed: {e}")
            return {
                "status": "error",
                "message": f"FTPS authentication or permission failed: {e}"
            }
        except Exception as e:
            self.connected = False
            logger.error(f"FTPS connection failed: {e}")
            return {
                "status": "error",
                "message": f"FTPS connection failed: {e}"
            }

    def list_dir(self):
        if not self.connected or not self.ftp:
            logger.warning("Attempted to list directory without active connection")
            return {
                "status": "error",
                "message": "Not connected to FTPS server"
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
            logger.error(f"Error listing directory: {e}")
            return {
                "status": "error",
                "message": f"Error listing directory: {e}"
            }

    def get_status(self):
        if self.connected:
            return {"status": "success", "message": f"Connected to {self.host}:{self.port}"}
        return {"status": "error", "message": "Not connected to FTPS server"}

    def disconnect(self):
        if self.connected and self.ftp:
            try:
                self.ftp.quit()
                self.connected = False
                logger.info("FTPS connection closed")
                return True
            except Exception as e:
                logger.error(f"Error closing FTPS connection: {e}")
                return False
        return True