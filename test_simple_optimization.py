#!/usr/bin/env python3

import requests
import json

def test_simple_optimization():
    """Test a simple optimization case"""
    print("🔧 Testing Simple Optimization...")
    
    # Simple test case with clear sum pattern
    test_code = '''def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total'''
    
    try:
        optimize_response = requests.post('http://localhost:5000/api/optimize/optimized-code', 
                                       json={
                                           'code': test_code,
                                           'metrics': {'complexity': 5, 'lines_of_code': 5},
                                           'language': 'python'
                                       },
                                       timeout=10)
        
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
            
            print(f"\n   Original Code:")
            for i, line in enumerate(test_code.split('\n')):
                print(f"   {i+1}: {line}")
            
            print(f"\n   Optimized Code:")
            for i, line in enumerate(optimized_code.split('\n')):
                print(f"   {i+1}: {line}")
            
            # Check for specific optimizations
            if 'sum(' in optimized_code and 'total = 0' not in optimized_code:
                print("\n   ✅ Sum optimization applied!")
                return True
            elif 'for item in' in optimized_code and 'range(len(' not in optimized_code:
                print("\n   ✅ Loop optimization applied!")
                return True
            else:
                print("\n   ❌ No significant optimizations applied")
                return False
        else:
            print(f"   ❌ Optimization failed: {optimize_response.status_code}")
            return False
        
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_simple_optimization()
