import os
import logging
import paramiko
from typing import Optional, Callable
from dotenv import load_dotenv

class FTPService:
    def __init__(self, host: str, port: int, username: str, password: str):
        """
        Initialize FTP service with configuration.
        
        Args:
            host: SFTP host address
            port: SFTP port number
            username: SFTP username
            password: SFTP password
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logger = logging.getLogger(__name__)
        
        # Load FTP configuration
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'ftp', '.env')
        load_dotenv(config_path)
        
        # Get base paths from configuration
        self.base_path = os.getenv('FTP_BASE_PATH')
        self.public_base_url = os.getenv('FTP_PUBLIC_BASE_URL')
        self.webdisk_path = os.getenv('FTP_WEBDISK_PATH')

    def create_remote_directory(self, path: str) -> None:
        """
        Create remote directory and all intermediate directories.
        
        Args:
            path: Remote path to create
        """
        transport = paramiko.Transport((self.host, self.port))
        try:
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            
            # Split path and create each directory level
            path_parts = path.split('/')
            current_path = ''
            for part in path_parts:
                if part:
                    current_path += '/' + part
                    try:
                        sftp.stat(current_path)
                    except FileNotFoundError:
                        self.logger.debug(f"Creating directory: {current_path}")
                        sftp.mkdir(current_path)
                        
        except Exception as e:
            self.logger.error(f"Error creating remote directory: {e}")
            raise
        finally:
            sftp.close()
            transport.close()

    def upload_file(
        self, 
        local_path: str, 
        remote_path: str, 
        filename: str,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> bool:
        """
        Upload a file to the FTP server with progress tracking.
        
        Args:
            local_path: Path to the local file
            remote_path: Remote directory path
            filename: Name for the uploaded file
            progress_callback: Optional callback for progress updates
            
        Returns:
            bool: True if upload successful, False otherwise
        """
        try:
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)

            try:
                # Create directory structure
                current_path = ''
                for folder in remote_path.split('/'):
                    if folder:
                        current_path += '/' + folder
                        try:
                            sftp.stat(current_path)
                        except FileNotFoundError:
                            sftp.mkdir(current_path)

                # Perform upload
                remote_file_path = os.path.join(remote_path, filename).replace('\\', '/')
                self.logger.info(f"Uploading file to: {remote_file_path}")
                
                # Get file size for progress tracking
                file_size = os.path.getsize(local_path)
                
                with open(local_path, 'rb') as local_file:
                    with sftp.file(remote_file_path, 'wb') as remote_file:
                        sent_bytes = 0
                        for chunk in iter(lambda: local_file.read(32768), b''):
                            remote_file.write(chunk)
                            sent_bytes += len(chunk)
                            if progress_callback:
                                progress_callback(sent_bytes, file_size)
                                
                return True

            finally:
                sftp.close()
                transport.close()

        except Exception as e:
            self.logger.error(f"FTP upload failed: {str(e)}")
            return False
            
    def get_public_url(self, remote_path: str) -> str:
        """
        Generate the public URL for an uploaded file.
        
        Args:
            remote_path: The remote path of the uploaded file
            
        Returns:
            str: Public URL for the uploaded file
        """
        try:
            # Extract the relative path after the webdisk path
            if self.base_path in remote_path:
                relative_path = remote_path.replace(self.base_path, '').lstrip('/')
            else:
                path_parts = remote_path.split(self.webdisk_path)
                relative_path = path_parts[1] if len(path_parts) > 1 else ''
            
            # Construct the public URL
            return f"{self.public_base_url}/{relative_path}/".rstrip('//')
            
        except Exception as e:
            self.logger.error(f"Error generating public URL: {e}")
            return f"{self.public_base_url}/"