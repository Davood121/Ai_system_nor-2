"""
Search Integration Module
Unified interface for all search functionality
"""

from advanced_search_engine import AdvancedSearchEngine
from specialized_search import SpecializedSearch
from typing import List, Dict, Union
import json

class UnifiedSearchEngine:
    """Unified search engine combining all search types"""
    
    def __init__(self):
        self.advanced_search = AdvancedSearchEngine()
        self.specialized_search = SpecializedSearch()
        self.search_history = []
        
    def search(self, query: str, search_type: str = 'auto', **kwargs) -> Union[List[Dict], Dict]:
        """
        Unified search interface
        
        Args:
            query: Search query
            search_type: Type of search (auto, news, academic, statistics, definition, etc.)
            **kwargs: Additional parameters
            
        Returns:
            Search results
        """
        # Log search
        self.search_history.append({
            'query': query,
            'type': search_type,
            'timestamp': str(__import__('datetime').datetime.now())
        })
        
        # Auto-detect search type if needed
        if search_type == 'auto':
            search_type = self._detect_search_type(query)
        
        # Route to appropriate search
        if search_type == 'news':
            results = self.specialized_search.search_news(query, kwargs.get('days', 7))
        elif search_type == 'academic':
            results = self.specialized_search.search_academic(query)
        elif search_type == 'statistics':
            results = self.specialized_search.search_statistics(query)
        elif search_type == 'definition':
            results = self.specialized_search.search_definitions(query)
        elif search_type == 'images':
            results = self.specialized_search.search_images(query)
        elif search_type == 'videos':
            results = self.specialized_search.search_videos(query)
        elif search_type == 'local':
            results = self.specialized_search.search_local(query, kwargs.get('location', 'India'))
        elif search_type == 'weather':
            results = self.specialized_search.search_weather(query)
        elif search_type == 'products':
            results = self.specialized_search.search_products(query)
        elif search_type == 'jobs':
            results = self.specialized_search.search_jobs(query, kwargs.get('location', 'India'))
        elif search_type == 'recipes':
            results = self.specialized_search.search_recipes(query)
        else:
            # Default: advanced search across all sources
            results = self.advanced_search.search(query, max_results=kwargs.get('max_results', 5))
        
        return results
    
    def _detect_search_type(self, query: str) -> str:
        """Auto-detect search type from query"""
        query_lower = query.lower()
        
        # News indicators
        if any(word in query_lower for word in ['news', 'latest', 'recent', 'today', 'breaking', 'current']):
            return 'news'
        
        # Academic indicators
        if any(word in query_lower for word in ['research', 'paper', 'study', 'academic', 'journal', 'thesis']):
            return 'academic'
        
        # Statistics indicators
        if any(word in query_lower for word in ['statistics', 'data', 'percent', 'average', 'rate', 'number']):
            return 'statistics'
        
        # Definition indicators
        if any(word in query_lower for word in ['define', 'meaning', 'what is', 'definition', 'explain']):
            return 'definition'
        
        # Image indicators
        if any(word in query_lower for word in ['image', 'picture', 'photo', 'show me', 'look like']):
            return 'images'
        
        # Video indicators
        if any(word in query_lower for word in ['video', 'youtube', 'watch', 'tutorial', 'how to']):
            return 'videos'
        
        # Local indicators
        if any(word in query_lower for word in ['near me', 'nearby', 'local', 'in my area', 'around']):
            return 'local'
        
        # Weather indicators
        if any(word in query_lower for word in ['weather', 'temperature', 'forecast', 'rain', 'sunny']):
            return 'weather'
        
        # Product indicators
        if any(word in query_lower for word in ['buy', 'price', 'product', 'shop', 'store', 'cost']):
            return 'products'
        
        # Job indicators
        if any(word in query_lower for word in ['job', 'hiring', 'career', 'position', 'employment']):
            return 'jobs'
        
        # Recipe indicators
        if any(word in query_lower for word in ['recipe', 'cook', 'ingredients', 'prepare', 'make']):
            return 'recipes'
        
        return 'general'
    
    def smart_search(self, query: str, **kwargs) -> Dict:
        """
        Smart search with automatic type detection and result formatting
        
        Returns:
            Formatted search results with metadata
        """
        search_type = self._detect_search_type(query)
        results = self.search(query, search_type, **kwargs)
        
        return {
            'query': query,
            'search_type': search_type,
            'results': results,
            'count': len(results) if isinstance(results, list) else 1,
            'formatted': self._format_results(results, search_type)
        }
    
    def _format_results(self, results: Union[List[Dict], Dict], search_type: str) -> str:
        """Format results for display"""
        if isinstance(results, dict):
            # Single result (like definition or weather)
            return self._format_single_result(results)
        
        if not results:
            return "❌ No results found."
        
        formatted = f"🔍 **{search_type.upper()} Results** ({len(results)} found)\n\n"
        
        for i, result in enumerate(results[:5], 1):
            formatted += f"**{i}. {result.get('title', 'Untitled')}**\n"
            
            if result.get('snippet'):
                formatted += f"   {result['snippet'][:150]}...\n"
            
            if result.get('source'):
                formatted += f"   📌 Source: {result['source']}\n"
            
            if result.get('url'):
                formatted += f"   🔗 {result['url']}\n"
            
            if result.get('relevance_score'):
                formatted += f"   ⭐ Relevance: {result['relevance_score']:.0%}\n"
            
            formatted += "\n"
        
        return formatted
    
    def _format_single_result(self, result: Dict) -> str:
        """Format single result"""
        formatted = f"**{result.get('title', 'Result')}**\n\n"
        
        if result.get('definition'):
            formatted += f"{result['definition']}\n\n"
        elif result.get('data'):
            formatted += f"{result['data']}\n\n"
        
        if result.get('url'):
            formatted += f"🔗 Source: {result['url']}\n"
        
        return formatted
    
    def get_search_suggestions(self, partial_query: str) -> List[str]:
        """Get search suggestions"""
        suggestions = []
        
        # Based on query type
        if 'weather' in partial_query.lower():
            suggestions = [
                f"{partial_query} today",
                f"{partial_query} forecast",
                f"{partial_query} temperature"
            ]
        elif 'recipe' in partial_query.lower():
            suggestions = [
                f"{partial_query} easy",
                f"{partial_query} ingredients",
                f"{partial_query} quick"
            ]
        elif 'job' in partial_query.lower():
            suggestions = [
                f"{partial_query} India",
                f"{partial_query} remote",
                f"{partial_query} entry level"
            ]
        else:
            suggestions = [
                f"{partial_query} latest",
                f"{partial_query} tutorial",
                f"{partial_query} guide",
                f"{partial_query} 2025"
            ]
        
        return suggestions[:5]
    
    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """Get recent search history"""
        return self.search_history[-limit:]
    
    def clear_search_history(self):
        """Clear search history"""
        self.search_history = []
    
    def export_results(self, results: Union[List[Dict], Dict], format: str = 'json') -> str:
        """Export results in different formats"""
        if format == 'json':
            return json.dumps(results, indent=2)
        elif format == 'csv':
            # Simple CSV export for list results
            if isinstance(results, list) and results:
                import csv
                import io
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
                return output.getvalue()
        
        return str(results)

