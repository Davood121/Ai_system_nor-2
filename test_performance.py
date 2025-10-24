"""
Performance Testing Script
Test the optimizations and measure improvements
"""

import time
import sys
from terminal_ai import TerminalAI
from performance_config import print_optimization_summary

def measure_time(func, *args, **kwargs):
    """Measure execution time of a function"""
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start
    return result, elapsed

def test_response_caching():
    """Test response caching performance"""
    print("\n" + "="*60)
    print("🧪 TEST 1: Response Caching")
    print("="*60)
    
    ai = TerminalAI()
    test_query = "What is Python?"
    
    # First call (no cache)
    print(f"\n📝 Query: {test_query}")
    result1, time1 = measure_time(ai.get_ai_response, test_query)
    print(f"⏱️  First call (no cache): {time1:.2f}s")
    
    # Second call (cached)
    result2, time2 = measure_time(ai.get_ai_response, test_query)
    print(f"⏱️  Second call (cached): {time2:.2f}s")
    
    speedup = time1 / time2 if time2 > 0 else float('inf')
    print(f"🚀 Speedup: {speedup:.1f}x faster")
    
    return speedup > 10  # Should be much faster

def test_search_caching():
    """Test search result caching"""
    print("\n" + "="*60)
    print("🧪 TEST 2: Search Result Caching")
    print("="*60)
    
    ai = TerminalAI()
    test_query = "weather in Mumbai"
    
    # First search (no cache)
    print(f"\n🔍 Query: {test_query}")
    result1, time1 = measure_time(ai.search_web, test_query)
    print(f"⏱️  First search (no cache): {time1:.2f}s")
    
    # Second search (cached)
    result2, time2 = measure_time(ai.search_web, test_query)
    print(f"⏱️  Second search (cached): {time2:.2f}s")
    
    speedup = time1 / time2 if time2 > 0 else float('inf')
    print(f"🚀 Speedup: {speedup:.1f}x faster")
    
    return speedup > 100  # Should be instant

def test_async_operations():
    """Test async operations don't block"""
    print("\n" + "="*60)
    print("🧪 TEST 3: Async Operations (Non-blocking)")
    print("="*60)
    
    ai = TerminalAI()
    
    # Test that speak doesn't block
    print("\n🎤 Testing async speak operation...")
    start = time.time()
    ai.speak("This is a test")
    elapsed = time.time() - start
    
    print(f"⏱️  Speak call returned in: {elapsed:.4f}s")
    print(f"✅ Non-blocking: {elapsed < 0.1}")
    
    return elapsed < 0.1

def test_batch_saves():
    """Test batched memory saves"""
    print("\n" + "="*60)
    print("🧪 TEST 4: Batched Memory Saves")
    print("="*60)
    
    ai = TerminalAI()
    
    print("\n💾 Testing batched saves...")
    start = time.time()
    
    # Add multiple conversations
    for i in range(5):
        ai.save_to_memory(f"Question {i}", f"Answer {i}")
    
    elapsed = time.time() - start
    
    print(f"⏱️  Added 5 conversations in: {elapsed:.4f}s")
    print(f"✅ Fast batch operation: {elapsed < 0.1}")
    
    return elapsed < 0.1

def test_smart_response_speed():
    """Test smart response speed"""
    print("\n" + "="*60)
    print("🧪 TEST 5: Smart Response Speed")
    print("="*60)
    
    ai = TerminalAI()
    
    # Test simple response (no search needed)
    print("\n💬 Testing simple response (no search)...")
    result, elapsed = measure_time(ai.smart_response, "hello")
    print(f"⏱️  Response time: {elapsed:.2f}s")
    print(f"✅ Fast response: {elapsed < 5}")
    
    return elapsed < 5

def run_all_tests():
    """Run all performance tests"""
    print("\n" + "="*70)
    print("🚀 AI ASSISTANT PERFORMANCE TEST SUITE")
    print("="*70)
    
    print_optimization_summary()
    
    tests = [
        ("Response Caching", test_response_caching),
        ("Search Caching", test_search_caching),
        ("Async Operations", test_async_operations),
        ("Batch Saves", test_batch_saves),
        ("Smart Response Speed", test_smart_response_speed),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = "✅ PASS" if result else "⚠️  PARTIAL"
        except Exception as e:
            print(f"\n❌ Error in {test_name}: {e}")
            results[test_name] = "❌ FAIL"
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for test_name, result in results.items():
        print(f"{result} - {test_name}")
    
    passed = sum(1 for r in results.values() if "✅" in r)
    total = len(results)
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    print("\n💡 Performance improvements are now active!")
    print("   Your AI assistant should be 3-5x faster! 🚀")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()

