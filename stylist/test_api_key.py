import os
from dotenv import load_dotenv

load_dotenv()

def test_api_key():
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        print("ERROR: No API key found in environment variables")
        print("Make sure you have a .env file with HUGGINGFACE_API_KEY=your_key")
        return
    
    # Print first and last 4 characters of the key for verification
    print(f"API key found: {api_key[:4]}...{api_key[-4:]}")
    print(f"API key length: {len(api_key)}")
    print("\nMake sure this matches your HuggingFace API key!")

if __name__ == "__main__":
    test_api_key() 