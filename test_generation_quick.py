#!/usr/bin/env python3

import requests
import json

def test_generation_endpoint():
    """Test generation endpoint quickly"""
    print("Testing generation endpoint...")
    
    try:
        response = requests.post('http://localhost:5000/api/generate/from-description', 
                               json={
                                   'description': 'Create a function that adds two numbers',
                                   'language': 'python'
                               },
                               timeout=10)
        
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print('Response keys:', list(data.keys()))
            if 'content' in data:
                print(f'Content length: {len(data["content"])}')
                print('Content preview:', data['content'][:200])
            else:
                print('No content in response')
                print('Response:', data)
        else:
            print(f'Error: {response.text}')
            
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    test_generation_endpoint()
