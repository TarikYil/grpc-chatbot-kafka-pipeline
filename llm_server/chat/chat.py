"""
Chat Module - Google Gemini API Integration
Handles conversation with Google's Gemini AI model
"""
import google.generativeai as genai
import logging
from .config import ChatConfig



class VoiceChatBot:
    """
    Voice Chat Bot class that handles conversation with Google Gemini AI.
    
    This class manages the chat session with Google's Gemini model,
    handles API communication, and provides intelligent responses
    to user queries.
    """
    
    def __init__(self):
        """
        Initialize the chat bot.
        
        Sets up the Google Gemini API configuration and starts
        a new chat session with the AI model.
        
        Raises:
            Exception: If initialization fails due to configuration or API issues
        """
        try:
            # Validate configuration
            ChatConfig.validate_config()
            
            # Configure Google AI
            genai.configure(api_key=ChatConfig.GOOGLE_API_KEY)
            
            # Initialize Gemini model
            self.model = genai.GenerativeModel(
                model_name=ChatConfig.MODEL,
                generation_config=ChatConfig.get_generation_config(),
                safety_settings=ChatConfig.SAFETY_SETTINGS,
                system_instruction=ChatConfig.SYSTEM_MESSAGE
            )
            
            # Start chat session
            self.chat_session = self.model.start_chat(history=[])
            
            print("Google Gemini chat bot initialized successfully!")
            
        except Exception as e:
            logging.error(f"Failed to initialize chat bot: {e}")
            raise
    
    def get_response(self, user_message):
        """
        Generate a response to user message using Google Gemini.
        
        Args:
            user_message (str): The user's input message
            
        Returns:
            str or None: Bot response text or None if error occurs
        """
        try:
            print(f"User: {user_message}")
            print("Generating Gemini AI response...")
            
            # Send message to Gemini
            response = self.chat_session.send_message(user_message)
            
            # Extract response text
            assistant_message = response.text.strip()
            
            print(f"Assistant: {assistant_message}")
            
            return assistant_message
            
        except Exception as e:
            logging.error(f"Gemini API error: {e}")
            
            # Specific error messages based on error type
            error_message = str(e).lower()
            if 'quota' in error_message or 'limit' in error_message:
                print("API usage limit exceeded. Please wait.")
            elif 'network' in error_message or 'connection' in error_message:
                print("Please check your internet connection.")
            elif 'api key' in error_message or 'authentication' in error_message:
                print("Please check your API key.")
            else:
                print("An error occurred while getting response.")
            
            return None
    
    def reset_conversation(self):
        """
        Reset the conversation history.
        
        This method starts a new chat session, effectively
        clearing all previous conversation context.
        """
        try:
            # Start new chat session
            self.chat_session = self.model.start_chat(history=[])
            print("Conversation history reset.")
        except Exception as e:
            logging.error(f"Conversation reset error: {e}")
    
    def get_conversation_summary(self):
        """
        Get a summary of the current conversation.
        
        Returns:
            dict: Dictionary containing conversation statistics
                  with keys: total_messages, user_messages, assistant_messages
        """
        try:
            history = self.chat_session.history
            user_messages = [msg for msg in history if msg.role == "user"]
            assistant_messages = [msg for msg in history if msg.role == "model"]
            
            return {
                "total_messages": len(history),
                "user_messages": len(user_messages),
                "assistant_messages": len(assistant_messages)
            }
        except Exception as e:
            logging.error(f"Failed to get conversation summary: {e}")
            return {"total_messages": 0, "user_messages": 0, "assistant_messages": 0}

