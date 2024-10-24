# app/services/session_manager.py

import datetime
import logging
from typing import Dict, Tuple, Optional

class SessionManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.logger = logging.getLogger(__name__)

    def create_session(self) -> str:
        """
        Create a new session ID.
        
        Returns:
            str: Newly created session ID
        """
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]

    def initialize_session(self, session_id: str, flask_session) -> None:
        """
        Initialize a new session with empty values.
        
        Args:
            session_id: The session identifier
            flask_session: Flask session object
        """
        flask_session['session_id'] = session_id
        flask_session['license_plate'] = ''
        flask_session['car_brand'] = ''

    def get_session_data(self, session_id: str) -> Tuple[str, str]:
        """
        Get license plate and car brand from session data.
        
        Args:
            session_id: The session identifier
            
        Returns:
            Tuple[str, str]: License plate and car brand
        """
        try:
            session_data = self.file_handler.load_session_data(session_id) or {}
            return (
                session_data.get('license_plate', ''),
                session_data.get('car_brand', '')
            )
        except Exception as e:
            self.logger.error(f"Error loading session data: {e}")
            return ('', '')

    def validate_session(self, session_id: str) -> bool:
        """
        Validate if a session ID is properly formatted and exists.
        
        Args:
            session_id: The session identifier to validate
            
        Returns:
            bool: True if session is valid, False otherwise
        """
        try:
            if not session_id or len(session_id) != 17:  # YYYYMMDDHHMMSSmmm format
                return False
                
            # Check if session data exists
            session_data = self.file_handler.load_session_data(session_id)
            return session_data is not None
            
        except Exception as e:
            self.logger.error(f"Error validating session: {e}")
            return False

    def get_session_file_paths(self, session_id: str, prefix: str) -> str:
        """
        Generate file paths for session-related files.
        
        Args:
            session_id: The session identifier
            prefix: File prefix (e.g., 'license', 'tire_brand')
            
        Returns:
            str: Path for the file
        """
        return self.file_handler.get_file_path(f"{prefix}_{session_id}.jpg")