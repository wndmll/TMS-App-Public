# app/handlers/route_handler.py

import logging
import threading
import queue 
from typing import Tuple
from flask import jsonify, render_template, redirect, url_for, Response, request
from flask import stream_with_context

class RouteHandler:
    def __init__(self, session_manager, file_handler, processing_service, status_service,
                 process_license_and_upload, process_tire_brand_and_upload):
        self.session_manager = session_manager
        self.file_handler = file_handler
        self.processing_service = processing_service
        self.status_service = status_service
        self.process_license_and_upload = process_license_and_upload
        self.process_tire_brand_and_upload = process_tire_brand_and_upload
        self.logger = logging.getLogger(__name__)

    def index(self):
        """Handle the index route."""
        return render_template('index.html')

    def start_session(self):
        """Create and redirect to a new session."""
        session_id = self.session_manager.create_session()
        return redirect(url_for('session_page', session_id=session_id))

    def session_page(self, session_id: str, flask_session):
        """
        Handle the session page route.
        
        Args:
            session_id: The session identifier
            flask_session: Flask session object
        """
        if not self.session_manager.validate_session(session_id):
            self.session_manager.initialize_session(session_id, flask_session)
        return render_template('license.html', session_id=session_id)

    def tire_brand_page(self, session_id: str) -> str:
        """
        Handle the tire brand page route.
        
        Args:
            session_id: The session identifier
        """
        try:
            license_plate, car_brand = self.session_manager.get_session_data(session_id)
            return render_template(
                'tire_brand.html',
                session_id=session_id,
                license_plate=license_plate,
                car_brand=car_brand
            )
        except Exception as e:
            self.logger.error(f"Error loading tire brand page: {e}")
            return render_template('tire_brand.html', session_id=session_id)

    def handle_license_plate_upload(self, session_id: str) -> Tuple[dict, int]:
        try:
            if 'image' not in request.files:
                return {'error': 'No image file provided'}, 400

            image = request.files['image']
            image_path = self.file_handler.save_temporary_file(image, session_id, 'license')
            
            if not image_path:
                return {'error': 'Failed to save uploaded file'}, 500

            # Use the instance method instead of global function
            threading.Thread(
                target=self.process_license_and_upload,
                args=(image_path, session_id)
            ).start()

            return {'message': 'File upload started'}, 202

        except Exception as e:
            self.logger.error(f"An error occurred while uploading: {e}")
            return {'error': str(e)}, 500

    def handle_tire_brand_upload(self, session_id: str) -> Tuple[dict, int]:
        try:
            self.logger.info(f"Starting tire brand upload for session {session_id}")
            
            if 'image' not in request.files:
                self.logger.error("No image file in request")
                return {'error': 'No image file provided'}, 400
            
            image = request.files['image']
            image_path = self.file_handler.save_temporary_file(image, session_id, 'tire_brand')
            
            if not image_path:
                return {'error': 'Failed to save uploaded file'}, 500

            # Use the instance method instead of global function
            threading.Thread(
                target=self.process_tire_brand_and_upload,
                args=(image_path, session_id)
            ).start()

            return {'message': 'File upload started'}, 202

        except Exception as e:
            self.logger.error(f"Error in upload_tire_brand: {str(e)}")
            return {'error': str(e)}, 500
        
    def handle_status_updates(self) -> Response:
        """Handle status update stream."""
        status_queue = self.status_service.get_status_queue()
        
        @stream_with_context
        def generate():
            try:
                client_ip = request.remote_addr
                self.logger.info(f"Client connected from: {client_ip}")
                
                while True:
                    try:
                        update = status_queue.get(timeout=30)
                        
                        if update == 'DONE':
                            yield f"data: {json.dumps({'status': 'done'})}\n\n"
                            self.logger.info(f"Processing completed for client: {client_ip}")
                            break
                        
                        if isinstance(update, str):
                            yield f"data: {update}\n\n"
                        else:
                            yield f"data: {json.dumps(update)}\n\n"
                            
                    except queue.Empty:
                        yield 'data: {"type": "heartbeat"}\n\n'
                        
            except GeneratorExit:
                self.logger.info(f"Client disconnected: {client_ip}")
            except Exception as e:
                self.logger.error(f"SSE error: {str(e)}")
                error_msg = json.dumps({"type": "error", "message": str(e)})
                yield f"data: {error_msg}\n\n"

        return Response(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'
            }
        )