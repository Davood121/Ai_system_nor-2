from search_engine import MultiSearchEngine

# Test the search engine
search = MultiSearchEngine()

print("Testing search engine...")
query = "common deaths India 2022"

print(f"\nQuery: {query}")
result = search.smart_search(query)
print(f"Result: {result}")

# Test individual sources
print("\n--- Testing individual sources ---")
print("Web:", search._search_web(query))
print("Wiki:", search._search_wiki("mortality India"))
print("News:", search._search_news(query))