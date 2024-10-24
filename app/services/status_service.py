# app/services/status_service.py

import json
import logging
from typing import Any, Dict, Optional
from queue import Queue

class StatusService:
    def __init__(self):
        self.queue = Queue()
        self.logger = logging.getLogger(__name__)

    def send_processing_status(self, process_type: str, status: str, message: str, 
                             additional_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Send a processing status update.
        
        Args:
            process_type: Type of process (e.g., 'license', 'tire_brand')
            status: Current status (e.g., 'processing', 'success', 'error')
            message: Status message
            additional_data: Optional additional data to include in the status
        """
        try:
            status_data = {
                "type": process_type,
                "status": status,
                "message": message
            }
            
            if additional_data:
                status_data.update(additional_data)
                
            self.queue.put(json.dumps(status_data))
            
        except Exception as e:
            self.logger.error(f"Error sending status update: {e}")

    def send_progress_update(self, progress: int) -> None:
        """
        Send a progress update.
        
        Args:
            progress: Progress percentage (0-100)
        """
        try:
            self.queue.put(json.dumps({
                "type": "progress",
                "status": "uploading",
                "progress": min(max(progress, 0), 100)
            }))
        except Exception as e:
            self.logger.error(f"Error sending progress update: {e}")

    def send_ftp_status(self, status: str, message: str, link: Optional[str] = None) -> None:
        """
        Send an FTP-related status update.
        
        Args:
            status: Current status (e.g., 'uploaded', 'error')
            message: Status message
            link: Optional public URL for uploaded file
        """
        try:
            status_data = {
                "type": "ftp",
                "status": status,
                "message": message
            }
            
            if link:
                status_data["link"] = link
                
            self.queue.put(json.dumps(status_data))
            
        except Exception as e:
            self.logger.error(f"Error sending FTP status: {e}")

    def send_error(self, message: str) -> None:
        """
        Send an error status update.
        
        Args:
            message: Error message
        """
        try:
            self.queue.put(json.dumps({
                "type": "error",
                "message": message
            }))
        except Exception as e:
            self.logger.error(f"Error sending error status: {e}")

    def send_completion(self) -> None:
        """Send a completion status update."""
        try:
            self.queue.put(json.dumps({"status": "done"}))
        except Exception as e:
            self.logger.error(f"Error sending completion status: {e}")

    def get_status_queue(self) -> Queue:
        """Get the status queue for the SSE endpoint."""
        return self.queue