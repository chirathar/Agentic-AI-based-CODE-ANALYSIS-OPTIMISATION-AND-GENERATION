from typing import Dict, Tuple, Optional, List
from skill_detector import SkillDetector
from concept_analyzer import ConceptAnalyzer
from task_generator import TaskGenerator
from feedback_engine import FeedbackEngine
from progress_tracker import ProgressTracker
from explain_code import CodeExplainer
from multilang_analyzer import MultiLanguageCodeAnalyzer

class LearningAgent:
    """
    Main orchestrator for the agentic learning system.
    Coordinates all modules to provide adaptive learning experience.
    """
    
    def __init__(self):
        """Initialize all learning system components"""
        self.skill_detector = SkillDetector()
        self.concept_analyzer = ConceptAnalyzer()
        self.task_generator = TaskGenerator()
        self.feedback_engine = FeedbackEngine()
        self.progress_tracker = ProgressTracker()
        self.code_explainer = CodeExplainer()
        self.code_analyzer = MultiLanguageCodeAnalyzer()
    
    def process_submission(self, user_id: str, code: str, 
                          task_id: Optional[str] = None, 
                          language: str = 'python') -> Dict:
        """
        Main learning loop: Process code submission and return comprehensive response
        
        Flow:
        1. Analyze & explain code
        2. Detect skill level
        3. Identify concept gaps
        4. Generate feedback
        5. Create next task
        6. Save progress
        7. Return comprehensive response
        """
        
        # Step 1: Analyze code
        analysis_result = self.code_analyzer.analyze(code, language)
        metrics = analysis_result.get('metrics', {})
        
        # Step 2: Detect skill level
        skill_level, confidence = self.skill_detector.detect_skill_level(code, metrics)
        
        # Step 3: Identify concept gaps
        expected_concepts = []
        if task_id:
            task = self.task_generator.get_task_by_id(task_id)
            if task:
                expected_concepts = task.get('concepts', [])
        
        concept_gaps, gap_analysis = self.concept_analyzer.detect_gaps(code, expected_concepts)
        
        # Step 4: Generate feedback
        feedback = self.feedback_engine.generate_feedback(
            code, metrics, skill_level, concept_gaps
        )
        
        # Step 5: Generate next recommended task
        # Get user progress
        uid = self.progress_tracker.get_or_create_user(user_id)
        user_progress = self.progress_tracker.get_user_progress(uid)
        weak_areas = user_progress.get('weak_areas', [])
        strong_areas = user_progress.get('strong_areas', [])
        
        next_task = self.task_generator.get_recommended_task(
            skill_level, weak_areas, strong_areas
        )
        
        # Step 6: Save progress
        self.progress_tracker.save_completion(
            uid, 1,  # task_id placeholder
            code, 
            str(feedback.get('summary', '')),
            feedback.get('overall_score', 0),
            concept_gaps
        )
        
        # Update skill level
        self.progress_tracker.update_skill_level(uid, skill_level)
        
        # Step 7: Generate explanation
        explanation = self.code_explainer.explain_code(code, language, skill_level)
        
        return {
            'success': True,
            'submission': {
                'code': code,
                'language': language,
                'submitted_at': 'timestamp'
            },
            'analysis': {
                'skill_level': skill_level,
                'skill_confidence': confidence,
                'metrics': metrics,
            },
            'explanation': explanation,
            'concept_analysis': {
                'found_concepts': gap_analysis.get('found_concepts', []),
                'missing_concepts': concept_gaps,
                'concept_details': gap_analysis.get('concept_details', {}),
                'recommendations': gap_analysis.get('recommendations', []),
                'next_topics': gap_analysis.get('next_topics', []),
            },
            'feedback': feedback,
            'next_task': {
                'id': next_task.get('id'),
                'title': next_task.get('title'),
                'description': next_task.get('description'),
                'concept': next_task.get('concept'),
                'difficulty': next_task.get('skill_level'),
                'starter_code': next_task.get('starter_code'),
                'hints': next_task.get('hints', []),
            },
            'progress': {
                'total_completed': user_progress.get('total_tasks_completed', 0),
                'average_score': user_progress.get('avg_score', 0),
                'weak_areas': weak_areas,
                'strong_areas': strong_areas,
            }
        }
    
    def get_next_task(self, user_id: str) -> Dict:
        """Get next recommended task for user"""
        uid = self.progress_tracker.get_or_create_user(user_id)
        skill_level = self.progress_tracker.get_user_skill_level(uid)
        user_progress = self.progress_tracker.get_user_progress(uid)
        
        weak_areas = user_progress.get('weak_areas', [])
        strong_areas = user_progress.get('strong_areas', [])
        
        task = self.task_generator.get_recommended_task(
            skill_level, weak_areas, strong_areas
        )
        
        return {
            'task': task,
            'skill_level': skill_level,
            'difficulty': self.task_generator.get_task_difficulty_score(task['id'])
        }
    
    def get_user_progress(self, user_id: str) -> Dict:
        """Get comprehensive user progress report"""
        uid = self.progress_tracker.get_or_create_user(user_id)
        progress = self.progress_tracker.get_user_progress(uid)
        recent = self.progress_tracker.get_recent_completions(uid, 5)
        skill_level = self.progress_tracker.get_user_skill_level(uid)
        
        return {
            'user_id': uid,
            'skill_level': skill_level,
            'total_tasks_completed': progress.get('total_tasks_completed', 0),
            'average_score': progress.get('avg_score', 0),
            'weak_areas': progress.get('weak_areas', []),
            'strong_areas': progress.get('strong_areas', []),
            'recommended_topics': progress.get('recommended_topics', []),
            'recent_completions': recent,
        }
    
    def analyze_concept_gap(self, concept: str) -> Dict:
        """Get detailed information about a concept gap"""
        explanation = self.concept_analyzer.get_concept_explanation(concept)
        
        # Find tasks related to concept
        related_tasks = []
        for level in ['beginner', 'intermediate', 'advanced']:
            for task_concept, tasks in self.task_generator.tasks.get(level, {}).items():
                if task_concept == concept or concept in [t.get('concept', '') for t in tasks]:
                    related_tasks.extend([{
                        'title': t['title'],
                        'id': t['id'],
                        'difficulty': level
                    } for t in tasks])
        
        return {
            'concept': concept,
            'explanation': explanation,
            'related_tasks': related_tasks[:3],
        }
    
    def get_learning_path(self, user_id: str) -> Dict:
        """Get personalized learning path for user"""
        uid = self.progress_tracker.get_or_create_user(user_id)
        skill_level = self.progress_tracker.get_user_skill_level(uid)
        progress = self.progress_tracker.get_user_progress(uid)
        
        weak_areas = progress.get('weak_areas', [])
        
        # Define learning paths by skill level
        paths = {
            'beginner': [
                'variables', 'loops', 'conditionals', 'functions', 'lists'
            ],
            'intermediate': [
                'dictionaries', 'exception_handling', 'classes', 'list_comprehension'
            ],
            'advanced': [
                'generators', 'decorators', 'async_await', 'type_hints'
            ]
        }
        
        current_path = paths.get(skill_level, [])
        
        # Prioritize weak areas
        prioritized = []
        if weak_areas:
            prioritized = [a for a in weak_areas if a in current_path]
        
        remaining = [c for c in current_path if c not in prioritized]
        recommended_order = prioritized + remaining
        
        return {
            'current_level': skill_level,
            'recommended_path': recommended_order,
            'focus_areas': weak_areas,
            'milestones': {
                'beginner': 'Master basic programming concepts',
                'intermediate': 'Learn intermediate techniques and OOP',
                'advanced': 'Master advanced concepts and patterns'
            }[skill_level]
        }
