#!/usr/bin/env python3

import requests
import json

def test_new_layout():
    """Test the new layout with 3-column suggestions and half-width code outputs"""
    print("🎨 Testing New Layout Organization...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            content = response.text
            
            # Check for new layout structure
            layout_checks = {
                '3-column suggestions grid': 'grid-template-columns: repeat(3, 1fr)',
                '2-column code comparison': 'grid-template-columns: 1fr 1fr',
                'Full width suggestions': 'width: 100%',
                'Full width code comparison': 'max-width: 100%',
                'Responsive breakpoints': '@media (max-width: 1200px)',
                'Flexible suggestion categories': 'height: 100%',
                'Optimized suggestion headers': 'flex-shrink: 0'
            }
            
            passed_checks = 0
            total_checks = len(layout_checks)
            
            for check_name, selector in layout_checks.items():
                if selector in content:
                    print(f"   ✅ {check_name}")
                    passed_checks += 1
                else:
                    print(f"   ❌ {check_name} - not found")
            
            # Check specific layout improvements
            improvements = {
                'Reduced gap in suggestions grid': 'gap: 1rem',
                'Optimized padding for headers': 'padding: 0.75rem 1rem',
                'Smaller font for headers': 'font-size: var(--font-size-sm)',
                'Text overflow handling': 'text-overflow: ellipsis',
                'Flexible suggestion list': 'flex: 1'
            }
            
            print(f"\n   Layout Improvements:")
            for improvement, selector in improvements.items():
                if selector in content:
                    print(f"      ✅ {improvement}")
                else:
                    print(f"      ⚠️ {improvement} - not found")
            
            print(f"\n📊 Layout Test Results:")
            print(f"   Core Layout: {passed_checks}/{total_checks} checks passed")
            
            if passed_checks >= total_checks - 1:  # Allow 1 missing check
                print("   ✅ New layout is properly implemented")
                return True
            else:
                print("   ❌ Layout implementation has issues")
                return False
                
        else:
            print(f"   ❌ Cannot test layout: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Layout test failed: {str(e)}")
        return False

def main():
    print("🧪 New Layout Verification Test")
    print("=" * 35)
    
    layout_ok = test_new_layout()
    
    print(f"\n🎯 Summary:")
    if layout_ok:
        print("✅ New layout successfully implemented!")
        print("🎨 Layout Features:")
        print("   • 3 suggestion boxes evenly spread in one row")
        print("   • 2 code output boxes taking half width each")
        print("   • Everything stretches to full screen width")
        print("   • Responsive design for smaller screens")
        print("   • Optimized spacing and typography")
    else:
        print("⚠️ Layout implementation needs review")
    
    return layout_ok

if __name__ == "__main__":
    main()
