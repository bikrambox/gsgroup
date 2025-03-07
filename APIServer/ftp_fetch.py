# APIServer/ftp_fetch.py
import ftplib
import os
import threading
import time
from dotenv import load_dotenv
import logging
import io
import ssl
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FTPConnection:
    def __init__(self, authenticated_username=None):
        load_dotenv()
        self.ftp = None
        self.host = os.getenv('FTP_HOST', '10.6.8.43')
        self.port = int(os.getenv('FTP_PORT', 21))
        self.username = os.getenv('FTP_USERNAME', r'BHSR\jeba').replace('\\\\', '\\')
        self.password = os.getenv('FTP_PASSWORD', 'Hundekoldt2006!')
        self.authenticated_username = authenticated_username  # Store the authenticated username from API key
        self.connected = False
        self.keep_alive_interval = 300  # Keep-alive check every 5 minutes (300 seconds)
        self.keep_alive_thread = None
        logger.info(f"Initializing FTPS connection from bastion host to {self.host}:{self.port}")
        logger.info(f"Using credentials - Username: '{self.username}', Password: '***'")
        logger.info(f"Raw username (repr): {repr(self.username)}")
        logger.info(f"Authenticated username: {self.authenticated_username}")

    def connect(self):
        if self.connected:
            return {"status": "success", "message": "Already connected"}
        try:
            # Try multiple TLS protocols to handle server compatibility
            for protocol in [ssl.PROTOCOL_TLSv1_2, ssl.PROTOCOL_TLSv1_1, ssl.PROTOCOL_TLS]:
                context = ssl.SSLContext(protocol)
                context.check_hostname = False  # Disable for testing
                context.verify_mode = ssl.CERT_NONE  # Disable cert verification for testing
                try:
                    self.ftp = ftplib.FTP_TLS(context=context, timeout=1200)  # Increased timeout to 20 minutes
                    logger.info(f"Attempting FTPS connection to {self.host}:{self.port} with protocol {protocol}")
                    self.ftp.connect(self.host, self.port)
                    self.ftp.login(self.username, self.password)
                    self.ftp.prot_p()  # Enable protected data connection
                    self.ftp.set_pasv(True)  # Enable passive mode for uploads
                    self.connected = True
                    logger.info(f"Successfully connected to FTPS server at {self.host}:{self.port} with protocol {protocol}")
                    break
                except Exception as e:
                    logger.warning(f"Connection failed with protocol {protocol}: {e}")
                    continue
            else:
                raise Exception("No compatible TLS protocol found")
            
            self.start_keep_alive()
            return {
                "status": "success",
                "message": f"Connected to FTPS server at {self.host}:{self.port}"
            }
        except ftplib.error_perm as e:
            self.connected = False
            logger.error(f"FTPS authentication or permission failed: {e}")
            return {"status": "error", "message": f"FTPS authentication or permission failed: {e}"}
        except ssl.SSLError as e:
            self.connected = False
            logger.error(f"TLS/SSL error: {e}")
            return {"status": "error", "message": f"TLS/SSL error: {e}"}
        except Exception as e:
            self.connected = False
            logger.error(f"FTPS connection failed: {e}")
            return {"status": "error", "message": f"FTPS connection failed: {e}"}

    def start_keep_alive(self):
        if self.keep_alive_thread and self.keep_alive_thread.is_alive():
            return

        def keep_alive_loop():
            while self.connected:
                try:
                    if self.ftp:
                        logger.info("Sending keep-alive NOOP command...")
                        self.ftp.sendcmd('NOOP')
                    time.sleep(self.keep_alive_interval)
                except Exception as e:
                    logger.error(f"Keep-alive failed: {e}")
                    self.connected = False
                    break

        self.keep_alive_thread = threading.Thread(target=keep_alive_loop, daemon=True)
        self.keep_alive_thread.start()
        logger.info(f"Started keep-alive thread with interval {self.keep_alive_interval} seconds")

    def ensure_connected(self):
        if not self.connected or not self.ftp:
            logger.warning("Connection lost, attempting to reconnect...")
            max_retries = 3
            for attempt in range(max_retries):
                result = self.connect()
                if result["status"] == "success":
                    return True
                logger.error(f"Reconnect attempt {attempt + 1}/{max_retries} failed: {result['message']}")
                time.sleep(5)
            logger.error("Failed to reconnect to FTPS server after all retries")
            return False
        return True

    def list_dir(self, path='/Reports/ELON_data/Nomeco_environments/PROD_internally'):
        if not self.ensure_connected():
            logger.warning("Attempted to list directory without active connection")
            return {"status": "error", "message": "Not connected to FTPS server"}
        try:
            current_dir = self.ftp.pwd()
            logger.info(f"Current FTP working directory: {current_dir}")
            normalized_path = path.replace('\\', '/')
            logger.info(f"Navigating to directory: {normalized_path}")
            self.ftp.cwd(normalized_path)
            files = []
            self.ftp.retrlines('LIST', files.append)
            items = []
            for line in files:
                parts = line.split()
                if len(parts) >= 9:
                    name = parts[-1]
                    is_dir = parts[0].startswith('d')
                    items.append({
                        "name": name,
                        "is_dir": is_dir,
                        "path": f"{normalized_path}/{name}" if normalized_path.endswith('/') else f"{normalized_path}/{name}"
                    })
            logger.info(f"Successfully retrieved directory listing from {normalized_path}")
            return {"status": "success", "data": items, "message": f"Directory listing retrieved successfully from {normalized_path}"}
        except ftplib.error_perm as e:
            logger.error(f"Permission error accessing directory: {e}")
            return {"status": "error", "message": f"Permission error accessing directory: {e}"}
        except ssl.SSLError as e:
            logger.error(f"TLS/SSL error listing directory: {e}")
            return {"status": "error", "message": f"TLS/SSL error listing directory: {e}"}
        except Exception as e:
            logger.error(f"Error listing directory: {e}")
            return {"status": "error", "message": f"Error listing directory: {e}"}

    def direct_ftp_download(self, file_path):
        if not self.ensure_connected():
            logger.warning("Attempted to download file without active connection")
            return {"status": "error", "message": "Not connected to FTPS server"}
        try:
            base_path = '/Reports/ELON_data/Nomeco_environments/PROD_internally'
            normalized_path = file_path if file_path.startswith(base_path) else f"{base_path}/{file_path}" if not file_path.startswith('/') else f"{base_path}{file_path}"
            while normalized_path.count(base_path) > 1:
                normalized_path = normalized_path.replace(base_path + base_path, base_path)
            normalized_path = normalized_path.replace('\\', '/')
            logger.info(f"Normalized FTP path for download: {normalized_path}")

            directory = '/'.join(normalized_path.split('/')[:-1]) or '/'
            filename = normalized_path.split('/')[-1]
            logger.info(f"Attempting to retrieve file: {filename} from {directory} via FTP")

            try:
                self.ftp.cwd(directory)
                logger.info(f"Verified directory exists: {directory}")
            except ftplib.error_perm as e:
                logger.error(f"Directory verification failed for {directory}: {e}")
                return {"status": "error", "message": f"Directory verification failed: {e}"}

            self.ftp.voidcmd("TYPE I")
            file_buffer = io.BytesIO()
            self.ftp.retrbinary(f"RETR {filename}", file_buffer.write)
            file_content = file_buffer.getvalue()
            logger.info(f"Successfully retrieved file: {filename} via FTP in binary mode")
            return {
                "status": "success",
                "data": file_content,
                "message": f"File {filename} retrieved successfully via FTP in binary mode"
            }
        except ftplib.error_perm as e:
            logger.error(f"Permission error accessing file via FTP: {e}")
            return {"status": "error", "message": f"Permission error accessing file via FTP: {e}"}
        except ssl.SSLError as e:
            logger.error(f"TLS/SSL error retrieving file via FTP: {e}")
            return {"status": "error", "message": f"TLS/SSL error retrieving file via FTP: {e}"}
        except Exception as e:
            logger.error(f"Error retrieving file via FTP: {e}")
            return {"status": "error", "message": f"Error retrieving file via FTP: {e}"}

    def upload_stream(self, file_buffer, original_filename):
        """Upload a file stream to the FTPS server with the specified naming convention."""
        if not self.ensure_connected():
            logger.warning("Attempted to upload file without active connection")
            return {"status": "error", "message": "Not connected to FTPS server"}

        try:
            # Validate file is .json
            if not original_filename.lower().endswith('.json'):
                return {"status": "error", "message": "Only JSON files are allowed"}

            # Validate JSON content
            file_buffer.seek(0)
            json_data = file_buffer.read().decode('utf-8')
            json.loads(json_data)  # Validate JSON
            file_buffer.seek(0)  # Reset buffer position

            # Define base path and folder structure
            base_path = '/Reports/ELON_data/Upload_test'
            today = time.strftime('%Y-%m-%d')
            # Use the authenticated username (e.g., 'firedrake') instead of FTPS username
            username = self.authenticated_username if self.authenticated_username else self.username.split('\\')[-1]
            folder_name = f"{username}_{today}"  # e.g., firedrake_2025-03-07
            upload_dir = f"{base_path}/{folder_name}"

            # Check if directory exists, create if it doesn't
            try:
                self.ftp.cwd(upload_dir)
                logger.info(f"Directory {upload_dir} already exists")
            except ftplib.error_perm:
                logger.info(f"Creating directory {upload_dir}")
                self.ftp.mkd(upload_dir)  # Create directory if it doesn't exist

            # Get existing files in the directory to determine the next index
            self.ftp.cwd(upload_dir)
            files = []
            self.ftp.retrlines('NLST', files.append)
            file_count = len([f for f in files if f.startswith(f"{folder_name}_")])

            # Determine new filename with index
            base_name = original_filename.rsplit('.', 1)[0]  # Get filename without extension
            extension = '.json'
            new_filename = f"{folder_name}_{base_name}"
            if file_count > 0:
                new_filename += f"_{file_count:02d}"  # Add index (e.g., _01, _02)
            new_filename += extension

            # Upload the file
            file_buffer.seek(0)
            self.ftp.storbinary(f"STOR {new_filename}", file_buffer)
            logger.info(f"Successfully uploaded {original_filename} as {new_filename} to {upload_dir}")

            return {
                "status": "success",
                "message": f"File uploaded successfully to {upload_dir}/{new_filename}",
                "file_path": f"{upload_dir}/{new_filename}"
            }

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON file: {e}")
            return {"status": "error", "message": f"Invalid JSON file: {e}"}
        except ftplib.error_perm as e:
            logger.error(f"Permission error during upload: {e}")
            return {"status": "error", "message": f"Permission error during upload: {e}"}
        except ssl.SSLError as e:
            logger.error(f"TLS/SSL error during upload: {e}")
            return {"status": "error", "message": f"TLS/SSL error during upload: {e}"}
        except Exception as e:
            logger.error(f"Error uploading file via FTPS: {e}")
            return {"status": "error", "message": f"Error uploading file via FTPS: {e}"}

    def get_status(self):
        if self.connected:
            return {"status": "success", "message": f"Connected to {self.host}:{self.port}"}
        return {"status": "error", "message": "Not connected to FTPS server"}

    def disconnect(self):
        if self.connected and self.ftp:
            try:
                self.connected = False
                if self.keep_alive_thread:
                    self.keep_alive_thread.join(timeout=1)
                self.ftp.quit()
                logger.info("FTPS connection closed")
                return True
            except Exception as e:
                logger.error(f"Error closing FTPS connection: {e}")
                return False
        return True

if __name__ == "__main__":
    ftp = FTPConnection(authenticated_username="testuser")
    ftp.connect()
    with open("test.json", 'rb') as f:
        result = ftp.upload_stream(io.BytesIO(f.read()), "test.json")
    print(result)
    ftp.disconnect()