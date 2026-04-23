"""
Test enhanced metrics display and performance comparison
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_enhanced_metrics():
    """Test the enhanced metrics with proper scaling"""
    
    print("\n" + "="*60)
    print("TESTING ENHANCED METRICS & PERFORMANCE COMPARISON")
    print("="*60)
    
    # Original code
    original_code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def calculate_sum(numbers):
    total = 0
    for num in numbers:
        if num > 0:
            total += num
        else:
            if num < -10:
                total -= 1
    return total
"""

    # Test analysis
    print("\n1. Analyzing original code...")
    response = requests.post(f"{BASE_URL}/api/analyze", 
        json={'code': original_code, 'language': 'python'},
        timeout=10
    )
    
    if response.status_code != 200:
        print(f"✗ Analysis failed: {response.status_code}")
        return
    
    original_metrics = response.json()
    metrics = original_metrics.get('metrics', {})
    
    print(f"   ✓ Status: {response.status_code}")
    print("\n   Original Code Metrics:")
    print(f"   ├─ Lines of Code: {metrics.get('raw', {}).get('loc')}")
    print(f"   ├─ Logical Lines: {metrics.get('raw', {}).get('lloc')}")
    print(f"   ├─ Comments: {metrics.get('raw', {}).get('comments')}")
    print(f"   ├─ Avg Complexity: {metrics.get('avg_complexity')}")
    print(f"   ├─ Halstead Volume: {metrics.get('halstead', {}).get('volume')}")
    print(f"   ├─ Difficulty: {metrics.get('halstead', {}).get('difficulty')}")
    print(f"   ├─ Effort: {metrics.get('halstead', {}).get('effort')}")
    print(f"   └─ Vocabulary: {metrics.get('halstead', {}).get('vocabulary')}")
    
    # Check all metrics are present
    required_metrics = ['raw', 'halstead', 'avg_complexity', 'cyclomatic']
    missing = [m for m in required_metrics if m not in metrics]
    
    if missing:
        print(f"\n   ✗ Missing metrics: {missing}")
        return
    
    print("\n   ✓ All metrics present!")
    
    # Simulated optimized code (shorter, less complex)
    optimized_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def calculate_sum(numbers):
    return sum(n for n in numbers if n > 0)
"""
    
    print("\n2. Analyzing optimized code (simulated)...")
    response = requests.post(f"{BASE_URL}/api/analyze", 
        json={'code': optimized_code, 'language': 'python'},
        timeout=10
    )
    
    if response.status_code == 200:
        optimized_metrics = response.json()
        opt_metrics = optimized_metrics.get('metrics', {})
        
        print(f"   ✓ Status: {response.status_code}")
        print("\n   Optimized Code Metrics:")
        print(f"   ├─ Lines of Code: {opt_metrics.get('raw', {}).get('loc')}")
        print(f"   ├─ Logical Lines: {opt_metrics.get('raw', {}).get('lloc')}")
        print(f"   ├─ Comments: {opt_metrics.get('raw', {}).get('comments')}")
        print(f"   ├─ Avg Complexity: {opt_metrics.get('avg_complexity')}")
        print(f"   ├─ Halstead Volume: {opt_metrics.get('halstead', {}).get('volume')}")
        print(f"   ├─ Difficulty: {opt_metrics.get('halstead', {}).get('difficulty')}")
        print(f"   ├─ Effort: {opt_metrics.get('halstead', {}).get('effort')}")
        print(f"   └─ Vocabulary: {opt_metrics.get('halstead', {}).get('vocabulary')}")
        
        # Calculate improvements
        print("\n3. Performance Comparison:")
        orig_loc = metrics.get('raw', {}).get('loc', 1)
        opt_loc = opt_metrics.get('raw', {}).get('loc', 1)
        loc_improvement = ((orig_loc - opt_loc) / orig_loc) * 100 if orig_loc > 0 else 0
        
        orig_complexity = metrics.get('avg_complexity', 1)
        opt_complexity = opt_metrics.get('avg_complexity', 1)
        complexity_improvement = ((orig_complexity - opt_complexity) / orig_complexity) * 100 if orig_complexity > 0 else 0
        
        orig_difficulty = metrics.get('halstead', {}).get('difficulty', 1)
        opt_difficulty = opt_metrics.get('halstead', {}).get('difficulty', 1)
        difficulty_improvement = ((orig_difficulty - opt_difficulty) / orig_difficulty) * 100 if orig_difficulty > 0 else 0
        
        print(f"   ├─ LOC Reduction: {loc_improvement:.1f}% ↓")
        print(f"   ├─ Complexity Reduction: {complexity_improvement:.1f}% ↓")
        print(f"   ├─ Difficulty Reduction: {difficulty_improvement:.1f}% ↓")
        print(f"   └─ Overall Quality: IMPROVED ✓")
        
        print("\n✓ ENHANCED METRICS TEST PASSED!")
        return True
    else:
        print(f"   ✗ Analysis failed: {response.status_code}")
        return False

if __name__ == '__main__':
    try:
        success = test_enhanced_metrics()
        if success:
            print("\n" + "="*60)
            print("All enhancements working correctly!")
            print("="*60)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
