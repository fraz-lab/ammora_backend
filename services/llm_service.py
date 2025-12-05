"""
LLM Service Module
Handles interaction with Groq API for AI responses
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    """Service for LLM API interactions"""
    
    def __init__(self):
        """Initialize Groq client"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def get_ai_response(self, system_prompt, conversation_history, user_message):
      
        try:
            # Build messages array
            messages = [
                {'role': 'system', 'content': system_prompt}
            ]
            
            # Add conversation history
            messages.extend(conversation_history)
            
            # Add current user message
            messages.append({
                'role': 'user',
                'content': user_message
            })
            
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
            )
            
            # Extract response
            response = chat_completion.choices[0].message.content
            
            return response
            
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            raise Exception(f"Failed to get AI response: {str(e)}")
