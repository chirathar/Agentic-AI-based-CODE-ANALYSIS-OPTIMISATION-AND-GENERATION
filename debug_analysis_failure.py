#!/usr/bin/env python3

import requests
import json
import traceback

def test_analysis_endpoint():
    """Test the analysis endpoint directly to identify the issue"""
    print("🔍 Debugging Analysis Failure...")
    
    # Test with simple Python code
    test_code = """
def hello_world():
    print("Hello, World!")
    return True

hello_world()
"""
    
    print(f"Testing with code:\n{test_code}")
    print("\n" + "="*50)
    
    try:
        # Test the API endpoint
        print("1. Testing API connection...")
        response = requests.post('http://localhost:5000/api/analyze', 
                               json={
                                   'code': test_code,
                                   'language': 'python'
                               },
                               timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("   ✅ API connection successful")
            data = response.json()
            print(f"   Response Data: {json.dumps(data, indent=2)}")
            
            # Check if metrics are valid
            if 'metrics' in data:
                metrics = data['metrics']
                print(f"\n2. Checking metrics structure...")
                
                required_sections = ['raw', 'cyclomatic', 'halstead', 'avg_complexity']
                for section in required_sections:
                    if section in metrics:
                        print(f"   ✅ {section}: {type(metrics[section])}")
                    else:
                        print(f"   ❌ Missing: {section}")
                        return False
                
                return True
            else:
                print("   ❌ No metrics in response")
                return False
        else:
            print(f"   ❌ API request failed")
            print(f"   Error Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server - Flask server may not be running")
        print("   💡 Try running: python app.py")
        return False
    except requests.exceptions.Timeout:
        print("   ❌ Request timeout - server may be overloaded")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {str(e)}")
        traceback.print_exc()
        return False

def test_backend_directly():
    """Test the backend analyzer directly without API"""
    print("\n2. Testing backend analyzer directly...")
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from multilang_analyzer import MultiLanguageCodeAnalyzer
        
        test_code = """
def hello_world():
    print("Hello, World!")
    return True

hello_world()
"""
        
        analyzer = MultiLanguageCodeAnalyzer(test_code, 'python')
        metrics = analyzer.get_all_metrics()
        
        print("   ✅ Backend analyzer working")
        print(f"   Metrics: {json.dumps(metrics, indent=2, default=str)}")
        return True
        
    except Exception as e:
        print(f"   ❌ Backend analyzer failed: {str(e)}")
        traceback.print_exc()
        return False

def check_flask_server():
    """Check if Flask server is running and accessible"""
    print("\n3. Checking Flask server status...")
    
    try:
        # Test basic connection
        response = requests.get('http://localhost:5000/', timeout=5)
        print(f"   Server Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Flask server is running")
            return True
        else:
            print("   ❌ Flask server returned unexpected status")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Flask server is not running")
        print("   💡 Start the server with: python app.py")
        return False
    except Exception as e:
        print(f"   ❌ Error checking server: {str(e)}")
        return False

def main():
    print("🚀 Analysis Failure Debug Tool")
    print("=" * 40)
    
    # Check Flask server
    server_ok = check_flask_server()
    
    if not server_ok:
        print("\n❌ MAIN ISSUE: Flask server is not running")
        print("💡 SOLUTION: Run 'python app.py' in the SEPM directory")
        return False
    
    # Test backend directly
    backend_ok = test_backend_directly()
    
    # Test API endpoint
    api_ok = test_analysis_endpoint()
    
    print("\n📊 Debug Results:")
    print("=" * 20)
    print(f"Flask Server: {'✅ RUNNING' if server_ok else '❌ NOT RUNNING'}")
    print(f"Backend Analyzer: {'✅ WORKING' if backend_ok else '❌ FAILED'}")
    print(f"API Endpoint: {'✅ WORKING' if api_ok else '❌ FAILED'}")
    
    if server_ok and backend_ok and api_ok:
        print("\n✅ Everything is working correctly!")
        print("💡 The issue might be in the frontend JavaScript")
        return True
    else:
        print("\n🔧 Issues found that need to be fixed")
        return False

if __name__ == "__main__":
    main()
