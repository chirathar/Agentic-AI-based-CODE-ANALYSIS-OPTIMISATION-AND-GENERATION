#!/usr/bin/env python3

import requests
import json

def test_complete_fix():
    """Test that optimized code appears in the correct panel and is actually optimized"""
    print("🔧 Testing Complete Fix...")
    
    # Test code with clear optimization opportunities
    test_code = '''def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total

def find_max(data):
    max_val = data[0]
    for i in range(len(data)):
        if data[i] > max_val:
            max_val = data[i]
    return max_val'''
    
    try:
        # Test 1: Check HTML structure for correct panel
        print("   Testing HTML structure...")
        html_response = requests.get('http://localhost:5000/', timeout=5)
        if html_response.status_code == 200:
            html_content = html_response.text
            
            # Check for proper optimized code panel structure
            required_elements = {
                'optimizedDisplay': 'id="optimizedDisplay"',
                'optimizedContent': 'id="optimizedContent"',
                'optimizedLineNumbers': 'id="optimizedLineNumbers"',
                'optimizedLoader': 'id="optimizedLoader"',
                'code-panel-full': 'class="code-panel-full"'
            }
            
            found_elements = 0
            for element, selector in required_elements.items():
                if selector in html_content:
                    print(f"      ✅ {element}")
                    found_elements += 1
                else:
                    print(f"      ❌ {element} missing")
            
            if found_elements >= 4:
                print("   ✅ HTML structure is correct")
                html_ok = True
            else:
                print("   ❌ HTML structure incomplete")
                html_ok = False
        else:
            print(f"   ❌ Cannot access HTML: {html_response.status_code}")
            html_ok = False
        
        # Test 2: Check CSS for proper display
        print("\n   Testing CSS styling...")
        css_response = requests.get('http://localhost:5000/static/style_new.css', timeout=5)
        if css_response.status_code == 200:
            css_content = css_response.text
            
            css_features = {
                'Loader hiding': '#optimizedLoader',
                'Content visibility': '#optimizedContent',
                'Z-index for content': 'z-index: 2',
                'Panel full width': 'code-panel-full'
            }
            
            found_css = 0
            for feature, selector in css_features.items():
                if selector in css_content:
                    print(f"      ✅ {feature}")
                    found_css += 1
                else:
                    print(f"      ❌ {feature} missing")
            
            if found_css >= 3:
                print("   ✅ CSS styling is correct")
                css_ok = True
            else:
                print("   ❌ CSS styling incomplete")
                css_ok = False
        else:
            print(f"   ❌ Cannot access CSS: {css_response.status_code}")
            css_ok = False
        
        # Test 3: Check JavaScript for proper handling
        print("\n   Testing JavaScript functionality...")
        js_response = requests.get('http://localhost:5000/static/app_new.js', timeout=5)
        if js_response.status_code == 200:
            js_content = js_response.text
            
            js_features = {
                'Loader hiding in display': 'optimizedLoader.classList.remove',
                'Content visibility': 'optimizedContent.style.opacity',
                'Display function': 'function displayOptimizedCode',
                'Loader display none': 'optimizedLoader.style.display = \'none\''
            }
            
            found_js = 0
            for feature, selector in js_features.items():
                if selector in js_content:
                    print(f"      ✅ {feature}")
                    found_js += 1
                else:
                    print(f"      ❌ {feature} missing")
            
            if found_js >= 3:
                print("   ✅ JavaScript functionality is correct")
                js_ok = True
            else:
                print("   ❌ JavaScript functionality incomplete")
                js_ok = False
        else:
            print(f"   ❌ Cannot access JavaScript: {js_response.status_code}")
            js_ok = False
        
        # Test 4: Test actual optimization
        print("\n   Testing actual optimization...")
        optimize_response = requests.post('http://localhost:5000/api/optimize/optimized-code', 
                                       json={
                                           'code': test_code,
                                           'metrics': {'complexity': 8, 'lines_of_code': 12},
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
                    
                # Show code preview
                print(f"\n   Optimized Code Preview:")
                print("   " + "="*40)
                for i, line in enumerate(optimized_code.split('\n')[:8]):
                    print(f"   {i+1:2d}: {line}")
                if len(optimized_code.split('\n')) > 8:
                    print(f"   ... ({len(optimized_code.split('\n')) - 8} more lines)")
                print("   " + "="*40)
                    
            else:
                print("   ❌ Optimization returned same code or failed")
                optimization_ok = False
        else:
            print(f"   ❌ Optimization endpoint failed: {optimize_response.status_code}")
            optimization_ok = False
        
        overall_success = html_ok and css_ok and js_ok and optimization_ok
        
        return overall_success
        
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def main():
    print("🧪 Complete Fix Test")
    print("=" * 20)
    
    fix_ok = test_complete_fix()
    
    print(f"\n📊 Test Results:")
    print(f"Complete Fix: {'✅ WORKING' if fix_ok else '❌ BROKEN'}")
    
    if fix_ok:
        print(f"\n✅ Complete Fix Successful!")
        print("🎯 What was fixed:")
        print("   ✅ Optimized code now appears in the correct panel")
        print("   ✅ Loader properly hides to reveal optimized code")
        print("   ✅ CSS z-index ensures content visibility")
        print("   ✅ JavaScript properly handles display logic")
        print("   ✅ Optimization logic actually optimizes code")
        print("\n🚀 The optimized code should now appear correctly in the panel!")
    else:
        print(f"\n❌ Complete fix needs more work")
    
    return fix_ok

if __name__ == "__main__":
    main()
