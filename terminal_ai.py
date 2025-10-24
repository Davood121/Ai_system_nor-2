import ollama
import threading
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from search_engine import MultiSearchEngine
from location_finder import LocationFinder
from weather_service import WeatherService
from memory_system import AdvancedMemorySystem
from translation_service import TranslationService
from story_finder import StoryFinder
from ai_personality import AIPersonality
from advanced_search import AdvancedSearchEngine
from smart_assistant import SmartAssistant
from voice_clone import VoiceCloneSystem


class TerminalAI:
    def __init__(self):
        self.knowledge_file = "ai_knowledge.json"
        self.conversation_context = []
        self.conversation_memory = []  # Store full conversation history
        self.search_engine = MultiSearchEngine()
        self.location_finder = LocationFinder()
        self.weather_service = WeatherService()
        self.memory_system = AdvancedMemorySystem()
        self.translation_service = TranslationService()
        self.story_finder = StoryFinder()
        self.ai_personality = AIPersonality()
        self.advanced_search = AdvancedSearchEngine()
        self.smart_assistant = SmartAssistant()
        self.voice = VoiceCloneSystem()

        # Performance optimizations
        self.executor = ThreadPoolExecutor(max_workers=4)  # Thread pool for async operations
        self.response_cache = {}  # Cache for frequently asked questions
        self.search_cache = {}  # Cache for search results
        self.cache_ttl = 3600  # Cache time-to-live in seconds
        self.last_cache_clear = datetime.now()

        self.load_knowledge()
        

    
    def speak(self, text, language=None):
        """Speak with your voice style (async)"""
        # Run in background thread to avoid blocking
        self.executor.submit(self.voice.speak_like_you, text)

    def _clear_old_cache(self):
        """Clear cache if TTL expired"""
        now = datetime.now()
        if (now - self.last_cache_clear).total_seconds() > self.cache_ttl:
            self.response_cache.clear()
            self.search_cache.clear()
            self.last_cache_clear = now

    def search_web(self, query):
        """Use smart search algorithm with clean query (cached)"""
        # Extract just the main question, not the full context
        clean_query = query.split("Current question:")[-1].strip() if "Current question:" in query else query

        # Check cache first
        cache_key = clean_query.lower()
        if cache_key in self.search_cache:
            return self.search_cache[cache_key]

        # Search in background and cache result
        result = self.search_engine.smart_search(clean_query)
        self.search_cache[cache_key] = result
        return result
    

    
    def get_ai_response(self, prompt, context="", show_thinking=False):
        """Get AI response (optimized - removed double call)"""
        try:
            # Check cache first
            cache_key = f"{prompt}:{context}".lower()[:100]
            if cache_key in self.response_cache:
                return self.response_cache[cache_key]

            # System prompt for consistent behavior
            system_prompt = "You are a helpful AI assistant. Respond naturally and conversationally. For greetings like 'hello', respond with a simple greeting. For questions, provide clear and accurate answers."

            if context:
                full_prompt = f"Based on this search data: {context}\n\nQuestion: {prompt}\n\nProvide a helpful response in 2-3 sentences."
            else:
                full_prompt = prompt

            # Single call instead of two
            response = ollama.chat(model='llama3.2', messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': full_prompt}
            ], stream=False)

            result = response['message']['content']

            # Cache the response
            self.response_cache[cache_key] = result

            return result
        except Exception as e:
            print(f"AI Error: {e}")
            return "AI model not available"
    
    def summarize(self, text):
        """Summarize text"""
        prompt = f"Summarize this in 2-3 sentences: {text}"
        return self.get_ai_response(prompt)
    
    def save_to_memory(self, query, response):
        """Save conversation to advanced memory system"""
        self.memory_system.add_conversation(query, response)
        
        # Also save to simple memory for backward compatibility
        self.conversation_memory.append({
            'question': query,
            'answer': response,
            'timestamp': datetime.now().isoformat()
        })
        
        if len(self.conversation_memory) > 10:
            self.conversation_memory = self.conversation_memory[-10:]
    
    def get_recent_memory(self):
        """Get intelligent context from advanced memory"""
        return self.memory_system.get_context_for_query("general")
    
    def resolve_pronouns(self, query):
        """Resolve pronouns using conversation context"""
        context = self.memory_system.get_context_for_query(query)
        if not context:
            return query
            
        # Simple pronoun resolution
        pronouns = {'it', 'that', 'this', 'they', 'them'}
        query_words = query.lower().split()
        
        if any(pronoun in query_words for pronoun in pronouns):
            # Add context to help AI understand pronouns
            return f"Context: {context} | Question: {query}"
        
        return query
    
    def load_knowledge(self):
        """Load saved knowledge"""
        try:
            with open(self.knowledge_file, 'r') as f:
                self.knowledge = json.load(f)
        except:
            self.knowledge = {}
    
    def save_knowledge(self, query, answer):
        """Save new knowledge"""
        self.knowledge[query.lower()] = {
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        }
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
    
    def needs_search(self, query):
        """Smart search decision - avoid over-searching"""
        query_lower = query.lower()
        
        # Don't search for basic conversational responses
        skip_search = [
            'hello', 'hi', 'thanks', 'thank you', 'bye', 'goodbye',
            'how are you', 'what can you do', 'who are you', 'good morning',
            'good evening', 'nice', 'great', 'okay', 'yes', 'no', 'sure',
            'alright', 'fine', 'cool', 'awesome', 'perfect'
        ]
        
        # Don't search for basic knowledge questions
        basic_knowledge = [
            'what is love', 'what is life', 'what is happiness', 'what is time',
            'what is water', 'what is fire', 'what is earth', 'what is air',
            'what is human', 'what is animal', 'what is plant', 'what is tree',
            'what is sun', 'what is moon', 'what is oxygen', 'what is carbon',
            'what is house', 'what is home', 'what is building', 'what is room'
        ]
        
        # Don't search for basic anatomy/science facts
        basic_science = [
            'bones in human', 'bones in body', 'human bones', 'total bones'
        ]
        
        # Don't search for general concepts or philosophical questions
        general_concepts = [
            'functions within', 'evolved over time', 'technological advancement',
            'societal values', 'how they have changed', 'what do you think',
            'your opinion', 'explain to me', 'tell me more', 'can you explain',
            'search story', 'story search'
        ]
        
        # Skip search for basic responses
        if any(skip in query_lower for skip in skip_search):
            return False
            
        if any(basic in query_lower for basic in basic_knowledge):
            return False
            
        if any(science in query_lower for science in basic_science):
            return False
            
        if any(concept in query_lower for concept in general_concepts):
            return False
        
        # Only search for specific information needs
        search_triggers = [
            # Current/time-sensitive info
            'current', 'latest', 'recent', 'today', 'now', '2024', '2025',
            # Specific data requests
            'price', 'cost', 'statistics', 'population', 'news', 'rate', 'crime',
            # Weather and location
            'weather', 'temperature', 'forecast',
            # Specific factual queries
            'best colleges', 'best hospitals', 'best restaurants',
            'deaths in', 'mortality in', 'happened in', 'crime rate'
        ]
        
        # Search for specific patterns
        search_patterns = [
            'tell me about current', 'latest information about', 'recent details about',
            'what happened recently', 'how many people', 'current statistics',
            'best in 2024', 'best in 2025', 'near me', 'in this pin code'
        ]
        
        # Don't search for conversational requests
        conversational = [
            'can you ask me', 'ask me a question', 'quiz me', 'test me',
            'can you help', 'help me with', 'i want to', 'let me',
            'what do you think', 'your thoughts', 'your opinion'
        ]
        
        if any(conv in query_lower for conv in conversational):
            return False
        
        # Don't search for simple "what is" questions about basic things
        if query_lower.startswith('what is ') and len(query.split()) <= 4:
            return False
        
        # Don't search for "how" questions about general concepts
        if query_lower.startswith('how ') and any(word in query_lower for word in ['evolved', 'changed', 'developed', 'work', 'function']):
            return False
        
        return (any(trigger in query_lower for trigger in search_triggers) or 
                any(pattern in query_lower for pattern in search_patterns))
    
    def extract_pincode_from_query(self, query):
        """Extract pincode from query"""
        import re
        pincode_match = re.search(r'\b\d{6}\b', query)
        return pincode_match.group() if pincode_match else None
    
    def enhance_query_with_location(self, query):
        """Enhance query with location information from pincode"""
        pincode = self.extract_pincode_from_query(query)
        if pincode:
            location_info = self.location_finder.find_location_by_pincode(pincode)
            if location_info:
                # Create better search query for colleges/local services
                base_query = query.replace(f"pin code, {pincode}", "").replace(f"pincode {pincode}", "")
                base_query = base_query.replace("near me", "").strip()
                
                # Enhanced query with specific location terms
                enhanced_query = f"{base_query} in {location_info['district']} {location_info['state']} near {location_info['area']}"
                return enhanced_query, location_info
        return query, None
    
    def smart_response(self, query):
        """Location-aware smart response (optimized)"""
        # Only search when actually needed
        if self.needs_search(query):
            print("🔍 Searching for latest information...")

            # Enhance query with location if pincode found
            enhanced_query, location_info = self.enhance_query_with_location(query)

            # Debug: show enhanced query
            if location_info:
                print(f"📍 Searching for: {enhanced_query}")

            # Use enhanced query for search (cached)
            search_results = self.search_web(enhanced_query)
            all_context = search_results[:1200]

            # Enhanced AI prompt with conversation memory
            enhanced_prompt = f"Using ONLY the latest search results provided, give current 2025 information about: {query}. Do not use outdated data from 2020-2021. Focus on recent statistics and current trends."

            # Add intelligent conversation context
            context = self.memory_system.get_context_for_query(query)
            if context:
                enhanced_prompt += f"\nConversation context: {context}"

            # Check user preferences
            location_pref = self.memory_system.get_preference('location')
            if location_pref and 'near me' in query.lower():
                enhanced_prompt += f"\nUser location preference: {location_pref}"

            if location_info:
                enhanced_prompt += f"\nLocation context: {location_info['area']}, {location_info['district']}, {location_info['state']}"

            # Get response without thinking process (faster)
            response = self.get_ai_response(enhanced_prompt, all_context, show_thinking=False)

            # Translate response if needed (async)
            current_lang = self.translation_service.current_language
            if current_lang != 'english':
                response = self.translation_service.translate_response(response, current_lang)

            # Save to memory (async)
            self.executor.submit(self.save_to_memory, query, response)
            self.executor.submit(self.save_knowledge, query, response)
            self.conversation_context.append(f"Q: {query} A: {response}")
            return response
        else:
            # Resolve pronouns and add context
            resolved_query = self.resolve_pronouns(query)
            context = self.memory_system.get_context_for_query(query)

            context_prompt = resolved_query
            if context:
                context_prompt = f"Conversation context: {context}\nCurrent question: {resolved_query}"

            # Get response without thinking process (faster)
            response = self.get_ai_response(context_prompt, show_thinking=False)

            # Translate response if needed (async)
            current_lang = self.translation_service.current_language
            if current_lang != 'english':
                response = self.translation_service.translate_response(response, current_lang)

            # Save to memory (async)
            self.executor.submit(self.save_to_memory, query, response)
            self.conversation_context.append(f"Q: {query} A: {response}")
            return response

def main():
    ai = TerminalAI()
    
    print("🤖 Advanced AI Assistant System")
    print("=" * 50)
    
    print("\n📝 BASIC COMMANDS:")
    print("  chat                    - Start conversation")
    print("  quit                    - Exit application")
    print("  voice test              - Test voice cloning")
    print("  voice sample            - Show voice sample used")
    print("  human effects on/off    - Toggle breathing & pauses")
    
    print("\n🔍 SEARCH & INFO:")
    print("  search [query]          - Web search")
    print("  smart search [query]    - AI-powered search")
    print("  wiki [topic]            - Wikipedia search")
    print("  weather [location]      - Weather info")
    print("  location [pincode]      - Location lookup")
    
    print("\n🌍 LANGUAGES:")
    print("  english/hindi/telugu    - Switch language")
    print("  translate [text] to [lang] - Translate text")
    
    print("\n📚 STORIES & FUN:")
    print("  story [ghost/adventure] - Get stories")
    print("  random story            - Random story")
    print("  ask me a question       - AI asks you")
    print("  quiz me                 - Interactive quiz")
    
    print("\n🧠 SMART FEATURES:")
    print("  personality mode        - Activate personality")
    print("  remind [msg] at [time]  - Set reminders")
    print("  habit [name]            - Track habits")
    print("  goal [name] [target]    - Set goals")
    print("  daily summary           - Progress overview")
    print("  suggestions             - Get personalized tips")
    
    print("\n💾 MEMORY & LEARNING:")
    print("  memory                  - View statistics")
    print("  learn [key] [value]     - Teach preferences")
    print("  export                  - Export conversations")
    print("  search memory [term]    - Search history")
    
    print("\n" + "=" * 50)
    
    print("🧠 Consciousness: Active | 🤖 Personality: Ready | 🎤 Voice Clone Active")
    print("\nType any command or just start chatting! 💬")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
                
            elif user_input.lower() == 'voice test':
                ai.voice.test_voice()
                
            elif user_input.lower() == 'voice sample':
                if ai.voice.sample_voice:
                    print(f"Voice sample: {os.path.basename(ai.voice.sample_voice)}")
                else:
                    print("No voice sample found")
                    
            elif user_input.lower() == 'human effects on':
                ai.voice.human_effects = True
                print("🎤 Human voice effects enabled (breathing, pauses, throat clearing)")
                
            elif user_input.lower() == 'human effects off':
                ai.voice.human_effects = False
                print("🎤 Human voice effects disabled (clean speech only)")
            

                    
            elif user_input.lower().startswith('language ') or user_input.lower() in ['telugu', 'hindi', 'english']:
                if user_input.lower() in ['telugu', 'hindi', 'english']:
                    lang = user_input.lower()
                else:
                    lang = user_input[9:].strip().lower()
                    
                if ai.translation_service.set_language(lang):
                    print(f"Language set to {lang.title()}")
                    ai.speak(f"Language changed to {lang}", lang)
                else:
                    print("Supported languages: English, Hindi, Telugu")
                    
            elif user_input.lower() == 'languages':
                current = ai.translation_service.current_language
                print(f"\nSupported Languages:")
                print(f"1. English {'(current)' if current == 'english' else ''}")
                print(f"2. Hindi {'(current)' if current == 'hindi' else ''}")
                print(f"3. Telugu {'(current)' if current == 'telugu' else ''}")
                print(f"\nUsage: Type 'english', 'hindi', or 'telugu' to switch")
                ai.speak(f"Current language is {current}. You can switch to English, Hindi, or Telugu.")
                    
            elif user_input.lower().startswith('translate '):
                text_to_translate = user_input[10:]
                parts = text_to_translate.split(' to ')
                if len(parts) == 2:
                    text, target_lang = parts
                    translation = ai.translation_service.translate_text(text.strip(), target_lang.strip())
                    print(f"\nTranslation: {translation}")
                    ai.speak(translation, target_lang.strip())
                else:
                    print("Usage: translate [text] to [language]")
                    
            elif user_input.lower() == 'memory':
                stats = ai.memory_system.get_memory_stats()
                print(f"\n📊 Memory Statistics:")
                print(f"Total conversations: {stats['total_conversations']}")
                print(f"Topics discussed: {stats['topics_discussed']}")
                print(f"Preferences learned: {stats['preferences_learned']}")
                print(f"Most discussed: {stats['most_discussed_topic']}")
                
            elif user_input.lower().startswith('search memory '):
                search_term = user_input[14:]
                results = ai.memory_system.search_conversations(search_term)
                print(f"\n🔍 Found {len(results)} conversations about '{search_term}':")
                for conv in results[-3:]:
                    print(f"- {conv['query'][:60]}...")
                    
            elif user_input.lower().startswith('topic '):
                topic = user_input[6:]
                summary = ai.memory_system.get_topic_summary(topic)
                print(f"\n📋 {summary}")
                
            elif user_input.lower() == 'export':
                filename = ai.memory_system.export_conversations()
                print(f"\n💾 Conversations exported to: {filename}")
                ai.speak(f"Conversations exported to {filename}")
                
            elif user_input.lower().startswith('learn '):
                # Learn user preferences: "learn location Mumbai"
                parts = user_input[6:].split(' ', 1)
                if len(parts) == 2:
                    key, value = parts
                    ai.memory_system.learn_preference(key, value)
                    print(f"✅ Learned: {key} = {value}")
                    ai.speak(f"I'll remember that your {key} is {value}")
                    
            elif user_input.lower().startswith('correct '):
                # Learn from corrections: "correct that was wrong, actual answer is..."
                correction = user_input[8:]
                if ai.conversation_memory:
                    last_response = ai.conversation_memory[-1]['answer']
                    ai.memory_system.add_correction(last_response, correction)
                    print("✅ Thanks for the correction! I'll remember that.")
                    ai.speak("Thanks for the correction, I'll remember that")
                    
            elif user_input.lower() == 'clear memory':
                ai.memory_system = AdvancedMemorySystem()  # Reset
                ai.conversation_memory = []
                ai.conversation_context = []
                print("🗑️ All memory cleared.")
                ai.speak("All memory cleared")
                
            elif user_input.lower().startswith('search '):
                query = user_input[7:]
                print(f"\nSearching: {query}")
                results = ai.search_web(query)
                
                # Summarize search results
                summary = ai.get_ai_response(f"Summarize and explain: {query}", results[:500])
                print(f"\nSummary:\n{summary}")
                ai.speak(summary)
                    
            elif user_input.lower().startswith('wiki '):
                query = user_input[5:]
                print(f"\nWikipedia: {query}")
                result = ai.search_wiki(query)
                
                # Summarize wiki result
                summary = ai.get_ai_response(f"Explain this simply: {query}", result)
                print(f"\nExplanation:\n{summary}")
                ai.speak(summary)
                    
            elif user_input.lower().startswith('summarize '):
                text = user_input[10:]
                print("\nSummarizing...")
                summary = ai.summarize(text)
                print(summary)
                ai.speak(summary)
                
            elif user_input.lower().startswith('weather '):
                location = user_input[8:].strip()
                print(f"\nGetting weather for: {location}")
                
                # Check if it's a pincode
                if location.isdigit() and len(location) == 6:
                    weather_data = ai.weather_service.get_weather_by_pincode(location, ai.location_finder)
                else:
                    weather_data = ai.weather_service.get_weather_by_location(location)
                
                response = ai.weather_service.format_weather_response(weather_data)
                print(response)
                
                # Speak weather info
                if weather_data:
                    speech_text = f"Weather in {weather_data['location']}: {weather_data['temperature']} degrees, {weather_data['condition']}"
                    ai.speak(speech_text)
                else:
                    ai.speak("Weather information not available")
                    
            elif user_input.lower().startswith('forecast '):
                location = user_input[9:].strip()
                print(f"\nGetting forecast for: {location}")
                
                forecast = ai.weather_service.get_forecast(location)
                print(f"\n🌦️ Forecast:\n{forecast}")
                ai.speak(f"Weather forecast for {location}: {forecast[:100]}")
                
            elif user_input.lower().startswith('location ') or user_input.lower().startswith('pincode '):
                pincode = user_input.split()[-1]  # Get last word as pincode
                print(f"\nFinding location for pincode: {pincode}")
                
                location_info = ai.location_finder.find_location_by_pincode(pincode)
                response = ai.location_finder.format_location_response(location_info)
                
                print(response)
                
                # Speak location details
                if location_info:
                    speech_text = f"Location found. {location_info['area']} in {location_info['district']} district, {location_info['state']} state."
                    ai.speak(speech_text)
                else:
                    ai.speak("Location not found for this pincode")
                    
            elif 'ask me' in user_input.lower() or 'quiz me' in user_input.lower():
                # AI asks user a question
                questions = [
                    "What's your favorite color?",
                    "Which city are you from?",
                    "What's your hobby?",
                    "What's your favorite food?",
                    "What do you like to do in your free time?",
                    "What's your favorite movie?",
                    "What subject interests you most?",
                    "What's your dream destination?"
                ]
                
                import random
                question = random.choice(questions)
                
                print("\nAI:")
                print(f"Here's a question for you: {question}")
                ai.speak(f"Here's a question for you: {question}")
                
                # Wait for user's answer
                print("\n[Waiting for your answer...]")
                
            elif user_input.lower().startswith('story '):
                story_type = user_input[6:].strip()
                print(f"\nFinding {story_type} stories...")
                
                stories = ai.story_finder.search_stories(story_type)
                if stories:
                    story = stories[0]  # Get first story
                    formatted_story = ai.story_finder.format_story(story)
                    print(f"\n{formatted_story}")
                    
                    # Speak story title and beginning
                    speech_text = f"Here's a {story_type} story: {story['title']}. {story['content'][:100]}..."
                    ai.speak(speech_text)
                else:
                    print(f"No {story_type} stories found.")
                    ai.speak(f"No {story_type} stories found")
                    
            elif user_input.lower() == 'random story':
                print("\nFinding a random story...")
                story = ai.story_finder.get_random_story()
                
                if story:
                    formatted_story = ai.story_finder.format_story(story)
                    print(f"\n{formatted_story}")
                    
                    speech_text = f"Here's a random story: {story['title']}. {story['content'][:100]}..."
                    ai.speak(speech_text)
                else:
                    print("No stories available.")
                    ai.speak("No stories available")
                    
            elif user_input.lower() == 'search story' or user_input.lower().startswith('search story '):
                if user_input.lower() == 'search story':
                    # Show all available stories
                    print("\nAvailable story types:")
                    print("- ghost/horror - Scary and supernatural stories")
                    print("- adventure - Action and exploration stories")
                    print("- romance - Love and relationship stories")
                    print("- general - Sci-fi and fantasy stories")
                    print("\nTry: 'story ghost' or 'random story'")
                    ai.speak("I have ghost stories, adventure stories, romance stories, and general stories available")
                else:
                    keyword = user_input[13:].strip()
                    print(f"\nSearching stories with keyword: {keyword}")
                    
                    stories = ai.story_finder.search_by_keyword(keyword)
                    if stories:
                        print(f"\nFound {len(stories)} stories:")
                        for i, story in enumerate(stories, 1):
                            print(f"\n{i}. {story['title']} ({story['source']})")
                            print(f"   {story['content'][:100]}...")
                        
                        ai.speak(f"Found {len(stories)} stories matching {keyword}")
                    else:
                        print(f"No stories found with keyword: {keyword}")
                        ai.speak(f"No stories found with keyword {keyword}")
                        

                    
            else:
                # Handle language commands first
                if user_input.lower() in ['telugu', 'hindi', 'english', 'languages']:
                    continue  # Already handled above
                
                # Detect input language and translate if needed
                input_lang = ai.translation_service.detect_language(user_input)
                if input_lang != 'english':
                    translated_input = ai.translation_service.translate_text(user_input, 'english')
                    print(f"Translated: {translated_input}")
                    response = ai.smart_response(translated_input)
                else:
                    response = ai.smart_response(user_input)
                
                # Display in English, but speak in selected language
                current_lang = ai.translation_service.current_language
                
                print("\nAI:")
                print(response)  # Always display in English
                
                if current_lang != 'english':
                    print(f"[Speaking in {current_lang}]")
                
                ai.speak(response)  # This will handle translation for voice only
                
                # Manual health check command
                if user_input.lower() == 'health':
                    health_status = ai.healer.monitor_and_heal()
                    status_msg = "System healthy" if health_status else "Issues detected and fixed"
                    print(status_msg)
                    ai.speak(status_msg)
                    
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()