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

    def list_dir(self, path='/Reports/ELON_data/Nomeco_environments/PROD_internally'):
        if not self.connected or not self.ftp:
            logger.warning("Attempted to list directory without active connection")
            return {
                "status": "error",
                "message": "Not connected to FTPS server"
            }
        try:
            # Log the current working directory before attempting to change
            current_dir = self.ftp.pwd()
            logger.info(f"Current FTP working directory: {current_dir}")
            
            # Change to the specified directory
            if path:
                logger.info(f"Navigating to directory: {path}")
                self.ftp.cwd(path)
            
            # Get directory listing with details to distinguish folders/files
            files = []
            self.ftp.retrlines('LIST', files.append)
            
            # Parse the listing to identify directories and files
            items = []
            for line in files:
                # Example parsing (format depends on FTP server, e.g., "drwxr-xr-x   2 user group 4096 Oct 10 2024 Nomeco_2024-10-10")
                parts = line.split()
                if len(parts) >= 9:
                    name = parts[-1]  # Last part is the name
                    is_dir = parts[0].startswith('d')  # 'd' indicates directory
                    items.append({
                        "name": name,
                        "is_dir": is_dir,
                        "path": f"{path}/{name}" if path.endswith('/') else f"{path}/{name}"
                    })
            
            logger.info(f"Successfully retrieved directory listing from {path}")
            return {
                "status": "success",
                "data": items,
                "message": f"Directory listing retrieved successfully from {path}"
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