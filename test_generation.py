#!/usr/bin/env python
"""Test script for code generation feature"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_generate_from_description():
    """Test 1: Generate code from description"""
    print("\n" + "="*60)
    print("Test 1: Generate Python code from description")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/api/generate/from-description",
        json={
            'description': 'Create a function that calculates the factorial of a number',
            'language': 'python'
        },
        stream=True
    )
    
    print(f"Status Code: {response.status_code}")
    print("\nStreaming Response:")
    
    for line in response.iter_lines():
        if line:
            try:
                decoded = line.decode() if isinstance(line, bytes) else line
                print(decoded)
            except Exception as e:
                print(f"Error: {e}")

def test_complete_code():
    """Test 2: Complete incomplete code"""
    print("\n" + "="*60)
    print("Test 2: Complete incomplete Python code")
    print("="*60)
    
    incomplete_code = '''def fibonacci(n):
    if n <= 1:
        return n
    return'''
    
    response = requests.post(
        f"{BASE_URL}/api/generate/complete-code",
        json={
            'code': incomplete_code,
            'language': 'python'
        },
        stream=True
    )
    
    print(f"Status Code: {response.status_code}")
    print("\nStreaming Response:")
    
    for line in response.iter_lines():
        if line:
            try:
                decoded = line.decode() if isinstance(line, bytes) else line
                print(decoded)
            except Exception as e:
                print(f"Error: {e}")

def test_generate_functions():
    """Test 3: Generate function definitions"""
    print("\n" + "="*60)
    print("Test 3: Generate Python function definitions")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/api/generate/functions",
        json={
            'description': 'Create a Password validator class with methods to check strength and validate format',
            'language': 'python'
        },
        stream=True
    )
    
    print(f"Status Code: {response.status_code}")
    print("\nStreaming Response:")
    
    for line in response.iter_lines():
        if line:
            try:
                decoded = line.decode() if isinstance(line, bytes) else line
                print(decoded)
            except Exception as e:
                print(f"Error: {e}")

def test_improve_code():
    """Test 4: Improve and complete code"""
    print("\n" + "="*60)
    print("Test 4: Improve Python code")
    print("="*60)
    
    partial_code = '''def sort_data(items):
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            if items[i] > items[j]:
                temp = items[i]
                items[i] = items[j]
                items[j] = temp'''
    
    improvement_idea = "Make the code more efficient using Python built-in functions and add type hints"
    
    response = requests.post(
        f"{BASE_URL}/api/generate/improve",
        json={
            'code': partial_code,
            'idea': improvement_idea,
            'language': 'python'
        },
        stream=True
    )
    
    print(f"Status Code: {response.status_code}")
    print("\nStreaming Response:")
    
    for line in response.iter_lines():
        if line:
            try:
                decoded = line.decode() if isinstance(line, bytes) else line
                print(decoded)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    print("\n🚀 Testing Code Generation API Endpoints")
    print("="*60)
    
    try:
        test_generate_from_description()
        time.sleep(2)
        
        test_complete_code()
        time.sleep(2)
        
        test_generate_functions()
        time.sleep(2)
        
        test_improve_code()
        
        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to Flask server at http://localhost:5000")
        print("Make sure Flask is running: python app.py")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
