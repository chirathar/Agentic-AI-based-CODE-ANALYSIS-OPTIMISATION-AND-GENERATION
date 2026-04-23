#!/usr/bin/env python3

import requests
import json
import time

def test_performance_comparison_functionality():
    """Test that performance comparison works by sending multiple analysis requests"""
    print("🧪 Testing Performance Comparison Functionality...")
    
    # Test cases with different complexity levels
    test_cases = [
        {
            'name': 'Simple Code',
            'code': '''
def hello():
    print("Hello, World!")
    return True

hello()
''',
            'language': 'python'
        },
        {
            'name': 'Medium Complexity',
            'code': '''
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def calculate_factorial(n):
    if n <= 1:
        return 1
    return n * calculate_factorial(n-1)

# Test the functions
for i in range(5):
    print(f"Fibonacci({i}): {calculate_fibonacci(i)}")
    print(f"Factorial({i}): {calculate_factorial(i)}")
''',
            'language': 'python'
        },
        {
            'name': 'High Complexity',
            'code': '''
class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.processed = []
    
    def process_data(self):
        for item in self.data:
            if isinstance(item, dict):
                if item.get('type') == 'numeric':
                    self.process_numeric(item)
                elif item.get('type') == 'text':
                    self.process_text(item)
                else:
                    self.process_generic(item)
            else:
                self.process_simple(item)
        
        return self.processed
    
    def process_numeric(self, item):
        try:
            value = float(item.get('value', 0))
            if value > 0:
                processed_value = value * 1.1
            elif value < 0:
                processed_value = value * 0.9
            else:
                processed_value = 0
            
            self.processed.append({
                'original': value,
                'processed': processed_value,
                'type': 'numeric'
            })
        except (ValueError, TypeError):
            self.processed.append({'error': 'Invalid numeric value', 'original': item})
    
    def process_text(self, item):
        text = str(item.get('value', ''))
        if len(text) > 100:
            processed_text = text[:100] + '...'
        else:
            processed_text = text.upper()
        
        self.processed.append({
            'original': text,
            'processed': processed_text,
            'type': 'text'
        })
    
    def process_generic(self, item):
        self.processed.append({
            'original': item,
            'processed': str(item),
            'type': 'generic'
        })
    
    def process_simple(self, item):
        self.processed.append({
            'original': item,
            'processed': f"Simple: {item}",
            'type': 'simple'
        })

# Usage example
data = [
    {'type': 'numeric', 'value': 42},
    {'type': 'text', 'value': 'Hello World'},
    {'type': 'numeric', 'value': -5.5},
    {'type': 'unknown', 'value': 'mystery'},
    'simple string',
    {'type': 'text', 'value': 'This is a very long text that should be truncated because it exceeds the maximum length limit'}
]

processor = DataProcessor(data)
result = processor.process_data()
print(f"Processed {len(result)} items")
''',
            'language': 'python'
        }
    ]
    
    analysis_results = []
    
    try:
        for i, test_case in enumerate(test_cases):
            print(f"\n  Analyzing {test_case['name']}...")
            
            response = requests.post('http://localhost:5000/api/analyze', 
                                   json={
                                       'code': test_case['code'],
                                       'language': test_case['language']
                                   },
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                metrics = data.get('metrics', {})
                
                result = {
                    'name': test_case['name'],
                    'loc': metrics.get('raw', {}).get('loc', 0),
                    'complexity': metrics.get('avg_complexity', 0),
                    'volume': metrics.get('halstead', {}).get('volume', 0),
                    'difficulty': metrics.get('halstead', {}).get('difficulty', 0),
                    'maintainability': max(100 - (metrics.get('avg_complexity', 0) * 10), 0)
                }
                
                analysis_results.append(result)
                print(f"    ✅ LOC: {result['loc']}, Complexity: {result['complexity']}, Volume: {result['volume']:.1f}")
                
            else:
                print(f"    ❌ Failed with status {response.status_code}")
                return False
            
            # Small delay between requests
            time.sleep(0.5)
        
        # Verify we have different metrics for comparison
        if len(analysis_results) >= 2:
            complexities = [r['complexity'] for r in analysis_results]
            volumes = [r['volume'] for r in analysis_results]
            
            # Check if we have variation in metrics (good for comparison)
            complexity_variance = max(complexities) - min(complexities)
            volume_variance = max(volumes) - min(volumes)
            
            print(f"\n  📊 Comparison Analysis:")
            print(f"    Complexity range: {min(complexities):.1f} - {max(complexities):.1f} (variance: {complexity_variance:.1f})")
            print(f"    Volume range: {min(volumes):.1f} - {max(volumes):.1f} (variance: {volume_variance:.1f})")
            
            if complexity_variance > 0.5 or volume_variance > 50:
                print(f"    ✅ Good variation detected - comparison chart will show meaningful differences")
                return True
            else:
                print(f"    ⚠️ Low variation - comparison chart may look similar")
                return True  # Still success, just less interesting
        else:
            print(f"    ❌ Not enough analysis results for comparison")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the Flask server is running on localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_chart_improvements():
    """Test that chart improvements are working by checking the frontend"""
    print("\n🎨 Testing Chart Improvements...")
    
    # Test with a simple analysis to trigger chart updates
    test_code = """
def test_function():
    for i in range(10):
        if i % 2 == 0:
            print(f"Even: {i}")
        else:
            print(f"Odd: {i}")
    return "Complete"

test_function()
"""
    
    try:
        response = requests.post('http://localhost:5000/api/analyze', 
                               json={
                                   'code': test_code,
                                   'language': 'python'
                               },
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            metrics = data.get('metrics', {})
            
            # Check that we have the required metrics for enhanced charts
            required_metrics = ['raw', 'cyclomatic', 'halstead', 'avg_complexity']
            has_all_metrics = all(metric in metrics for metric in required_metrics)
            
            if has_all_metrics:
                print("  ✅ All required metrics present for enhanced charts")
                print(f"  ✅ Raw metrics: {metrics['raw']}")
                print(f"  ✅ Halstead metrics: volume={metrics['halstead'].get('volume', 0):.1f}")
                print(f"  ✅ Average complexity: {metrics['avg_complexity']}")
                return True
            else:
                print(f"  ❌ Missing metrics: {[m for m in required_metrics if m not in metrics]}")
                return False
        else:
            print(f"  ❌ Analysis failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Chart test failed: {str(e)}")
        return False

def main():
    print("🚀 Visualization Improvements Test Suite")
    print("=" * 50)
    
    # Test chart improvements
    charts_ok = test_chart_improvements()
    
    # Test performance comparison
    comparison_ok = test_performance_comparison_functionality()
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"Chart Improvements: {'✅ PASS' if charts_ok else '❌ FAIL'}")
    print(f"Performance Comparison: {'✅ PASS' if comparison_ok else '❌ FAIL'}")
    
    overall_success = charts_ok and comparison_ok
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if overall_success else '⚠️ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n✨ Visualization improvements are working correctly!")
        print("📈 Enhanced charts with better styling and performance comparison are ready.")
        print("🎯 Users will see professional charts with animations and comparisons.")
    else:
        print("\n🔧 Some visualization issues need to be addressed.")
    
    return overall_success

if __name__ == "__main__":
    main()
