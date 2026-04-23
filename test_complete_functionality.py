#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multilang_analyzer import MultiLanguageCodeAnalyzer
from llm_optimizer import CodeGenerator, LLMOptimizer

def test_analysis_functionality():
    """Test analysis with multiple languages"""
    print("🔍 Testing Analysis Functionality...")
    
    test_cases = [
        {
            'language': 'python',
            'code': '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(fibonacci(i))
'''
        },
        {
            'language': 'javascript',
            'code': '''
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

for (let i = 0; i < 10; i++) {
    console.log(fibonacci(i));
}
'''
        },
        {
            'language': 'java',
            'code': '''
public class Fibonacci {
    public static int fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n-1) + fibonacci(n-2);
    }
    
    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            System.out.println(fibonacci(i));
        }
    }
}
'''
        }
    ]
    
    success_count = 0
    for test_case in test_cases:
        try:
            analyzer = MultiLanguageCodeAnalyzer(test_case['code'], test_case['language'])
            metrics = analyzer.get_all_metrics()
            
            print(f"✅ {test_case['language'].title()} Analysis: SUCCESS")
            print(f"   LOC: {metrics['raw']['loc']}, Complexity: {metrics['avg_complexity']}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ {test_case['language'].title()} Analysis: FAILED - {str(e)}")
    
    return success_count == len(test_cases)

def test_code_generation():
    """Test code generation with multiple languages"""
    print("\n🚀 Testing Code Generation Functionality...")
    
    generator = CodeGenerator()
    
    test_cases = [
        {
            'language': 'python',
            'description': 'Create a function that calculates the factorial of a number'
        },
        {
            'language': 'javascript',
            'description': 'Create a function that sorts an array of numbers'
        },
        {
            'language': 'rust',
            'description': 'Create a struct for a person with name and age fields'
        },
        {
            'language': 'go',
            'description': 'Create a simple HTTP server that responds with hello world'
        }
    ]
    
    success_count = 0
    for test_case in test_cases:
        try:
            result = generator.generate_from_description(test_case['description'], test_case['language'])
            
            if result and not result.startswith("❌ ERROR") and not result.startswith("Error:"):
                print(f"✅ {test_case['language'].title()} Generation: SUCCESS")
                print(f"   Generated {len(result)} characters of code")
                success_count += 1
            else:
                print(f"❌ {test_case['language'].title()} Generation: FAILED - API or key issue")
                
        except Exception as e:
            print(f"❌ {test_case['language'].title()} Generation: FAILED - {str(e)}")
    
    return success_count > 0  # At least one should work if API key is valid

def test_language_normalization():
    """Test language normalization in code generator"""
    print("\n🌍 Testing Language Normalization...")
    
    generator = CodeGenerator()
    
    test_cases = [
        ('js', 'javascript'),
        ('ts', 'typescript'),
        ('py', 'python'),
        ('c++', 'cpp'),
        ('c#', 'c#'),
        ('go', 'go'),
        ('rs', 'rust'),
        ('rb', 'ruby'),
        ('kt', 'kotlin'),
        ('sh', 'bash'),
        ('Dockerfile', 'dockerfile'),
        ('unknown_lang', 'unknown_lang')  # Should remain unchanged
    ]
    
    success_count = 0
    for input_lang, expected in test_cases:
        try:
            result = generator._normalize_language(input_lang)
            if result == expected:
                print(f"✅ '{input_lang}' → '{result}': SUCCESS")
                success_count += 1
            else:
                print(f"❌ '{input_lang}' → '{result}' (expected '{expected}'): FAILED")
        except Exception as e:
            print(f"❌ '{input_lang}' normalization: FAILED - {str(e)}")
    
    return success_count == len(test_cases)

def main():
    print("🧪 Complete Functionality Test Suite")
    print("=" * 50)
    
    # Test all functionality
    analysis_ok = test_analysis_functionality()
    generation_ok = test_code_generation()
    normalization_ok = test_language_normalization()
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    print(f"Analysis: {'✅ PASS' if analysis_ok else '❌ FAIL'}")
    print(f"Generation: {'✅ PASS' if generation_ok else '❌ FAIL'}")
    print(f"Language Normalization: {'✅ PASS' if normalization_ok else '❌ FAIL'}")
    
    overall_success = analysis_ok and generation_ok and normalization_ok
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if overall_success else '⚠️ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n✨ The application is ready for production use!")
        print("🚀 Analysis and code generation are working with multi-language support.")
    else:
        print("\n🔧 Some issues need to be addressed before production use.")
    
    return overall_success

if __name__ == "__main__":
    main()
