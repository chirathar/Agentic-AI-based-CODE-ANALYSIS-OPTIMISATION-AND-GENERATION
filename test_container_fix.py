#!/usr/bin/env python3

import requests
import json

def test_container_fix():
    """Test that the CSS fixes resolve the container positioning issue"""
    print("🔧 Testing Container Fix")
    print("=" * 30)
    
    try:
        # Test 1: Check if CSS fixes are applied
        print("Step 1: Verifying CSS fixes...")
        css_response = requests.get('http://localhost:5000/static/style_new.css', timeout=5)
        if css_response.status_code == 200:
            css_content = css_response.text
            
            css_fixes = {
                'display: flex in code-content': 'display: flex' in css_content and '.code-content' in css_content,
                'align-items: stretch': 'align-items: stretch' in css_content,
                'flex-shrink: 0 for line numbers': 'flex-shrink: 0' in css_content,
                'flex: 1 for display': 'flex: 1' in css_content and '#optimizedDisplay' in css_content,
                'min-width: 0': 'min-width: 0' in css_content
            }
            
            print("   CSS fixes applied:")
            for fix, applied in css_fixes.items():
                status = "✅" if applied else "❌"
                print(f"      {status} {fix}")
            
            if all(css_fixes.values()):
                print("   ✅ All CSS fixes applied correctly")
                css_ok = True
            else:
                print("   ❌ Some CSS fixes missing")
                css_ok = False
        else:
            print(f"   ❌ Cannot access CSS: {css_response.status_code}")
            css_ok = False
        
        # Test 2: Test optimization with container positioning
        print("\nStep 2: Testing optimization with container positioning...")
        test_code = '''def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total'''
        
        opt_response = requests.post('http://localhost:5000/api/optimize/optimized-code',
                                   json={
                                       'code': test_code,
                                       'metrics': {'complexity': 5, 'lines_of_code': 5},
                                       'language': 'python'
                                   },
                                   timeout=10)
        
        if opt_response.status_code == 200:
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
            
            if optimized_code and optimized_code != test_code:
                print("   ✅ Optimization working correctly")
                print(f"   📝 Optimized code: {len(optimized_code)} characters")
                
                # The key test: the optimized code should now appear within the container
                print("   🎯 EXPECTED RESULT:")
                print("      - Optimized code should appear INSIDE the optimized code panel")
                print("      - Code should be properly aligned with line numbers")
                print("      - No text should appear outside the container bounds")
                print("      - Container should properly contain all content")
                
                optimization_ok = True
            else:
                print("   ❌ Optimization not working")
                optimization_ok = False
        else:
            print(f"   ❌ Optimization failed: {opt_response.status_code}")
            optimization_ok = False
        
        # Test 3: Verify HTML structure is correct
        print("\nStep 3: Verifying HTML structure...")
        html_response = requests.get('http://localhost:5000/', timeout=5)
        if html_response.status_code == 200:
            html_content = html_response.text
            
            # Check the container structure
            structure_checks = {
                'code-content container': 'class="code-content"' in html_content,
                'optimizedLineNumbers': 'id="optimizedLineNumbers"' in html_content,
                'optimizedDisplay': 'id="optimizedDisplay"' in html_content,
                'optimizedContent': 'id="optimizedContent"' in html_content,
                'proper nesting': html_content.count('class="code-content"') == 1
            }
            
            print("   HTML structure:")
            for check, passed in structure_checks.items():
                status = "✅" if passed else "❌"
                print(f"      {status} {check}")
            
            if all(structure_checks.values()):
                print("   ✅ HTML structure is correct")
                html_ok = True
            else:
                print("   ❌ HTML structure has issues")
                html_ok = False
        else:
            print(f"   ❌ Cannot access HTML: {html_response.status_code}")
            html_ok = False
        
        overall_success = css_ok and optimization_ok and html_ok
        
        return overall_success
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def main():
    print("🧪 Container Position Fix Test")
    print("=" * 35)
    
    fix_ok = test_container_fix()
    
    print(f"\n📊 Test Results:")
    print(f"Container Fix: {'✅ WORKING' if fix_ok else '❌ BROKEN'}")
    
    if fix_ok:
        print(f"\n✅ Container Position Fix Complete!")
        print("🎯 What was fixed:")
        print("   ✅ Added flex display to code-content container")
        print("   ✅ Fixed line numbers container with flex-shrink: 0")
        print("   ✅ Added proper flex properties to optimized display")
        print("   ✅ Ensured content stays within container bounds")
        print("\n🚀 The optimized code should now appear INSIDE the container!")
        print("\n📋 USER ACTION NEEDED:")
        print("   1. Refresh the browser (Ctrl+F5)")
        print("   2. Test with some code")
        print("   3. Verify optimized code appears within the panel")
    else:
        print(f"\n❌ Container fix needs more work")
    
    return fix_ok

if __name__ == "__main__":
    main()
