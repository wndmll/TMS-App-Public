# Imports
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, Response, session, current_app
from flask import stream_with_context
from contextlib import contextmanager
import os
import datetime
import json
import paramiko
from dotenv import load_dotenv
import threading
import queue
import logging
import sys
import subprocess
import functools
from services.ftp_service import FTPService
from services.processing_service import ProcessingService
from services.status_service import StatusService
from services.file_handler import FileHandler
from services.session_manager import SessionManager
from handlers.route_handler import RouteHandler

# Configuration loading
def load_configurations():
    """Load all environment configurations"""
    config_dir = os.path.join(os.path.dirname(__file__), 'config')
    
    # Load Flask configuration
    load_dotenv(os.path.join(config_dir, 'flask', '.env'))
    
    # Load FTP configuration
    load_dotenv(os.path.join(config_dir, 'ftp', '.env'))
    
    # Load OpenAI configuration
    load_dotenv(os.path.join(config_dir, 'openai', '.env'))

# SCSS compilation
def run_compile_scss():
    try:
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'compile_scss.py')
        subprocess.run(['python', script_path], check=True)
        logging.debug("SCSS compiled successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"SCSS compilation failed: {e}")

# Check if the script is running in the reloader process
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    run_compile_scss()

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(threadName)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'app.log')),
        logging.StreamHandler()
    ]
)

logging.debug("Logging is set up.")

# Load all configurations
load_configurations()

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

# Initialize services
ftp_service = FTPService(
    host=os.getenv('SFTP_HOST'),
    port=int(os.getenv('SFTP_PORT')),
    username=os.getenv('SFTP_USER'),
    password=os.getenv('SFTP_PASS')
)

file_handler = FileHandler(app.config['UPLOAD_FOLDER'])
processing_service = ProcessingService(app.config['UPLOAD_FOLDER'])
status_service = StatusService()
session_manager = SessionManager(file_handler)

# Helper functions
def send_progress_update(progress):
    """Helper function to send progress updates"""
    try:
        status_service.send_progress_update(progress)
    except Exception as e:
        logging.error(f"Error sending progress update: {e}")

def process_license_and_upload(image_path, session_id):
    try:
        logging.info(f"Started processing for session {session_id}")
        status_service.send_processing_status(
            "license", 
            "processing",
            "Processing license plate..."
        )

        result = processing_service.process_license_plate(image_path, session_id)
        if result is None:
            status_service.send_processing_status(
                "license",
                "error",
                "License plate detection failed"
            )
            return

        status_service.send_processing_status(
            "license",
            "success",
            "License plate and car brand detected.",
            {
                "license_plate": result['license_plate'],
                "car_brand": result['car_brand']
            }
        )

        # Fix path construction
        cleaned_license = result['license_plate'].replace('-', '')
        remote_path = os.path.join(
            os.getenv('FTP_BASE_PATH', '/home/appuwauto/public_html/apps/5/webdisk'),
            'car',
            cleaned_license,
            'tire',
            session_id
        ).replace('\\', '/')  # Convert Windows paths to Unix

        upload_to_ftp(image_path, remote_path, 'license_plate.jpg')

    except Exception as e:
        logging.error(f"Error in process_license_and_upload: {e}")
        status_service.send_error(str(e))
    finally:
        file_handler.cleanup_file(image_path)
        status_service.send_completion()
        
def process_tire_brand_and_upload(image_path, session_id):
    try:
        logging.info(f"Starting tire brand processing for session {session_id}")
        
        session_data = file_handler.load_session_data(session_id) or {}
        license_plate = session_data.get('license_plate', '')
        car_brand = session_data.get('car_brand', '')
        
        status_service.send_processing_status(
            "tire_brand",
            "processing",
            "Processing tire brand...",
            {
                "license_plate": license_plate,
                "car_brand": car_brand
            }
        )

        result = processing_service.process_tire_brand(image_path, session_id)
        if result is None:
            status_service.send_processing_status(
                "tire_brand",
                "error",
                "Tire brand detection failed",
                {
                    "license_plate": license_plate,
                    "car_brand": car_brand
                }
            )
            return

        status_service.send_processing_status(
            "tire_brand",
            "success",
            "Tire brand detected",
            {
                "tire_brand": result['tire_brand'],
                "license_plate": license_plate,
                "car_brand": car_brand
            }
        )

        cleaned_license = license_plate.replace('-', '')
        remote_path = os.path.join(
            os.getenv('FTP_BASE_PATH', ''),
            'car',
            cleaned_license,
            'tire',
            session_id
        )
        upload_to_ftp(image_path, remote_path, 'tire_brand.jpg')

    except Exception as e:
        logging.error(f"Error in process_tire_brand_and_upload: {e}")
        status_service.send_processing_status(
            "tire_brand",
            "error",
            str(e),
            {
                "license_plate": license_plate,
                "car_brand": car_brand
            }
        )
    finally:
        file_handler.cleanup_file(image_path)
        status_service.send_completion()

def upload_to_ftp(image_path, remote_path, filename):
    """Upload file to FTP server with progress updates"""
    try:
        def progress_callback(sent, total):
            try:
                progress = min(int((sent / total) * 100), 100)
                send_progress_update(progress)
            except Exception as e:
                logging.error(f"Progress callback error: {e}")

        send_progress_update(0)
        
        # Ensure remote path uses forward slashes
        remote_path = remote_path.replace('\\', '/')
        
        # Create remote directory structure if it doesn't exist
        logging.debug(f"Creating remote directory: {remote_path}")
        ftp_service.create_remote_directory(remote_path)
        
        upload_success = ftp_service.upload_file(
            local_path=image_path,
            remote_path=remote_path,
            filename=filename,
            progress_callback=progress_callback
        )

        if not upload_success:
            raise Exception("FTP upload failed")

        send_progress_update(100)
        public_url = ftp_service.get_public_url(remote_path)
        status_service.send_ftp_status(
            status="uploaded",
            message="File uploaded successfully",
            link=public_url
        )

    except Exception as e:
        logging.error(f"FTP upload failed: {e}")
        status_service.send_error(f"FTP upload failed: {str(e)}")
        
# Route handler initialization
route_handler = RouteHandler(
    session_manager=session_manager,
    file_handler=file_handler,
    processing_service=processing_service,
    status_service=status_service,
    process_license_and_upload=process_license_and_upload,
    process_tire_brand_and_upload=process_tire_brand_and_upload
)

# Route definitions
@app.route('/')
def index():
    return route_handler.index()

@app.route('/start-session', methods=['POST'])
def start_session():
    return route_handler.start_session()

@app.route('/session/<session_id>')
def session_page(session_id):
    return route_handler.session_page(session_id, session)

@app.route('/session/<session_id>/tire-brand')
def tire_brand_page(session_id):
    return route_handler.tire_brand_page(session_id)

@app.route('/session/<session_id>/upload_license_plate', methods=['POST'])
def upload_license_plate(session_id):
    response, status_code = route_handler.handle_license_plate_upload(session_id)
    return jsonify(response), status_code

@app.route('/session/<session_id>/upload_tire_brand', methods=['POST'])
def upload_tire_brand(session_id):
    response, status_code = route_handler.handle_tire_brand_upload(session_id)
    return jsonify(response), status_code
        
@app.route('/upload-status')
def upload_status():
    return route_handler.handle_status_updates()

# App context decorator
def with_app_context(f):
    """Decorator to ensure function runs in app context"""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        with current_app.app_context():
            return f(*args, **kwargs)
    return decorated

# Main block
if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('logs', exist_ok=True)
    file_handler.ensure_upload_folder_exists()
    
    # Start the Flask application
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=port,
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
        use_reloader=True,
        threaded=True
    )