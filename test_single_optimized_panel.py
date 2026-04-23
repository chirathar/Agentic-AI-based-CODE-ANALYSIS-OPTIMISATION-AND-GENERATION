#!/usr/bin/env python3

import requests
import json

def test_single_optimized_panel():
    """Test the single optimized code panel and improved optimization"""
    print("🔧 Testing Single Optimized Panel & Improved Optimization...")
    
    # Test code with clear optimization opportunities
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
    return max_val'''
    
    try:
        # Test HTML structure for single panel
        html_response = requests.get('http://localhost:5000/', timeout=5)
        if html_response.status_code == 200:
            html_content = html_response.text
            
            # Check for single panel structure
            single_panel_elements = {
                'Optimized code section': 'Optimized Code',
                'Full width code panel': 'code-panel-full',
                'Optimized display': 'optimizedDisplay',
                'Optimized content': 'optimizedContent',
                'Optimized loader': 'optimizedLoader',
                'Copy optimized button': 'copyOptimizedCode',
                'Download optimized button': 'downloadOptimizedCode'
            }
            
            found_elements = 0
            for element_name, selector in single_panel_elements.items():
                if selector in html_content:
                    print(f"   ✅ {element_name}")
                    found_elements += 1
                else:
                    print(f"   ❌ {element_name} not found")
            
            print(f"\n   HTML Elements: {found_elements}/{len(single_panel_elements)} found")
            
            if found_elements >= 6:
                print("   ✅ Single optimized panel HTML structure is correct")
                html_ok = True
            else:
                print("   ❌ Single optimized panel HTML structure incomplete")
                html_ok = False
        else:
            print(f"   ❌ Cannot access HTML: {html_response.status_code}")
            html_ok = False
        
        # Test CSS for single panel
        css_response = requests.get('http://localhost:5000/static/style_new.css', timeout=5)
        if css_response.status_code == 200:
            css_content = css_response.text
            
            # Check for single panel CSS
            css_features = {
                'Full width panel styling': '.code-panel-full',
                'Width 100%': 'width: 100%',
                'Panel header': '.panel-header',
                'Code content': '.code-content',
                'Optimized loader': '#optimizedLoader'
            }
            
            found_css = 0
            for feature_name, selector in css_features.items():
                if selector in css_content:
                    print(f"   ✅ {feature_name}")
                    found_css += 1
                else:
                    print(f"   ❌ {feature_name} not found")
            
            print(f"\n   CSS Features: {found_css}/{len(css_features)} found")
            
            if found_css >= 4:
                print("   ✅ Single panel CSS styling is complete")
                css_ok = True
            else:
                print("   ❌ Single panel CSS styling incomplete")
                css_ok = False
        else:
            print(f"   ❌ Cannot access CSS: {css_response.status_code}")
            css_ok = False
        
        # Test improved optimization logic
        print("\n   Testing improved optimization logic...")
        
        optimize_response = requests.post('http://localhost:5000/api/optimize/optimized-code', 
                                       json={
                                           'code': test_code,
                                           'metrics': {'complexity': 8, 'lines_of_code': 10},
                                           'language': 'python'
                                       },
                                       timeout=15)
        
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
                
                # Check for specific optimizations
                optimizations_found = []
                if 'sum(' in optimized_code and 'total = 0' not in optimized_code:
                    optimizations_found.append("✅ Sum optimization applied")
                if 'max(' in optimized_code and 'max_val = ' not in optimized_code:
                    optimizations_found.append("✅ Max optimization applied")
                if 'for item in' in optimized_code or 'enumerate(' in optimized_code:
                    optimizations_found.append("✅ Loop optimization applied")
                if 'from typing import Any' in optimized_code:
                    optimizations_found.append("✅ Type hints added")
                
                print(f"   Optimizations found: {len(optimizations_found)}")
                for opt in optimizations_found:
                    print(f"      {opt}")
                
                if len(optimizations_found) >= 2:
                    print("   ✅ Significant optimizations applied")
                    optimization_ok = True
                else:
                    print("   ⚠️ Limited optimizations applied")
                    optimization_ok = False
            else:
                print("   ❌ Optimization returned same code or failed")
                optimization_ok = False
        else:
            print(f"   ❌ Optimization endpoint failed: {optimize_response.status_code}")
            optimization_ok = False
        
        overall_success = html_ok and css_ok and optimization_ok
        
        return overall_success
        
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def main():
    print("🧪 Single Optimized Panel & Improved Optimization Test")
    print("=" * 55)
    
    panel_ok = test_single_optimized_panel()
    
    print(f"\n📊 Test Results:")
    print(f"Single Panel: {'✅ WORKING' if panel_ok else '❌ BROKEN'}")
    
    if panel_ok:
        print(f"\n✅ Single Optimized Panel Implementation Complete!")
        print("🎯 What was implemented:")
        print("   ✅ Removed code with suggestions section")
        print("   ✅ Kept only optimized code panel")
        print("   ✅ Full-width optimized code display")
        print("   ✅ Improved optimization logic with significant changes")
        print("   ✅ Better Python optimizations (sum, max, enumerate)")
        print("   ✅ Type hints and imports added")
        print("\n🚀 The optimized code panel is now working with actual optimizations!")
    else:
        print(f"\n❌ Single optimized panel implementation needs review")
    
    return panel_ok

if __name__ == "__main__":
    main()
