from typing import Dict, List
import random

class TaskGenerator:
    """Generates adaptive coding tasks based on skill level"""
    
    def __init__(self):
        """Initialize with task library"""
        self.tasks = {
            'beginner': {
                'variables': [
                    {
                        'id': 'b_var_1',
                        'title': 'Create Your First Variables',
                        'description': 'Create variables to store a person\'s name, age, and height. Print them out.',
                        'starter_code': '# Store information about a person\nname = \nage = \nheight = \n\nprint(name, age, height)',
                        'expected_output': 'Your name, age, and height on one line',
                        'hints': ['Use the = sign to assign values', 'Numbers don\'t need quotes, but text does'],
                        'concepts': ['variables', 'print'],
                    },
                    {
                        'id': 'b_var_2',
                        'title': 'Variable Arithmetic',
                        'description': 'Create two number variables and calculate their sum, difference, and product.',
                        'starter_code': 'num1 = 10\nnum2 = 5\n\n# Calculate operations here\nprint()',
                        'expected_output': 'Sum, difference, and product values',
                        'hints': ['Use +, -, * for arithmetic'],
                        'concepts': ['variables', 'arithmetic'],
                    }
                ],
                'loops': [
                    {
                        'id': 'b_loop_1',
                        'title': 'Print Numbers with a Loop',
                        'description': 'Use a loop to print numbers from 1 to 5.',
                        'starter_code': '# Use a for loop to print 1 to 5\n',
                        'expected_output': '1\n2\n3\n4\n5',
                        'hints': ['Use range()', 'for loops iterate through sequences'],
                        'concepts': ['loops', 'range'],
                    },
                    {
                        'id': 'b_loop_2',
                        'title': 'Loop Through a List',
                        'description': 'Create a list of fruits and print each one using a loop.',
                        'starter_code': 'fruits = ["apple", "banana", "cherry"]\n\n# Loop through fruits here\n',
                        'expected_output': 'apple\nbanana\ncherry',
                        'hints': ['Use for fruit in fruits', 'print each fruit'],
                        'concepts': ['loops', 'lists'],
                    }
                ],
                'conditionals': [
                    {
                        'id': 'b_cond_1',
                        'title': 'Even or Odd Checker',
                        'description': 'Create a program that checks if a number is even or odd.',
                        'starter_code': 'num = 7\n\n# Check if even or odd\nif :\n    print()\nelse:\n    print()',
                        'expected_output': 'Odd' if 7 % 2 != 0 else 'Even',
                        'hints': ['Use num % 2 == 0 for even check', 'if/else structure'],
                        'concepts': ['conditionals', 'modulo'],
                    },
                    {
                        'id': 'b_cond_2',
                        'title': 'Age Category Classifier',
                        'description': 'Classify a person into age categories: child (0-12), teen (13-19), adult (20+)',
                        'starter_code': 'age = 15\n\n# Classify age here\nif age <= 12:\n    print("Child")\nelif :  # teen\n    print()\nelse:  # adult\n    print()',
                        'expected_output': 'Teen',
                        'hints': ['Use elif for multiple conditions', 'Use and for ranges'],
                        'concepts': ['conditionals', 'comparison'],
                    }
                ],
                'functions': [
                    {
                        'id': 'b_func_1',
                        'title': 'Create a Greeting Function',
                        'description': 'Create a function that takes a name and prints a greeting.',
                        'starter_code': 'def greet(name):\n    # Your code here\n    \ngreet("Alice")',
                        'expected_output': 'Hello, Alice!',
                        'hints': ['Define function with def', 'Use the parameter'],
                        'concepts': ['functions', 'parameters'],
                    },
                    {
                        'id': 'b_func_2',
                        'title': 'Return a Calculation',
                        'description': 'Create a function that takes two numbers and returns their product.',
                        'starter_code': 'def multiply(a, b):\n    # Your code here\n    \nresult = multiply(4, 5)\nprint(result)',
                        'expected_output': '20',
                        'hints': ['Use return statement', 'Function should return the result'],
                        'concepts': ['functions', 'return'],
                    }
                ]
            },
            'intermediate': {
                'list_comprehension': [
                    {
                        'id': 'i_lc_1',
                        'title': 'Square Numbers with Comprehension',
                        'description': 'Use list comprehension to create a list of squares for numbers 1-5.',
                        'starter_code': '# Create list of squares using comprehension\nsquares = \nprint(squares)',
                        'expected_output': '[1, 4, 9, 16, 25]',
                        'hints': ['Use [x**2 for x in range(...)]', 'Syntax: [expression for item in list]'],
                        'concepts': ['list_comprehension', 'loops'],
                    }
                ],
                'exception_handling': [
                    {
                        'id': 'i_exc_1',
                        'title': 'Safe Division',
                        'description': 'Create a function that divides two numbers safely.',
                        'starter_code': 'def safe_divide(a, b):\n    try:\n        # Your code here\n    except:\n        # Handle error\n        \nprint(safe_divide(10, 2))\nprint(safe_divide(10, 0))',
                        'expected_output': '5.0\nError: Cannot divide by zero',
                        'hints': ['Use try/except', 'Handle ZeroDivisionError'],
                        'concepts': ['exception_handling', 'functions'],
                    }
                ],
                'classes': [
                    {
                        'id': 'i_class_1',
                        'title': 'Create a Person Class',
                        'description': 'Create a Person class with name and age attributes.',
                        'starter_code': 'class Person:\n    def __init__(self, name, age):\n        # Store attributes\n        \nperson = Person("Alice", 25)\nprint(person.name, person.age)',
                        'expected_output': 'Alice 25',
                        'hints': ['Use __init__ for initialization', 'Use self.attribute to store data'],
                        'concepts': ['classes', 'attributes', 'methods'],
                    }
                ]
            },
            'advanced': {
                'generators': [
                    {
                        'id': 'a_gen_1',
                        'title': 'Fibonacci Generator',
                        'description': 'Create a generator that yields Fibonacci numbers.',
                        'starter_code': 'def fibonacci(limit):\n    a, b = 0, 1\n    while a < limit:\n        # Your code here\n        \nfor num in fibonacci(100):\n    print(num)',
                        'expected_output': '0\n1\n1\n2\n3\n5\n8\n13\n21\n34\n55\n89',
                        'hints': ['Use yield instead of return', 'Generators are memory efficient'],
                        'concepts': ['generators', 'yield'],
                    }
                ],
                'decorators': [
                    {
                        'id': 'a_dec_1',
                        'title': 'Timing Decorator',
                        'description': 'Create a decorator that measures function execution time.',
                        'starter_code': 'import time\n\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        # Your code here\n        \n    return wrapper\n\n@timer\ndef slow_function():\n    time.sleep(1)',
                        'expected_output': 'Function took approximately 1 second',
                        'hints': ['Decorators wrap functions', 'Use time.time() to measure'],
                        'concepts': ['decorators', 'time'],
                    }
                ]
            }
        }
    
    def generate_task(self, skill_level: str, concept: str = None, language: str = 'python') -> Dict:
        """Generate a task based on skill level and optionally concept"""
        if skill_level not in self.tasks:
            skill_level = 'beginner'
        
        level_tasks = self.tasks[skill_level]
        
        if concept and concept in level_tasks:
            task_list = level_tasks[concept]
        else:
            # Pick random concept from level
            concept = random.choice(list(level_tasks.keys()))
            task_list = level_tasks[concept]
        
        task = random.choice(task_list)
        return {
            **task,
            'skill_level': skill_level,
            'concept': concept,
            'language': language
        }
    
    def get_concept_list(self, skill_level: str) -> List[str]:
        """Get available concepts for a skill level"""
        if skill_level not in self.tasks:
            skill_level = 'beginner'
        
        return list(self.tasks[skill_level].keys())
    
    def get_task_by_id(self, task_id: str) -> Dict:
        """Get specific task by ID"""
        for level, concepts in self.tasks.items():
            for concept, tasks in concepts.items():
                for task in tasks:
                    if task['id'] == task_id:
                        return {**task, 'skill_level': level, 'concept': concept}
        
        return None
    
    def get_recommended_task(self, skill_level: str, weak_areas: List[str], strong_areas: List[str]) -> Dict:
        """Get recommended task based on progress"""
        # Prioritize weak areas
        if weak_areas:
            preferred_concept = weak_areas[0]
        else:
            # If no weak areas, suggest next level
            preferred_concept = None
        
        return self.generate_task(skill_level, preferred_concept)
    
    def get_task_difficulty_score(self, task_id: str) -> float:
        """Get difficulty score for a task (0-1)"""
        difficulty_map = {
            'b_': 0.2,
            'i_': 0.6,
            'a_': 0.9
        }
        
        for prefix, score in difficulty_map.items():
            if task_id.startswith(prefix):
                return score
        
        return 0.5
