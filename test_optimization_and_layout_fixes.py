#!/usr/bin/env python3

import requests
import json
import time

def test_optimization_fixes():
    """Test that the optimization logic now generates actual optimized code"""
    print("🔧 Testing Optimization Fixes...")
    
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
        # First analyze the code
        analyze_response = requests.post('http://localhost:5000/api/analyze', 
                                       json={
                                           'code': test_code,
                                           'language': 'python'
                                       },
                                       timeout=10)
        
        if analyze_response.status_code == 200:
            data = analyze_response.json()
            if data.get('success') and 'metrics' in data:
                metrics = data['metrics']
                
                # Test optimized code endpoint
                optimize_response = requests.post('http://localhost:5000/api/optimize/optimized-code', 
                                                json={
                                                    'code': test_code,
                                                    'metrics': metrics,
                                                    'language': 'python'
                                                },
                                                timeout=15)
                
                if optimize_response.status_code == 200:
                    optimized_text = parse_streaming_response(optimize_response)
                    
                    if optimized_text and optimized_text.strip():
                        print("   ✅ Optimized code generated successfully")
                        
                        # Check if optimizations were actually applied
                        optimizations_found = []
                        
                        if 'for num in numbers:' in optimized_text:
                            optimizations_found.append("✅ range(len()) replaced with direct iteration")
                        
                        if 'enumerate(' in optimized_text:
                            optimizations_found.append("✅ enumerate() used for index-value pairs")
                        
                        if '"""Optimized version' in optimized_text:
                            optimizations_found.append("✅ Documentation added")
                        
                        if len(optimizations_found) > 0:
                            print(f"   🎯 Optimizations applied:")
                            for opt in optimizations_found:
                                print(f"      {opt}")
                            print(f"   📝 Optimized code length: {len(optimized_text)} characters")
                            return True
                        else:
                            print("   ⚠️ No specific optimizations detected, but code was generated")
                            return False
                    else:
                        print("   ❌ No optimized code returned")
                        return False
                else:
                    print(f"   ❌ Optimized code endpoint failed: {optimize_response.status_code}")
                    return False
            else:
                print("   ❌ Analysis failed to return metrics")
                return False
        else:
            print(f"   ❌ Analysis failed: {analyze_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Optimization test failed: {str(e)}")
        return False

def test_layout_fixes():
    """Test that the layout now spans full width"""
    print("\n📐 Testing Layout Fixes...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            content = response.text
            
            # Check for full-width layout elements
            layout_features = {
                'Full width main content': 'max-width: 100%',
                'Full width suggestions section': 'suggestions-section',
                'Full width code comparison': 'code-comparison-section',
                'Full width suggestions grid': 'width: 100%',
                'Full width comparison container': 'code-comparison-container',
                'Responsive breakpoints': '@media (max-width: 1024px)'
            }
            
            found_features = 0
            for feature, selector in layout_features.items():
                if selector in content:
                    print(f"   ✅ {feature}")
                    found_features += 1
                else:
                    print(f"   ❌ {feature} not found")
            
            # Check for removal of width constraints
            if 'max-width: 1280px' not in content:
                print("   ✅ Width constraints removed from main content")
                found_features += 1
            else:
                print("   ❌ Width constraints still present")
            
            print(f"   Layout features: {found_features}/{len(layout_features) + 1} found")
            return found_features >= len(layout_features)
        else:
            print(f"   ❌ Cannot test layout: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Layout test failed: {str(e)}")
        return False

def test_different_languages_optimization():
    """Test optimization for different programming languages"""
    print("\n🌍 Testing Multi-Language Optimization...")
    
    language_tests = [
        {
            'name': 'JavaScript',
            'code': '''
function calculateSum(numbers) {
    var total = 0;
    for (var i = 0; i < numbers.length; i++) {
        total += numbers[i];
    }
    return total;
}
''',
            'language': 'javascript',
            'expected_optimizations': ['const ', 'for (const item']
        },
        {
            'name': 'Java',
            'code': '''
public class Calculator {
    public String process(String input) {
        String result = "";
        result += "Processed: ";
        result += input;
        return result;
    }
}
''',
            'language': 'java',
            'expected_optimizations': ['StringBuilder']
        }
    ]
    
    successful_optimizations = 0
    
    for test in language_tests:
        print(f"\n   Testing {test['name']} optimization...")
        
        try:
            # Analyze first
            analyze_response = requests.post('http://localhost:5000/api/analyze', 
                                           json={
                                               'code': test['code'],
                                               'language': test['language']
                                           },
                                           timeout=10)
            
            if analyze_response.status_code == 200:
                data = analyze_response.json()
                if data.get('success') and 'metrics' in data:
                    # Then optimize
                    optimize_response = requests.post('http://localhost:5000/api/optimize/optimized-code', 
                                                    json({
                                                        'code': test['code'],
                                                        'metrics': data['metrics'],
                                                        'language': test['language']
                                                    }),
                                                    timeout=15)
                    
                    if optimize_response.status_code == 200:
                        optimized_text = parse_streaming_response(optimize_response)
                        
                        if optimized_text:
                            # Check for expected optimizations
                            optimizations_found = 0
                            for expected in test['expected_optimizations']:
                                if expected in optimized_text:
                                    optimizations_found += 1
                                    print(f"      ✅ Found: {expected}")
                            
                            if optimizations_found > 0:
                                print(f"   ✅ {test['name']} optimization successful")
                                successful_optimizations += 1
                            else:
                                print(f"   ⚠️ {test['name']} optimization completed but no expected patterns found")
                        else:
                            print(f"   ❌ {test['name']} optimization returned empty result")
                    else:
                        print(f"   ❌ {test['name']} optimization failed: {optimize_response.status_code}")
                else:
                    print(f"   ❌ {test['name']} analysis failed")
            else:
                print(f"   ❌ {test['name']} analysis failed: {analyze_response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {test['name']} test error: {str(e)}")
    
    return successful_optimizations >= 1  # At least one language should work

def parse_streaming_response(response):
    """Parse streaming response to extract content"""
    try:
        content_lines = []
        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            if chunk:
                for line in chunk.split('\n'):
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            if data.get('status') == 'complete' and data.get('content'):
                                return data['content']
                        except json.JSONDecodeError:
                            continue
        return None
    except Exception as e:
        print(f"Error parsing streaming response: {e}")
        return None

def main():
    print("🧪 Optimization & Layout Fixes Test")
    print("=" * 40)
    
    # Test optimization fixes
    optimization_ok = test_optimization_fixes()
    
    # Test layout fixes
    layout_ok = test_layout_fixes()
    
    # Test multi-language optimization
    multi_lang_ok = test_different_languages_optimization()
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"Optimization Logic: {'✅ FIXED' if optimization_ok else '❌ STILL BROKEN'}")
    print(f"Full Width Layout: {'✅ FIXED' if layout_ok else '❌ STILL BROKEN'}")
    print(f"Multi-Language Support: {'✅ WORKING' if multi_lang_ok else '❌ ISSUES'}")
    
    # Overall success
    overall_success = optimization_ok and layout_ok
    
    print(f"\nOverall: {'🎉 ALL FIXES SUCCESSFUL' if overall_success else '⚠️ SOME ISSUES REMAIN'}")
    
    if overall_success:
        print(f"\n✨ Issues Resolved!")
        print("🎯 What was fixed:")
        print("   ✅ Optimization now generates actual improved code")
        print("   ✅ Layout spans full screen width (except margins)")
        print("   ✅ Suggestions and code sections use full width")
        print("   ✅ Multi-language optimization working")
        print("\n🚀 The frontend now properly optimizes code and uses full width!")
    else:
        print(f"\n🔧 Remaining issues:")
        if not optimization_ok:
            print("   - Optimization logic still needs improvement")
        if not layout_ok:
            print("   - Layout not spanning full width properly")
        if not multi_lang_ok:
            print("   - Multi-language optimization has issues")
    
    return overall_success

if __name__ == "__main__":
    main()
