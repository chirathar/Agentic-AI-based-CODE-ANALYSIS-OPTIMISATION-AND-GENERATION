#!/usr/bin/env python3

import requests
import json

def test_analysis_api():
    """Test the analysis API endpoint to ensure it returns proper structure"""
    print("🧪 Testing Analysis API...")
    
    # Test data
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(fibonacci(i))
"""
    
    try:
        # Make API request
        response = requests.post('http://localhost:5000/api/analyze', 
                               json={
                                   'code': test_code,
                                   'language': 'python'
                               },
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ API Response Structure:")
            print(f"  Success: {data.get('success')}")
            print(f"  Language: {data.get('language')}")
            
            metrics = data.get('metrics', {})
            print(f"\n  Metrics Structure:")
            
            # Check raw metrics
            raw = metrics.get('raw', {})
            print(f"    Raw metrics:")
            print(f"      LOC: {raw.get('loc')}")
            print(f"      LLOC: {raw.get('lloc')}")
            print(f"      Comments: {raw.get('comments')}")
            print(f"      Blank: {raw.get('blank')}")
            
            # Check cyclomatic complexity
            cyclomatic = metrics.get('cyclomatic', {})
            print(f"    Cyclomatic complexity:")
            for func, data in cyclomatic.items():
                print(f"      {func}: {data.get('complexity')}")
            
            # Check halstead metrics
            halstead = metrics.get('halstead', {})
            print(f"    Halstead metrics:")
            print(f"      Volume: {halstead.get('volume')}")
            print(f"      Difficulty: {halstead.get('difficulty')}")
            print(f"      Effort: {halstead.get('effort')}")
            
            # Check average complexity
            print(f"    Average complexity: {metrics.get('avg_complexity')}")
            
            # Verify all required fields are present
            required_fields = ['raw', 'cyclomatic', 'halstead', 'avg_complexity']
            missing_fields = [field for field in required_fields if field not in metrics]
            
            if missing_fields:
                print(f"\n❌ Missing fields: {missing_fields}")
                return False
            else:
                print(f"\n✅ All required metrics fields present!")
                return True
                
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the Flask server is running on localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_frontend_compatibility():
    """Test that the API response structure matches what the frontend expects"""
    print("\n🔗 Testing Frontend Compatibility...")
    
    test_code = """
def calculate_sum(a, b):
    return a + b

result = calculate_sum(5, 3)
print(result)
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
            
            # Check the structure that frontend JavaScript expects
            frontend_checks = {
                'metrics.raw.loc': metrics.get('raw', {}).get('loc') is not None,
                'metrics.raw.lloc': metrics.get('raw', {}).get('lloc') is not None,
                'metrics.raw.comments': metrics.get('raw', {}).get('comments') is not None,
                'metrics.halstead.volume': metrics.get('halstead', {}).get('volume') is not None,
                'metrics.halstead.difficulty': metrics.get('halstead', {}).get('difficulty') is not None,
                'metrics.avg_complexity': metrics.get('avg_complexity') is not None,
                'metrics.cyclomatic': len(metrics.get('cyclomatic', {})) > 0
            }
            
            print("Frontend compatibility checks:")
            all_passed = True
            for check, passed in frontend_checks.items():
                status = "✅" if passed else "❌"
                print(f"  {status} {check}")
                if not passed:
                    all_passed = False
            
            if all_passed:
                print("\n✅ All frontend compatibility checks passed!")
                return True
            else:
                print("\n❌ Some frontend compatibility checks failed!")
                return False
                
        else:
            print(f"❌ API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Compatibility test failed: {str(e)}")
        return False

def main():
    print("🚀 Analysis Display Test Suite")
    print("=" * 40)
    
    # Test API functionality
    api_ok = test_analysis_api()
    
    # Test frontend compatibility
    frontend_ok = test_frontend_compatibility()
    
    print("\n📊 Test Results:")
    print("=" * 20)
    print(f"API Test: {'✅ PASS' if api_ok else '❌ FAIL'}")
    print(f"Frontend Compatibility: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    
    overall_success = api_ok and frontend_ok
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if overall_success else '⚠️ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n✨ Analysis display should now work correctly!")
        print("📈 Metrics, charts, and detailed results should be visible.")
    else:
        print("\n🔧 Some issues remain that need to be addressed.")
    
    return overall_success

if __name__ == "__main__":
    main()
