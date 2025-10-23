import requests
import json
from bs4 import BeautifulSoup
import random

class StoryFinder:
    def __init__(self):
        self.story_sources = {
            'gutenberg': 'https://www.gutenberg.org',
            'creepypasta': 'https://www.creepypasta.com',
            'reddit_nosleep': 'https://www.reddit.com/r/nosleep.json'
        }
        
    def search_stories(self, story_type="ghost"):
        """Search for stories by type"""
        stories = []
        
        if story_type.lower() in ['ghost', 'horror', 'scary']:
            stories.extend(self.get_ghost_stories())
        elif story_type.lower() in ['adventure', 'action']:
            stories.extend(self.get_adventure_stories())
        elif story_type.lower() in ['romance', 'love']:
            stories.extend(self.get_romance_stories())
        else:
            stories.extend(self.get_general_stories())
            
        return stories[:5]  # Return top 5 stories
    
    def get_ghost_stories(self):
        """Get ghost/horror stories from various sources"""
        stories = []
        
        # Built-in ghost stories collection
        builtin_stories = [
            {
                'title': 'The Bhangarh Fort Spirit',
                'content': 'In Rajasthan\'s Bhangarh Fort, visitors report seeing a beautiful woman in white robes walking the ruins at midnight. Local legends say she was Princess Ratnavati, cursed by a tantrik. The Archaeological Survey of India has banned entry after sunset. Those who stayed overnight claim to hear anklets jingling and see glowing eyes in the darkness...',
                'source': 'Indian Legends'
            },
            {
                'title': 'The Crying Woman of Dow Hill',
                'content': 'In Kurseong\'s Dow Hill, students at Victoria Boys School hear a woman crying in the corridors at night. The headless boy of Dow Hill Road appears to travelers, walking beside them before vanishing. Local woodcutters refuse to work alone, claiming they see red eyes watching from the dense forest...',
                'source': 'Indian Ghost Stories'
            },
            {
                'title': 'The Shaniwarwada Fort Ghost',
                'content': 'Every full moon night in Pune\'s Shaniwarwada Fort, locals hear a young boy crying "Kaka mala vachva" (Uncle, save me). This is the spirit of 13-year-old Prince Narayanrao, murdered by his own uncle in 1773. Guards report seeing a small figure running through the ruins, calling for help that never comes...',
                'source': 'Marathi Folklore'
            },
            {
                'title': 'The Haunted Mirror',
                'content': 'Sarah inherited an antique mirror from her grandmother. Every night at 3 AM, she saw a figure standing behind her reflection. The figure grew clearer each night, until one morning, Sarah realized the figure was herself - but older, warning her about something terrible that was about to happen...',
                'source': 'Classic Collection'
            },
            {
                'title': 'The Kuldhara Village Mystery',
                'content': 'The entire village of Kuldhara in Rajasthan was abandoned overnight in 1825. 1,500 people vanished without a trace, leaving behind a curse that no one should ever settle there again. Visitors report strange sounds, moving shadows, and an overwhelming feeling of being watched. Even today, no one dares to stay after dark...',
                'source': 'Rajasthani Legends'
            },
            {
                'title': 'The GP Block Meerut Ghost',
                'content': 'In Meerut\'s GP Block, residents report seeing four friends who died in a car accident still hanging out at their usual spot. They appear normal until you notice they cast no shadows. Local shopkeepers serve them tea, only to find the cups untouched and money turned to leaves by morning...',
                'source': 'Urban Indian Legends'
            }
        ]
        
        stories.extend(builtin_stories)
        
        # Try to fetch from online sources
        try:
            online_stories = self.fetch_online_stories('horror')
            stories.extend(online_stories)
        except:
            pass
            
        return stories
    
    def get_adventure_stories(self):
        """Get adventure stories"""
        stories = [
            {
                'title': 'The Lost Treasure Map',
                'content': 'Captain Morgan discovered an ancient map hidden in a bottle washed ashore. The map led to a mysterious island where pirates had buried their greatest treasure 300 years ago. But the island held secrets darker than gold...',
                'source': 'Adventure Collection'
            },
            {
                'title': 'The Mountain Expedition',
                'content': 'Five friends set out to climb the uncharted Mount Kailash. What started as an adventure became a fight for survival when they discovered the mountain was home to something ancient and powerful...',
                'source': 'Expedition Stories'
            }
        ]
        return stories
    
    def get_romance_stories(self):
        """Get romance stories"""
        stories = [
            {
                'title': 'Letters Across Time',
                'content': 'Emma found old love letters in her new apartment. When she replied to the address, she discovered the letters were from 1945, but somehow, her responses were reaching the original writer...',
                'source': 'Romance Collection'
            },
            {
                'title': 'The Coffee Shop Meeting',
                'content': 'Every morning at 8 AM, Alex and Maya ordered the same coffee at the same shop but never spoke. One day, Maya left a note on his table. That simple gesture changed both their lives forever...',
                'source': 'Modern Romance'
            }
        ]
        return stories
    
    def get_general_stories(self):
        """Get general stories"""
        stories = [
            {
                'title': 'The Time Traveler\'s Diary',
                'content': 'Dr. Chen invented a time machine but could only travel back 24 hours. He used it to prevent small accidents and help people. But one day, he discovered someone else was also changing the timeline...',
                'source': 'Sci-Fi Collection'
            },
            {
                'title': 'The Magic Library',
                'content': 'In the old library, books chose their readers. When 12-year-old Lily touched a mysterious book, she was transported into the story. Now she must complete the tale to return home...',
                'source': 'Fantasy Stories'
            }
        ]
        return stories
    
    def fetch_online_stories(self, category):
        """Fetch stories from online sources"""
        stories = []
        
        # This is a placeholder for actual web scraping
        # In a real implementation, you would scrape from:
        # - Project Gutenberg (public domain stories)
        # - Reddit r/nosleep (with proper API)
        # - Other open-source story collections
        
        return stories
    
    def get_random_story(self):
        """Get a random story from all categories"""
        all_stories = []
        all_stories.extend(self.get_ghost_stories())
        all_stories.extend(self.get_adventure_stories())
        all_stories.extend(self.get_romance_stories())
        all_stories.extend(self.get_general_stories())
        
        return random.choice(all_stories) if all_stories else None
    
    def format_story(self, story):
        """Format story for display"""
        if not story:
            return "No story found."
            
        formatted = f"📖 **{story['title']}**\n"
        formatted += f"Source: {story['source']}\n\n"
        formatted += f"{story['content']}\n"
        
        return formatted
    
    def search_by_keyword(self, keyword):
        """Search stories by keyword"""
        all_stories = []
        all_stories.extend(self.get_ghost_stories())
        all_stories.extend(self.get_adventure_stories())
        all_stories.extend(self.get_romance_stories())
        all_stories.extend(self.get_general_stories())
        
        matching_stories = []
        keyword_lower = keyword.lower()
        
        for story in all_stories:
            if (keyword_lower in story['title'].lower() or 
                keyword_lower in story['content'].lower()):
                matching_stories.append(story)
        
        return matching_stories[:3]  # Return top 3 matches