from typing import Dict, List

class FeedbackEngine:
    """Generates comprehensive feedback based on code analysis and skill level"""
    
    def __init__(self, analyzer=None):
        """Initialize feedback engine with optional code analyzer"""
        self.analyzer = analyzer
    
    def generate_feedback(self, code: str, metrics: Dict, 
                         skill_level: str, concept_gaps: List[str] = None) -> Dict:
        """
        Generate comprehensive feedback for submitted code
        Integrates with MultiLanguageCodeAnalyzer metrics
        """
        feedback_sections = []
        score = 0
        
        # 1. Structure and Quality Feedback
        structure_feedback = self._analyze_structure(metrics, skill_level)
        feedback_sections.append(structure_feedback)
        score += structure_feedback.get('score', 0) * 0.3
        
        # 2. Complexity Feedback
        complexity_feedback = self._analyze_complexity(metrics, skill_level)
        feedback_sections.append(complexity_feedback)
        score += complexity_feedback.get('score', 0) * 0.2
        
        # 3. Error and Quality Feedback
        quality_feedback = self._analyze_quality(metrics, skill_level)
        feedback_sections.append(quality_feedback)
        score += quality_feedback.get('score', 0) * 0.25
        
        # 4. Concept-Specific Feedback
        if concept_gaps:
            concept_feedback = self._analyze_concepts(code, concept_gaps, skill_level)
            feedback_sections.append(concept_feedback)
            score += concept_feedback.get('score', 0) * 0.25
        
        return {
            'overall_score': min(100, score),
            'feedback_sections': feedback_sections,
            'summary': self._generate_summary(feedback_sections, skill_level),
            'suggestions': self._generate_suggestions(metrics, concept_gaps, skill_level)
        }
    
    def _analyze_structure(self, metrics: Dict, skill_level: str) -> Dict:
        """Analyze code structure"""
        feedback = {'category': 'Structure & Organization'}
        
        lines = metrics.get('total_lines', 0)
        functions = metrics.get('function_count', 0)
        classes = metrics.get('class_count', 0)
        
        positive_points = []
        improvement_points = []
        
        # Check function usage
        if skill_level == 'beginner':
            if functions >= 1:
                positive_points.append("Good! You're using functions to organize code.")
            else:
                improvement_points.append("Try breaking your code into functions for better organization.")
        
        elif skill_level == 'intermediate':
            if functions >= 2:
                positive_points.append("Great use of multiple functions for modularity.")
            else:
                improvement_points.append("Consider breaking code into more functions for better structure.")
            
            if classes >= 1:
                positive_points.append("Good! You're using classes for object-oriented design.")
            else:
                improvement_points.append("Consider using classes to organize related data and methods.")
        
        else:  # advanced
            if classes >= 1 and functions >= 3:
                positive_points.append("Excellent code organization with classes and functions.")
            else:
                improvement_points.append("Consider better separation of concerns with classes.")
        
        feedback['positive'] = positive_points
        feedback['improvements'] = improvement_points
        feedback['score'] = 80 if len(positive_points) >= 2 else (60 if len(positive_points) >= 1 else 40)
        
        return feedback
    
    def _analyze_complexity(self, metrics: Dict, skill_level: str) -> Dict:
        """Analyze code complexity"""
        feedback = {'category': 'Complexity'}
        
        complexity_index = metrics.get('cyclomatic_complexity', 1)
        nesting_level = metrics.get('nesting_level', 0)
        
        positive_points = []
        improvement_points = []
        
        if complexity_index <= 5:
            positive_points.append("Good! Your code has manageable complexity.")
        elif complexity_index <= 10:
            improvement_points.append("Consider breaking complex logic into smaller functions.")
        else:
            improvement_points.append("Your code is quite complex. Break it into simpler functions.")
        
        if nesting_level <= 3:
            positive_points.append("Good nesting level - code is easy to follow.")
        elif nesting_level <= 5:
            improvement_points.append("Try to reduce nesting depth for better readability.")
        else:
            improvement_points.append("High nesting level makes code hard to read. Refactor to reduce it.")
        
        feedback['positive'] = positive_points
        feedback['improvements'] = improvement_points
        feedback['score'] = 80 if complexity_index <= 5 else (60 if complexity_index <= 10 else 40)
        
        return feedback
    
    def _analyze_quality(self, metrics: Dict, skill_level: str) -> Dict:
        """Analyze code quality"""
        feedback = {'category': 'Code Quality'}
        
        positive_points = []
        improvement_points = []
        
        # Error count
        errors = metrics.get('errors', 0)
        if errors == 0:
            positive_points.append("Excellent! No syntax errors detected.")
        elif errors <= 2:
            improvement_points.append(f"You have {errors} error(s) to fix.")
        else:
            improvement_points.append(f"Work on fixing {errors} errors in your code.")
        
        # Maintainability
        maintainability = metrics.get('maintainability_index', 50)
        if maintainability >= 80:
            positive_points.append("Excellent maintainability - code is clean and readable.")
        elif maintainability >= 60:
            improvement_points.append("Code is moderately readable. Add comments and improve naming.")
        else:
            improvement_points.append("Work on readability. Use clear variable names and add comments.")
        
        feedback['positive'] = positive_points
        feedback['improvements'] = improvement_points
        feedback['score'] = min(100, max(0, maintainability))
        
        return feedback
    
    def _analyze_concepts(self, code: str, concept_gaps: List[str], skill_level: str) -> Dict:
        """Analyze concept usage"""
        feedback = {'category': 'Concept Usage'}
        
        positive_points = []
        improvement_points = []
        
        if not concept_gaps:
            positive_points.append("You've used all expected concepts well!")
            feedback['score'] = 90
        else:
            improvement_points.append(f"Missing concepts: {', '.join(concept_gaps[:3])}")
            feedback['score'] = max(40, 100 - (len(concept_gaps) * 10))
        
        feedback['positive'] = positive_points
        feedback['improvements'] = improvement_points
        
        return feedback
    
    def _generate_summary(self, sections: List[Dict], skill_level: str) -> str:
        """Generate overall feedback summary"""
        avg_score = sum(s.get('score', 0) for s in sections) / len(sections) if sections else 0
        
        summaries = {
            'beginner': {
                90: "Excellent work! You're grasping the fundamentals well.",
                80: "Good progress! Keep practicing these concepts.",
                70: "You're on the right track. Focus on the improvement areas.",
                60: "Keep practicing. Don't get discouraged!",
                0: "This is just the beginning. Keep coding!"
            },
            'intermediate': {
                90: "Outstanding! You're mastering intermediate concepts.",
                80: "Great work! You're improving your skills.",
                70: "Good effort. Focus on the areas for improvement.",
                60: "You're getting there. Keep practicing!",
                0: "Keep working on it. You'll get better!"
            },
            'advanced': {
                90: "Excellent! Your advanced skills are showing.",
                80: "Great work! Keep pushing to the next level.",
                70: "Good effort. Keep refining your techniques.",
                60: "You're working hard. Keep it up!",
                0: "Interesting attempt. Keep experimenting!"
            }
        }
        
        # Find appropriate summary
        level_summaries = summaries.get(skill_level, summaries['beginner'])
        for threshold in [90, 80, 70, 60, 0]:
            if avg_score >= threshold:
                return level_summaries[threshold]
        
        return "Keep coding and improving!"
    
    def _generate_suggestions(self, metrics: Dict, concept_gaps: List[str], 
                             skill_level: str) -> List[str]:
        """Generate actionable suggestions"""
        suggestions = []
        
        # Suggestion 1: Structure
        if metrics.get('function_count', 0) < 2 and skill_level != 'beginner':
            suggestions.append("💡 Use more functions to make your code modular and reusable.")
        
        # Suggestion 2: Comments
        if metrics.get('comment_lines', 0) == 0:
            suggestions.append("💡 Add comments to explain your logic and make code readable.")
        
        # Suggestion 3: Error handling
        if skill_level in ['intermediate', 'advanced'] and 'exception_handling' in (concept_gaps or []):
            suggestions.append("💡 Add try-except blocks to handle potential errors gracefully.")
        
        # Suggestion 4: Naming
        if metrics.get('long_variable_names', 0) > 5:
            suggestions.append("💡 Use shorter, more descriptive variable names.")
        
        # Suggestion 5: Next steps
        if concept_gaps:
            next_concept = concept_gaps[0]
            suggestions.append(f"📚 Next, work on mastering '{next_concept}' to improve your skills.")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def get_improvement_tips(self, metric_name: str, skill_level: str) -> str:
        """Get specific improvement tips for a metric"""
        tips = {
            'cyclomatic_complexity': {
                'beginner': 'Try breaking your code into smaller functions with single responsibilities.',
                'intermediate': 'Use helper functions or refactor nested logic into separate methods.',
                'advanced': 'Consider design patterns like Strategy or Chain of Responsibility.'
            },
            'maintainability_index': {
                'beginner': 'Add comments and use clear variable names.',
                'intermediate': 'Improve code structure and follow naming conventions.',
                'advanced': 'Apply design patterns and best practices for clarity.'
            },
            'nesting_level': {
                'beginner': 'Try using elif instead of nested ifs when possible.',
                'intermediate': 'Extract nested logic into separate methods.',
                'advanced': 'Use guard clauses to reduce nesting depth.'
            }
        }
        
        return tips.get(metric_name, {}).get(skill_level, 'Keep improving!')
