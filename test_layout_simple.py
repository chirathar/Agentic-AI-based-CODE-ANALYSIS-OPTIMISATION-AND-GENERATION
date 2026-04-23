#!/usr/bin/env python3

import requests

def test_layout_simple():
    """Simple test to verify the layout changes are being served"""
    print("🎨 Testing Layout Implementation...")
    
    try:
        # Test if the CSS file is accessible
        css_response = requests.get('http://localhost:5000/static/style_new.css', timeout=5)
        if css_response.status_code == 200:
            css_content = css_response.text
            
            # Check for key layout features
            layout_features = {
                '3-column suggestions': 'repeat(3, 1fr)',
                '2-column code comparison': 'grid-template-columns: 1fr 1fr',
                'Full width': 'width: 100%',
                'Responsive design': '@media (max-width: 1200px)',
                'Flexible categories': 'height: 100%'
            }
            
            found_features = 0
            for feature, pattern in layout_features.items():
                if pattern in css_content:
                    print(f"   ✅ {feature}")
                    found_features += 1
                else:
                    print(f"   ❌ {feature} not found")
            
            print(f"\n   CSS Features: {found_features}/{len(layout_features)} found")
            
            if found_features >= 4:
                print("   ✅ Layout CSS is properly implemented")
                return True
            else:
                print("   ❌ Layout CSS has missing features")
                return False
        else:
            print(f"   ❌ CSS file not accessible: {css_response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def test_frontend_structure():
    """Test if the frontend HTML structure supports the new layout"""
    print("\n🏗️ Testing Frontend Structure...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            html_content = response.text
            
            # Check for required HTML structure
            structure_elements = {
                'Suggestions section': 'suggestions-section',
                'Suggestions grid': 'suggestions-grid',
                'Code comparison section': 'code-comparison-section',
                'Code comparison container': 'code-comparison-container',
                'Quality suggestions': 'qualitySuggestions',
                'Refactoring suggestions': 'refactoringSuggestions',
                'Performance suggestions': 'performanceSuggestions'
            }
            
            found_elements = 0
            for element, selector in structure_elements.items():
                if selector in html_content:
                    print(f"   ✅ {element}")
                    found_elements += 1
                else:
                    print(f"   ❌ {element} not found")
            
            print(f"\n   HTML Elements: {found_elements}/{len(structure_elements)} found")
            
            if found_elements >= 6:
                print("   ✅ Frontend structure supports new layout")
                return True
            else:
                print("   ❌ Frontend structure missing elements")
                return False
        else:
            print(f"   ❌ Frontend not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def main():
    print("🧪 Simple Layout Verification")
    print("=" * 30)
    
    css_ok = test_layout_simple()
    html_ok = test_frontend_structure()
    
    print(f"\n📊 Results:")
    print(f"CSS Implementation: {'✅ OK' if css_ok else '❌ ISSUES'}")
    print(f"HTML Structure: {'✅ OK' if html_ok else '❌ ISSUES'}")
    
    overall_success = css_ok and html_ok
    
    if overall_success:
        print(f"\n✅ Layout Successfully Implemented!")
        print("🎯 New Layout Features:")
        print("   • 3 suggestion boxes in one row (evenly spaced)")
        print("   • 2 code output boxes (half width each)")
        print("   • Full screen width utilization")
        print("   • Responsive design for smaller screens")
    else:
        print(f"\n⚠️ Layout Implementation Needs Review")
        if not css_ok:
            print("   - CSS changes not properly applied")
        if not html_ok:
            print("   - HTML structure issues")
    
    return overall_success

if __name__ == "__main__":
    main()
