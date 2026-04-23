#!/usr/bin/env python3

import requests
import json

def test_container_position():
    """Test to verify where the optimized code is actually being placed"""
    print("🔍 Testing Container Position Issue")
    print("=" * 40)
    
    try:
        # Get the HTML to see the structure
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            html_content = response.text
            
            # Find the optimized code container structure
            print("📋 HTML Structure Analysis:")
            
            # Look for the optimized code section
            if 'id="optimizedContent"' in html_content:
                print("✅ optimizedContent element found")
                
                # Extract the container structure around optimizedContent
                lines = html_content.split('\n')
                for i, line in enumerate(lines):
                    if 'id="optimizedContent"' in line:
                        print(f"\n📍 Found optimizedContent at line {i+1}:")
                        # Show context around the element
                        start = max(0, i-3)
                        end = min(len(lines), i+4)
                        for j in range(start, end):
                            marker = ">>> " if j == i else "    "
                            print(f"{marker}{j+1:3d}: {lines[j]}")
                        break
            else:
                print("❌ optimizedContent element NOT found")
            
            # Check for any other elements that might be getting the content
            print("\n🔍 Looking for potential target elements:")
            potential_targets = [
                'id="optimizedDisplay"',
                'class="code-content"',
                'class="code-panel-full"',
                'class="optimized"'
            ]
            
            for target in potential_targets:
                if target in html_content:
                    count = html_content.count(target)
                    print(f"   ✅ {target}: {count} occurrence(s)")
                else:
                    print(f"   ❌ {target}: Not found")
        
        # Test the optimization to see what gets returned
        print("\n🧪 Testing Optimization API:")
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
            
            if optimized_code:
                print("✅ Optimization working")
                print(f"📝 Optimized code preview: {optimized_code[:100]}...")
                
                # The issue is likely that this content is being written correctly
                # but CSS positioning makes it appear outside the container
                print("\n🎯 LIKELY ISSUE:")
                print("   The JavaScript is correctly writing to optimizedContent")
                print("   But CSS positioning is causing the text to appear outside")
                print("   the visible container bounds")
                
                print("\n🔧 POSSIBLE FIXES:")
                print("   1. Check CSS overflow and positioning")
                print("   2. Verify container dimensions")
                print("   3. Check for CSS transforms or absolute positioning")
                print("   4. Ensure content is within container bounds")
                
            else:
                print("❌ No optimized code received")
        else:
            print(f"❌ Optimization API failed: {opt_response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_container_position()
