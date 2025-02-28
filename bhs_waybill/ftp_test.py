import ftplib
import os
import logging
import io
from dotenv import load_dotenv
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_ftp():
    """Connect to the FTPS server using credentials from .env, optimized for Windows FTP."""
    load_dotenv()
    
    ftp_host = os.getenv('FTP_HOST', '10.6.8.43')
    ftp_port = int(os.getenv('FTP_PORT', 21))
    ftp_username = os.getenv('FTP_USERNAME', r'BHSR\jeba').replace('\\\\', '\\')
    ftp_password = os.getenv('FTP_PASSWORD', 'Hundekoldt2006!')
    
    logger.info(f"Initializing FTPS connection to {ftp_host}:{ftp_port}")
    logger.info(f"Using credentials - Username: '{ftp_username}', Password: '{ftp_password}'")
    
    try:
        # Use a modern, non-deprecated TLS protocol
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)  # Use TLSv1.2 for compatibility (non-deprecated in Python 3.12+)
        context.load_default_certs()  # Load default certificates
        ftp = ftplib.FTP_TLS(context=context, timeout=600)  # Set timeout to 10 minutes
        
        logger.info(f"Attempting FTPS connection to {ftp_host}:{ftp_port} with TLSv1.2 and timeout 600s")
        ftp.connect(ftp_host, ftp_port)
        ftp.login(ftp_username, ftp_password)
        ftp.prot_p()  # Enable protected data connection
        
        logger.info(f"Successfully connected to FTPS server at {ftp_host}:{ftp_port}")
        return ftp
    except ftplib.error_perm as e:
        logger.error(f"FTPS authentication or permission failed: {e}")
        raise Exception(f"FTPS authentication or permission failed: {e}")
    except ssl.SSLError as e:
        logger.error(f"TLS/SSL error: {e}")
        raise Exception(f"TLS/SSL error: {e}")
    except Exception as e:
        logger.error(f"FTPS connection failed: {e}")
        raise Exception(f"FTPS connection failed: {e}")

def list_ftp_directory(ftp, path='.'):
    """List the contents of an FTP directory, handling Windows FTP paths."""
    try:
        # Use forward slashes for FTP commands, as many servers (including Windows) accept them
        normalized_path = path.replace('\\', '/')
        logger.info(f"Listing directory contents at: {normalized_path}")
        
        # Change to the specified directory
        ftp.cwd(normalized_path)
        
        # Get directory listing
        files = []
        ftp.retrlines('LIST', files.append)
        
        logger.info(f"Directory listing for {normalized_path}:")
        for line in files:
            logger.info(line)
        
        return True
    except ftplib.error_perm as e:
        logger.error(f"Permission error listing directory {path}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error listing directory {path}: {e}")
        return False

def download_file(ftp, file_path, local_path):
    """Download a specific file from FTP and save it locally, handling Windows FTP paths."""
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
            ftp.cwd(directory)
            logger.info(f"Verified directory exists: {directory}")
        except ftplib.error_perm as e:
            logger.error(f"Directory verification failed for {directory}: {e}")
            raise Exception(f"Directory verification failed: {e}")

        # Switch to binary mode for file transfer (avoid ASCII mode issues on Windows)
        ftp.voidcmd("TYPE I")  # Switch to binary mode (Image mode)
        
        # Download the file in binary mode
        with open(local_path, 'wb') as local_file:
            ftp.retrbinary(f"RETR {filename}", local_file.write)
        
        logger.info(f"Successfully downloaded file: {filename} to {local_path}")
    except ftplib.error_perm as e:
        logger.error(f"Permission error accessing file via FTP: {e}")
        raise Exception(f"Permission error accessing file via FTP: {e}")
    except ssl.SSLError as e:
        logger.error(f"TLS/SSL error retrieving file via FTP: {e}")
        raise Exception(f"TLS/SSL error retrieving file via FTP: {e}")
    except Exception as e:
        logger.error(f"Error retrieving file via FTP: {e}")
        raise Exception(f"Error retrieving file via FTP: {e}")
    finally:
        # Ensure the file is closed properly
        try:
            if 'local_file' in locals():
                local_file.close()
        except Exception as e:
            logger.error(f"Error closing local file: {e}")

def main():
    """Main function to test FTP connection, list directories, and download a file."""
    file_path = 'Reports/ELON_data/Nomeco_environments/PROD_internally/Nomeco_2024-10-16/20241016163203_BZ761831_Final.csv'
    local_filename = os.path.basename(file_path)  # Get the filename from the path
    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), local_filename)  # Save in the same directory as this script
    
    try:
        # Connect to FTP
        ftp = connect_to_ftp()
        
        # Print the current working directory
        current_dir = ftp.pwd()
        logger.info(f"Current working directory on FTP server: {current_dir}")
        
        # List directory contents at the root and relevant subdirectories to find the file
        root_paths = ['/', '\\']  # Test both forward and backslashes for Windows FTP
        for root_path in root_paths:
            if list_ftp_directory(ftp, root_path):
                # Try to navigate and list subdirectories to find the file
                potential_dirs = [
                    'Reports',
                    'Reports/ELON_data',
                    'Reports/ELON_data/Nomeco_environments',
                    'Reports/ELON_data/Nomeco_environments/PROD_internally',
                    'Reports/ELON_data/Nomeco_environments/PROD_internally/Nomeco_2024-10-16'
                ]
                for dir_path in potential_dirs:
                    full_dir = f"{root_path}{dir_path}".replace('//', '/').replace('\\\\', '\\')
                    if list_ftp_directory(ftp, full_dir):
                        logger.info(f"Found directory: {full_dir}")
        
        # Attempt to download the file from the normalized path
        download_file(ftp, file_path, local_path)
        ftp.quit()
        logger.info(f"FTPS connection closed after download")
    except Exception as e:
        logger.error(f"Failed to download file: {e}")
    finally:
        try:
            if 'ftp' in locals() and ftp:
                ftp.quit()
                logger.info("FTPS connection closed due to error")
        except Exception as e:
            logger.error(f"Error closing FTPS connection: {e}")

if __name__ == '__main__':
    main()