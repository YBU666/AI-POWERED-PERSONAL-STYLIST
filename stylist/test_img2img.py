import os
import requests
from dotenv import load_dotenv
import base64
from PIL import Image
import io
from requests_toolbelt.multipart.encoder import MultipartEncoder

load_dotenv()

def compress_image(input_path, max_size=(512, 512), quality=85):
    img = Image.open(input_path)
    img.thumbnail(max_size)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(input_path, "JPEG", quality=quality)

compress_image("stylist/test_person.jpg")
compress_image("stylist/test_clothing.jpg")

def test_img2img():
    # Get API key from environment
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    # API URL for SDXL
    api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        # Load a test image and convert to base64
        test_image_path = "test_image.jpg"  # You'll need to provide a test image
        with open(test_image_path, "rb") as image_file:
            image_bytes = image_file.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # First test: Simple API access
        print("Testing API access...")
        response = requests.get(api_url, headers=headers)
        print(f"API access test status: {response.status_code}")

        # Second test: Text-to-image generation
        print("\nTesting text-to-image...")
        txt2img_payload = {
            "inputs": "A professional photo of a fashion model in a blue dress"
        }
        response = requests.post(api_url, headers=headers, json=txt2img_payload)
        print(f"Text-to-image status: {response.status_code}")
        if response.status_code == 200:
            # Save the generated image
            image = Image.open(io.BytesIO(response.content))
            image.save("test_txt2img_output.png")
            print("Text-to-image test successful - saved as test_txt2img_output.png")

        # Third test: Image-to-image generation
        print("\nTesting image-to-image...")
        img2img_payload = {
            "inputs": f"A person wearing a red dress, high quality, detailed fabric, realistic {image_base64}",
            "parameters": {
                "negative_prompt": "poor quality, blurry, distorted",
                "num_inference_steps": 30,
                "guidance_scale": 7.5
            }
        }
        response = requests.post(api_url, headers=headers, json=img2img_payload)
        print(f"Image-to-image status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        if response.status_code != 200:
            print(f"Error response: {response.text}")
        else:
            # Save the generated image
            image = Image.open(io.BytesIO(response.content))
            image.save("test_img2img_output.png")
            print("Image-to-image test successful - saved as test_img2img_output.png")

    except Exception as e:
        print(f"Test failed with error: {str(e)}")

def test_kolors_virtual_tryon():
    # Paths to your test images
    person_image_path = "stylist/test_person.jpg"  # Provide a sample person image
    clothing_image_path = "stylist/test_clothing.jpg"  # Provide a sample clothing image

    # Load and encode person image
    with open(person_image_path, "rb") as f:
        person_bytes = f.read()
        person_base64 = base64.b64encode(person_bytes).decode('utf-8')

    # Load and encode clothing image
    with open(clothing_image_path, "rb") as f:
        clothing_bytes = f.read()
        clothing_base64 = base64.b64encode(clothing_bytes).decode('utf-8')

    # Kolors Virtual Try-On API endpoint
    api_url = "https://hf.space/embed/Kwai-Kolors/Kolors-Virtual-Try-On/api/predict/"
    payload = {
        "data": [
            f"data:image/jpeg;base64,{person_base64}",
            f"data:image/jpeg;base64,{clothing_base64}"
        ]
    }

    try:
        print("Sending request to Kolors Virtual Try-On API...")
        response = requests.post(api_url, json=payload, timeout=120)
        print("Status code:", response.status_code)
        print("Response text:", response.text[:500])  # Print first 500 chars for debug
        if response.status_code != 200:
            print("Error: API call failed.")
            return
        result = response.json()
        if not result.get('data') or not result['data'][0].startswith('data:image'):
            print("Error: Unexpected response from try-on API.")
            return
        result_base64 = result['data'][0].split(",", 1)[1]
        # Decode and save the result image
        result_bytes = base64.b64decode(result_base64)
        with open("test_kolors_tryon_output.png", "wb") as out_f:
            out_f.write(result_bytes)
        print("Success! Output saved as test_kolors_tryon_output.png")
    except Exception as e:
        print("Exception during test:", str(e))

def test_rapidapi_viton_tryon():
    rapidapi_key = ""  # Replace with your actual RapidAPI key
    url = "https://try-on-diffusion.p.rapidapi.com/try-on-file"
    m = MultipartEncoder(
        fields={
            'clothing_image': ('clothing.jpg', open('stylist/test_clothing.jpg', 'rb'), 'image/jpeg'),
            'avatar_image': ('person.jpg', open('stylist/test_person.jpg', 'rb'), 'image/jpeg')
        }
    )
    headers = {
        "Content-Type": m.content_type,
        "x-rapidapi-host": "try-on-diffusion.p.rapidapi.com",
        "x-rapidapi-key": rapidapi_key
    }
    print("Sending request to Try-On Diffusion RapidAPI...")
    response = requests.post(url, data=m, headers=headers)
    print("Status code:", response.status_code)
    if response.status_code == 200:
        with open("tryon_result_rapidapi.jpg", "wb") as f:
            f.write(response.content)
        print("Success! Output saved as tryon_result_rapidapi.jpg")
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    # test_img2img()  # Commented out to avoid missing test_image.jpg error
    # test_kolors_virtual_tryon()  # Commented out to focus on RapidAPI test
    test_rapidapi_viton_tryon() 