from ddgs import DDGS
import wikipedia
wikipedia.set_lang("en")
# Fix Wikipedia parser warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')
import requests
from bs4 import BeautifulSoup

class MultiSearchEngine:
    def __init__(self):
        self.sources = {
            'web': self._search_web,
            'news': self._search_news,
            'wiki': self._search_wiki,
            'reddit': self._search_reddit,
            'academic': self._search_academic
        }
    
    def search(self, query, sources=['web', 'wiki']):
        """Main search function"""
        results = {}
        for source in sources:
            if source in self.sources:
                results[source] = self.sources[source](query)
        return self._combine_results(results)
    
    def _search_web(self, query):
        """Enhanced web search with better results"""
        try:
            results = []
            with DDGS() as ddgs:
                # Get more results for better information
                for result in ddgs.text(query, max_results=5):
                    # Filter for more relevant results
                    if any(word in result['body'].lower() for word in query.lower().split()[:3]):
                        results.append(f"{result['title']}: {result['body']}")
            
            if not results:  # If no relevant results, get any results
                with DDGS() as ddgs:
                    for result in ddgs.text(query, max_results=3):
                        results.append(f"{result['title']}: {result['body']}")
            
            return " | ".join(results)
        except Exception as e:
            print(f"Web search failed: {e}")
            return self._fallback_search(query)
    
    def _search_news(self, query):
        """Enhanced news search"""
        try:
            results = []
            with DDGS() as ddgs:
                # Try news search first
                for result in ddgs.news(query, max_results=3):
                    results.append(f"{result['title']}: {result['body']}")
                
                # If no news results, try recent web results with better terms
                if not results:
                    recent_query = f"{query} 2025 latest statistics"
                    for result in ddgs.text(recent_query, max_results=3):
                        results.append(f"Recent: {result['title']}: {result['body']}")
            
            return " | ".join(results)
        except Exception as e:
            print(f"News search failed: {e}")
            return ""
    
    def _search_wiki(self, query):
        """Wikipedia search with better error handling"""
        # Extract key terms only
        key_terms = []
        important_words = ['deaths', 'mortality', 'india', 'statistics', 'causes', 'disease', 'health']
        
        for word in query.lower().split():
            if word in important_words or len(word) > 5:
                key_terms.append(word)
                if len(key_terms) >= 2:
                    break
        
        if not key_terms:
            return ""
        
        search_query = " ".join(key_terms)
        
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                return wikipedia.summary(search_query, sentences=2)
        except:
            # Final fallback with single word
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    return wikipedia.summary(key_terms[0], sentences=1)
            except:
                return ""
    
    def _search_reddit(self, query):
        """Reddit discussions - disabled for better performance"""
        return ""
    
    def _search_academic(self, query):
        """Academic sources"""
        try:
            with DDGS() as ddgs:
                for result in ddgs.text(f"site:arxiv.org OR site:scholar.google.com {query}", max_results=1):
                    return result['body'][:200]
            return ""
        except:
            return ""
    
    def _combine_results(self, results):
        """Combine all search results"""
        combined = []
        for source, content in results.items():
            if content:
                combined.append(f"[{source.upper()}] {content}")
        return " ".join(combined) if combined else "No search results found"
    
    def _fallback_search(self, query):
        """Fallback search using requests"""
        try:
            # Simple Google search fallback
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                snippets = soup.find_all('span', class_='aCOpRe')
                if snippets:
                    return snippets[0].get_text()[:300]
            return "Fallback search failed"
        except:
            return "All search methods failed"
    
    def smart_search(self, query):
        """Intelligent search based on query type"""
        query_lower = query.lower()
        
        # Clean and optimize query for better results
        clean_query = self._optimize_query(query)
        
        # Determine best sources based on query (ChatGPT-like)
        if any(word in query_lower for word in ['news', 'latest', 'recent', 'today', 'current']):
            sources = ['news', 'web', 'wiki']
        elif any(word in query_lower for word in ['college', 'university', 'school', 'education']):
            sources = ['web']  # Educational queries need web search
        elif any(word in query_lower for word in ['what is', 'define', 'meaning', 'explain']):
            sources = ['web', 'wiki']
        elif any(word in query_lower for word in ['population', 'statistics', 'data', 'demographics']):
            sources = ['web', 'news']  # Focus on current data sources
        elif any(word in query_lower for word in ['college', 'university', 'school', 'education', 'institute']):
            sources = ['web']  # Focus on educational institution data
        elif any(word in query_lower for word in ['deaths', 'mortality', 'crime', 'crime rate']):
            sources = ['web', 'news']  # Focus on current data, avoid outdated wiki
        elif any(word in query_lower for word in ['company', 'business', 'stock', 'economy']):
            sources = ['web', 'news']
        elif any(word in query_lower for word in ['technology', 'science', 'research']):
            sources = ['web', 'wiki']
        else:
            sources = ['web']
        
        return self.search(clean_query, sources)
    
    def _optimize_query(self, query):
        """Optimize query for better search results"""
        # Remove common words and optimize
        stop_words = ['was', 'were', 'is', 'are', 'the', 'on', 'in', 'at', 'about', 'tell', 'me']
        words = [word for word in query.split() if word.lower() not in stop_words]
        
        # Add current year for population/statistics/deaths/crime queries
        if any(word in query.lower() for word in ['population', 'statistics', 'data', 'current', 'deaths', 'mortality', 'crime', 'rate']):
            if '2025' not in query and '2024' not in query:
                words.append('2025')
                words.append('latest')
                words.append('current')
        
        return " ".join(words[:6])  # Limit to 6 key words