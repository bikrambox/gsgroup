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
        self.host = os.getenv('FTP_HOST', '10.6.8.43')
        self.port = int(os.getenv('FTP_PORT', 21))
        self.username = os.getenv('FTP_USERNAME', 'BHSR\jeba').replace('\\\\', '\\')
        self.password = os.getenv('FTP_PASSWORD', 'Hundekoldt2006!')
        self.connected = False
        logger.info(f"Initializing FTPS connection from bastion host to {self.host}:{self.port}")
        logger.info(f"Using credentials - Username: '{self.username}', Password: '{self.password}'")
        logger.info(f"Raw username (repr): {repr(self.username)}")

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
            # Define the target directory (Windows path with backslashes)
            target_dir = r"\Reports\ELON_data\Nomeco_environments\PROD_internally"
            logger.info(f"Navigating to directory: {target_dir}")
            
            # Change to the specified directory
            self.ftp.cwd(target_dir)
            
            # List the contents of the directory
            files = self.ftp.nlst()
            logger.info(f"Successfully retrieved directory listing from {target_dir}")
            return {
                "status": "success",
                "data": files,
                "message": f"Directory listing retrieved successfully from {target_dir}"
            }
        except ftplib.error_perm as e:
            logger.error(f"Permission error accessing directory: {e}")
            return {
                "status": "error",
                "message": f"Permission error accessing directory: {e}"
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