# app/services/file_handler.py

import os
import json
import logging
from typing import Optional, Dict, Any

class FileHandler:
    def __init__(self, upload_folder: str):
        self.upload_folder = upload_folder
        self.logger = logging.getLogger(__name__)

    def save_temporary_file(self, file, session_id: str, prefix: str) -> Optional[str]:
        """
        Save an uploaded file temporarily.
        
        Args:
            file: The uploaded file object
            session_id: Session identifier
            prefix: Prefix for the filename (e.g., 'license', 'tire_brand')
            
        Returns:
            str: Path to the saved file, or None if save failed
        """
        try:
            if not file or file.filename == '':
                self.logger.error("No valid file provided")
                return None

            filename = f"{prefix}_{session_id}.jpg"
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            self.logger.info(f"File saved temporarily at: {file_path}")
            return file_path

        except Exception as e:
            self.logger.error(f"Error saving temporary file: {e}")
            return None

    def load_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load session data from file.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Optional[Dict]: Session data or None if not found
        """
        try:
            session_file = os.path.join(self.upload_folder, f'session_{session_id}.json')
            if os.path.exists(session_file):
                with open(session_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            self.logger.error(f"Error loading session data: {e}")
            return None

    def cleanup_file(self, file_path: str) -> bool:
        """
        Remove a temporary file.
        
        Args:
            file_path: Path to the file to remove
            
        Returns:
            bool: True if cleanup successful, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.logger.info(f"Cleaned up file: {file_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error cleaning up file: {e}")
            return False

    def ensure_upload_folder_exists(self) -> None:
        """Ensure the upload folder exists."""
        try:
            os.makedirs(self.upload_folder, exist_ok=True)
        except Exception as e:
            self.logger.error(f"Error creating upload folder: {e}")
            
    def get_file_path(self, filename: str) -> str:
        """
        Get the full path for a file in the upload folder.
        
        Args:
            filename: Name of the file
            
        Returns:
            str: Full path to the file
        """
        return os.path.join(self.upload_folder, filename)            