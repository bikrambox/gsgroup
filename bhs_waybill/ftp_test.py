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
    """Connect to the FTPS server using credentials from .env."""
    load_dotenv()
    
    ftp_host = os.getenv('FTP_HOST', '10.6.8.43')
    ftp_port = int(os.getenv('FTP_PORT', 21))
    ftp_username = os.getenv('FTP_USERNAME', r'BHSR\jeba').replace('\\\\', '\\')
    ftp_password = os.getenv('FTP_PASSWORD', 'Hundekoldt2006!')
    
    logger.info(f"Initializing FTPS connection to {ftp_host}:{ftp_port}")
    logger.info(f"Using credentials - Username: '{ftp_username}', Password: '{ftp_password}'")
    
    try:
        # Create FTP_TLS object with custom SSL context for better TLS handling
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)  # Specify TLS version for compatibility
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

def download_file(ftp, file_path, local_path):
    """Download a specific file from FTP and save it locally."""
    try:
        # Normalize the file path to ensure it starts with the base path
        base_path = '/Reports/ELON_data/Nomeco_environments/PROD_internally'
        if not file_path.startswith(base_path):
            file_path = f"{base_path}/{file_path}" if not file_path.startswith('/') else f"{base_path}{file_path}"
        logger.info(f"Normalized FTP path for download: {file_path}")

        # Navigate to the directory containing the file (remove filename from path)
        directory = '/'.join(file_path.split('/')[:-1]) or '/'
        filename = file_path.split('/')[-1]
        
        logger.info(f"Attempting to retrieve file: {filename} from {directory} via FTP")
        
        # Verify the directory exists before attempting to download
        try:
            ftp.cwd(directory)
            logger.info(f"Verified directory exists: {directory}")
        except ftplib.error_perm as e:
            logger.error(f"Directory verification failed for {directory}: {e}")
            raise Exception(f"Directory verification failed: {e}")

        # Switch to binary mode for file transfer
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
    """Main function to test FTP connection and download a file."""
    file_path = 'Reports/ELON_data/Nomeco_environments/PROD_internally/Nomeco_2024-10-01/20241001000000_BZ760818_Investigate.txt'
    local_filename = os.path.basename(file_path)  # Get the filename from the path
    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), local_filename)  # Save in the same directory as this script
    
    try:
        ftp = connect_to_ftp()
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