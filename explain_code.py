"""
Code Explanation Module - Adaptive Learning Agent
Provides multi-level code explanations from beginner to advanced
"""

class CodeExplainer:
    """Main class for explaining code at different skill levels"""
    
    def __init__(self):
        self.skill_levels = {
            'beginner': 'Explain what this code does in simple terms',
            'intermediate': 'Explain the logic flow and key concepts',
            'advanced': 'Analyze the algorithm, complexity, and design patterns'
        }
    
    def detect_skill_level(self, code_quality_score, error_count):
        """
        Detect user skill level based on code metrics
        
        Args:
            code_quality_score: Quality score from 0-100
            error_count: Number of errors in the code
            
        Returns:
            str: Skill level ('beginner', 'intermediate', 'advanced')
        """
        if code_quality_score > 80 and error_count < 2:
            return "advanced"
        elif code_quality_score > 50:
            return "intermediate"
        return "beginner"
    
    def explain_code(self, code, language='python', skill_level=None):
        """
        Provide code explanation at appropriate skill level
        
        Args:
            code: Code string to explain
            language: Programming language
            skill_level: Target skill level (auto-detect if None)
            
        Returns:
            dict: Explanation with structure appropriate for skill level
        """
        if not code.strip():
            return {"error": "No code provided"}
        
        # Auto-detect skill level if not provided
        if skill_level is None:
            quality_score = self._assess_code_quality(code)
            error_count = self._count_errors(code)
            skill_level = self.detect_skill_level(quality_score, error_count)
        
        explanation = {
            'skill_level': skill_level,
            'language': language,
            'code': code
        }
        
        if skill_level == 'beginner':
            explanation['overview'] = self._beginner_explanation(code, language)
        elif skill_level == 'intermediate':
            explanation['overview'] = self._intermediate_explanation(code, language)
        else:
            explanation['overview'] = self._advanced_explanation(code, language)
        
        # Add concept gaps if identified
        gaps = self._identify_concept_gaps(code)
        if gaps:
            explanation['concept_gaps'] = gaps
        
        return explanation
    
    def _beginner_explanation(self, code, language):
        """Generate beginner-friendly explanation"""
        lines = code.split('\n')
        
        explanation = f"This {language} code does the following:\n\n"
        
        # Simple breakdown by line
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                explanation += f"Line {i}: {self._explain_line_simple(stripped, language)}\n"
        
        explanation += "\nKey concepts used:\n"
        explanation += self._extract_concepts_simple(code, language)
        
        return explanation
    
    def _intermediate_explanation(self, code, language):
        """Generate intermediate-level explanation"""
        explanation = f"This {language} code implements the following logic:\n\n"
        
        # Identify main components
        components = self._identify_components(code, language)
        for component in components:
            explanation += f"• {component}\n"
        
        explanation += "\nAlgorithm flow:\n"
        explanation += self._trace_algorithm_flow(code)
        
        explanation += "\nDesign patterns used:\n"
        explanation += self._identify_patterns(code)
        
        return explanation
    
    def _advanced_explanation(self, code, language):
        """Generate advanced technical explanation"""
        explanation = f"Technical Analysis of {language} Code:\n\n"
        
        explanation += "Architecture:\n"
        explanation += self._analyze_architecture(code)
        
        explanation += "\nTime & Space Complexity:\n"
        explanation += self._analyze_complexity(code)
        
        explanation += "\nPotential Issues:\n"
        explanation += self._identify_issues(code)
        
        explanation += "\nOptimization Opportunities:\n"
        explanation += self._suggest_optimizations(code)
        
        return explanation
    
    def _explain_line_simple(self, line, language):
        """Simple explanation of a single line"""
        if 'def ' in line or 'function' in line:
            return "This defines a new function"
        elif '=' in line:
            return "This assigns a value to a variable"
        elif 'if ' in line or 'while' in line or 'for' in line:
            return "This is a control flow statement"
        elif 'return' in line:
            return "This returns a value from the function"
        else:
            return "This performs an operation"
    
    def _extract_concepts_simple(self, code, language):
        """Extract simple concepts from code"""
        concepts = []
        if 'def ' in code:
            concepts.append("✓ Functions - reusable blocks of code")
        if 'class ' in code:
            concepts.append("✓ Classes - templates for creating objects")
        if 'for ' in code or 'while' in code:
            concepts.append("✓ Loops - repeat operations")
        if 'if ' in code:
            concepts.append("✓ Conditionals - make decisions")
        
        return "\n".join(concepts) if concepts else "Basic syntax and operations"
    
    def _identify_components(self, code, language):
        """Identify major components in the code"""
        components = []
        
        if 'def ' in code:
            functions = [line.strip() for line in code.split('\n') if line.strip().startswith('def ')]
            components.extend([f"Function: {f}" for f in functions[:3]])
        
        if 'class ' in code:
            classes = [line.strip() for line in code.split('\n') if line.strip().startswith('class ')]
            components.extend([f"Class: {c}" for c in classes[:3]])
        
        return components if components else ["Data processing", "Operations"]
    
    def _trace_algorithm_flow(self, code):
        """Trace the flow of the algorithm"""
        return "1. Input received\n2. Process data\n3. Output result\n"
    
    def _identify_patterns(self, code):
        """Identify design patterns used"""
        patterns = []
        
        if 'class ' in code and 'def __init__' in code:
            patterns.append("• Object-Oriented Design")
        if 'def ' in code and code.count('def ') > 3:
            patterns.append("• Functional Programming")
        if 'try:' in code or 'except' in code:
            patterns.append("• Error Handling Pattern")
        
        return "\n".join(patterns) if patterns else "Imperative Programming"
    
    def _analyze_architecture(self, code):
        """Analyze the architectural structure"""
        return "Module structure with clear separation of concerns\n"
    
    def _analyze_complexity(self, code):
        """Analyze time and space complexity"""
        lines = code.split('\n')
        loop_count = sum(1 for line in lines if 'for ' in line or 'while' in line)
        
        if loop_count == 0:
            return "Time: O(1), Space: O(1) - Constant time and space"
        elif loop_count == 1:
            return "Time: O(n), Space: O(1) - Linear time complexity"
        else:
            return f"Time: O(n^{loop_count}), Space: O(1) - Polynomial complexity"
    
    def _identify_issues(self, code):
        """Identify potential issues"""
        issues = []
        
        if len(code.split('\n')) > 100:
            issues.append("• Long code length - consider refactoring")
        if code.count('global ') > 0:
            issues.append("• Global variable usage - consider scope management")
        if 'TODO' in code or 'FIXME' in code:
            issues.append("• Incomplete implementation markers found")
        
        return "\n".join(issues) if issues else "Code appears well-structured"
    
    def _suggest_optimizations(self, code):
        """Suggest optimization opportunities"""
        suggestions = []
        
        if 'append(' in code:
            suggestions.append("• Consider using list comprehension")
        if code.count('for ') > 2:
            suggestions.append("• Potential for vectorization")
        if 'try:' not in code:
            suggestions.append("• Add error handling")
        
        return "\n".join(suggestions) if suggestions else "Code is already well-optimized"
    
    def _identify_concept_gaps(self, code):
        """Identify concept gaps in the code"""
        gaps = []
        
        if 'for ' in code and 'for ' in code:
            nested = code.count('for ') > 1
            if nested and 'O(n' not in code:
                gaps.append("May lack understanding of nested loop complexity")
        
        if 'import ' not in code and 'def ' in code:
            gaps.append("No external dependencies - good practice")
        
        return gaps
    
    def _assess_code_quality(self, code):
        """Simple assessment of code quality (0-100)"""
        score = 50
        
        if code.count('\n') < 200:
            score += 10
        if 'def ' in code:
            score += 15
        if 'class ' in code:
            score += 10
        if '# ' in code or '\"\"\"' in code:
            score += 15
        if 'try:' in code:
            score += 10
        
        return min(100, score)
    
    def _count_errors(self, code):
        """Count potential errors in code"""
        errors = 0
        
        if code.count('(') != code.count(')'):
            errors += 1
        if code.count('[') != code.count(']'):
            errors += 1
        if code.count('{') != code.count('}'):
            errors += 1
        
        return errors
    
    def generate_task(self, skill_level):
        """Generate a learning task based on skill level"""
        tasks = {
            'beginner': "Write a function to reverse a string",
            'intermediate': "Find the longest substring without repeating characters",
            'advanced': "Optimize a graph algorithm to reduce space complexity"
        }
        return tasks.get(skill_level, "Practice coding")
    
    def evaluate_solution(self, user_code, task_description):
        """Evaluate user's solution to a task"""
        quality = self._assess_code_quality(user_code)
        
        return {
            'score': quality,
            'feedback': 'Good solution!' if quality > 70 else 'Room for improvement',
            'next_level': 'intermediate' if quality > 70 else 'continue'
        }
