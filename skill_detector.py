from typing import Dict, Tuple
import re

class SkillDetector:
    """ML-based skill level detection from code submissions"""
    
    def __init__(self):
        """Initialize skill detector with heuristic rules"""
        self.beginner_patterns = {
            'basic_syntax': r'(def|class|if|for|while)',
            'print_usage': r'print\(',
            'variable_assignment': r'=',
            'simple_loops': r'for .* in|while .*:',
        }
        
        self.intermediate_patterns = {
            'list_comprehension': r'\[.*for.*in.*\]',
            'lambda_functions': r'lambda',
            'decorators': r'@\w+',
            'context_managers': r'with .*:',
            'exception_handling': r'try:|except|finally:',
            'data_structures': r'dict|set|tuple',
            'string_formatting': r'f".*{.*}|\.format\(',
        }
        
        self.advanced_patterns = {
            'generators': r'yield',
            'metaclasses': r'metaclass',
            'async_await': r'async def|await',
            'type_hints': r'->\s*\w+|:\s*\w+\s*=',
            'property_decorators': r'@property',
            'abstract_base_classes': r'ABC|abstractmethod',
            'multiple_inheritance': r'class.*\(.*,.*\)',
            'context_vars': r'__enter__|__exit__',
            'descriptors': r'__get__|__set__',
        }
    
    def detect_skill_level(self, code: str, metrics: Dict = None) -> Tuple[str, float]:
        """
        Detect skill level from code
        Returns: (skill_level: str, confidence: float)
        """
        if not code or not code.strip():
            return 'beginner', 0.5
        
        scores = {
            'beginner': self._count_patterns(code, self.beginner_patterns),
            'intermediate': self._count_patterns(code, self.intermediate_patterns),
            'advanced': self._count_patterns(code, self.advanced_patterns)
        }
        
        # Get quality metrics
        if metrics:
            quality_score = metrics.get('maintainability_index', 50)
            error_count = metrics.get('errors', 0)
        else:
            quality_score = 50
            error_count = 0
        
        # Adjust scores based on code quality
        if error_count > 5:
            scores['intermediate'] *= 0.7
            scores['advanced'] *= 0.5
        
        if quality_score < 40:
            scores['advanced'] *= 0.6
        
        # Determine skill level
        if scores['advanced'] > 2:
            skill_level = 'advanced'
            confidence = min(0.95, 0.7 + (scores['advanced'] * 0.1))
        elif scores['intermediate'] > 2:
            skill_level = 'intermediate'
            confidence = min(0.95, 0.6 + (scores['intermediate'] * 0.1))
        else:
            skill_level = 'beginner'
            confidence = min(0.95, 0.5 + (scores['beginner'] * 0.1))
        
        return skill_level, confidence
    
    def _count_patterns(self, code: str, patterns: Dict[str, str]) -> int:
        """Count occurrences of patterns in code"""
        count = 0
        for pattern_name, pattern in patterns.items():
            matches = len(re.findall(pattern, code, re.MULTILINE))
            count += min(matches, 3)  # Cap contribution per pattern
        return count
    
    def get_skill_indicators(self, code: str) -> Dict:
        """Get detailed skill indicators"""
        return {
            'has_functions': bool(re.search(r'def\s+\w+', code)),
            'has_classes': bool(re.search(r'class\s+\w+', code)),
            'has_error_handling': bool(re.search(r'try:|except|finally:', code)),
            'has_list_comprehension': bool(re.search(r'\[.*for.*in.*\]', code)),
            'has_lambda': bool(re.search(r'lambda', code)),
            'has_decorators': bool(re.search(r'@\w+', code)),
            'has_type_hints': bool(re.search(r'->\s*\w+|:\s*\w+\s*=', code)),
            'has_async': bool(re.search(r'async def|await', code)),
            'has_generators': bool(re.search(r'yield', code)),
            'has_context_managers': bool(re.search(r'with .*:', code)),
            'lines_of_code': len(code.split('\n')),
            'code_complexity': self._estimate_complexity(code),
        }
    
    def _estimate_complexity(self, code: str) -> str:
        """Estimate code complexity"""
        lines = len(code.split('\n'))
        nesting_level = max([len(line) - len(line.lstrip()) for line in code.split('\n')])
        has_loops = bool(re.search(r'for|while', code))
        has_conditionals = bool(re.search(r'if|elif|else', code))
        has_functions = bool(re.search(r'def', code))
        
        complexity_score = 0
        if has_loops:
            complexity_score += 2
        if has_conditionals:
            complexity_score += 1
        if has_functions:
            complexity_score += 1
        
        complexity_score += nesting_level // 4
        
        if complexity_score >= 5:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def get_missing_concepts(self, current_level: str) -> list:
        """Get concepts missing from current skill level"""
        level_concepts = {
            'beginner': [
                'variables', 'loops', 'conditionals', 'functions',
                'lists', 'strings', 'basic input/output'
            ],
            'intermediate': [
                'dictionaries', 'lambda functions', 'list comprehension',
                'decorators', 'exception handling', 'file I/O', 'OOP basics'
            ],
            'advanced': [
                'generators', 'async/await', 'type hints', 'design patterns',
                'metaclasses', 'descriptors', 'performance optimization'
            ]
        }
        
        if current_level == 'beginner':
            return level_concepts['beginner'] + level_concepts['intermediate'] + level_concepts['advanced']
        elif current_level == 'intermediate':
            return level_concepts['intermediate'] + level_concepts['advanced']
        else:
            return level_concepts['advanced']
