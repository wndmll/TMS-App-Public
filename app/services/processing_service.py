# app/services/processing_service.py

import os
import json
import logging
from typing import Optional, Dict, Any
from services.get_license import get_license_from_image
from services.get_tire_brand import get_tire_brand_from_image

class ProcessingService:
    def __init__(self, upload_folder: str):
        self.upload_folder = upload_folder
        self.logger = logging.getLogger(__name__)

    def process_license_plate(self, image_path: str, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Process license plate image and store results.
        
        Args:
            image_path: Path to the license plate image
            session_id: Current session identifier
            
        Returns:
            Optional[Dict]: Processing results or None if processing failed
        """
        try:
            self.logger.info(f"Processing license plate for session {session_id}")
            
            # Get license plate info
            license_info_str = get_license_from_image(image_path)
            if license_info_str is None:
                self.logger.error("License plate detection failed")
                return None

            # Parse the response
            try:
                license_info_str = license_info_str.replace("'", '"')
                license_info = json.loads(license_info_str)
                
                # Extract information
                license_plate = license_info.get('license_plate')
                car_brand = license_info.get('car_brand', 'Unknown')

                # Store session data
                session_data = {
                    'license_plate': license_plate,
                    'car_brand': car_brand,
                    'session_id': session_id
                }
                
                self._save_session_data(session_id, session_data)
                return session_data

            except json.JSONDecodeError as e:
                self.logger.error(f"Error parsing license info JSON: {e}")
                self.logger.error(f"Raw license info: {license_info_str}")
                return None

        except Exception as e:
            self.logger.error(f"Error processing license plate: {e}")
            return None

    def process_tire_brand(self, image_path: str, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Process tire brand image and store results.
        
        Args:
            image_path: Path to the tire brand image
            session_id: Current session identifier
            
        Returns:
            Optional[Dict]: Processing results or None if processing failed
        """
        try:
            self.logger.info(f"Processing tire brand for session {session_id}")
            
            # Get existing session data
            session_data = self._load_session_data(session_id)
            if not session_data:
                session_data = {'session_id': session_id}

            # Get tire brand info
            tire_brand_info = get_tire_brand_from_image(image_path)
            if tire_brand_info is None:
                self.logger.error("Tire brand detection failed")
                return None

            try:
                tire_brand_data = json.loads(tire_brand_info)
                tire_brand = tire_brand_data.get('tire_brand', 'Unknown')
                
                # Update session data
                session_data['tire_brand'] = tire_brand
                self._save_session_data(session_id, session_data)
                
                return session_data

            except json.JSONDecodeError as e:
                self.logger.error(f"Error parsing tire brand JSON: {e}")
                return None

        except Exception as e:
            self.logger.error(f"Error processing tire brand: {e}")
            return None

    def _save_session_data(self, session_id: str, data: Dict[str, Any]) -> None:
        """Save session data to a file."""
        try:
            session_file = os.path.join(self.upload_folder, f'session_{session_id}.json')
            with open(session_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            self.logger.error(f"Error saving session data: {e}")

    def _load_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data from a file."""
        try:
            session_file = os.path.join(self.upload_folder, f'session_{session_id}.json')
            if os.path.exists(session_file):
                with open(session_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading session data: {e}")
        return None