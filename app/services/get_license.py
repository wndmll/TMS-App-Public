import base64
import requests
import os
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)  # Get a logger instance for this module

def encode_image(image_path):
    """Encode the image to base64 format"""
    try:
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return None
            
        with open(image_path, "rb") as image_file:
            logger.debug(f"Reading image file: {image_path}")
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding image: {str(e)}")
        return None

def get_license_from_image(image_path):
    """Deduces the license plate from the image using OpenAI API"""
    try:
        logger.info(f"Starting license plate detection for image: {image_path}")
        base64_image = encode_image(image_path)
        if not base64_image:
            return None

        logger.debug("Image encoded successfully")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": 'This image contains a sticker on a car tire. Get the license plate and car brand from the image. Only return the license plate number and the car brand (not the model). Please return a json with the keys "license_plate" and "car_brand" using double quotes. For example: {"license_plate": "ABC1234", "car_brand": "Toyota"}.'
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        logger.debug("Sending request to OpenAI API")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        logger.debug(f"OpenAI API Response Status: {response.status_code}")
        logger.debug(f"OpenAI API Response: {response.text}")

        if response.status_code == 200:
            result = response.json().get('choices', [{}])[0].get('message', {}).get('content', None)
            if result:
                # Clean the response
                logger.debug(f"Raw result from API: {result}")
                result = result.replace("```json", "").replace("```", "").strip()
                # Replace single quotes with double quotes if needed
                result = result.replace("'", '"')
                # Validate JSON format
                json.loads(result)  # This will raise an error if JSON is invalid
                logger.info(f"Successfully processed license plate result: {result}")
                return result
            else:
                logger.error("No content in OpenAI response")
        else:
            logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        logger.error(f"Error in get_license_from_image: {str(e)}")
        return None

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
app_dir = os.path.dirname(os.path.dirname(current_dir))
# Construct the path to the .env file
dotenv_path = os.path.join(app_dir, 'app', 'config', 'openai', '.env')

logger.debug(f"Loading .env file from: {dotenv_path}")

# Load the environment variables from the .env file
load_dotenv(dotenv_path=dotenv_path)

# Get the OpenAI API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

if api_key:
    logger.info("OpenAI API key loaded successfully")
else:
    logger.error("Failed to load OpenAI API key")