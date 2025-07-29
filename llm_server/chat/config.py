"""
Configuration Module - Google Gemini API Settings
Manages API keys and model configuration for the chat functionality
"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class ChatConfig:
    """
    Configuration class for Google Gemini API settings.
    
    This class manages all configuration parameters for the chat functionality,
    including API keys, model settings, safety configurations, and system messages.
    """
    
    # Google API Key (from .env file or environment variable)
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Model settings
    MODEL = "gemini-1.5-flash"  # Google Gemini model
    MAX_TOKENS = 500
    TEMPERATURE = 0.7
    
    # System message (defines assistant behavior)
    SYSTEM_MESSAGE = """You are a helpful and friendly voice assistant. 
    Provide short and clear responses. Speak in English. 
    Engage in natural conversation with the user. 
    Keep your responses concise and to the point."""
    
    # Safety settings
    SAFETY_SETTINGS = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]
    
    @classmethod
    def validate_config(cls):
        """
        Validate configuration settings.
        
        Checks if the required API key is present and valid.
        
        Returns:
            bool: True if configuration is valid
            
        Raises:
            ValueError: If GOOGLE_API_KEY is not found or invalid
        """
        if not cls.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY not found. "
                "Please define GOOGLE_API_KEY=your_api_key_here in .env file "
                "or set as system environment variable."
            )
        return True
    
    @classmethod
    def get_generation_config(cls):
        """
        Get generation configuration for Gemini model.
        
        Returns:
            dict: Dictionary containing generation parameters
                  including max_output_tokens and temperature
        """
        return {
            'max_output_tokens': cls.MAX_TOKENS,
            'temperature': cls.TEMPERATURE,
        }

