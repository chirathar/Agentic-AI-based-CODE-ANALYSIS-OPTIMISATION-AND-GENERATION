#!/usr/bin/env python3

import requests
import json

def debug_optimized_display():
    """Debug the optimized code display issue step by step"""
    print("🔍 DEBUG: Optimized Code Display Issue")
    print("=" * 50)
    
    try:
        # Step 1: Check if server is running
        print("Step 1: Checking server connection...")
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code != 200:
            print(f"❌ Server not responding: {response.status_code}")
            return False
        print("✅ Server is running")
        
        # Step 2: Check HTML structure
        print("\nStep 2: Analyzing HTML structure...")
        html_content = response.text
        
        # Count critical elements
        elements_to_check = {
            'optimizedDisplay': html_content.count('id="optimizedDisplay"'),
            'optimizedContent': html_content.count('id="optimizedContent"'),
            'optimizedLineNumbers': html_content.count('id="optimizedLineNumbers"'),
            'optimizedLoader': html_content.count('id="optimizedLoader"')
        }
        
        print("Element counts:")
        for element, count in elements_to_check.items():
            status = "✅" if count == 1 else "❌" if count > 1 else "⚠️"
            print(f"   {status} {element}: {count}")
        
        if any(count > 1 for count in elements_to_check.values()):
            print("❌ DUPLICATE ELEMENTS FOUND - This could be the issue!")
            return False
        
        # Step 3: Test optimization endpoint directly
        print("\nStep 3: Testing optimization endpoint...")
        test_code = '''def test():
    total = 0
    for i in range(5):
        total += i
    return total'''
        
        opt_response = requests.post('http://localhost:5000/api/optimize/optimized-code',
                                   json={
                                       'code': test_code,
                                       'metrics': {'complexity': 3, 'lines_of_code': 5},
                                       'language': 'python'
                                   },
                                   timeout=10)
        
        if opt_response.status_code != 200:
            print(f"❌ Optimization endpoint failed: {opt_response.status_code}")
            return False
        
        print("✅ Optimization endpoint responding")
        
        # Parse the response
        optimized_code = ""
        for line in opt_response.iter_lines():
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
        
        if not optimized_code:
            print("❌ No optimized code received")
            return False
        
        print(f"✅ Received optimized code: {len(optimized_code)} characters")
        print(f"First 100 chars: {optimized_code[:100]}...")
        
        # Step 4: Check if JavaScript files are accessible
        print("\nStep 4: Checking JavaScript files...")
        js_response = requests.get('http://localhost:5000/static/app_new.js', timeout=5)
        if js_response.status_code != 200:
            print(f"❌ JavaScript file not accessible: {js_response.status_code}")
            return False
        
        js_content = js_response.text
        if 'displayOptimizedCode' not in js_content:
            print("❌ displayOptimizedCode function not found in JavaScript")
            return False
        
        if 'getElementById("optimizedContent")' not in js_content:
            print("❌ JavaScript not targeting optimizedContent element")
            return False
        
        print("✅ JavaScript file contains required functions")
        
        # Step 5: Check CSS files
        print("\nStep 5: Checking CSS files...")
        css_response = requests.get('http://localhost:5000/static/style_new.css', timeout=5)
        if css_response.status_code != 200:
            print(f"❌ CSS file not accessible: {css_response.status_code}")
            return False
        
        css_content = css_response.text
        if '#optimizedContent' not in css_content:
            print("❌ CSS rules for optimizedContent not found")
            return False
        
        print("✅ CSS file contains optimized content rules")
        
        # Step 6: Simulate what should happen in browser
        print("\nStep 6: Simulating browser behavior...")
        print("   1. User clicks 'Analyze Code'")
        print("   2. JavaScript calls loadOptimizedCode()")
        print("   3. JavaScript calls displayOptimizedCode()")
        print("   4. Should update: optimizedContent.textContent")
        print("   5. Should hide: optimizedLoader")
        
        print(f"\n   Expected result: Optimized code should appear in panel")
        print(f"   Actual issue: Code appears below panel instead")
        
        print("\n🎯 LIKELY ISSUES:")
        print("   1. JavaScript function not being called")
        print("   2. Wrong element being targeted")
        print("   3. CSS hiding the content")
        print("   4. Loader still covering content")
        print("   5. Multiple elements with same ID")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {str(e)}")
        return False

if __name__ == "__main__":
    debug_optimized_display()
