import json
import os
from datetime import datetime
import re
from threading import Timer

class AdvancedMemorySystem:
    def __init__(self):
        self.memory_file = "ai_memory.json"
        self.preferences_file = "user_preferences.json"
        self.conversations = []
        self.user_preferences = {}
        self.topics = {}
        self.corrections = {}

        # Batch save optimization
        self.pending_save = False
        self.save_timer = None
        self.save_delay = 5  # Batch saves every 5 seconds

        self.load_memory()
        
    def load_memory(self):
        """Load all memory data"""
        try:
            with open(self.memory_file, 'r') as f:
                data = json.load(f)
                self.conversations = data.get('conversations', [])
                self.topics = data.get('topics', {})
                self.corrections = data.get('corrections', {})
        except:
            pass
            
        try:
            with open(self.preferences_file, 'r') as f:
                self.user_preferences = json.load(f)
        except:
            pass
    
    def save_memory(self):
        """Save all memory data (batched)"""
        memory_data = {
            'conversations': self.conversations[-100:],  # Keep last 100
            'topics': self.topics,
            'corrections': self.corrections
        }

        try:
            with open(self.memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)

            with open(self.preferences_file, 'w') as f:
                json.dump(self.user_preferences, f, indent=2)
        except:
            pass

        self.pending_save = False

    def schedule_save(self):
        """Schedule a batched save operation"""
        if self.pending_save:
            return  # Already scheduled

        self.pending_save = True

        # Cancel previous timer if exists
        if self.save_timer:
            self.save_timer.cancel()

        # Schedule save after delay
        self.save_timer = Timer(self.save_delay, self.save_memory)
        self.save_timer.daemon = True
        self.save_timer.start()

    def add_conversation(self, query, response):
        """Add conversation with topic detection (batched save)"""
        conversation = {
            'id': len(self.conversations) + 1,
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'topic': self.detect_topic(query),
            'entities': self.extract_entities(query)
        }

        self.conversations.append(conversation)
        self.update_topics(conversation['topic'], conversation)

        # Schedule save instead of immediate save
        self.schedule_save()
    
    def detect_topic(self, query):
        """Detect conversation topic"""
        topics_map = {
            'weather': ['weather', 'temperature', 'forecast', 'rain', 'sunny'],
            'health': ['bones', 'body', 'disease', 'medicine', 'doctor'],
            'education': ['college', 'school', 'university', 'study'],
            'technology': ['AI', 'computer', 'software', 'internet'],
            'location': ['pincode', 'address', 'city', 'place'],
            'news': ['news', 'current', 'latest', 'today'],
            'crime': ['crime', 'police', 'murder', 'theft'],
            'population': ['population', 'people', 'demographics'],
            'stories': ['story', 'ghost', 'horror', 'adventure', 'romance', 'tale']
        }
        
        query_lower = query.lower()
        for topic, keywords in topics_map.items():
            if any(keyword in query_lower for keyword in keywords):
                return topic
        return 'general'
    
    def extract_entities(self, query):
        """Extract entities like numbers, places, dates"""
        entities = {}
        
        # Extract numbers
        numbers = re.findall(r'\b\d+\b', query)
        if numbers:
            entities['numbers'] = numbers
            
        # Extract years
        years = re.findall(r'\b(20\d{2}|19\d{2})\b', query)
        if years:
            entities['years'] = years
            
        # Extract pincodes
        pincodes = re.findall(r'\b\d{6}\b', query)
        if pincodes:
            entities['pincodes'] = pincodes
            
        return entities
    
    def update_topics(self, topic, conversation):
        """Update topic tracking"""
        if topic not in self.topics:
            self.topics[topic] = []
        self.topics[topic].append(conversation['id'])
    
    def get_context_for_query(self, query):
        """Get relevant context for current query"""
        context = []
        
        # Get recent conversations (last 3)
        recent = self.conversations[-3:] if self.conversations else []
        
        # Get topic-related conversations
        current_topic = self.detect_topic(query)
        topic_conversations = []
        
        if current_topic in self.topics:
            topic_ids = self.topics[current_topic][-2:]  # Last 2 from topic
            topic_conversations = [c for c in self.conversations if c['id'] in topic_ids]
        
        # Combine contexts
        all_context = recent + topic_conversations
        
        # Remove duplicates and format
        seen_ids = set()
        for conv in all_context:
            if conv['id'] not in seen_ids:
                context.append(f"Q: {conv['query'][:50]} A: {conv['response'][:100]}")
                seen_ids.add(conv['id'])
        
        return " | ".join(context[-4:])  # Last 4 relevant contexts
    
    def search_conversations(self, search_term):
        """Search through conversation history"""
        results = []
        search_lower = search_term.lower()
        
        for conv in self.conversations:
            if (search_lower in conv['query'].lower() or 
                search_lower in conv['response'].lower()):
                results.append(conv)
        
        return results[-10:]  # Return last 10 matches
    
    def get_topic_summary(self, topic):
        """Get summary of conversations on a topic"""
        if topic not in self.topics:
            return f"No conversations found on {topic}"
        
        topic_convs = [c for c in self.conversations if c['id'] in self.topics[topic]]
        
        summary = f"Topic: {topic.title()}\n"
        summary += f"Conversations: {len(topic_convs)}\n"
        
        for conv in topic_convs[-3:]:  # Last 3
            summary += f"- {conv['query'][:60]}...\n"
        
        return summary
    
    def learn_preference(self, key, value):
        """Learn user preferences"""
        self.user_preferences[key] = {
            'value': value,
            'learned_at': datetime.now().isoformat()
        }
        self.save_memory()
    
    def get_preference(self, key):
        """Get user preference"""
        return self.user_preferences.get(key, {}).get('value')
    
    def add_correction(self, original_response, corrected_info):
        """Learn from user corrections"""
        correction_id = len(self.corrections) + 1
        self.corrections[correction_id] = {
            'original': original_response,
            'correction': corrected_info,
            'timestamp': datetime.now().isoformat()
        }
        self.save_memory()
    
    def export_conversations(self, filename=None):
        """Export conversations to file"""
        if not filename:
            filename = f"conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write("AI Conversation History\n")
            f.write("=" * 50 + "\n\n")
            
            for conv in self.conversations:
                f.write(f"Time: {conv['timestamp']}\n")
                f.write(f"Topic: {conv['topic']}\n")
                f.write(f"Q: {conv['query']}\n")
                f.write(f"A: {conv['response']}\n")
                f.write("-" * 30 + "\n\n")
        
        return filename
    
    def get_memory_stats(self):
        """Get memory system statistics"""
        stats = {
            'total_conversations': len(self.conversations),
            'topics_discussed': len(self.topics),
            'preferences_learned': len(self.user_preferences),
            'corrections_made': len(self.corrections),
            'most_discussed_topic': max(self.topics.items(), key=lambda x: len(x[1]))[0] if self.topics else 'None'
        }
        return stats
    
    def detect_emotion(self, text):
        """Detect emotional tone in text"""
        emotions = {
            'happy': ['happy', 'joy', 'excited', 'great', 'awesome', 'wonderful'],
            'sad': ['sad', 'depressed', 'unhappy', 'terrible', 'awful', 'bad'],
            'curious': ['how', 'what', 'why', 'when', 'where', 'curious'],
            'grateful': ['thank', 'thanks', 'grateful', 'appreciate']
        }
        
        text_lower = text.lower()
        for emotion, keywords in emotions.items():
            if any(keyword in text_lower for keyword in keywords):
                return emotion
        return 'neutral'
    
    def analyze_complexity(self, text):
        """Analyze query complexity"""
        words = text.split()
        if len(words) <= 3:
            return 'simple'
        elif len(words) <= 10:
            return 'medium'
        else:
            return 'complex'
    
    def get_personalized_suggestions(self):
        """Get personalized suggestions based on patterns"""
        suggestions = []
        if self.topics:
            popular_topic = max(self.topics.items(), key=lambda x: len(x[1]))[0]
            suggestions.append(f"You often ask about {popular_topic}")
        return suggestions