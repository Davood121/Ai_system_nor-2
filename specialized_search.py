"""
Specialized Search Module
Handles specific search types: News, Academic, Statistics, Local, etc.
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict
import json

class SpecializedSearch:
    """Specialized search for different query types"""
    
    def __init__(self):
        self.cache = {}
        
    def search_news(self, query: str, days: int = 7) -> List[Dict]:
        """Search for recent news"""
        try:
            from duckduckgo_search import DDGS
            
            # Add date filter
            date_filter = f"after:{(datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')}"
            search_query = f"{query} {date_filter}"
            
            results = []
            with DDGS() as ddgs:
                for result in ddgs.news(query, max_results=5):
                    results.append({
                        'source': 'News',
                        'title': result['title'],
                        'snippet': result['body'],
                        'url': result['url'],
                        'date': result.get('date', ''),
                        'source_name': result.get('source', ''),
                        'type': 'news',
                        'relevance_score': 0.9
                    })
            return results
        except:
            return []
    
    def search_statistics(self, query: str) -> List[Dict]:
        """Search for statistical data"""
        try:
            from duckduckgo_search import DDGS
            
            search_query = f"{query} statistics data 2024 2025"
            results = []
            
            with DDGS() as ddgs:
                for result in ddgs.text(search_query, max_results=5):
                    # Filter for statistical content
                    if any(word in result['body'].lower() for word in ['percent', '%', 'million', 'billion', 'data', 'statistics', 'average']):
                        results.append({
                            'source': 'Statistics',
                            'title': result['title'],
                            'snippet': result['body'],
                            'url': result['href'],
                            'type': 'statistics',
                            'relevance_score': 0.85
                        })
            return results[:5]
        except:
            return []
    
    def search_academic(self, query: str) -> List[Dict]:
        """Search academic papers and research"""
        results = []
        
        # Search arXiv
        try:
            url = "http://export.arxiv.org/api/query"
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': 3,
                'sortBy': 'relevance'
            }
            
            response = requests.get(url, params=params, timeout=5)
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.find('{http://www.w3.org/2005/Atom}title').text
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
                arxiv_id = entry.find('{http://www.w3.org/2005/Atom}id').text.split('/abs/')[-1]
                
                results.append({
                    'source': 'arXiv',
                    'title': title,
                    'snippet': summary[:200],
                    'url': f"https://arxiv.org/abs/{arxiv_id}",
                    'type': 'academic',
                    'relevance_score': 0.95
                })
        except:
            pass
        
        # Search Google Scholar via DuckDuckGo
        try:
            from duckduckgo_search import DDGS
            
            search_query = f"{query} site:scholar.google.com OR site:researchgate.net"
            with DDGS() as ddgs:
                for result in ddgs.text(search_query, max_results=2):
                    results.append({
                        'source': 'Scholar',
                        'title': result['title'],
                        'snippet': result['body'],
                        'url': result['href'],
                        'type': 'academic',
                        'relevance_score': 0.85
                    })
        except:
            pass
        
        return results[:5]
    
    def search_definitions(self, query: str) -> Dict:
        """Search for definitions and meanings"""
        try:
            # Try Wiktionary API
            url = "https://en.wiktionary.org/w/api.php"
            params = {
                'action': 'query',
                'titles': query,
                'prop': 'extracts',
                'explaintext': True,
                'format': 'json'
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            for page_id, page in data.get('query', {}).get('pages', {}).items():
                if 'extract' in page:
                    return {
                        'source': 'Wiktionary',
                        'term': query,
                        'definition': page['extract'][:300],
                        'url': f"https://en.wiktionary.org/wiki/{query}",
                        'type': 'definition'
                    }
        except:
            pass
        
        return None
    
    def search_images(self, query: str) -> List[Dict]:
        """Search for images (metadata only)"""
        try:
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                for result in ddgs.images(query, max_results=5):
                    results.append({
                        'source': 'Images',
                        'title': result.get('title', ''),
                        'url': result.get('image', ''),
                        'source_url': result.get('url', ''),
                        'type': 'image',
                        'relevance_score': 0.8
                    })
            return results
        except:
            return []
    
    def search_videos(self, query: str) -> List[Dict]:
        """Search for videos (metadata only)"""
        try:
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                for result in ddgs.videos(query, max_results=5):
                    results.append({
                        'source': 'Videos',
                        'title': result.get('title', ''),
                        'url': result.get('content', ''),
                        'duration': result.get('duration', ''),
                        'type': 'video',
                        'relevance_score': 0.8
                    })
            return results
        except:
            return []
    
    def search_local(self, query: str, location: str = "India") -> List[Dict]:
        """Search for local information"""
        try:
            from duckduckgo_search import DDGS
            
            search_query = f"{query} in {location} local"
            results = []
            
            with DDGS() as ddgs:
                for result in ddgs.text(search_query, max_results=5):
                    results.append({
                        'source': 'Local',
                        'title': result['title'],
                        'snippet': result['body'],
                        'url': result['href'],
                        'location': location,
                        'type': 'local',
                        'relevance_score': 0.8
                    })
            return results
        except:
            return []
    
    def search_weather(self, location: str) -> Dict:
        """Search for weather information"""
        try:
            from duckduckgo_search import DDGS
            
            search_query = f"weather {location} today temperature"
            
            with DDGS() as ddgs:
                for result in ddgs.text(search_query, max_results=1):
                    return {
                        'source': 'Weather',
                        'location': location,
                        'data': result['body'],
                        'url': result['href'],
                        'type': 'weather'
                    }
        except:
            return None
    
    def search_products(self, query: str) -> List[Dict]:
        """Search for products and prices"""
        try:
            from duckduckgo_search import DDGS
            
            search_query = f"{query} price buy online"
            results = []
            
            with DDGS() as ddgs:
                for result in ddgs.text(search_query, max_results=5):
                    results.append({
                        'source': 'Products',
                        'title': result['title'],
                        'snippet': result['body'],
                        'url': result['href'],
                        'type': 'product',
                        'relevance_score': 0.75
                    })
            return results
        except:
            return []
    
    def search_jobs(self, query: str, location: str = "India") -> List[Dict]:
        """Search for job opportunities"""
        try:
            from duckduckgo_search import DDGS
            
            search_query = f"{query} jobs {location} hiring"
            results = []
            
            with DDGS() as ddgs:
                for result in ddgs.text(search_query, max_results=5):
                    results.append({
                        'source': 'Jobs',
                        'title': result['title'],
                        'snippet': result['body'],
                        'url': result['href'],
                        'location': location,
                        'type': 'job',
                        'relevance_score': 0.8
                    })
            return results
        except:
            return []
    
    def search_recipes(self, query: str) -> List[Dict]:
        """Search for recipes"""
        try:
            from duckduckgo_search import DDGS
            
            search_query = f"{query} recipe ingredients instructions"
            results = []
            
            with DDGS() as ddgs:
                for result in ddgs.text(search_query, max_results=5):
                    results.append({
                        'source': 'Recipes',
                        'title': result['title'],
                        'snippet': result['body'],
                        'url': result['href'],
                        'type': 'recipe',
                        'relevance_score': 0.8
                    })
            return results
        except:
            return []

