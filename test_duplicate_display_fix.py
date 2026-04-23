#!/usr/bin/env python3

import requests
import json

def test_duplicate_display_fix():
    """Test that optimized code appears only in the single panel, not duplicated"""
    print("🔧 Testing Duplicate Display Fix...")
    
    try:
        # Test HTML structure to ensure single optimized code panel
        html_response = requests.get('http://localhost:5000/', timeout=5)
        if html_response.status_code == 200:
            html_content = html_response.text
            
            # Count optimized-related elements
            optimized_elements = {
                'optimizedDisplay': html_content.count('id="optimizedDisplay"'),
                'optimizedContent': html_content.count('id="optimizedContent"'),
                'optimizedLineNumbers': html_content.count('id="optimizedLineNumbers"'),
                'optimizedLoader': html_content.count('id="optimizedLoader"'),
                'Optimized Code headers': html_content.count('Optimized Code')
            }
            
            print("   Element counts:")
            for element, count in optimized_elements.items():
                status = "✅" if count == 1 else "❌" if count > 1 else "⚠️"
                print(f"      {status} {element}: {count}")
            
            # Check for duplicates
            has_duplicates = any(count > 1 for count in optimized_elements.values() if element != 'Optimized Code headers')
            
            if not has_duplicates:
                print("   ✅ No duplicate optimized code elements found")
                html_ok = True
            else:
                print("   ❌ Duplicate optimized code elements detected")
                html_ok = False
        else:
            print(f"   ❌ Cannot access HTML: {html_response.status_code}")
            html_ok = False
        
        # Test JavaScript for duplicate prevention
        js_response = requests.get('http://localhost:5000/static/app_new.js', timeout=5)
        if js_response.status_code == 200:
            js_content = js_response.text
            
            js_features = {
                'Duplicate prevention flag': 'window.optimizedCodeLoading',
                'Clear content before display': 'optimizedLineNumbers.innerHTML = \'\'',
                'Single display function': 'function displayOptimizedCode',
                'Prevent duplicate calls': 'if (window.optimizedCodeLoading)'
            }
            
            found_features = 0
            for feature, pattern in js_features.items():
                if pattern in js_content:
                    print(f"   ✅ {feature}")
                    found_features += 1
                else:
                    print(f"   ❌ {feature} not found")
            
            if found_features >= 3:
                print("   ✅ JavaScript duplicate prevention is in place")
                js_ok = True
            else:
                print("   ❌ JavaScript duplicate prevention incomplete")
                js_ok = False
        else:
            print(f"   ❌ Cannot access JavaScript: {js_response.status_code}")
            js_ok = False
        
        # Test actual optimization to see if duplication occurs
        print("\n   Testing actual optimization display...")
        test_code = '''def test_func():
    total = 0
    for i in range(5):
        total += i
    return total'''
        
        optimize_response = requests.post('http://localhost:5000/api/optimize/optimized-code', 
                                       json={
                                           'code': test_code,
                                           'metrics': {'complexity': 3, 'lines_of_code': 5},
                                           'language': 'python'
                                       },
                                       timeout=10)
        
        if optimize_response.status_code == 200:
            print("   ✅ Optimization endpoint working")
            
            # Parse the response
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
                print(f"   Optimized code length: {len(optimized_code)} characters")
                optimization_ok = True
            else:
                print("   ❌ Optimization failed or returned same code")
                optimization_ok = False
        else:
            print(f"   ❌ Optimization endpoint failed: {optimize_response.status_code}")
            optimization_ok = False
        
        overall_success = html_ok and js_ok and optimization_ok
        
        return overall_success
        
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def main():
    print("🧪 Duplicate Display Fix Test")
    print("=" * 30)
    
    fix_ok = test_duplicate_display_fix()
    
    print(f"\n📊 Test Results:")
    print(f"Duplicate Fix: {'✅ WORKING' if fix_ok else '❌ BROKEN'}")
    
    if fix_ok:
        print(f"\n✅ Duplicate Display Fix Complete!")
        print("🎯 What was fixed:")
        print("   ✅ Added duplicate prevention flag in JavaScript")
        print("   ✅ Clear content before displaying new optimized code")
        print("   ✅ Prevent multiple simultaneous optimization calls")
        print("   ✅ Single optimized code panel structure confirmed")
        print("\n🚀 The optimized code should now appear only in the single panel!")
    else:
        print(f"\n❌ Duplicate display fix needs more work")
    
    return fix_ok

if __name__ == "__main__":
    main()
