"""
Comprehensive end-to-end test of multi-language code analyzer
Tests all languages with realistic code samples
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_language(language, code, description):
    """Test a single language"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Language: {language.upper()}")
    print(f"{'='*60}")
    
    # Test analysis
    print(f"\n1. Analyzing code...")
    analyze_url = f"{BASE_URL}/api/analyze"
    analyze_payload = {
        "code": code,
        "language": language
    }
    
    try:
        response = requests.post(analyze_url, json=analyze_payload, timeout=10)
        if response.status_code == 200:
            metrics = response.json()
            print(f"   ✓ Status: {response.status_code}")
            print(f"   ✓ Detected Language: {metrics.get('language')}")
            print(f"   ✓ Code Length: {metrics.get('code_length')} chars")
            
            # Display metrics
            if 'metrics' in metrics:
                raw = metrics['metrics'].get('raw', {})
                print(f"   ✓ Metrics:")
                print(f"      - Lines of Code: {raw.get('loc')}")
                print(f"      - Logical Lines: {raw.get('lloc')}")
                print(f"      - Comments: {raw.get('comments')}")
                print(f"      - Blank Lines: {raw.get('blank')}")
                
                complexity = metrics['metrics'].get('cyclomatic', {})
                if complexity:
                    print(f"   ✓ Cyclomatic Complexity:")
                    for func, data in complexity.items():
                        print(f"      - {func}(): {data.get('complexity')} (line {data.get('line')})")
        else:
            print(f"   ✗ Error: {response.status_code}")
            print(f"   {response.text}")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return False
    
    return True

# Test cases with realistic code samples
tests = [
    ("python", """
def fibonacci(n):
    \"\"\"Calculate fibonacci number\"\"\"
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    for i in range(10):
        print(fibonacci(i))
""", "Python - Fibonacci Function"),

    ("javascript", """
function quickSort(arr) {
    if (arr.length <= 1) return arr;
    
    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const right = arr.filter(x => x > pivot);
    
    return [...quickSort(left), pivot, ...quickSort(right)];
}

const data = [5, 2, 8, 1, 9];
console.log(quickSort(data));
""", "JavaScript - Quick Sort"),

    ("java", """
public class BinarySearch {
    public static int search(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
}
""", "Java - Binary Search"),

    ("cpp", """
#include <iostream>
using namespace std;

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    for (int i = 1; i <= 5; i++) {
        cout << i << "! = " << factorial(i) << endl;
    }
    return 0;
}
""", "C++ - Factorial Function"),

    ("c", """
#include <stdio.h>

int gcd(int a, int b) {
    if (b == 0) {
        return a;
    }
    return gcd(b, a % b);
}

int main() {
    int x = 48;
    int y = 18;
    printf("GCD of %d and %d is %d\\n", x, y, gcd(x, y));
    return 0;
}
""", "C - Greatest Common Divisor"),

    ("csharp", """
using System;

public class Calculator {
    public static int Add(int a, int b) {
        if (a < 0 || b < 0) {
            throw new ArgumentException("Numbers must be positive");
        }
        return a + b;
    }
    
    public static void Main() {
        try {
            int result = Add(5, 3);
            Console.WriteLine($"Result: {result}");
        } catch (ArgumentException ex) {
            Console.WriteLine($"Error: {ex.Message}");
        }
    }
}
""", "C# - Calculator with Error Handling"),
]

def main():
    print("\n" + "="*60)
    print("MULTI-LANGUAGE CODE ANALYZER - COMPREHENSIVE TEST")
    print("="*60)
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check server health
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print(f"\n✓ Server is running")
            print(f"✓ Ollama Model: {health.get('ollama_model')}")
        else:
            print(f"\n✗ Server health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"\n✗ Cannot connect to server: {str(e)}")
        return
    
    # Run all tests
    results = []
    for language, code, description in tests:
        success = test_language(language, code, description)
        results.append((description, success))
    
    # Summary
    print(f"\n\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {description}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Multi-language support is working correctly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

if __name__ == '__main__':
    main()
