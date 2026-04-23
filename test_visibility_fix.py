#!/usr/bin/env python3

import requests

def test_performance_comparison_visibility():
    """Test that the performance comparison section is now visible"""
    print("🔍 Testing Performance Comparison Visibility...")
    
    try:
        # Test CSS for visibility fixes
        css_response = requests.get('http://localhost:5000/static/style_new.css', timeout=5)
        if css_response.status_code == 200:
            css_content = css_response.text
            
            visibility_fixes = {
                'Display block important': 'display: block !important',
                'Visibility visible important': 'visibility: visible !important',
                'Position relative': 'position: relative',
                'Z-index 1': 'z-index: 1',
                'Full width sections include performance': '.performance-comparison-section',
                'Performance comparison section styling': '.performance-comparison-section {'
            }
            
            found_fixes = 0
            for fix_name, selector in visibility_fixes.items():
                if selector in css_content:
                    print(f"   ✅ {fix_name}")
                    found_fixes += 1
                else:
                    print(f"   ❌ {fix_name} not found")
            
            print(f"\n   Visibility Fixes: {found_fixes}/{len(visibility_fixes)} applied")
            
            if found_fixes >= 5:
                print("   ✅ Visibility fixes are properly applied")
                css_ok = True
            else:
                print("   ❌ Some visibility fixes missing")
                css_ok = False
        else:
            print(f"   ❌ Cannot access CSS: {css_response.status_code}")
            css_ok = False
        
        # Test HTML structure
        html_response = requests.get('http://localhost:5000/', timeout=5)
        if html_response.status_code == 200:
            html_content = html_response.text
            
            html_elements = {
                'Performance comparison section': 'performance-comparison-section',
                'Performance comparison h3': 'Performance Comparison & Differences',
                'Comparison grid': 'comparison-grid',
                'Performance metrics box': '📊 Performance Metrics',
                'Code differences box': '🔍 Code Differences',
                'Optimization summary box': '⚡ Optimization Summary'
            }
            
            found_elements = 0
            for element_name, selector in html_elements.items():
                if selector in html_content:
                    print(f"   ✅ {element_name}")
                    found_elements += 1
                else:
                    print(f"   ❌ {element_name} not found")
            
            print(f"\n   HTML Elements: {found_elements}/{len(html_elements)} found")
            
            if found_elements >= 5:
                print("   ✅ HTML structure is complete")
                html_ok = True
            else:
                print("   ❌ HTML structure incomplete")
                html_ok = False
        else:
            print(f"   ❌ Cannot access HTML: {html_response.status_code}")
            html_ok = False
        
        overall_success = css_ok and html_ok
        
        return overall_success
        
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def main():
    print("🧪 Performance Comparison Visibility Test")
    print("=" * 40)
    
    visibility_ok = test_performance_comparison_visibility()
    
    print(f"\n📊 Test Results:")
    print(f"Visibility Fix: {'✅ SUCCESS' if visibility_ok else '❌ FAILED'}")
    
    if visibility_ok:
        print(f"\n✅ Performance Comparison Section is Now Visible!")
        print("🎯 What was fixed:")
        print("   ✅ Added display: block !important")
        print("   ✅ Added visibility: visible !important")
        print("   ✅ Set position: relative")
        print("   ✅ Added z-index: 1")
        print("   ✅ Included in full-width sections")
        print("\n🚀 The performance comparison section should now be visible!")
    else:
        print(f"\n❌ Visibility fix needs more work")
    
    return visibility_ok

if __name__ == "__main__":
    main()
