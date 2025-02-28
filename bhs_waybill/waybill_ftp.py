import ftplib
import os
import threading
import time
from dotenv import load_dotenv
import logging
import io
import ssl

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FTPConnection:
    def __init__(self):
        load_dotenv()
        self.ftp = None
        self.host = os.getenv('FTP_HOST', '10.6.8.43')
        self.port = int(os.getenv('FTP_PORT', 21))
        self.username = os.getenv('FTP_USERNAME', r'BHSR\jeba').replace('\\\\', '\\')
        self.password = os.getenv('FTP_PASSWORD', 'Hundekoldt2006!')
        self.connected = False
        self.keep_alive_interval = 300  # Keep-alive check every 5 minutes (300 seconds)
        self.keep_alive_thread = None
        logger.info(f"Initializing FTPS connection from bastion host to {self.host}:{self.port}")
        logger.info(f"Using credentials - Username: '{self.username}', Password: '{self.password}'")
        logger.info(f"Raw username (repr): {repr(self.username)}")

    def connect(self):
        if self.connected:
            return {"status": "success", "message": "Already connected"}
        try:
            # Use a modern, non-deprecated TLS protocol
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)  # Use TLSv1.2 for compatibility (non-deprecated in Python 3.12+)
            context.load_default_certs()  # Load default certificates
            self.ftp = ftplib.FTP_TLS(context=context, timeout=600)  # Set timeout to 10 minutes
            logger.info(f"Attempting FTPS connection to {self.host}:{self.port} with TLSv1.2 and timeout 600s")
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.username, self.password)
            self.ftp.prot_p()  # Enable protected data connection
            self.connected = True
            logger.info(f"Successfully connected to FTPS server at {self.host}:{self.port}")
            
            # Start keep-alive thread
            self.start_keep_alive()
            
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
        except ssl.SSLError as e:
            self.connected = False
            logger.error(f"TLS/SSL error: {e}")
            return {
                "status": "error",
                "message": f"TLS/SSL error: {e}"
            }
        except Exception as e:
            self.connected = False
            logger.error(f"FTPS connection failed: {e}")
            return {
                "status": "error",
                "message": f"FTPS connection failed: {e}"
            }

    def start_keep_alive(self):
        """Start a background thread to send keep-alive commands periodically."""
        if self.keep_alive_thread and self.keep_alive_thread.is_alive():
            return

        def keep_alive_loop():
            while self.connected:
                try:
                    if self.ftp:
                        logger.info("Sending keep-alive NOOP command...")
                        self.ftp.sendcmd('NOOP')  # Send NOOP to keep connection alive
                    time.sleep(self.keep_alive_interval)
                except Exception as e:
                    logger.error(f"Keep-alive failed: {e}")
                    self.connected = False
                    break

        self.keep_alive_thread = threading.Thread(target=keep_alive_loop, daemon=True)
        self.keep_alive_thread.start()
        logger.info(f"Started keep-alive thread with interval {self.keep_alive_interval} seconds")

    def ensure_connected(self):
        """Ensure the connection is active; reconnect if necessary with retries."""
        if not self.connected or not self.ftp:
            logger.warning("Connection lost, attempting to reconnect...")
            max_retries = 3
            for attempt in range(max_retries):
                result = self.connect()
                if result["status"] == "success":
                    return True
                logger.error(f"Reconnect attempt {attempt + 1}/{max_retries} failed: {result['message']}")
                time.sleep(5)  # Wait before retrying
            logger.error("Failed to reconnect to FTPS server after all retries")
            return False
        return True

    def list_dir(self, path='/Reports/ELON_data/Nomeco_environments/PROD_internally'):
        if not self.ensure_connected():
            logger.warning("Attempted to list directory without active connection")
            return {
                "status": "error",
                "message": "Not connected to FTPS server"
            }
        try:
            # Log the current working directory before attempting to change
            current_dir = self.ftp.pwd()
            logger.info(f"Current FTP working directory: {current_dir}")
            
            # Normalize path for Windows FTP (use forward slashes for FTP commands)
            normalized_path = path.replace('\\', '/')
            logger.info(f"Navigating to directory: {normalized_path}")
            self.ftp.cwd(normalized_path)
            
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
                        "path": f"{normalized_path}/{name}" if normalized_path.endswith('/') else f"{normalized_path}/{name}"
                    })
            
            logger.info(f"Successfully retrieved directory listing from {normalized_path}")
            return {
                "status": "success",
                "data": items,
                "message": f"Directory listing retrieved successfully from {normalized_path}"
            }
        except ftplib.error_perm as e:
            logger.error(f"Permission error accessing directory: {e}")
            return {
                "status": "error",
                "message": f"Permission error accessing directory: {e}"
            }
        except ssl.SSLError as e:
            logger.error(f"TLS/SSL error listing directory: {e}")
            return {
                "status": "error",
                "message": f"TLS/SSL error listing directory: {e}"
            }
        except Exception as e:
            logger.error(f"Error listing directory: {e}")
            return {
                "status": "error",
                "message": f"Error listing directory: {e}"
            }

    def direct_ftp_download(self, file_path):
        """Directly download a file from the FTP server and return its contents, optimized for Windows FTP."""
        if not self.ensure_connected():
            logger.warning("Attempted to download file without active connection")
            return {
                "status": "error",
                "message": "Not connected to FTPS server"
            }
        try:
            # Normalize the file path for Windows FTP, ensuring no duplicate base paths
            base_path = '/Reports/ELON_data/Nomeco_environments/PROD_internally'
            if file_path.startswith(base_path):
                normalized_path = file_path  # Use the path as-is if it already starts with the base
            else:
                normalized_path = f"{base_path}/{file_path}" if not file_path.startswith('/') else f"{base_path}{file_path}"
            
            # Remove any duplicate base paths
            while normalized_path.count(base_path) > 1:
                normalized_path = normalized_path.replace(base_path + base_path, base_path)
            
            # Use forward slashes for FTP commands, as Windows FTP servers often accept them
            normalized_path = normalized_path.replace('\\', '/')
            logger.info(f"Normalized FTP path for download (Windows): {normalized_path}")

            # Navigate to the directory containing the file (remove filename from path)
            directory = '/'.join(normalized_path.split('/')[:-1]) or '/'
            filename = normalized_path.split('/')[-1]
            
            logger.info(f"Attempting to retrieve file: {filename} from {directory} via FTP (Windows)")
            
            # Verify the directory exists before attempting to download
            try:
                self.ftp.cwd(directory)
                logger.info(f"Verified directory exists: {directory}")
            except ftplib.error_perm as e:
                logger.error(f"Directory verification failed for {directory}: {e}")
                return {
                    "status": "error",
                    "message": f"Directory verification failed: {e}"
                }

            # Switch to binary mode for file transfer (avoid ASCII mode issues on Windows)
            self.ftp.voidcmd("TYPE I")  # Switch to binary mode (Image mode)
            
            # Use a BytesIO buffer to store the file content
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
            return {
                "status": "error",
                "message": f"Permission error accessing file via FTP: {e}"
            }
        except ssl.SSLError as e:
            logger.error(f"TLS/SSL error retrieving file via FTP: {e}")
            return {
                "status": "error",
                "message": f"TLS/SSL error retrieving file via FTP: {e}"
            }
        except Exception as e:
            logger.error(f"Error retrieving file via FTP: {e}")
            return {
                "status": "error",
                "message": f"Error retrieving file via FTP: {e}"
            }

    def get_status(self):
        if self.connected:
            return {"status": "success", "message": f"Connected to {self.host}:{self.port}"}
        return {"status": "error", "message": "Not connected to FTPS server"}

    def disconnect(self):
        if self.connected and self.ftp:
            try:
                self.connected = False  # Stop keep-alive thread
                if self.keep_alive_thread:
                    self.keep_alive_thread.join(timeout=1)  # Wait briefly for thread to stop
                self.ftp.quit()
                logger.info("FTPS connection closed")
                return True
            except Exception as e:
                logger.error(f"Error closing FTPS connection: {e}")
                return False
        return True