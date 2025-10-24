"""
Advanced Search Engine with Multiple Open Sources
Uses: Wikipedia API, Wikidata, OpenLibrary, DuckDuckGo, and more
Provides precise, ranked, and filtered results
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Tuple
import re
from urllib.parse import quote

class AdvancedSearchEngine:
    """Advanced search engine with multiple open sources and precision ranking"""
    
    def __init__(self):
        self.sources = {
            'wikipedia': self._search_wikipedia,
            'wikidata': self._search_wikidata,
            'openlibrary': self._search_openlibrary,
            'duckduckgo': self._search_duckduckgo,
            'arxiv': self._search_arxiv,
            'dbpedia': self._search_dbpedia,
        }
        self.cache = {}
        self.result_cache_ttl = 3600  # 1 hour
        
    def search(self, query: str, sources: List[str] = None, max_results: int = 5) -> Dict:
        """
        Perform advanced search across multiple sources
        
        Args:
            query: Search query
            sources: List of sources to search (default: all)
            max_results: Maximum results per source
            
        Returns:
            Dictionary with ranked and filtered results
        """
        if sources is None:
            sources = list(self.sources.keys())
        
        # Check cache
        cache_key = f"{query}:{','.join(sorted(sources))}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if (datetime.now() - cached_data['timestamp']).total_seconds() < self.result_cache_ttl:
                return cached_data['results']
        
        # Optimize query
        optimized_query = self._optimize_query(query)
        
        # Search all sources
        all_results = []
        for source in sources:
            if source in self.sources:
                try:
                    results = self.sources[source](optimized_query, max_results)
                    if results:
                        all_results.extend(results)
                except Exception as e:
                    print(f"Error searching {source}: {e}")
        
        # Rank and filter results
        ranked_results = self._rank_results(all_results, query)
        
        # Cache results
        self.cache[cache_key] = {
            'results': ranked_results,
            'timestamp': datetime.now()
        }
        
        return ranked_results
    
    def _search_wikipedia(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Wikipedia API"""
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'srwhat': 'text',
                'format': 'json',
                'srlimit': max_results
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            results = []
            for item in data.get('query', {}).get('search', []):
                results.append({
                    'source': 'Wikipedia',
                    'title': item['title'],
                    'snippet': item['snippet'].replace('<span class="searchmatch">', '').replace('</span>', ''),
                    'url': f"https://en.wikipedia.org/wiki/{quote(item['title'])}",
                    'relevance_score': 0.9,
                    'type': 'encyclopedia'
                })
            return results
        except:
            return []
    
    def _search_wikidata(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Wikidata for structured data"""
        try:
            url = "https://www.wikidata.org/w/api.php"
            params = {
                'action': 'wbsearchentities',
                'search': query,
                'language': 'en',
                'format': 'json',
                'limit': max_results
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            results = []
            for item in data.get('search', []):
                results.append({
                    'source': 'Wikidata',
                    'title': item['label'],
                    'snippet': item.get('description', ''),
                    'url': f"https://www.wikidata.org/wiki/{item['id']}",
                    'relevance_score': 0.85,
                    'type': 'structured_data',
                    'entity_id': item['id']
                })
            return results
        except:
            return []
    
    def _search_openlibrary(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search OpenLibrary for books and publications"""
        try:
            url = "https://openlibrary.org/search.json"
            params = {
                'q': query,
                'limit': max_results
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            results = []
            for item in data.get('docs', []):
                results.append({
                    'source': 'OpenLibrary',
                    'title': item.get('title', ''),
                    'snippet': f"Author: {', '.join(item.get('author_name', [])[:2])}. Published: {item.get('first_publish_year', 'N/A')}",
                    'url': f"https://openlibrary.org{item.get('key', '')}",
                    'relevance_score': 0.8,
                    'type': 'book',
                    'author': ', '.join(item.get('author_name', [])[:2])
                })
            return results
        except:
            return []
    
    def _search_duckduckgo(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search DuckDuckGo for web results"""
        try:
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                for result in ddgs.text(query, max_results=max_results):
                    results.append({
                        'source': 'DuckDuckGo',
                        'title': result['title'],
                        'snippet': result['body'],
                        'url': result['href'],
                        'relevance_score': 0.75,
                        'type': 'web'
                    })
            return results
        except:
            return []
    
    def _search_arxiv(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search arXiv for academic papers"""
        try:
            url = "http://export.arxiv.org/api/query"
            params = {
                'search_query': f'all:{query}',
                'start': 0,
                'max_results': max_results,
                'sortBy': 'relevance'
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            results = []
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
                    'relevance_score': 0.9,
                    'type': 'academic_paper'
                })
            return results
        except:
            return []
    
    def _search_dbpedia(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search DBpedia for linked data"""
        try:
            url = "https://dbpedia.org/sparql"
            sparql_query = f"""
            SELECT ?resource ?label ?abstract WHERE {{
                ?resource rdfs:label ?label ;
                          dbo:abstract ?abstract .
                FILTER (regex(?label, "{query}", "i") && langMatches(lang(?label), "en"))
                FILTER (langMatches(lang(?abstract), "en"))
            }}
            LIMIT {max_results}
            """
            
            params = {
                'query': sparql_query,
                'format': 'json'
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            results = []
            for binding in data.get('results', {}).get('bindings', []):
                results.append({
                    'source': 'DBpedia',
                    'title': binding['label']['value'],
                    'snippet': binding['abstract']['value'][:200],
                    'url': binding['resource']['value'],
                    'relevance_score': 0.85,
                    'type': 'linked_data'
                })
            return results
        except:
            return []
    
    def _optimize_query(self, query: str) -> str:
        """Optimize query for better search results"""
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'are', 'was', 'were'}
        words = [w for w in query.lower().split() if w not in stop_words]
        
        # Keep important keywords
        return ' '.join(words[:5])
    
    def _rank_results(self, results: List[Dict], original_query: str) -> List[Dict]:
        """Rank results by relevance"""
        query_words = set(original_query.lower().split())
        
        for result in results:
            # Calculate relevance score
            title_matches = sum(1 for word in query_words if word in result['title'].lower())
            snippet_matches = sum(1 for word in query_words if word in result['snippet'].lower())
            
            # Boost score based on matches
            relevance = result.get('relevance_score', 0.5)
            relevance += (title_matches * 0.1)
            relevance += (snippet_matches * 0.05)
            
            result['relevance_score'] = min(relevance, 1.0)
        
        # Sort by relevance score
        return sorted(results, key=lambda x: x['relevance_score'], reverse=True)
    
    def format_results(self, results: List[Dict], max_display: int = 5) -> str:
        """Format results for display"""
        if not results:
            return "No results found."
        
        formatted = "🔍 **Search Results:**\n\n"
        
        for i, result in enumerate(results[:max_display], 1):
            formatted += f"{i}. **{result['title']}** [{result['source']}]\n"
            formatted += f"   {result['snippet'][:150]}...\n"
            formatted += f"   🔗 {result['url']}\n"
            formatted += f"   Relevance: {result['relevance_score']:.0%}\n\n"
        
        return formatted

