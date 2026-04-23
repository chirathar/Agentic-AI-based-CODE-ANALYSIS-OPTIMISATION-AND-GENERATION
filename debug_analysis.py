#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multilang_analyzer import MultiLanguageCodeAnalyzer

def debug_analysis():
    print("🔍 Debugging Analysis Functionality...")
    
    # Test with simple Python code
    test_code = """
def calculate_sum(a, b):
    if a > 0 and b > 0:
        return a + b
    else:
        return 0

def main():
    for i in range(10):
        print(calculate_sum(i, i+1))
"""
    
    print("Input Code:")
    print(test_code)
    print("\n" + "="*50)
    
    try:
        analyzer = MultiLanguageCodeAnalyzer(test_code, 'python')
        metrics = analyzer.get_all_metrics()
        
        print("Complete Metrics Structure:")
        for key, value in metrics.items():
            print(f"  {key}:")
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    print(f"    {sub_key}: {sub_value}")
            else:
                print(f"    {value}")
        
        print(f"\nAverage Complexity: {metrics.get('avg_complexity', 'Not found')}")
        print(f"Language: {metrics.get('language', 'Not found')}")
        
        # Check if we have meaningful data
        raw_metrics = metrics.get('raw', {})
        cyclomatic = metrics.get('cyclomatic', {})
        halstead = metrics.get('halstead', {})
        
        print(f"\nRaw Metrics Check:")
        print(f"  Lines of Code: {raw_metrics.get('loc', 0)}")
        print(f"  Logical Lines: {raw_metrics.get('lloc', 0)}")
        print(f"  Comments: {raw_metrics.get('comments', 0)}")
        
        print(f"\nCyclomatic Complexity Check:")
        print(f"  Functions found: {len(cyclomatic)}")
        for func_name, data in cyclomatic.items():
            print(f"    {func_name}: complexity {data.get('complexity', 0)}")
        
        print(f"\nHalstead Metrics Check:")
        print(f"  Volume: {halstead.get('volume', 0)}")
        print(f"  Difficulty: {halstead.get('difficulty', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_analysis()
