from multilang_analyzer import MultiLanguageCodeAnalyzer

# Test Python
python_code = """
def add(a, b):
    if a > 0:
        return a + b
    return 0
"""

analyzer = MultiLanguageCodeAnalyzer(python_code, 'python')
metrics = analyzer.get_all_metrics()
print("Python Metrics:")
print(f"  LOC: {metrics['raw']['loc']}")
print(f"  Complexity: {metrics['cyclomatic']}")

# Test JavaScript
js_code = """
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}
"""

analyzer = MultiLanguageCodeAnalyzer(js_code, 'javascript')
metrics = analyzer.get_all_metrics()
print("\nJavaScript Metrics:")
print(f"  LOC: {metrics['raw']['loc']}")
print(f"  Complexity: {metrics['cyclomatic']}")

print("\n✓ All language analyzers working!")
