#!/usr/bin/env python3

import requests
import json

def test_optimization_endpoints():
    """Test all optimization endpoints that are called after analysis"""
    print("🔍 Testing Optimization Endpoints...")
    
    test_code = """
def hello_world():
    print("Hello, World!")
    return True

hello_world()
"""
    
    test_metrics = {
        "avg_complexity": 1.0,
        "cyclomatic": {"hello_world": {"complexity": 1, "line": 1}},
        "halstead": {"volume": 55.35, "difficulty": 2.92},
        "raw": {"loc": 5, "comments": 0}
    }
    
    endpoints = [
        '/api/optimize/suggestions',
        '/api/optimize/refactoring', 
        '/api/optimize/performance',
        '/api/optimize/optimized-code'
    ]
    
    results = {}
    
    for endpoint in endpoints:
        try:
            print(f"\nTesting {endpoint}...")
            
            response = requests.post(f'http://localhost:5000{endpoint}', 
                                   json={
                                       'code': test_code,
                                       'metrics': test_metrics,
                                       'language': 'python'
                                   },
                                   timeout=15)
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ Success")
                results[endpoint] = True
            else:
                print(f"  ❌ Failed: {response.text}")
                results[endpoint] = False
                
        except requests.exceptions.Timeout:
            print(f"  ❌ Timeout")
            results[endpoint] = False
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results[endpoint] = False
    
    return results

def main():
    print("🚀 Optimization Endpoints Test")
    print("=" * 40)
    
    results = test_optimization_endpoints()
    
    print("\n📊 Results Summary:")
    print("=" * 20)
    
    all_passed = True
    for endpoint, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{endpoint}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print(f"\n✅ All optimization endpoints working!")
        print("💡 The issue might be elsewhere in the frontend")
    else:
        print(f"\n❌ Some optimization endpoints are failing!")
        print("💡 This could cause the 'analysis failed' error")
        print("🔧 The frontend tries to load all optimization data after analysis")
    
    return all_passed

if __name__ == "__main__":
    main()
