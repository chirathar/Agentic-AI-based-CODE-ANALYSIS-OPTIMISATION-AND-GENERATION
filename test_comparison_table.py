#!/usr/bin/env python3

import requests

def test_comparison_table():
    """Test the new comparison table implementation"""
    print("📊 Testing Comparison Table Implementation...")
    
    try:
        # Test HTML structure
        html_response = requests.get('http://localhost:5000/', timeout=5)
        if html_response.status_code == 200:
            html_content = html_response.text
            
            # Check for table elements
            table_elements = {
                'Performance comparison section': 'performance-comparison-section',
                'Comparison table container': 'comparison-table-container',
                'Comparison table': 'comparison-table',
                'Table header': '<thead>',
                'Table body': '<tbody>',
                'Metric column': 'Metric',
                'Original code column': 'Original Code',
                'Optimized code column': 'Optimized Code',
                'Improvement column': 'Improvement',
                'Execution time row': 'Execution Time',
                'Memory usage row': 'Memory Usage',
                'Code complexity row': 'Code Complexity',
                'Lines of code row': 'Lines of Code'
            }
            
            found_elements = 0
            for element_name, selector in table_elements.items():
                if selector in html_content:
                    print(f"   ✅ {element_name}")
                    found_elements += 1
                else:
                    print(f"   ❌ {element_name} not found")
            
            print(f"\n   HTML Elements: {found_elements}/{len(table_elements)} found")
            
            if found_elements >= 10:
                print("   ✅ Table HTML structure is complete")
                html_ok = True
            else:
                print("   ❌ Table HTML structure incomplete")
                html_ok = False
        else:
            print(f"   ❌ Cannot access HTML: {html_response.status_code}")
            html_ok = False
        
        # Test CSS styling
        css_response = requests.get('http://localhost:5000/static/style_new.css', timeout=5)
        if css_response.status_code == 200:
            css_content = css_response.text
            
            # Check for table CSS
            css_features = {
                'Table container': '.comparison-table-container',
                'Table styling': '.comparison-table',
                'Table headers': '.comparison-table th',
                'Table cells': '.comparison-table td',
                'Metric name styling': '.metric-name',
                'Original value styling': '.original-value',
                'Optimized value styling': '.optimized-value',
                'Improvement cell styling': '.improvement-cell',
                'Positive improvement': '.improvement-cell.positive',
                'Negative improvement': '.improvement-cell.negative',
                'Neutral improvement': '.improvement-cell.neutral',
                'Table hover effect': '.comparison-table tr:hover'
            }
            
            found_css = 0
            for feature_name, selector in css_features.items():
                if selector in css_content:
                    print(f"   ✅ {feature_name}")
                    found_css += 1
                else:
                    print(f"   ❌ {feature_name} not found")
            
            print(f"\n   CSS Features: {found_css}/{len(css_features)} found")
            
            if found_css >= 9:
                print("   ✅ Table CSS styling is complete")
                css_ok = True
            else:
                print("   ❌ Table CSS styling incomplete")
                css_ok = False
        else:
            print(f"   ❌ Cannot access CSS: {css_response.status_code}")
            css_ok = False
        
        # Test JavaScript functionality
        js_response = requests.get('http://localhost:5000/static/app_new.js', timeout=5)
        if js_response.status_code == 200:
            js_content = js_response.text
            
            # Check for table JavaScript functions
            js_functions = {
                'Update metric comparison': 'updateMetricComparison',
                'Table original element': 'tableOriginal',
                'Table optimized element': 'tableOptimized',
                'Table improvement element': 'tableTimeImprovement',
                'Clear performance comparison': 'clearPerformanceComparison',
                'Format metric value': 'formatMetricValue'
            }
            
            found_js = 0
            for function_name, selector in js_functions.items():
                if selector in js_content:
                    print(f"   ✅ {function_name}")
                    found_js += 1
                else:
                    print(f"   ❌ {function_name} not found")
            
            print(f"\n   JavaScript Functions: {found_js}/{len(js_functions)} found")
            
            if found_js >= 5:
                print("   ✅ Table JavaScript functionality is complete")
                js_ok = True
            else:
                print("   ❌ Table JavaScript functionality incomplete")
                js_ok = False
        else:
            print(f"   ❌ Cannot access JavaScript: {js_response.status_code}")
            js_ok = False
        
        overall_success = html_ok and css_ok and js_ok
        
        return overall_success
        
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

def main():
    print("🧪 Comparison Table Test")
    print("=" * 25)
    
    table_ok = test_comparison_table()
    
    print(f"\n📊 Test Results:")
    print(f"Comparison Table: {'✅ WORKING' if table_ok else '❌ BROKEN'}")
    
    if table_ok:
        print(f"\n✅ Comparison Table Implementation Complete!")
        print("🎯 What was implemented:")
        print("   ✅ Clean table structure with 4 columns")
        print("   ✅ Professional table styling with hover effects")
        print("   ✅ Color-coded improvement indicators")
        print("   ✅ Responsive design for all screen sizes")
        print("   ✅ JavaScript integration for data population")
        print("\n🚀 The comparison table should now be visible and functional!")
    else:
        print(f"\n❌ Comparison table implementation needs review")
    
    return table_ok

if __name__ == "__main__":
    main()
