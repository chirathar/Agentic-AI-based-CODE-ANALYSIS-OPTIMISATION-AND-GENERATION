#!/usr/bin/env python3

import requests
import json
import time

def test_frontend_flow():
    """Test the exact flow that the frontend JavaScript follows"""
    print("🔍 Testing Frontend Analysis Flow...")
    
    test_code = """
def hello_world():
    print("Hello, World!")
    return True

hello_world()
"""
    
    try:
        print("1. Testing main analysis endpoint...")
        
        # Step 1: Main analysis (this should work)
        metrics_response = requests.post('http://localhost:5000/api/analyze', 
                                       json={
                                           'code': test_code,
                                           'language': 'python'
                                       },
                                       timeout=10)
        
        print(f"   Analysis Status: {metrics_response.status_code}")
        
        if not metrics_response.ok:
            print("   ❌ Main analysis failed - this is the problem!")
            return False
        
        metrics_data = metrics_response.json()
        print("   ✅ Main analysis successful")
        
        # Step 2: Test all optimization endpoints (these should work too)
        print("\n2. Testing optimization endpoints...")
        
        endpoints = [
            ('/api/optimize/suggestions', 'optimizationSuggestions'),
            ('/api/optimize/refactoring', 'refactoringSuggestions'),
            ('/api/optimize/performance', 'performanceSuggestions'),
            ('/api/optimize/optimized-code', 'optimizedCode')
        ]
        
        for endpoint, container_id in endpoints:
            try:
                response = requests.post(f'http://localhost:5000{endpoint}', 
                                       json={
                                           'code': test_code,
                                           'metrics': metrics_data['metrics'],
                                           'language': 'python'
                                       },
                                       timeout=15)
                
                print(f"   {endpoint}: {response.status_code}")
                
                if not response.ok:
                    print(f"   ❌ {endpoint} failed - this could cause analysis failure!")
                    return False
                    
            except Exception as e:
                print(f"   ❌ {endpoint} error: {str(e)}")
                return False
        
        print("   ✅ All optimization endpoints working")
        
        # Step 3: Test response format
        print("\n3. Checking response format...")
        
        required_fields = ['success', 'metrics', 'code_length', 'language']
        for field in required_fields:
            if field not in metrics_data:
                print(f"   ❌ Missing field: {field}")
                return False
        
        print("   ✅ Response format is correct")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Frontend flow test failed: {str(e)}")
        return False

def test_specific_error_scenarios():
    """Test specific scenarios that might cause 'analysis failed'"""
    print("\n🧪 Testing Error Scenarios...")
    
    # Test 1: Empty code
    print("1. Testing empty code...")
    try:
        response = requests.post('http://localhost:5000/api/analyze', 
                               json={'code': '', 'language': 'python'},
                               timeout=10)
        print(f"   Empty code status: {response.status_code}")
        if response.status_code == 400:
            print("   ✅ Empty code properly rejected")
    except Exception as e:
        print(f"   ❌ Empty code test error: {str(e)}")
    
    # Test 2: Invalid language
    print("2. Testing invalid language...")
    try:
        response = requests.post('http://localhost:5000/api/analyze', 
                               json={'code': 'print("test")', 'language': 'invalid'},
                               timeout=10)
        print(f"   Invalid language status: {response.status_code}")
        if response.status_code == 400:
            print("   ✅ Invalid language properly rejected")
    except Exception as e:
        print(f"   ❌ Invalid language test error: {str(e)}")
    
    # Test 3: Malformed JSON
    print("3. Testing malformed request...")
    try:
        response = requests.post('http://localhost:5000/api/analyze', 
                               data="invalid json",
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        print(f"   Malformed JSON status: {response.status_code}")
        if response.status_code >= 400:
            print("   ✅ Malformed JSON properly rejected")
    except Exception as e:
        print(f"   ❌ Malformed JSON test error: {str(e)}")

def check_javascript_issues():
    """Check for common JavaScript issues"""
    print("\n🔍 Checking for JavaScript Issues...")
    
    issues = []
    
    # Check if required DOM elements might be missing
    print("1. Checking for potential DOM element issues...")
    
    required_elements = [
        'codeInput',
        'analyzeBtn', 
        'analysisStatus',
        'analysisResults',
        'locValue',
        'complexityValue',
        'commentsValue',
        'volumeValue',
        'complexityChart',
        'compositionChart',
        'performanceComparisonChart'
    ]
    
    for element_id in required_elements:
        print(f"   Required element: {element_id}")
    
    print("   💡 If any of these elements are missing from HTML, analysis could fail")
    
    # Check for potential async issues
    print("\n2. Checking for potential async issues...")
    print("   💡 The loadAllAnalysisData function uses await - if any endpoint fails, entire analysis fails")
    print("   💡 This could be the cause of 'analysis failed' even when main analysis works")
    
    return issues

def main():
    print("🚀 Frontend Analysis Debug Tool")
    print("=" * 40)
    
    # Test the frontend flow
    flow_ok = test_frontend_flow()
    
    # Test error scenarios
    test_specific_error_scenarios()
    
    # Check for JavaScript issues
    check_javascript_issues()
    
    print("\n📊 Debug Results:")
    print("=" * 20)
    print(f"Frontend Flow: {'✅ WORKING' if flow_ok else '❌ FAILED'}")
    
    if flow_ok:
        print("\n✅ Backend is working perfectly!")
        print("💡 The issue is likely in the frontend JavaScript:")
        print("   1. Missing DOM elements in HTML")
        print("   2. JavaScript errors in browser console")
        print("   3. Network issues preventing API calls")
        print("   4. Timing issues with async operations")
        print("\n🔧 RECOMMENDATIONS:")
        print("   1. Open browser developer tools and check console for errors")
        print("   2. Check Network tab to see if API calls are being made")
        print("   3. Verify all required HTML elements exist")
        print("   4. Try analyzing with simple code to isolate the issue")
    else:
        print("\n❌ Backend issues found - fix these first")
    
    return flow_ok

if __name__ == "__main__":
    main()
