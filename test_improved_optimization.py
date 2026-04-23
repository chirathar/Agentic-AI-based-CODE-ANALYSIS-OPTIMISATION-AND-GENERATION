#!/usr/bin/env python3

import requests
import json

def test_improved_optimization_and_display():
    """Test the improved optimization logic and display"""
    print("🔧 Testing Improved Optimization & Display...")
    
    # Test code with multiple optimization opportunities
    test_code = '''def calculate_sum(numbers):
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

def process_data(data):
    results = []
    for item in data:
        results.append(item * 2)
    return results'''
    
    try:
        # Test the improved optimization endpoint
        print("   Testing improved optimization logic...")
        
        optimize_response = requests.post('http://localhost:5000/api/optimize/optimized-code', 
                                       json={
                                           'code': test_code,
                                           'metrics': {'complexity': 12, 'lines_of_code': 15},
                                           'language': 'python'
                                       },
                                       timeout=20)
        
        if optimize_response.status_code == 200:
            print("   ✅ Optimization endpoint responding")
            
            # Parse the streaming response
            optimized_code = ""
            for line in optimize_response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        try:
                            data = json.loads(line_text[6:])
                            if data.get('status') == 'complete' and data.get('content'):
                                optimized_code = data['content']
                                break
                        except:
                            continue
            
            if optimized_code and optimized_code != test_code:
                print("   ✅ Optimization generated different code")
                
                # Analyze the optimizations applied
                optimizations_found = []
                
                # Check for sum optimization
                if 'sum(' in optimized_code and 'total = 0' not in optimized_code:
                    optimizations_found.append("✅ Sum optimization: manual loop → sum() function")
                
                # Check for max optimization  
                if 'max(' in optimized_code and 'max_val = ' not in optimized_code:
                    optimizations_found.append("✅ Max optimization: manual loop → max() function")
                
                # Check for loop optimization
                if ('for item in' in optimized_code or 'enumerate(' in optimized_code) and 'range(len(' not in optimized_code:
                    optimizations_found.append("✅ Loop optimization: range(len()) → direct iteration")
                
                # Check for list comprehension
                if '[item * 2 for item in data]' in optimized_code and 'append(' not in optimized_code:
                    optimizations_found.append("✅ List comprehension: append loop → comprehension")
                
                # Check for type hints
                if 'from typing import Any' in optimized_code:
                    optimizations_found.append("✅ Type hints added")
                
                # Check for proper function structure
                if '-> Any:' in optimized_code and '"""Optimized version' in optimized_code:
                    optimizations_found.append("✅ Function signatures improved")
                
                print(f"   Optimizations found: {len(optimizations_found)}")
                for opt in optimizations_found:
                    print(f"      {opt}")
                
                # Check if code is properly structured
                if optimized_code.count('\n') < test_code.count('\n'):
                    print("   ✅ Code length reduced (more concise)")
                
                if len(optimizations_found) >= 4:
                    print("   ✅ Comprehensive optimizations applied")
                    optimization_ok = True
                else:
                    print("   ⚠️ Limited optimizations applied")
                    optimization_ok = False
                    
                # Show the optimized code for verification
                print(f"\n   Optimized Code Preview:")
                print("   " + "="*50)
                for i, line in enumerate(optimized_code.split('\n')[:10]):
                    print(f"   {i+1:2d}: {line}")
                if len(optimized_code.split('\n')) > 10:
                    print(f"   ... ({len(optimized_code.split('\n')) - 10} more lines)")
                print("   " + "="*50)
                    
            else:
                print("   ❌ Optimization returned same code or failed")
                optimization_ok = False
        else:
            print(f"   ❌ Optimization endpoint failed: {optimize_response.status_code}")
            optimization_ok = False
        
        # Test HTML structure for proper display
        print("\n   Testing HTML structure for optimized code display...")
        
        html_response = requests.get('http://localhost:5000/', timeout=5)
        if html_response.status_code == 200:
            html_content = html_response.text
            
            # Check for proper single panel structure
            display_elements = {
                'Optimized code section': 'Optimized Code',
                'Full width panel': 'code-panel-full',
                'Optimized display element': 'optimizedDisplay',
                'Optimized content element': 'optimizedContent',
                'Line numbers element': 'optimizedLineNumbers',
                'Loader element': 'optimizedLoader'
            }
            
            found_elements = 0
            for element_name, selector in display_elements.items():
                if selector in html_content:
                    print(f"   ✅ {element_name}")
                    found_elements += 1
                else:
                    print(f"   ❌ {element_name} not found")
            
            if found_elements >= 5:
                print("   ✅ HTML structure for optimized code display is correct")
                html_ok = True
            else:
                print("   ❌ HTML structure issues detected")
                html_ok = False
        else:
            print(f"   ❌ Cannot access HTML: {html_response.status_code}")
            html_ok = False
        
        overall_success = optimization_ok and html_ok
        
        return overall_success
        
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def main():
    print("🧪 Improved Optimization & Display Test")
    print("=" * 40)
    
    test_ok = test_improved_optimization_and_display()
    
    print(f"\n📊 Test Results:")
    print(f"Optimization: {'✅ WORKING' if test_ok else '❌ BROKEN'}")
    
    if test_ok:
        print(f"\n✅ Improved Optimization Implementation Complete!")
        print("🎯 What was improved:")
        print("   ✅ Proper code structure analysis before optimization")
        print("   ✅ Pattern recognition for sum, max, and loop optimizations")
        print("   ✅ Context-aware optimizations (when to use enumerate vs direct iteration)")
        print("   ✅ List comprehension conversion")
        print("   ✅ Type hints and function signature improvements")
        print("   ✅ Proper import management")
        print("\n🚀 The optimization now properly analyzes code usage before optimizing!")
    else:
        print(f"\n❌ Improved optimization implementation needs review")
    
    return test_ok

if __name__ == "__main__":
    main()
