import os
import requests
from dotenv import load_dotenv
from PIL import Image
import io
import base64
from requests_toolbelt.multipart.encoder import MultipartEncoder

load_dotenv()

class HuggingFaceImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        # Model for generating fashion items and virtual try-on
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def test_api_access(self):
        """Test if we can access the API successfully."""
        try:
            response = requests.get(self.api_url, headers=self.headers)
            if response.status_code == 200:
                return "API access test successful"
            else:
                return f"API access test failed with status code: {response.status_code}"
        except Exception as e:
            return f"API access test failed with error: {str(e)}"

    def generate_fashion_image(self, prompt):
        """Generate a fashion image based on the given prompt."""
        try:
            # Enhance the prompt for better fashion-focused results
            enhanced_prompt = f"High quality professional fashion photography of {prompt}, fashion model, detailed fabric texture, studio lighting, white background, 4k, realistic"
            
            # Make the API call
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": enhanced_prompt, "negative_prompt": "wrong gender, incorrect gender, opposite gender"}
            )

            # Check if the request was successful
            if response.status_code != 200:
                return None, f"Error: API request failed with status code {response.status_code}"

            # Convert the response to an image
            image = Image.open(io.BytesIO(response.content))
            
            # Save the image to a bytes buffer
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Convert to base64 for easy transmission
            base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
            
            return base64_image, "Image generated successfully"
        except Exception as e:
            return None, f"Error generating image: {str(e)}"

    def virtual_try_on(self, person_image, clothing_image, clothing_description=None):
        """
        Use Try-On Diffusion RapidAPI for virtual try-on.
        Args:
            person_image: Base64 encoded image of the person
            clothing_image: Base64 encoded image of the clothing item
            clothing_description: (Unused, for compatibility)
        Returns:
            Tuple of (base64_result_image, message)
        """
        import base64
        import io
        rapidapi_key = "aee7765f26msh82287fbd3051e54p1835e6jsn3114304c19fd"  # Move to env for production
        url = "https://try-on-diffusion.p.rapidapi.com/try-on-file"
        # Decode base64 images to bytes
        person_bytes = base64.b64decode(person_image)
        clothing_bytes = base64.b64decode(clothing_image)
        m = MultipartEncoder(
            fields={
                'clothing_image': ('clothing.jpg', io.BytesIO(clothing_bytes), 'image/jpeg'),
                'avatar_image': ('person.jpg', io.BytesIO(person_bytes), 'image/jpeg')
            }
        )
        headers = {
            "Content-Type": m.content_type,
            "x-rapidapi-host": "try-on-diffusion.p.rapidapi.com",
            "x-rapidapi-key": rapidapi_key
        }
        try:
            response = requests.post(url, data=m, headers=headers, timeout=120)
            if response.status_code == 200:
                # Return as base64 for template rendering
                result_base64 = base64.b64encode(response.content).decode('utf-8')
                return result_base64, "Virtual try-on completed successfully"
            else:
                return None, f"Error: API call failed. Status: {response.status_code}, {response.text}"
        except Exception as e:
            return None, f"Exception during try-on: {str(e)}" 