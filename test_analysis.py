#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multilang_analyzer import MultiLanguageCodeAnalyzer

def test_analysis():
    print("Testing code analysis functionality...")
    
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
    
    try:
        analyzer = MultiLanguageCodeAnalyzer(test_code, 'python')
        metrics = analyzer.get_all_metrics()
        
        print("✅ Analysis successful!")
        print(f"Raw metrics: {metrics['raw']}")
        print(f"Cyclomatic complexity: {metrics['cyclomatic']}")
        print(f"Halstead metrics: {metrics['halstead']}")
        print(f"Average complexity: {metrics['avg_complexity']}")
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_analysis()
