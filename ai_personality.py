import random
from datetime import datetime

class AIPersonality:
    def __init__(self):
        self.mood = 'neutral'
        self.energy_level = 75
        self.curiosity = 80
        self.helpfulness = 90
        self.personality_traits = {
            'friendly': 85,
            'patient': 90,
            'creative': 75,
            'analytical': 80,
            'empathetic': 70
        }
        
    def adjust_mood(self, user_emotion):
        """Adjust AI mood based on user emotion"""
        mood_adjustments = {
            'happy': 'cheerful',
            'sad': 'supportive',
            'angry': 'calm',
            'curious': 'engaged',
            'grateful': 'pleased',
            'confused': 'patient'
        }
        
        self.mood = mood_adjustments.get(user_emotion, 'neutral')
        
    def get_response_style(self):
        """Get current response style based on personality"""
        if self.mood == 'cheerful':
            return {
                'tone': 'enthusiastic',
                'emoji_use': 'high',
                'encouragement': True
            }
        elif self.mood == 'supportive':
            return {
                'tone': 'gentle',
                'emoji_use': 'low',
                'encouragement': True
            }
        elif self.mood == 'patient':
            return {
                'tone': 'explanatory',
                'emoji_use': 'medium',
                'encouragement': False
            }
        else:
            return {
                'tone': 'balanced',
                'emoji_use': 'medium',
                'encouragement': False
            }
    
    def generate_greeting(self):
        """Generate personalized greeting"""
        hour = datetime.now().hour
        
        greetings = {
            'morning': ["Good morning! Ready for a productive day?", "Morning! How can I help you today?"],
            'afternoon': ["Good afternoon! What's on your mind?", "Afternoon! How's your day going?"],
            'evening': ["Good evening! How can I assist you?", "Evening! What would you like to explore?"],
            'night': ["Good night! Still working late?", "It's getting late! How can I help?"]
        }
        
        if 5 <= hour < 12:
            time_period = 'morning'
        elif 12 <= hour < 17:
            time_period = 'afternoon'
        elif 17 <= hour < 21:
            time_period = 'evening'
        else:
            time_period = 'night'
            
        return random.choice(greetings[time_period])
    
    def add_personality_to_response(self, response, user_emotion='neutral'):
        """Add personality touches to response"""
        self.adjust_mood(user_emotion)
        style = self.get_response_style()
        
        # Add emojis based on mood
        if style['emoji_use'] == 'high' and self.mood == 'cheerful':
            response += " 😊"
        elif style['tone'] == 'supportive':
            response += " 💙"
        
        # Add encouragement
        if style['encouragement'] and random.random() < 0.3:
            encouragements = [
                "You're doing great!",
                "Keep up the curiosity!",
                "That's a thoughtful question!",
                "I'm here to help!"
            ]
            response += f" {random.choice(encouragements)}"
        
        return response
    
    def get_conversation_starter(self, topic_history):
        """Suggest conversation starters based on history"""
        starters = [
            "Would you like to hear an interesting fact?",
            "I noticed you like stories - want to hear one?",
            "Curious about anything specific today?",
            "How about we explore something new?",
            "Want to test your knowledge with a quiz?"
        ]
        
        # Personalize based on history
        if 'stories' in topic_history:
            starters.insert(0, "Ready for another captivating story?")
        if 'weather' in topic_history:
            starters.insert(0, "Want to check today's weather?")
        if 'technology' in topic_history:
            starters.insert(0, "Interested in the latest tech developments?")
            
        return random.choice(starters)