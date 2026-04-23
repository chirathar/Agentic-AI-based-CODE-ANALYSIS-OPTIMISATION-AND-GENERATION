#!/usr/bin/env python3

import requests
import json
import time

def test_generation_endpoints():
    """Test all generation endpoints to identify issues"""
    print("🔍 Debugging Generation Endpoints...")
    
    # Test cases for each generation mode
    test_cases = [
        {
            'endpoint': '/api/generate/from-description',
            'data': {
                'description': 'Create a function that calculates the factorial of a number',
                'language': 'python'
            },
            'name': 'Description Generation'
        },
        {
            'endpoint': '/api/generate/complete-code',
            'data': {
                'incomplete_code': 'def fibonacci(n):\n    # Complete this function\n    pass',
                'language': 'python'
            },
            'name': 'Code Completion'
        },
        {
            'endpoint': '/api/generate/functions',
            'data': {
                'description': 'Create functions for a calculator that can add, subtract, multiply, and divide',
                'language': 'python'
            },
            'name': 'Function Generation'
        },
        {
            'endpoint': '/api/generate/improve',
            'data': {
                'code': 'def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b',
                'idea': 'Add input validation and error handling',
                'language': 'python'
            },
            'name': 'Code Improvement'
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        print(f"\n📝 Testing {test_case['name']}...")
        
        try:
            response = requests.post(f'http://localhost:5000{test_case["endpoint"]}', 
                                   json=test_case['data'],
                                   timeout=15)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Success")
                    print(f"   Response keys: {list(data.keys())}")
                    
                    if 'content' in data:
                        content_length = len(data['content'])
                        print(f"   Content length: {content_length} characters")
                        print(f"   Content preview: {data['content'][:200]}...")
                        results[test_case['name']] = 'SUCCESS'
                    else:
                        print(f"   ❌ No content in response")
                        print(f"   Response: {data}")
                        results[test_case['name']] = 'NO_CONTENT'
                        
                except json.JSONDecodeError as e:
                    print(f"   ❌ JSON decode error: {e}")
                    print(f"   Raw response: {response.text[:200]}...")
                    results[test_case['name']] = 'JSON_ERROR'
                    
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
                results[test_case['name']] = f'HTTP_{response.status_code}'
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection error - server not running")
            results[test_case['name']] = 'CONNECTION_ERROR'
        except requests.exceptions.Timeout:
            print(f"   ❌ Request timeout")
            results[test_case['name']] = 'TIMEOUT'
        except Exception as e:
            print(f"   ❌ Unexpected error: {str(e)}")
            results[test_case['name']] = f'ERROR: {str(e)}'
    
    return results

def test_optimization_endpoints():
    """Test optimization endpoints"""
    print("\n🔍 Debugging Optimization Endpoints...")
    
    test_code = '''
def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total

def find_max(numbers):
    max_val = numbers[0]
    for i in range(len(numbers)):
        if numbers[i] > max_val:
            max_val = numbers[i]
    return max_val
'''
    
    test_metrics = {
        'raw': {'loc': 15, 'lloc': 12, 'comments': 0, 'blank': 3},
        'avg_complexity': 2.0,
        'halstead': {'volume': 100.0, 'difficulty': 5.0}
    }
    
    endpoints = [
        '/api/optimize/suggestions',
        '/api/optimize/refactoring',
        '/api/optimize/performance'
    ]
    
    results = {}
    
    for endpoint in endpoints:
        print(f"\n📝 Testing {endpoint}...")
        
        try:
            response = requests.post(f'http://localhost:5000{endpoint}', 
                                   json={
                                       'code': test_code,
                                       'metrics': test_metrics,
                                       'language': 'python'
                                   },
                                   timeout=15)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                # Check if it's streaming response
                content_type = response.headers.get('content-type', '')
                
                if 'text/event-stream' in content_type:
                    print(f"   ✅ Streaming response")
                    # Read a few chunks to see if it's working
                    chunks = []
                    try:
                        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                            if chunk:
                                chunks.append(chunk[:100])  # Just preview
                                if len(chunks) >= 3:  # Read first 3 chunks
                                    break
                        print(f"   Streaming chunks: {len(chunks)}")
                        results[endpoint] = 'STREAMING_SUCCESS'
                    except Exception as e:
                        print(f"   ❌ Streaming error: {e}")
                        results[endpoint] = 'STREAMING_ERROR'
                else:
                    try:
                        data = response.json()
                        print(f"   ✅ JSON response")
                        print(f"   Response keys: {list(data.keys())}")
                        results[endpoint] = 'JSON_SUCCESS'
                    except json.JSONDecodeError:
                        print(f"   ❌ Invalid JSON response")
                        results[endpoint] = 'INVALID_JSON'
                        
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
                results[endpoint] = f'HTTP_{response.status_code}'
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection error - server not running")
            results[endpoint] = 'CONNECTION_ERROR'
        except Exception as e:
            print(f"   ❌ Unexpected error: {str(e)}")
            results[endpoint] = f'ERROR: {str(e)}'
    
    return results

def check_server_status():
    """Check if server is running and accessible"""
    print("🔍 Checking Server Status...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        print(f"   Server Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Server is running and accessible")
            return True
        else:
            print(f"   ❌ Server returned error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Server is not running or not accessible")
        print("   💡 Start the server with: python app.py")
        return False
    except Exception as e:
        print(f"   ❌ Error checking server: {str(e)}")
        return False

def main():
    print("🚀 Generation & Optimization Debug Tool")
    print("=" * 50)
    
    # Check server status first
    server_ok = check_server_status()
    
    if not server_ok:
        print("\n❌ Server is not running - cannot proceed with tests")
        return False
    
    # Test generation endpoints
    generation_results = test_generation_endpoints()
    
    # Test optimization endpoints
    optimization_results = test_optimization_endpoints()
    
    print("\n📊 Debug Results Summary:")
    print("=" * 30)
    
    print("\nGeneration Endpoints:")
    for name, result in generation_results.items():
        status = "✅" if result == 'SUCCESS' else "❌"
        print(f"   {status} {name}: {result}")
    
    print("\nOptimization Endpoints:")
    for endpoint, result in optimization_results.items():
        status = "✅" if 'SUCCESS' in result else "❌"
        print(f"   {status} {endpoint}: {result}")
    
    # Identify issues
    generation_issues = [name for name, result in generation_results.items() if result != 'SUCCESS']
    optimization_issues = [endpoint for endpoint, result in optimization_results.items() if 'SUCCESS' not in result]
    
    if generation_issues or optimization_issues:
        print(f"\n🔧 Issues Found:")
        if generation_issues:
            print(f"   Generation: {', '.join(generation_issues)}")
        if optimization_issues:
            print(f"   Optimization: {', '.join(optimization_issues)}")
        
        print(f"\n💡 Recommendations:")
        if 'CONNECTION_ERROR' in generation_results.values() or 'CONNECTION_ERROR' in optimization_results.values():
            print("   - Start the Flask server: python app.py")
        if 'JSON_ERROR' in generation_results.values():
            print("   - Check generation endpoint implementations")
        if 'TIMEOUT' in generation_results.values():
            print("   - Check LLM service availability and API keys")
        if 'STREAMING_ERROR' in optimization_results.values():
            print("   - Fix streaming response handling")
    else:
        print(f"\n✅ All endpoints are working correctly!")
    
    return len(generation_issues) == 0 and len(optimization_issues) == 0

if __name__ == "__main__":
    main()
