import base64
import requests
import os
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

def get_tire_brand_from_image(image_path):
    """Deduces the tire brand from the image using OpenAI API"""
    try:
        logger.info(f"Starting tire brand detection for image: {image_path}")
        
        # Load API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OpenAI API key not found")
            return None
        
        # Encode image
        base64_image = encode_image(image_path)
        if not base64_image:
            return None
            
        logger.debug("Image encoded successfully")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Note: Using double quotes in the prompt text for proper JSON formatting
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": 'This image of a section of a car tire contains the brand. Please get the brand from the image. Return the result as a JSON with a "tire_brand" key using double quotes. For example: {"tire_brand": "Michelin"}'
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
            json=payload,
            timeout=30
        )
        
        logger.debug(f"OpenAI API Response Status: {response.status_code}")
        logger.debug(f"OpenAI API Response: {response.text}")

        if response.status_code == 200:
            result = response.json().get('choices', [{}])[0].get('message', {}).get('content', None)
            if result:
                logger.info(f"Successfully got tire brand result: {result}")
                # Clean the response and handle potential JSON formatting issues
                try:
                    # Remove markdown formatting if present
                    clean_result = result.replace("```json", "").replace("```", "").strip()
                    # Convert single quotes to double quotes if needed
                    clean_result = clean_result.replace("'", '"')
                    # Parse and re-serialize to ensure proper JSON format
                    parsed_data = json.loads(clean_result)
                    final_result = json.dumps(parsed_data)
                    logger.debug(f"Cleaned and formatted result: {final_result}")
                    return final_result
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing error: {e}")
                    # Fallback: try to extract brand name and create proper JSON
                    if "tire_brand" in result:
                        try:
                            brand = result.split(":")[1].strip().replace("'", "").replace('"', "").replace("}", "").strip()
                            fallback_result = json.dumps({"tire_brand": brand})
                            logger.debug(f"Created fallback result: {fallback_result}")
                            return fallback_result
                        except Exception as e:
                            logger.error(f"Fallback parsing failed: {e}")
                            return None
            else:
                logger.error("No content in OpenAI response")
        else:
            logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
        
        return None
        
    except Exception as e:
        logger.error(f"Error in get_tire_brand_from_image: {str(e)}")
        return None