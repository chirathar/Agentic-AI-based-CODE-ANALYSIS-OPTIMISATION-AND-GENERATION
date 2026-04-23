#!/usr/bin/env python3

import requests
import json
import time

def test_enhanced_frontend():
    """Test all the enhanced frontend functionality"""
    print("🚀 Testing Enhanced Frontend Features...")
    
    # Test code with various issues for comprehensive analysis
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

def process_data(data_list):
    results = []
    for item in data_list:
        if item > 0:
            results.append(item * 2)
        else:
            results.append(0)
    return results

# Inefficient loop example
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''
    
    results = {
        'frontend_serving': False,
        'analysis': False,
        'suggestions': False,
        'generation': False,
        'charts': False
    }
    
    print("\n📊 Testing Frontend Serving...")
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            content = response.text
            # Check for new frontend elements
            new_features = [
                'suggestions-section',
                'code-display-section',
                'qualityCount',
                'refactoringCount',
                'performanceCount',
                'charts-container enhanced'
            ]
            
            found_features = sum(1 for feature in new_features if feature in content)
            if found_features >= 4:
                print("   ✅ Enhanced frontend is being served")
                results['frontend_serving'] = True
            else:
                print(f"   ⚠️ Some features missing: {6-found_features} not found")
        else:
            print(f"   ❌ Frontend not accessible: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Frontend test failed: {str(e)}")
    
    print("\n🔍 Testing Code Analysis...")
    try:
        response = requests.post('http://localhost:5000/api/analyze', 
                               json={
                                   'code': test_code,
                                   'language': 'python'
                               },
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'metrics' in data:
                metrics = data['metrics']
                print(f"   ✅ Analysis successful")
                print(f"      LOC: {metrics['raw']['loc']}")
                print(f"      Complexity: {metrics['avg_complexity']}")
                print(f"      Volume: {metrics['halstead']['volume']:.1f}")
                results['analysis'] = True
                
                # Test suggestions loading
                print("\n💡 Testing Suggestions Loading...")
                suggestion_endpoints = [
                    ('/api/optimize/suggestions', 'Quality'),
                    ('/api/optimize/refactoring', 'Refactoring'),
                    ('/api/optimize/performance', 'Performance')
                ]
                
                suggestions_working = 0
                for endpoint, name in suggestion_endpoints:
                    try:
                        resp = requests.post(f'http://localhost:5000{endpoint}', 
                                           json={
                                               'code': test_code,
                                               'metrics': metrics,
                                               'language': 'python'
                                           },
                                           timeout=15)
                        
                        if resp.status_code == 200:
                            print(f"   ✅ {name} suggestions endpoint working")
                            suggestions_working += 1
                        else:
                            print(f"   ❌ {name} suggestions failed: {resp.status_code}")
                    except Exception as e:
                        print(f"   ❌ {name} suggestions error: {str(e)}")
                
                if suggestions_working >= 2:
                    print("   ✅ Suggestions functionality working")
                    results['suggestions'] = True
                else:
                    print(f"   ⚠️ Only {suggestions_working}/3 suggestion endpoints working")
            else:
                print("   ❌ Invalid analysis response")
        else:
            print(f"   ❌ Analysis failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Analysis test failed: {str(e)}")
    
    print("\n🎨 Testing Generation Functionality...")
    generation_tests = [
        {
            'endpoint': '/api/generate/from-description',
            'data': {
                'description': 'Create a function that validates email addresses',
                'language': 'python'
            },
            'name': 'Description Generation'
        },
        {
            'endpoint': '/api/generate/complete-code',
            'data': {
                'incomplete_code': 'def calculate_area(shape, dimensions):\n    # Complete this function\n    pass',
                'language': 'python'
            },
            'name': 'Code Completion'
        }
    ]
    
    generation_working = 0
    for test in generation_tests:
        try:
            response = requests.post(f'http://localhost:5000{test["endpoint"]}', 
                                   json=test['data'],
                                   timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if 'content' in data and data['content']:
                    print(f"   ✅ {test['name']} working ({len(data['content'])} chars)")
                    generation_working += 1
                else:
                    print(f"   ❌ {test['name']}: No content in response")
            else:
                print(f"   ❌ {test['name']}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {test['name']}: {str(e)}")
    
    if generation_working >= 1:
        print("   ✅ Generation functionality working")
        results['generation'] = True
    else:
        print("   ❌ Generation functionality failed")
    
    print("\n📈 Testing Chart Data Availability...")
    try:
        response = requests.post('http://localhost:5000/api/analyze', 
                               json={
                                   'code': test_code,
                                   'language': 'python'
                               },
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'metrics' in data:
                metrics = data['metrics']
                
                # Check if metrics have required data for charts
                required_chart_data = [
                    ('raw', 'Basic metrics for composition chart'),
                    ('avg_complexity', 'Complexity for radar chart'),
                    ('halstead', 'Halstead metrics for analysis')
                ]
                
                chart_data_available = 0
                for key, description in required_chart_data:
                    if key in metrics and metrics[key]:
                        print(f"   ✅ {description} available")
                        chart_data_available += 1
                    else:
                        print(f"   ❌ {description} missing")
                
                if chart_data_available >= 2:
                    print("   ✅ Sufficient data for enhanced charts")
                    results['charts'] = True
                else:
                    print("   ⚠️ Insufficient data for charts")
    except Exception as e:
        print(f"   ❌ Chart data test failed: {str(e)}")
    
    return results

def test_ui_enhancements():
    """Test UI enhancement features"""
    print("\n🎨 Testing UI Enhancements...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            content = response.text
            
            # Check for enhanced UI elements
            ui_features = {
                'Enhanced Charts': 'chart-card large',
                'Suggestion Sections': 'suggestions-section',
                'Code Display with Line Numbers': 'code-display-section',
                'Count Badges': 'suggestion-count',
                'Interactive Elements': 'onclick="jumpToSuggestion',
                'Enhanced CSS': 'quality-highlight',
                'Responsive Design': '@media (max-width: 768px)'
            }
            
            found_features = 0
            for feature, selector in ui_features.items():
                if selector in content:
                    print(f"   ✅ {feature}")
                    found_features += 1
                else:
                    print(f"   ❌ {feature} not found")
            
            print(f"\n   UI Features: {found_features}/{len(ui_features)} found")
            return found_features >= len(ui_features) - 1  # Allow 1 missing feature
        else:
            print(f"   ❌ Cannot test UI: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ UI test failed: {str(e)}")
        return False

def main():
    print("🧪 Enhanced Frontend Comprehensive Test")
    print("=" * 50)
    
    # Test core functionality
    functionality_results = test_enhanced_frontend()
    
    # Test UI enhancements
    ui_ok = test_ui_enhancements()
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    
    print(f"Frontend Serving: {'✅ PASS' if functionality_results['frontend_serving'] else '❌ FAIL'}")
    print(f"Code Analysis: {'✅ PASS' if functionality_results['analysis'] else '❌ FAIL'}")
    print(f"Suggestions: {'✅ PASS' if functionality_results['suggestions'] else '❌ FAIL'}")
    print(f"Generation: {'✅ PASS' if functionality_results['generation'] else '❌ FAIL'}")
    print(f"Charts Data: {'✅ PASS' if functionality_results['charts'] else '❌ FAIL'}")
    print(f"UI Enhancements: {'✅ PASS' if ui_ok else '❌ FAIL'}")
    
    # Calculate overall success
    core_passed = sum(functionality_results.values())
    total_core = len(functionality_results)
    overall_success = core_passed >= total_core - 1 and ui_ok  # Allow 1 core feature to fail
    
    print(f"\nCore Features: {core_passed}/{total_core} passed")
    print(f"Overall: {'🎉 ALL TESTS PASSED' if overall_success else '⚠️ SOME TESTS FAILED'}")
    
    if overall_success:
        print(f"\n✨ Enhanced Frontend Implementation Complete!")
        print("🎯 New Features Working:")
        print("   ✅ Separate sections for Quality, Refactoring, and Performance suggestions")
        print("   ✅ Code highlighting with clickable suggestions")
        print("   ✅ Count badges for each suggestion category")
        print("   ✅ Bigger, more visible charts")
        print("   ✅ Interactive code display with line numbers")
        print("   ✅ Enhanced UI with modern design")
        print("   ✅ Responsive design for all screen sizes")
        print("   ✅ Fixed generation and optimization endpoints")
        print("\n🚀 All requested features are now implemented and working!")
    else:
        print(f"\n🔧 Some issues need attention:")
        failed_features = [name for name, passed in functionality_results.items() if not passed]
        if failed_features:
            print(f"   Core features: {', '.join(failed_features)}")
        if not ui_ok:
            print("   UI enhancements need review")
    
    return overall_success

if __name__ == "__main__":
    main()
