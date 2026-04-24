import re
from typing import List, Dict, Tuple

class ConceptAnalyzer:
    """Analyzes code for concept gaps and learning needs"""
    
    def __init__(self):
        """Initialize concept analyzer with concept patterns"""
        self.concept_patterns = {
            'variables': {
                'patterns': [r'\w+\s*=\s*\d+', r'\w+\s*=\s*["\'].*["\']'],
                'importance': 'critical',
                'level': 'beginner'
            },
            'loops': {
                'patterns': [r'for\s+\w+\s+in|while\s+'],
                'importance': 'critical',
                'level': 'beginner'
            },
            'conditionals': {
                'patterns': [r'if\s+|elif\s+|else:'],
                'importance': 'critical',
                'level': 'beginner'
            },
            'functions': {
                'patterns': [r'def\s+\w+\s*\('],
                'importance': 'high',
                'level': 'beginner'
            },
            'lists': {
                'patterns': [r'\[.*\]', r'list\('],
                'importance': 'high',
                'level': 'beginner'
            },
            'dictionaries': {
                'patterns': [r'\{.*:\s*.*\}', r'dict\('],
                'importance': 'high',
                'level': 'intermediate'
            },
            'list_comprehension': {
                'patterns': [r'\[.*for.*in.*\]'],
                'importance': 'medium',
                'level': 'intermediate'
            },
            'lambda_functions': {
                'patterns': [r'lambda\s+.*:'],
                'importance': 'medium',
                'level': 'intermediate'
            },
            'exception_handling': {
                'patterns': [r'try:|except|finally:|raise'],
                'importance': 'high',
                'level': 'intermediate'
            },
            'decorators': {
                'patterns': [r'@\w+'],
                'importance': 'medium',
                'level': 'intermediate'
            },
            'context_managers': {
                'patterns': [r'with\s+.*:'],
                'importance': 'medium',
                'level': 'intermediate'
            },
            'generators': {
                'patterns': [r'yield\s+'],
                'importance': 'medium',
                'level': 'advanced'
            },
            'type_hints': {
                'patterns': [r'->\s*\w+', r':\s*\w+\s*='],
                'importance': 'low',
                'level': 'advanced'
            },
            'async_await': {
                'patterns': [r'async\s+def|await\s+'],
                'importance': 'medium',
                'level': 'advanced'
            },
            'classes': {
                'patterns': [r'class\s+\w+'],
                'importance': 'high',
                'level': 'intermediate'
            },
            'inheritance': {
                'patterns': [r'class\s+\w+\s*\(.*\):'],
                'importance': 'medium',
                'level': 'intermediate'
            },
            'string_formatting': {
                'patterns': [r'f".*{.*}"', r'\.format\(', r'%\s*\('],
                'importance': 'low',
                'level': 'beginner'
            },
            'file_operations': {
                'patterns': [r'open\(', r'\.read\(\)', r'\.write\('],
                'importance': 'high',
                'level': 'intermediate'
            }
        }
    
    def detect_gaps(self, code: str, expected_concepts: List[str] = None) -> Tuple[List[str], Dict]:
        """
        Detect concept gaps in submitted code
        Returns: (missing_concepts, analysis_dict)
        """
        found_concepts = self.extract_concepts(code)
        
        # If expected concepts provided, check for gaps
        if expected_concepts:
            missing = [c for c in expected_concepts if c not in found_concepts]
        else:
            # Find missing foundational concepts
            missing = self._find_missing_foundational(found_concepts)
        
        # Detailed analysis
        analysis = {
            'found_concepts': found_concepts,
            'missing_concepts': missing,
            'concept_details': self._analyze_concept_usage(code, found_concepts),
            'recommendations': self._generate_recommendations(missing, found_concepts),
            'next_topics': self._suggest_next_topics(found_concepts)
        }
        
        return missing, analysis
    
    def extract_concepts(self, code: str) -> List[str]:
        """Extract all concepts found in code"""
        found = []
        
        for concept, info in self.concept_patterns.items():
            for pattern in info['patterns']:
                if re.search(pattern, code, re.MULTILINE):
                    found.append(concept)
                    break
        
        return found
    
    def _find_missing_foundational(self, found_concepts: List[str]) -> List[str]:
        """Find missing foundational concepts"""
        foundational = ['variables', 'loops', 'conditionals', 'functions', 'lists']
        missing = [c for c in foundational if c not in found_concepts]
        return missing
    
    def _analyze_concept_usage(self, code: str, concepts: List[str]) -> Dict:
        """Analyze how well concepts are used"""
        analysis = {}
        
        for concept in concepts:
            info = self.concept_patterns.get(concept, {})
            patterns = info.get('patterns', [])
            
            usage_count = 0
            for pattern in patterns:
                usage_count += len(re.findall(pattern, code, re.MULTILINE))
            
            # Assess usage quality
            if usage_count == 0:
                quality = 'unused'
            elif usage_count < 3:
                quality = 'minimal'
            elif usage_count < 10:
                quality = 'moderate'
            else:
                quality = 'extensive'
            
            analysis[concept] = {
                'count': usage_count,
                'quality': quality,
                'importance': info.get('importance', 'medium'),
                'level': info.get('level', 'beginner')
            }
        
        return analysis
    
    def _generate_recommendations(self, missing: List[str], found: List[str]) -> List[str]:
        """Generate learning recommendations"""
        recommendations = []
        
        # Prioritize by importance and foundational needs
        priority_order = {
            'variables': 1,
            'loops': 2,
            'conditionals': 3,
            'functions': 4,
            'lists': 5,
            'dictionaries': 6,
            'exception_handling': 7,
            'classes': 8,
        }
        
        sorted_missing = sorted(missing, key=lambda x: priority_order.get(x, 99))
        
        for concept in sorted_missing[:3]:  # Top 3 recommendations
            info = self.concept_patterns.get(concept, {})
            importance = info.get('importance', 'medium')
            level = info.get('level', 'beginner')
            
            if importance == 'critical':
                rec = f"Master '{concept}' - this is essential for your skill level"
            elif importance == 'high':
                rec = f"Learn '{concept}' to improve your programming foundation"
            else:
                rec = f"Explore '{concept}' to enhance your skills"
            
            recommendations.append(rec)
        
        return recommendations
    
    def _suggest_next_topics(self, found_concepts: List[str]) -> List[str]:
        """Suggest next learning topics based on current knowledge"""
        level_progressions = {
            'beginner': {
                'prerequisites': ['variables', 'loops', 'conditionals'],
                'next': ['functions', 'lists', 'strings']
            },
            'intermediate': {
                'prerequisites': ['functions', 'lists', 'dictionaries'],
                'next': ['classes', 'exception_handling', 'file_operations']
            },
            'advanced': {
                'prerequisites': ['classes', 'exception_handling'],
                'next': ['generators', 'decorators', 'async_await']
            }
        }
        
        # Determine current learning phase
        current_phase = 'beginner'
        if all(c in found_concepts for c in ['functions', 'lists']):
            current_phase = 'intermediate'
        if all(c in found_concepts for c in ['classes', 'exception_handling']):
            current_phase = 'advanced'
        
        next_topics = level_progressions[current_phase]['next']
        return next_topics
    
    def get_concept_explanation(self, concept: str) -> Dict:
        """Get explanation for a concept"""
        explanations = {
            'variables': {
                'definition': 'Named containers that store data values',
                'why_learn': 'Essential for storing and manipulating data',
                'example': 'name = "John"  # stores text\nage = 25  # stores number'
            },
            'loops': {
                'definition': 'Structures that repeat code blocks multiple times',
                'why_learn': 'Allows processing of multiple items without repetition',
                'example': 'for i in range(5):\n    print(i)  # prints 0 to 4'
            },
            'conditionals': {
                'definition': 'Decision structures that execute code based on conditions',
                'why_learn': 'Enables different code paths based on conditions',
                'example': 'if age >= 18:\n    print("Adult")\nelse:\n    print("Minor")'
            },
            'functions': {
                'definition': 'Reusable blocks of code that perform specific tasks',
                'why_learn': 'Reduces code repetition and improves organization',
                'example': 'def greet(name):\n    return f"Hello, {name}!"'
            },
            'lists': {
                'definition': 'Ordered collections of items',
                'why_learn': 'Essential for storing and manipulating multiple values',
                'example': 'fruits = ["apple", "banana", "orange"]\nprint(fruits[0])  # apple'
            },
            'dictionaries': {
                'definition': 'Key-value pairs that map keys to values',
                'why_learn': 'Efficient way to organize and access related data',
                'example': 'person = {"name": "John", "age": 25}\nprint(person["name"])'
            },
            'exception_handling': {
                'definition': 'Mechanism to handle errors gracefully',
                'why_learn': 'Prevents crashes and allows recovery from errors',
                'example': 'try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print("Cannot divide by zero")'
            },
            'classes': {
                'definition': 'Blueprints for creating objects with attributes and methods',
                'why_learn': 'Enables object-oriented programming and code organization',
                'example': 'class Dog:\n    def __init__(self, name):\n        self.name = name'
            }
        }
        
        return explanations.get(concept, {
            'definition': 'No explanation available',
            'why_learn': 'Learn more about this concept',
            'example': 'No example available'
        })
