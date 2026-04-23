#!/usr/bin/env python3

import requests
import json

def test_minimal_fix():
    """Test with a minimal approach to identify the exact issue"""
    print("🔧 MINIMAL TEST: Identifying the exact issue")
    print("=" * 50)
    
    try:
        # Test 1: Check if we're getting the right HTML file
        print("Step 1: Verifying HTML file being served...")
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            html_content = response.text
            
            # Check for our specific debug code
            if 'displayOptimizedCode called with:' in html_content:
                print("❌ OLD HTML being served (contains debug code)")
            else:
                print("✅ HTML file appears to be current")
            
            # Check for the exact optimized content element
            if 'id="optimizedContent"' in html_content:
                print("✅ optimizedContent element found in HTML")
            else:
                print("❌ optimizedContent element NOT found in HTML")
                
            # Check if there are any other elements that might be getting the content
            content_elements = []
            lines = html_content.split('\n')
            for i, line in enumerate(lines):
                if 'content' in line.lower() and ('id=' in line or 'class=' in line):
                    content_elements.append(f"Line {i+1}: {line.strip()}")
            
            if content_elements:
                print(f"Found {len(content_elements)} content-related elements:")
                for elem in content_elements[:5]:  # Show first 5
                    print(f"   {elem}")
        
        # Test 2: Check if JavaScript is being updated
        print("\nStep 2: Verifying JavaScript file...")
        js_response = requests.get('http://localhost:5000/static/app_new.js', timeout=5)
        if js_response.status_code == 200:
            js_content = js_response.text
            
            if 'console.log(\'displayOptimizedCode called with:' in js_content:
                print("✅ JavaScript contains debug code")
            else:
                print("❌ JavaScript does NOT contain debug code (old version)")
            
            if 'getElementById("optimizedContent")' in js_content:
                print("✅ JavaScript targets optimizedContent")
            else:
                print("❌ JavaScript does NOT target optimizedContent")
        
        # Test 3: Try a direct DOM manipulation test
        print("\nStep 3: Creating a simple test...")
        test_html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test</title>
        </head>
        <body>
            <div id="testPanel">
                <h3>Test Panel</h3>
                <pre id="testContent">Test content here</pre>
            </div>
            <script>
                // Test if we can update this element
                setTimeout(() => {
                    const element = document.getElementById('testContent');
                    if (element) {
                        element.textContent = 'UPDATED: This should appear in the panel';
                        console.log('Test: Element updated successfully');
                    } else {
                        console.error('Test: Element not found');
                    }
                }, 1000);
            </script>
        </body>
        </html>
        '''
        
        # Write test file to verify basic functionality
        with open('c:/Users/muthu/SEPM/test_simple.html', 'w') as f:
            f.write(test_html)
        
        print("✅ Test file created: test_simple.html")
        print("   Open http://localhost:5000/test_simple.html to test basic DOM manipulation")
        
        # Test 4: Check if there's a CSS issue hiding content
        print("\nStep 4: Checking for CSS issues...")
        css_response = requests.get('http://localhost:5000/static/style_new.css', timeout=5)
        if css_response.status_code == 200:
            css_content = css_response.text
            
            # Look for any CSS that might hide content
            hiding_rules = []
            lines = css_content.split('\n')
            for i, line in enumerate(lines):
                if any(rule in line.lower() for rule in ['display: none', 'visibility: hidden', 'opacity: 0']):
                    hiding_rules.append(f"Line {i+1}: {line.strip()}")
            
            if hiding_rules:
                print(f"Found {len(hiding_rules)} CSS rules that might hide content:")
                for rule in hiding_rules[:5]:
                    print(f"   {rule}")
            else:
                print("✅ No obvious CSS hiding rules found")
        
        # Test 5: Try a completely different approach
        print("\nStep 5: Alternative approach test...")
        print("   The issue might be:")
        print("   1. Browser caching - try Ctrl+F5")
        print("   2. Wrong element being targeted")
        print("   3. CSS overlay covering content")
        print("   4. JavaScript error preventing execution")
        print("   5. Multiple elements with same ID")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_minimal_fix()
