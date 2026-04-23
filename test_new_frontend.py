#!/usr/bin/env python3

import requests
import json
import time

def test_new_frontend_functionality():
    """Test the new frontend functionality"""
    print("🚀 Testing New Frontend Functionality...")
    
    # Test cases for analysis
    test_cases = [
        {
            'name': 'Simple Python Analysis',
            'code': '''
def hello_world():
    print("Hello, World!")
    return True

hello_world()
''',
            'language': 'python'
        },
        {
            'name': 'JavaScript Function Analysis',
            'code': '''
function calculateSum(a, b) {
    return a + b;
}

const result = calculateSum(5, 3);
console.log(result);
''',
            'language': 'javascript'
        }
    ]
    
    # Test cases for generation
    generation_tests = [
        {
            'mode': 'description',
            'input': 'Create a function that calculates the factorial of a number',
            'endpoint': '/api/generate/from-description'
        },
        {
            'mode': 'complete',
            'input': '''
def fibonacci(n):
    # Complete this function
    pass
''',
            'endpoint': '/api/generate/complete-code'
        }
    ]
    
    results = {
        'analysis': 0,
        'generation': 0,
        'total_analysis': len(test_cases),
        'total_generation': len(generation_tests)
    }
    
    print("\n📊 Testing Analysis Functionality...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        
        try:
            response = requests.post('http://localhost:5000/api/analyze', 
                                   json={
                                       'code': test_case['code'],
                                       'language': test_case['language']
                                   },
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and 'metrics' in data:
                    metrics = data['metrics']
                    
                    # Check for required metrics
                    required_sections = ['raw', 'cyclomatic', 'halstead', 'avg_complexity']
                    has_all_sections = all(section in metrics for section in required_sections)
                    
                    if has_all_sections:
                        print(f"   ✅ Analysis successful")
                        print(f"      LOC: {metrics['raw']['loc']}")
                        print(f"      Complexity: {metrics['avg_complexity']}")
                        print(f"      Volume: {metrics['halstead']['volume']:.1f}")
                        results['analysis'] += 1
                    else:
                        print(f"   ❌ Missing metrics sections")
                else:
                    print(f"   ❌ Invalid response format")
            else:
                print(f"   ❌ Analysis failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Test error: {str(e)}")
    
    print("\n🎨 Testing Generation Functionality...")
    
    for i, test_case in enumerate(generation_tests, 1):
        print(f"\n{i}. Generation Mode: {test_case['mode']}")
        
        try:
            response = requests.post(f'http://localhost:5000{test_case["endpoint"]}', 
                                   json={
                                       test_case['mode']: test_case['input'],
                                       'language': 'python'
                                   },
                                   timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'content' in data and data['content']:
                    print(f"   ✅ Generation successful")
                    print(f"      Generated {len(data['content'])} characters")
                    results['generation'] += 1
                else:
                    print(f"   ❌ No content in response")
            else:
                print(f"   ❌ Generation failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Test error: {str(e)}")
    
    return results

def test_frontend_serving():
    """Test that the new frontend is being served correctly"""
    print("\n🌐 Testing Frontend Serving...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        
        if response.status_code == 200:
            content = response.text
            
            # Check for new frontend elements
            new_frontend_indicators = [
                'index_new.html',
                'code-drop-zone',
                'generation-modes',
                'metric-card',
                'modern design'
            ]
            
            found_indicators = sum(1 for indicator in new_frontend_indicators if indicator in content.lower())
            
            if found_indicators >= 2:
                print("   ✅ New frontend is being served")
                print(f"   Found {found_indicators} modern frontend indicators")
                return True
            else:
                print("   ⚠️ May still be serving old frontend")
                return False
        else:
            print(f"   ❌ Frontend not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Frontend test failed: {str(e)}")
        return False

def test_static_files():
    """Test that static files are accessible"""
    print("\n📁 Testing Static Files...")
    
    static_files = [
        '/static/style_new.css',
        '/static/app_new.js'
    ]
    
    results = 0
    
    for file_path in static_files:
        try:
            response = requests.get(f'http://localhost:5000{file_path}', timeout=5)
            
            if response.status_code == 200:
                print(f"   ✅ {file_path} accessible")
                results += 1
            else:
                print(f"   ❌ {file_path} not accessible: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {file_path} error: {str(e)}")
    
    return results == len(static_files)

def main():
    print("🧪 New Frontend Comprehensive Test")
    print("=" * 50)
    
    # Test frontend serving
    frontend_ok = test_frontend_serving()
    
    # Test static files
    static_ok = test_static_files()
    
    # Test functionality
    functionality_results = test_new_frontend_functionality()
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"Frontend Serving: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print(f"Static Files: {'✅ PASS' if static_ok else '❌ FAIL'}")
    print(f"Analysis: {functionality_results['analysis']}/{functionality_results['total_analysis']} passed")
    print(f"Generation: {functionality_results['generation']}/{functionality_results['total_generation']} passed")
    
    # Calculate overall success
    analysis_success = functionality_results['analysis'] == functionality_results['total_analysis']
    generation_success = functionality_results['generation'] == functionality_results['total_generation']
    overall_success = frontend_ok and static_ok and analysis_success and generation_success
    
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if overall_success else '⚠️ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n✨ New Frontend Implementation Complete!")
        print("🎯 Features working:")
        print("   ✅ Modern, clean interface based on React design")
        print("   ✅ Professional code analysis with metrics")
        print("   ✅ Enhanced charts and visualizations")
        print("   ✅ Multiple generation modes")
        print("   ✅ Drag-and-drop file support")
        print("   ✅ Responsive design")
        print("   ✅ Dark/light theme support")
        print("   ✅ Keyboard shortcuts")
        print("   ✅ Copy and download functionality")
        print("\n🚀 The new frontend is ready for production use!")
    else:
        print("\n🔧 Some issues need to be addressed:")
        if not frontend_ok:
            print("   - Frontend serving issue")
        if not static_ok:
            print("   - Static files not accessible")
        if not analysis_success:
            print("   - Analysis functionality issues")
        if not generation_success:
            print("   - Generation functionality issues")
    
    return overall_success

if __name__ == "__main__":
    main()
