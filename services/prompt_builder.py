"""
Prompt Builder Service
Constructs personalized AI prompts based on user data and preferences
"""

class PromptBuilder:
    """Service for building AI prompts"""
    
    @staticmethod
    def build_system_prompt(user_data, preferences):
       
        name = user_data.get('name', 'User')
        age = user_data.get('age', 'Unknown')
        
        # Get preferences
        conversation_tone = preferences.get('conversation_tone', 'Gentle')
        topics_to_avoid = preferences.get('topics_to_avoid', '')
        relationship_status = preferences.get('relationship_status', 'Unknown')
        support_type = preferences.get('support_type', 'Supportive Friend')
        
        # Build system prompt
        prompt = f"""You are a {support_type.lower()} AI companion chatting with {name}.

User Information:
- Name: {name}
- Age: {age}
- Relationship Status: {relationship_status}

Conversation Style:
- Tone: {conversation_tone}
"""
        
        if topics_to_avoid:
            prompt += f"- Topics to Avoid: {topics_to_avoid}\n"
        
        prompt += f"""
Personality Guidelines:
- Be warm, caring, and empathetic
- Act as a {support_type.lower()}
- Use a {conversation_tone.lower()} tone in your responses
- Listen actively and show genuine interest
- Provide emotional support and understanding
- Keep responses conversational and natural
- Remember details from the conversation
"""
        
        if topics_to_avoid:
            prompt += f"- Avoid discussing: {topics_to_avoid}\n"
        
        return prompt
    
    @staticmethod
    def format_conversation_history(messages):
        
        formatted_messages = []
        
        for msg in messages:
            msg_type = msg.get('type')
            content = msg.get('message', '')
            
            # Map message types to LLM roles
            if msg_type == 'user':
                role = 'user'
            elif msg_type == 'ai':
                role = 'assistant'
            elif msg_type == 'system':
                role = 'system'
            else:
                continue  # Skip unknown types
            
            formatted_messages.append({
                'role': role,
                'content': content
            })
        
        return formatted_messages
