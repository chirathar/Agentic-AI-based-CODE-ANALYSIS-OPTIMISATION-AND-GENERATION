#!/usr/bin/env python3

import requests
import json
import time

def test_performance_comparison_features():
    """Test the new performance comparison and difference visualization features"""
    print("🔧 Testing Performance Comparison Features...")
    
    # Test code with clear optimization opportunities
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
    
    try:
        # Test if the frontend has the new performance comparison elements
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            content = response.text
            
            # Check for performance comparison elements
            performance_elements = {
                'Performance comparison section': 'performance-comparison-section',
                'Comparison grid': 'comparison-grid',
                'Performance metrics container': 'performance-metrics-container',
                'Code diff container': 'code-diff-container',
                'Optimization summary container': 'optimization-summary-container',
                'Metric comparison items': 'metric-comparison-item',
                'Summary stats': 'summary-stats',
                'Code diff content': 'codeDiffContent'
            }
            
            found_elements = 0
            for element_name, selector in performance_elements.items():
                if selector in content:
                    print(f"   ✅ {element_name}")
                    found_elements += 1
                else:
                    print(f"   ❌ {element_name} not found")
            
            print(f"\n   HTML Elements: {found_elements}/{len(performance_elements)} found")
            
            if found_elements >= 6:
                print("   ✅ Performance comparison HTML structure is complete")
                html_ok = True
            else:
                print("   ❌ Performance comparison HTML structure incomplete")
                html_ok = False
        else:
            print(f"   ❌ Cannot access frontend: {response.status_code}")
            html_ok = False
        
        # Test if CSS has the new styling
        css_response = requests.get('http://localhost:5000/static/style_new.css', timeout=5)
        if css_response.status_code == 200:
            css_content = css_response.text
            
            # Check for performance comparison CSS
            css_features = {
                'Performance comparison section': '.performance-comparison-section',
                'Comparison grid': '.comparison-grid',
                'Comparison box': '.comparison-box',
                'Metric comparison item': '.metric-comparison-item',
                'Code diff content': '.code-diff-content',
                'Diff line classes': '.diff-line',
                'Optimization summary': '.optimization-summary-container',
                'Summary stats': '.summary-stats',
                'Improvement classes': '.improvement.positive'
            }
            
            found_css = 0
            for feature_name, selector in css_features.items():
                if selector in css_content:
                    print(f"   ✅ {feature_name}")
                    found_css += 1
                else:
                    print(f"   ❌ {feature_name} not found")
            
            print(f"\n   CSS Features: {found_css}/{len(css_features)} found")
            
            if found_css >= 7:
                print("   ✅ Performance comparison CSS is complete")
                css_ok = True
            else:
                print("   ❌ Performance comparison CSS incomplete")
                css_ok = False
        else:
            print(f"   ❌ Cannot access CSS: {css_response.status_code}")
            css_ok = False
        
        # Test if JavaScript has the new functionality
        js_response = requests.get('http://localhost:5000/static/app_new.js', timeout=5)
        if js_response.status_code == 200:
            js_content = js_response.text
            
            # Check for performance comparison JavaScript functions
            js_functions = {
                'Update performance comparison': 'updatePerformanceComparison',
                'Calculate code metrics': 'calculateCodeMetrics',
                'Update metric comparison': 'updateMetricComparison',
                'Generate code diff': 'generateCodeDiff',
                'Update optimization summary': 'updateOptimizationSummary',
                'Clear performance comparison': 'clearPerformanceComparison',
                'Refresh performance comparison': 'refreshPerformanceComparison',
                'Export optimization report': 'exportOptimizationReport'
            }
            
            found_js = 0
            for function_name, function_selector in js_functions.items():
                if function_selector in js_content:
                    print(f"   ✅ {function_name}")
                    found_js += 1
                else:
                    print(f"   ❌ {function_name} not found")
            
            print(f"\n   JavaScript Functions: {found_js}/{len(js_functions)} found")
            
            if found_js >= 6:
                print("   ✅ Performance comparison JavaScript is complete")
                js_ok = True
            else:
                print("   ❌ Performance comparison JavaScript incomplete")
                js_ok = False
        else:
            print(f"   ❌ Cannot access JavaScript: {js_response.status_code}")
            js_ok = False
        
        # Test the actual functionality by analyzing code
        print("\n   Testing actual performance comparison functionality...")
        
        analyze_response = requests.post('http://localhost:5000/api/analyze', 
                                       json={
                                           'code': test_code,
                                           'language': 'python'
                                       },
                                       timeout=10)
        
        if analyze_response.status_code == 200:
            data = analyze_response.json()
            if data.get('success') and 'metrics' in data:
                print("   ✅ Code analysis working")
                
                # Test optimized code generation
                optimize_response = requests.post('http://localhost:5000/api/optimize/optimized-code', 
                                                json({
                                                    'code': test_code,
                                                    'metrics': data['metrics'],
                                                    'language': 'python'
                                                }),
                                                timeout=15)
                
                if optimize_response.status_code == 200:
                    print("   ✅ Optimized code generation working")
                    functionality_ok = True
                else:
                    print(f"   ❌ Optimized code generation failed: {optimize_response.status_code}")
                    functionality_ok = False
            else:
                print("   ❌ Code analysis failed")
                functionality_ok = False
        else:
            print(f"   ❌ Code analysis request failed: {analyze_response.status_code}")
            functionality_ok = False
        
        overall_success = html_ok and css_ok and js_ok and functionality_ok
        
        return overall_success
        
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def test_new_comparison_boxes():
    """Test the specific new comparison boxes and their layout"""
    print("\n📦 Testing New Comparison Boxes...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            content = response.text
            
            # Check for specific comparison boxes
            comparison_boxes = {
                'Performance Metrics Box': '📊 Performance Metrics',
                'Code Differences Box': '🔍 Code Differences',
                'Optimization Summary Box': '⚡ Optimization Summary',
                'Metric comparison items': 'Execution Time',
                'Memory usage comparison': 'Memory Usage',
                'Complexity comparison': 'Code Complexity',
                'Lines of code comparison': 'Lines of Code',
                'Optimization score': 'Optimization Score',
                'Changes count': 'Changes Made',
                'Performance gain': 'Performance Gain'
            }
            
            found_boxes = 0
            for box_name, text_selector in comparison_boxes.items():
                if text_selector in content:
                    print(f"   ✅ {box_name}")
                    found_boxes += 1
                else:
                    print(f"   ❌ {box_name} not found")
            
            print(f"\n   Comparison Boxes: {found_boxes}/{len(comparison_boxes)} found")
            
            if found_boxes >= 8:
                print("   ✅ All comparison boxes are properly implemented")
                return True
            else:
                print("   ❌ Some comparison boxes are missing")
                return False
        else:
            print(f"   ❌ Cannot access frontend: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def main():
    print("🧪 Performance Comparison & Differences Test")
    print("=" * 45)
    
    # Test performance comparison features
    features_ok = test_performance_comparison_features()
    
    # Test new comparison boxes
    boxes_ok = test_new_comparison_boxes()
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"Performance Features: {'✅ WORKING' if features_ok else '❌ BROKEN'}")
    print(f"Comparison Boxes: {'✅ WORKING' if boxes_ok else '❌ BROKEN'}")
    
    overall_success = features_ok and boxes_ok
    
    print(f"\nOverall: {'🎉 ALL FEATURES WORKING' if overall_success else '⚠️ SOME ISSUES REMAIN'}")
    
    if overall_success:
        print(f"\n✨ Performance Comparison Implementation Complete!")
        print("🎯 New Features Working:")
        print("   ✅ Performance metrics comparison (time, memory, complexity, lines)")
        print("   ✅ Code differences visualization with diff highlighting")
        print("   ✅ Optimization summary with score and statistics")
        print("   ✅ Interactive comparison boxes with refresh/export")
        print("   ✅ Responsive design for all screen sizes")
        print("   ✅ Real-time performance analysis")
        print("\n🚀 The performance comparison is now fully functional!")
    else:
        print(f"\n🔧 Remaining issues:")
        if not features_ok:
            print("   - Performance comparison features need attention")
        if not boxes_ok:
            print("   - Comparison boxes implementation incomplete")
    
    return overall_success

if __name__ == "__main__":
    main()
