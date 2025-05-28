from groq import Groq
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

class GroqStyleAssistant:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = "llama-3.3-70b-versatile"  # Using Mixtral for better reasoning

    def generate_outfit_suggestion(self, event_type: str, climate: str, style_preference: str, 
                                 color_preferences: List[str], user_profile: Dict = None) -> Dict:
        """
        Generate personalized outfit suggestions using Groq's LLM.
        
        Args:
            event_type: Type of event (casual, formal, etc.)
            climate: Weather condition
            style_preference: Preferred style
            color_preferences: List of preferred colors
            user_profile: Optional user profile data
        
        Returns:
            Dict containing outfit description and items
        """
        # Construct the prompt
        profile_context = ""
        if user_profile:
            profile_context = f"""
            Consider the following user profile:
            - Gender: {user_profile.get('gender', 'Not specified')}
            - Body type: {user_profile.get('body_type', 'Not specified')}
            - Height: {user_profile.get('height', 'Not specified')}
            - Skin tone: {user_profile.get('skin_tone', 'Not specified')}

            Please ensure all clothing suggestions are appropriate for {user_profile.get('gender', 'the user')}'s gender.
            """

        color_prefs = ", ".join(color_preferences) if color_preferences else "any colors"
        
        prompt = f"""As a professional fashion stylist, create a detailed outfit suggestion for the following scenario:

        Event type: {event_type}
        Climate/Weather: {climate}
        Style preference: {style_preference}
        Color preferences: {color_prefs}
        {profile_context}

        Please provide:
        1. A detailed description of a gender-appropriate complete outfit
        2. A list of specific items with the following details for each:
           - Item type (top, bottom, dress, outerwear, footwear, or accessory)
           - Detailed description (make sure items are appropriate for the specified gender)
           - Shopping keywords for finding similar items

        Format the response as a JSON object with the following structure:
        {{
            "description": "overall outfit description",
            "items": [
                {{
                    "type": "item type",
                    "description": "detailed item description",
                    "shopping_keywords": "search terms for shopping"
                }}
            ]
        }}
        """

        # Call Groq API
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional fashion stylist with expertise in creating personalized outfit recommendations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=self.model,
            temperature=0.7,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )

        # Parse and return the response
        try:
            response = chat_completion.choices[0].message.content
            return eval(response)  # Convert string to dict
        except Exception as e:
            print(f"Error parsing Groq response: {e}")
            # Return a fallback response
            return {
                "description": f"A stylish {style_preference} outfit for {event_type} in {climate} weather.",
                "items": [
                    {
                        "type": "top",
                        "description": "Classic piece suitable for the occasion",
                        "shopping_keywords": f"{style_preference} top {event_type}"
                    }
                ]
            } 