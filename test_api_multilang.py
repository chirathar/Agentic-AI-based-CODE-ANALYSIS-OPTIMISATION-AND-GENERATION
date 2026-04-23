"""
Test multi-language support in the code analyzer.
Tests API endpoints with different programming languages.
"""

from app import app
import json

# Create a test client
client = app.test_client()

def test_analyze_endpoint():
    """Test the analyze endpoint with different languages"""
    
    # Test Python
    python_code = """
def calculate(x, y):
    if x > 0:
        return x * y
    return 0
"""
    
    response = client.post('/api/analyze',
        data=json.dumps({
            'code': python_code,
            'language': 'python'
        }),
        content_type='application/json'
    )
    
    print("Python Analysis:")
    print(f"  Status: {response.status_code}")
    data = response.get_json()
    print(f"  Metrics: {json.dumps(data['metrics'], indent=2)}")
    assert response.status_code == 200, "Python analysis failed"
    
    # Test JavaScript
    js_code = """
function process(items) {
    if (items.length > 0) {
        return items.map(x => x * 2);
    }
    return [];
}
"""
    
    response = client.post('/api/analyze',
        data=json.dumps({
            'code': js_code,
            'language': 'javascript'
        }),
        content_type='application/json'
    )
    
    print("\nJavaScript Analysis:")
    print(f"  Status: {response.status_code}")
    data = response.get_json()
    print(f"  Language detected: {data.get('language')}")
    assert response.status_code == 200, "JavaScript analysis failed"
    
    # Test Java
    java_code = """
public class Calculator {
    public int add(int a, int b) {
        if (a > 0 && b > 0) {
            return a + b;
        }
        return 0;
    }
}
"""
    
    response = client.post('/api/analyze',
        data=json.dumps({
            'code': java_code,
            'language': 'java'
        }),
        content_type='application/json'
    )
    
    print("\nJava Analysis:")
    print(f"  Status: {response.status_code}")
    data = response.get_json()
    print(f"  Language detected: {data.get('language')}")
    assert response.status_code == 200, "Java analysis failed"
    
    # Test C++
    cpp_code = """
int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}
"""
    
    response = client.post('/api/analyze',
        data=json.dumps({
            'code': cpp_code,
            'language': 'cpp'
        }),
        content_type='application/json'
    )
    
    print("\nC++ Analysis:")
    print(f"  Status: {response.status_code}")
    data = response.get_json()
    print(f"  Language detected: {data.get('language')}")
    assert response.status_code == 200, "C++ analysis failed"
    
    # Test C
    c_code = """
int max(int a, int b) {
    if (a > b) {
        return a;
    }
    return b;
}
"""
    
    response = client.post('/api/analyze',
        data=json.dumps({
            'code': c_code,
            'language': 'c'
        }),
        content_type='application/json'
    )
    
    print("\nC Analysis:")
    print(f"  Status: {response.status_code}")
    data = response.get_json()
    print(f"  Language detected: {data.get('language')}")
    assert response.status_code == 200, "C analysis failed"
    
    # Test C#
    csharp_code = """
public class StringUtils {
    public string Reverse(string text) {
        if (string.IsNullOrEmpty(text)) {
            return text;
        }
        return new string(text.Reverse().ToArray());
    }
}
"""
    
    response = client.post('/api/analyze',
        data=json.dumps({
            'code': csharp_code,
            'language': 'csharp'
        }),
        content_type='application/json'
    )
    
    print("\nC# Analysis:")
    print(f"  Status: {response.status_code}")
    data = response.get_json()
    print(f"  Language detected: {data.get('language')}")
    assert response.status_code == 200, "C# analysis failed"
    
    print("\n✓ All language tests passed!")

def test_invalid_language():
    """Test error handling for invalid language"""
    
    response = client.post('/api/analyze',
        data=json.dumps({
            'code': 'print("hello")',
            'language': 'ruby'
        }),
        content_type='application/json'
    )
    
    print("\nInvalid Language Test:")
    print(f"  Status: {response.status_code}")
    data = response.get_json()
    print(f"  Error: {data.get('error')}")
    assert response.status_code == 400, "Should reject invalid language"
    print("✓ Invalid language properly rejected")

if __name__ == '__main__':
    print("=== Testing Multi-Language Code Analyzer ===\n")
    test_analyze_endpoint()
    test_invalid_language()
    print("\n=== All tests completed successfully! ===")
