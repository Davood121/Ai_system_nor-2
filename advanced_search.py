import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

class AdvancedSearchEngine:
    def __init__(self):
        self.search_history = []
        self.cached_results = {}
        self.search_patterns = {}
        
    def intelligent_search(self, query, search_type='auto'):
        """AI-powered search with context awareness"""
        # Analyze query intent
        intent = self.analyze_search_intent(query)
        
        # Choose best search strategy
        if intent == 'factual':
            return self.factual_search(query)
        elif intent == 'current_events':
            return self.news_search(query)
        elif intent == 'educational':
            return self.educational_search(query)
        elif intent == 'local':
            return self.local_search(query)
        else:
            return self.general_search(query)
    
    def analyze_search_intent(self, query):
        """Analyze what type of search the user wants"""
        query_lower = query.lower()
        
        # Current events indicators
        if any(word in query_lower for word in ['latest', 'recent', 'today', 'news', '2024', '2025']):
            return 'current_events'
        
        # Educational indicators
        if any(word in query_lower for word in ['how to', 'what is', 'explain', 'learn', 'tutorial']):
            return 'educational'
        
        # Local search indicators
        if any(word in query_lower for word in ['near me', 'nearby', 'local', 'in my area']):
            return 'local'
        
        # Factual indicators
        if any(word in query_lower for word in ['definition', 'meaning', 'facts about', 'information']):
            return 'factual'
        
        return 'general'
    
    def factual_search(self, query):
        """Search for factual information"""
        try:
            # Try Wikipedia first for factual content
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
            response = requests.get(wiki_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'source': 'Wikipedia',
                    'title': data.get('title', ''),
                    'summary': data.get('extract', ''),
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                }
        except:
            pass
        
        return self.general_search(query)
    
    def news_search(self, query):
        """Search for current news and events"""
        try:
            # Use DuckDuckGo for news
            from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                results = list(ddgs.news(query, max_results=3))
                
            if results:
                formatted_results = []
                for result in results:
                    formatted_results.append({
                        'title': result.get('title', ''),
                        'summary': result.get('body', ''),
                        'source': result.get('source', ''),
                        'date': result.get('date', ''),
                        'url': result.get('url', '')
                    })
                return formatted_results
        except:
            pass
        
        return self.general_search(query)
    
    def educational_search(self, query):
        """Search for educational content"""
        try:
            from duckduckgo_search import DDGS
            
            # Add educational keywords to improve results
            educational_query = f"{query} tutorial guide explanation"
            
            with DDGS() as ddgs:
                results = list(ddgs.text(educational_query, max_results=5))
            
            if results:
                # Filter for educational sources
                educational_sources = ['wikipedia', 'edu', 'tutorial', 'guide', 'howto']
                filtered_results = []
                
                for result in results:
                    url = result.get('href', '').lower()
                    title = result.get('title', '').lower()
                    
                    if any(source in url or source in title for source in educational_sources):
                        filtered_results.append({
                            'title': result.get('title', ''),
                            'summary': result.get('body', ''),
                            'url': result.get('href', ''),
                            'type': 'educational'
                        })
                
                return filtered_results[:3] if filtered_results else results[:3]
        except:
            pass
        
        return self.general_search(query)
    
    def local_search(self, query):
        """Search for local information"""
        # This would integrate with location services
        # For now, return general search with location context
        location_query = f"{query} India local"
        return self.general_search(location_query)
    
    def general_search(self, query):
        """General web search"""
        try:
            from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
            
            if results:
                return [{
                    'title': result.get('title', ''),
                    'summary': result.get('body', ''),
                    'url': result.get('href', ''),
                    'type': 'general'
                } for result in results]
        except:
            pass
        
        return [{'title': 'Search Error', 'summary': 'Unable to perform search at this time', 'url': '', 'type': 'error'}]
    
    def smart_summarize(self, search_results, query):
        """Create intelligent summary from search results"""
        if not search_results:
            return "No results found for your query."
        
        # Combine relevant information
        combined_info = ""
        sources = []
        
        for result in search_results[:3]:  # Use top 3 results
            if result.get('summary'):
                combined_info += result['summary'] + " "
                if result.get('source'):
                    sources.append(result['source'])
        
        # Create contextual summary
        summary = f"Based on current information: {combined_info[:500]}..."
        
        if sources:
            summary += f" Sources: {', '.join(set(sources))}"
        
        return summary
    
    def get_search_suggestions(self, partial_query):
        """Get search suggestions based on partial input"""
        suggestions = []
        
        # Common search patterns
        if 'weather' in partial_query.lower():
            suggestions = ['weather today', 'weather forecast', 'weather in my city']
        elif 'news' in partial_query.lower():
            suggestions = ['latest news', 'breaking news', 'news today']
        elif 'how' in partial_query.lower():
            suggestions = ['how to cook', 'how to learn', 'how to fix']
        else:
            # Generic suggestions
            suggestions = [
                f"{partial_query} tutorial",
                f"{partial_query} guide",
                f"{partial_query} latest news",
                f"{partial_query} facts"
            ]
        
        return suggestions[:5]
    
    def track_search_patterns(self, query, results_quality):
        """Track user search patterns for improvement"""
        pattern = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'intent': self.analyze_search_intent(query),
            'quality': results_quality
        }
        
        self.search_history.append(pattern)
        
        # Keep only last 100 searches
        if len(self.search_history) > 100:
            self.search_history = self.search_history[-100:]