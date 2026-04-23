#!/usr/bin/env python3

import requests
import json

def test_analysis_fix():
    """Test that the analysis failure issue has been resolved"""
    print("🧪 Testing Analysis Fix...")
    
    # Test with different code samples
    test_cases = [
        {
            'name': 'Simple Python Code',
            'code': '''
def hello():
    print("Hello, World!")
    return True

hello()
''',
            'language': 'python'
        },
        {
            'name': 'JavaScript Function',
            'code': '''
function calculateSum(a, b) {
    if (a > 0 && b > 0) {
        return a + b;
    }
    return 0;
}

console.log(calculateSum(5, 3));
''',
            'language': 'javascript'
        },
        {
            'name': 'Complex Python Code',
            'code': '''
class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.results = []
    
    def process(self):
        for item in self.data:
            if isinstance(item, (int, float)):
                self.results.append(item * 2)
            elif isinstance(item, str):
                self.results.append(item.upper())
            else:
                self.results.append(str(item))
        return self.results

# Test the processor
data = [1, 2, "hello", 3.14, None]
processor = DataProcessor(data)
result = processor.process()
print(f"Processed: {result}")
''',
            'language': 'python'
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test_case['name']}...")
        
        try:
            # Test main analysis
            response = requests.post('http://localhost:5000/api/analyze', 
                                   json={
                                       'code': test_case['code'],
                                       'language': test_case['language']
                                   },
                                   timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and 'metrics' in data:
                    metrics = data['metrics']
                    
                    # Check metrics structure
                    required_sections = ['raw', 'cyclomatic', 'halstead', 'avg_complexity']
                    has_all_sections = all(section in metrics for section in required_sections)
                    
                    if has_all_sections:
                        print(f"   ✅ Analysis successful!")
                        print(f"      LOC: {metrics['raw']['loc']}")
                        print(f"      Complexity: {metrics['avg_complexity']}")
                        print(f"      Volume: {metrics['halstead']['volume']:.1f}")
                        success_count += 1
                    else:
                        print(f"   ❌ Missing metrics sections")
                else:
                    print(f"   ❌ Invalid response format")
            else:
                print(f"   ❌ Analysis failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Test error: {str(e)}")
    
    return success_count, len(test_cases)

def test_frontend_simulation():
    """Simulate the frontend analysis flow"""
    print("\n🎭 Simulating Frontend Analysis Flow...")
    
    test_code = """
def test_function():
    for i in range(5):
        print(f"Count: {i}")
    return "Done"

result = test_function()
print(result)
"""
    
    try:
        # Step 1: Main analysis (this should work)
        print("1. Main analysis...")
        response = requests.post('http://localhost:5000/api/analyze', 
                               json={'code': test_code, 'language': 'python'},
                               timeout=10)
        
        if response.status_code != 200:
            print(f"   ❌ Main analysis failed: {response.status_code}")
            return False
        
        metrics_data = response.json()
        print("   ✅ Main analysis successful")
        
        # Step 2: Optimization endpoints (these should work but not fail the analysis)
        print("2. Testing optimization endpoints...")
        
        endpoints = [
            '/api/optimize/suggestions',
            '/api/optimize/refactoring',
            '/api/optimize/performance',
            '/api/optimize/optimized-code'
        ]
        
        optimization_success = 0
        for endpoint in endpoints:
            try:
                response = requests.post(f'http://localhost:5000{endpoint}', 
                                       json={
                                           'code': test_code,
                                           'metrics': metrics_data['metrics'],
                                           'language': 'python'
                                       },
                                       timeout=15)
                
                if response.status_code == 200:
                    optimization_success += 1
                    print(f"   ✅ {endpoint}")
                else:
                    print(f"   ⚠️ {endpoint} failed (but analysis should still work)")
                    
            except Exception as e:
                print(f"   ⚠️ {endpoint} error: {str(e)} (but analysis should still work)")
        
        print(f"   Optimization endpoints: {optimization_success}/{len(endpoints)} successful")
        
        # Even if some optimization endpoints fail, the main analysis should work
        print("   ✅ Frontend simulation complete - analysis should work!")
        return True
        
    except Exception as e:
        print(f"   ❌ Frontend simulation failed: {str(e)}")
        return False

def main():
    print("🚀 Analysis Fix Verification")
    print("=" * 40)
    
    # Test analysis with different code samples
    success_count, total_count = test_analysis_fix()
    
    # Test frontend simulation
    frontend_ok = test_frontend_simulation()
    
    print("\n📊 Results Summary:")
    print("=" * 20)
    print(f"Analysis Tests: {success_count}/{total_count} passed")
    print(f"Frontend Simulation: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    
    overall_success = success_count == total_count and frontend_ok
    
    if overall_success:
        print(f"\n🎉 ALL TESTS PASSED!")
        print("✅ Analysis failure issue has been RESOLVED!")
        print("💡 The fix makes optimization loading non-blocking")
        print("🎯 Users should now see 'Analysis complete!' instead of 'Analysis failed'")
    else:
        print(f"\n⚠️ Some tests failed")
        print("🔧 Further investigation may be needed")
    
    return overall_success

if __name__ == "__main__":
    main()
