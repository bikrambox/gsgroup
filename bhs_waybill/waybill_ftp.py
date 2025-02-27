import ftplib
import os
from dotenv import load_dotenv

class FTPConnection:
    def __init__(self):
        load_dotenv()
        self.ftp = None
        self.host = os.getenv('FTP_HOST')
        self.username = os.getenv('FTP_USERNAME')
        self.password = os.getenv('FTP_PASSWORD')
        self.connected = False

    def connect(self):
        try:
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.username, self.password)
            self.connected = True
            return {
                "status": "success",
                "message": f"Successfully connected to FTP server at {self.host}"
            }
        except Exception as e:
            self.connected = False
            return {
                "status": "error",
                "message": f"FTP connection failed: {str(e)}"
            }

    def list_dir(self):
        if not self.connected or not self.ftp:
            return {
                "status": "error",
                "message": "Not connected to FTP server"
            }
        try:
            files = self.ftp.nlst()
            return {
                "status": "success",
                "data": files,
                "message": "Directory listing retrieved successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error listing directory: {str(e)}"
            }

    def disconnect(self):
        if self.ftp:
            try:
                self.ftp.quit()
                self.connected = False
                return True
            except:
                return False
        return True