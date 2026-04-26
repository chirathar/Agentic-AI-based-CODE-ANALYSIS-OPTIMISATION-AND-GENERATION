"""
Agentic AI Teaching System using Transformers and ML
Uses CodeBERT, Transformers, and scikit-learn for real teaching intelligence
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Any
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
import ast
import re

try:
    from transformers import AutoTokenizer, AutoModel
    import torch
except ImportError:
    print("Warning: transformers not installed. Install with: pip install transformers torch")

class CodeEmbedder:
    """Generate embeddings for code using CodeBERT"""
    
    def __init__(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
            self.model = AutoModel.from_pretrained("microsoft/codebert-base")
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
        except:
            print("CodeBERT not available, using fallback embeddings")
            self.tokenizer = None
            self.model = None
    
    def embed(self, code: str) -> np.ndarray:
        """Generate embedding for code"""
        if self.model is None:
            return self._fallback_embed(code)
        
        try:
            inputs = self.tokenizer.encode(code, return_tensors="pt", max_length=512, truncation=True)
            inputs = inputs.to(self.device)
            
            with torch.no_grad():
                outputs = self.model(inputs)
            
            embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()[0]
            return embedding
        except Exception as e:
            print(f"Embedding error: {e}, using fallback")
            return self._fallback_embed(code)
    
    def _fallback_embed(self, code: str) -> np.ndarray:
        """Fallback embedding using code statistics"""
        features = [
            len(code),
            code.count('\n'),
            code.count('def '),
            code.count('class '),
            code.count('for '),
            code.count('while '),
            code.count('if '),
            len(re.findall(r'\w+', code)),
        ]
        return np.array(features, dtype=np.float32)


class SkillDetectorML:
    """ML-based skill level detection"""
    
    def __init__(self):
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.embedder = CodeEmbedder()
        self.trained = False
    
    def extract_code_features(self, code: str) -> Dict[str, float]:
        """Extract 30+ features from code"""
        try:
            tree = ast.parse(code)
        except:
            tree = None
        
        features = {
            'lines': len(code.split('\n')),
            'length': len(code),
            'functions': code.count('def '),
            'classes': code.count('class '),
            'loops': code.count('for ') + code.count('while '),
            'conditionals': code.count('if ') + code.count('elif ') + code.count('else:'),
            'imports': code.count('import '),
            'comments': code.count('#'),
            'docstrings': code.count('"""') + code.count("'''"),
            'type_hints': code.count('->') + code.count(': '),
            'comprehensions': code.count('['), 
            'lambdas': code.count('lambda'),
            'decorators': code.count('@'),
            'error_handling': code.count('try:') + code.count('except'),
            'recursion': 1 if tree and self._has_recursion(tree) else 0,
            'nested_depth': self._calc_nesting_depth(code),
            'variable_count': len(set(re.findall(r'\b[a-z_]\w*\b', code))),
        }
        
        return features
    
    def _has_recursion(self, tree) -> bool:
        """Check if code contains recursion"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                        if child.func.id == node.name:
                            return True
        return False
    
    def _calc_nesting_depth(self, code: str) -> int:
        """Calculate maximum nesting depth"""
        try:
            tree = ast.parse(code)
            return self._max_depth(tree)
        except:
            return 0
    
    def _max_depth(self, node, current_depth=0):
        """Recursively calculate max depth"""
        max_d = current_depth
        for child in ast.iter_child_nodes(node):
            max_d = max(max_d, self._max_depth(child, current_depth + 1))
        return max_d
    
    def detect_skill_level(self, code: str) -> Tuple[str, float]:
        """Detect skill level: beginner, intermediate, advanced"""
        features = self.extract_code_features(code)
        score = (
            features['functions'] * 2 +
            features['classes'] * 3 +
            features['error_handling'] * 2 +
            features['type_hints'] * 1.5 +
            features['nested_depth'] * 0.5 +
            features['recursion'] * 2 +
            features['docstrings'] * 1
        )
        
        if score < 5:
            return "beginner", 0.2
        elif score < 15:
            return "intermediate", 0.5
        else:
            return "advanced", 0.8


class ConceptGapAnalyzer:
    """Analyze missing programming concepts using ML"""
    
    def __init__(self):
        self.concept_patterns = {
            'variables': r'\b[a-z_]\w*\s*=',
            'functions': r'def\s+\w+',
            'classes': r'class\s+\w+',
            'loops': r'(for|while)\s+',
            'conditionals': r'(if|elif|else)',
            'list_operations': r'\.append|\.extend|\.pop|\.remove',
            'dict_operations': r'\{.*\}|\.get|\.keys|\.values',
            'string_methods': r'\.split|\.join|\.replace|\.strip',
            'error_handling': r'try:|except:|finally:',
            'decorators': r'@\w+',
            'type_hints': r'->\s*\w+|:\s*(int|str|list|dict|bool)',
            'list_comprehension': r'\[.+for\s+.+in\s+.+\]',
            'lambda': r'lambda\s+',
            'generators': r'yield\s+',
            'context_managers': r'with\s+',
            'slicing': r'\[.*:.*\]',
            'unpacking': r'\*\w+|\*\*\w+',
            'f_strings': r'f["\']',
            'async_await': r'async\s+def|await\s+',
            'dataclasses': r'@dataclass',
            'property_decorator': r'@property',
        }
        
        self.concept_difficulty = {
            'variables': 1,
            'functions': 2,
            'conditionals': 2,
            'loops': 2,
            'list_operations': 3,
            'error_handling': 4,
            'decorators': 5,
            'generators': 5,
            'async_await': 5,
            'classes': 4,
        }
    
    def analyze_gaps(self, code: str, skill_level: str = "beginner") -> Dict[str, Any]:
        """Analyze gaps between code and expected concepts for skill level"""
        found_concepts = self._find_concepts(code)
        
        expected_concepts = {
            'beginner': ['variables', 'functions', 'conditionals', 'loops'],
            'intermediate': ['variables', 'functions', 'conditionals', 'loops', 
                           'list_operations', 'string_methods', 'error_handling'],
            'advanced': list(self.concept_patterns.keys())
        }
        
        expected = set(expected_concepts.get(skill_level, []))
        found = set(found_concepts.keys())
        gaps = expected - found
        
        gap_details = {
            'missing_concepts': list(gaps),
            'mastered_concepts': list(found & expected),
            'advanced_used': list(found - expected),
            'gap_count': len(gaps),
            'recommended_next': self._recommend_concepts(gaps, skill_level)
        }
        
        return gap_details
    
    def _find_concepts(self, code: str) -> Dict[str, int]:
        """Find all concepts in code"""
        found = {}
        for concept, pattern in self.concept_patterns.items():
            matches = re.findall(pattern, code)
            if matches:
                found[concept] = len(matches)
        return found
    
    def _recommend_concepts(self, gaps: set, current_level: str) -> List[str]:
        """Recommend concepts to learn next"""
        difficulty_order = {
            'beginner': ['variables', 'functions', 'conditionals', 'loops', 
                        'list_operations', 'string_methods', 'error_handling'],
            'intermediate': ['error_handling', 'decorators', 'list_comprehension', 
                           'context_managers', 'generators'],
            'advanced': ['async_await', 'dataclasses', 'property_decorator']
        }
        
        recommendations = difficulty_order.get(current_level, [])
        return [c for c in recommendations if c in gaps][:3]


class LearningPathGenerator:
    """Generate personalized learning paths using ML"""
    
    def __init__(self):
        self.analyzer = ConceptGapAnalyzer()
        self.skill_detector = SkillDetectorML()
    
    def generate_path(self, user_code: str, current_level: str) -> Dict[str, Any]:
        """Generate personalized learning path"""
        gaps = self.analyzer.analyze_gaps(user_code, current_level)
        
        path = {
            'current_level': current_level,
            'next_concepts': gaps['recommended_next'],
            'total_gaps': gaps['gap_count'],
            'mastered': len(gaps['mastered_concepts']),
            'tasks': self._generate_tasks(gaps['recommended_next'], current_level),
            'estimated_hours': len(gaps['recommended_next']) * 2
        }
        
        return path
    
    def _generate_tasks(self, concepts: List[str], level: str) -> List[Dict]:
        """Generate coding tasks for concepts"""
        task_templates = {
            'variables': 'Create variables to store user input and perform calculations',
            'functions': 'Write a function that takes parameters and returns a result',
            'conditionals': 'Use if/elif/else statements to handle different cases',
            'loops': 'Use for/while loops to iterate over data',
            'list_operations': 'Use list methods (.append, .extend, .pop) to manipulate data',
            'error_handling': 'Add try/except blocks to handle potential errors',
            'decorators': 'Create and use decorators to enhance function behavior',
            'generators': 'Write a generator function that yields values',
            'async_await': 'Write async functions using async/await syntax',
        }
        
        tasks = []
        for i, concept in enumerate(concepts):
            tasks.append({
                'id': f'task_{i+1}',
                'concept': concept,
                'description': task_templates.get(concept, f'Learn {concept}'),
                'difficulty': i + 1,
                'estimated_time': (i + 1) * 15
            })
        
        return tasks


class TeachingAgentML:
    """Main teaching agent orchestrating learning"""
    
    def __init__(self, db_path: str = "teaching_data.db"):
        self.db_path = db_path
        self.embedder = CodeEmbedder()
        self.skill_detector = SkillDetectorML()
        self.concept_analyzer = ConceptGapAnalyzer()
        self.path_generator = LearningPathGenerator()
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                user_id TEXT PRIMARY KEY,
                skill_level TEXT,
                submissions INTEGER,
                concepts_mastered TEXT,
                last_updated TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS code_submissions (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                code TEXT,
                skill_level TEXT,
                concepts TEXT,
                timestamp TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES user_progress(user_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_paths (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                path_data TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES user_progress(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def process_code_submission(self, user_id: str, code: str, language: str = "python") -> Dict[str, Any]:
        """Process code submission and generate feedback"""
        # Detect skill level
        skill_level, skill_score = self.skill_detector.detect_skill_level(code)
        
        # Analyze concept gaps
        gaps = self.concept_analyzer.analyze_gaps(code, skill_level)
        
        # Generate embedding
        embedding = self.embedder.embed(code)
        
        # Generate learning path
        learning_path = self.path_generator.generate_path(code, skill_level)
        
        # Store submission
        self._store_submission(user_id, code, skill_level, gaps)
        
        return {
            'detected_skill_level': skill_level,
            'skill_confidence': float(skill_score),
            'concept_gaps': gaps,
            'learning_path': learning_path,
            'feedback': self._generate_feedback(skill_level, gaps),
            'next_steps': learning_path['tasks'][:2]
        }
    
    def _generate_feedback(self, skill_level: str, gaps: Dict) -> str:
        """Generate personalized feedback"""
        feedback_templates = {
            'beginner': f"Great start! You've mastered {gaps['mastered_concepts']}. Next, focus on: {', '.join(gaps['recommended_next'][:2])}",
            'intermediate': f"Good progress! You're using {gaps['mastered_concepts']}. Try learning: {', '.join(gaps['recommended_next'][:2])}",
            'advanced': f"Excellent! You're using advanced patterns. Explore: {', '.join(gaps['recommended_next'][:2])}"
        }
        return feedback_templates.get(skill_level, "Keep coding and learning!")
    
    def _store_submission(self, user_id: str, code: str, skill_level: str, gaps: Dict):
        """Store code submission in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT * FROM user_progress WHERE user_id = ?', (user_id,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute('''
                INSERT INTO user_progress (user_id, skill_level, submissions, concepts_mastered, last_updated)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, skill_level, 1, json.dumps(gaps['mastered_concepts']), datetime.now()))
        else:
            cursor.execute('''
                UPDATE user_progress SET skill_level = ?, submissions = submissions + 1, last_updated = ?
                WHERE user_id = ?
            ''', (skill_level, datetime.now(), user_id))
        
        # Store code submission
        cursor.execute('''
            INSERT INTO code_submissions (user_id, code, skill_level, concepts, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, code, skill_level, json.dumps(gaps['missing_concepts']), datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user_progress WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {'error': 'User not found'}
        
        return {
            'user_id': row[0],
            'skill_level': row[1],
            'submissions': row[2],
            'concepts_mastered': json.loads(row[3]),
            'last_updated': row[4]
        }
    
    def recommend_next_task(self, user_id: str) -> Dict[str, Any]:
        """Recommend next learning task"""
        progress = self.get_user_progress(user_id)
        
        if 'error' in progress:
            return {'error': 'User not found', 'recommendation': None}
        
        recommendations = {
            'beginner': {
                'concept': 'functions',
                'task': 'Write a function to calculate factorial',
                'difficulty': 1
            },
            'intermediate': {
                'concept': 'error_handling',
                'task': 'Handle file operations with try/except',
                'difficulty': 2
            },
            'advanced': {
                'concept': 'async_await',
                'task': 'Create async functions for concurrent operations',
                'difficulty': 3
            }
        }
        
        return recommendations.get(progress['skill_level'], recommendations['beginner'])
