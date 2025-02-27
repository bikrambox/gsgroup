import paramiko
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SFTPConnection:
    def __init__(self):
        load_dotenv()
        self.sftp = None
        self.transport = None
        self.host = os.getenv('SFTP_HOST', '10.6.8.72')  # Default to your host
        self.port = int(os.getenv('SFTP_PORT', 22))      # Default SSH/SFTP port
        self.username = os.getenv('SFTP_USERNAME')
        self.password = os.getenv('SFTP_PASSWORD')
        self.connected = False
        logger.info(f"Initializing SFTP connection from bastion host to {self.host}:{self.port}")

    def connect(self):
        if self.connected:
            return {"status": "success", "message": "Already connected"}
        try:
            # Set up SSH transport
            self.transport = paramiko.Transport((self.host, self.port))
            self.transport.connect(username=self.username, password=self.password)
            # Open SFTP session
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.connected = True
            logger.info(f"Successfully connected to SFTP server at {self.host}:{self.port}")
            return {
                "status": "success",
                "message": f"Connected to SFTP server at {self.host}:{self.port}"
            }
        except paramiko.AuthenticationException as e:
            self.connected = False
            logger.error(f"SFTP authentication failed: {str(e)}")
            return {
                "status": "error",
                "message": f"SFTP authentication failed: {str(e)}"
            }
        except Exception as e:
            self.connected = False
            logger.error(f"SFTP connection failed: {str(e)}")
            return {
                "status": "error",
                "message": f"SFTP connection failed: {str(e)}"
            }

    def list_dir(self, path='.'):
        if not self.connected or not self.sftp:
            logger.warning("Attempted to list directory without active connection")
            return {
                "status": "error",
                "message": "Not connected to SFTP server"
            }
        try:
            files = self.sftp.listdir(path)
            logger.info(f"Successfully retrieved directory listing from {path}")
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
        if self.connected:
            return {"status": "success", "message": f"Connected to {self.host}:{self.port}"}
        return {"status": "error", "message": "Not connected to SFTP server"}

    def disconnect(self):
        if self.connected:
            try:
                if self.sftp:
                    self.sftp.close()
                if self.transport:
                    self.transport.close()
                self.connected = False
                logger.info("SFTP connection closed")
                return True
            except Exception as e:
                logger.error(f"Error closing SFTP connection: {str(e)}")
                return False
        return True