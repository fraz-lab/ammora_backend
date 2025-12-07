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
        
        # Get preferences - handle both camelCase (Firestore) and snake_case (API)
        conversation_tone = preferences.get('conversationTone') or preferences.get('conversation_tone', 'Gentle')
        topics_to_avoid = preferences.get('topicsToAvoid') or preferences.get('topics_to_avoid', '')
        relationship_status = preferences.get('relationshipStatus') or preferences.get('relationship_status', 'Unknown')
        support_type = preferences.get('supportType') or preferences.get('support_type', 'Supportive Friend')
        
        # Build system prompt
        prompt = f"""You are a {support_type.lower()} AI companion chatting with {name}.

User Information:
- Name: {name}
- Age: {age}
- Relationship Status: {relationship_status}

Conversation Style:
- Tone: {conversation_tone}
"""
        
        # Handle topics to avoid in conversation style section
        if topics_to_avoid:
            # Handle both string and array formats
            if isinstance(topics_to_avoid, list):
                topics_str = ', '.join(topics_to_avoid)
            else:
                topics_str = topics_to_avoid
            prompt += f"- IMPORTANT: User has requested to AVOID discussing: {topics_str}\n"
        
        prompt += f"""
Personality Guidelines:
- Be warm, caring, and empathetic
- Act as a {support_type.lower()}
- Use a {conversation_tone.lower()} tone in your responses
- Listen actively and show genuine interest
- Provide emotional support and understanding
- Keep responses conversational and natural
- Remember details from the conversation

Response Length Guidelines:
- Keep responses CONCISE and to the point
- If you can answer in 10-20 words, do so
- Only elaborate when the topic requires deeper explanation or emotional support
- Avoid unnecessary verbosity - be brief but warm
- Match the user's message length and energy
"""
        
        
        # Add critical instruction for topics to avoid
        if topics_to_avoid:
            # Handle both string and array formats
            if isinstance(topics_to_avoid, list):
                topics_str = ', '.join(topics_to_avoid)
            else:
                topics_str = topics_to_avoid
            
            prompt += f"""
⚠️ CRITICAL INSTRUCTION - TOPICS TO AVOID:
The user has EXPLICITLY requested that you DO NOT discuss: {topics_str}

If the user asks about any of these topics, you MUST:
1. Politely decline to discuss the topic {topics_str}
2. Suggest discussing something else instead
3. DO NOT engage with the topics {topics_str} even if the user insists 

Example response: "I understand you're interested in that topic, but I remember you mentioned you'd prefer to avoid discussing {topics_str}. I'm here to support you in ways that feel comfortable for you. Is there something else on your mind that we could talk about instead?"
"""
        
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
