import re
import math
from typing import Dict, Any


class MultiLanguageCodeAnalyzer:
    """
    Analyzer for multiple programming languages.
    Supports: Python, JavaScript, Java, C, C++, C#
    """

    def __init__(self, code: str, language: str = 'python'):
        self.code = code
        self.language = language.lower()
        self.lines = code.split('\n')

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get metrics for all languages"""
        raw = self.get_raw_metrics()
        cyclomatic = self.get_cyclomatic_complexity()
        halstead = self.get_halstead_metrics()
        
        # Calculate average complexity
        avg_complexity = 1.0
        if cyclomatic:
            complexities = [data.get('complexity', 1) for data in cyclomatic.values()]
            avg_complexity = sum(complexities) / len(complexities) if complexities else 1.0
        
        return {
            'raw': raw,
            'cyclomatic': cyclomatic,
            'halstead': halstead,
            'avg_complexity': round(avg_complexity, 2),
            'language': self.language,
        }

    def get_raw_metrics(self) -> Dict[str, int]:
        """Calculate basic code metrics"""
        loc = len(self.lines)
        lloc = 0
        comments = 0
        blank = 0

        for line in self.lines:
            stripped = line.strip()

            if not stripped:
                blank += 1
                continue

            # Count comments based on language
            if self._is_comment_line(stripped):
                comments += 1
            elif stripped:
                lloc += 1

        return {
            'loc': loc,
            'lloc': lloc,
            'comments': comments,
            'blank': blank,
        }

    def _is_comment_line(self, line: str) -> bool:
        """Check if line is a comment based on language"""
        if self.language == 'python':
            return line.startswith('#')
        elif self.language == 'javascript':
            return line.startswith('//') or line.startswith('/*') or line.startswith('*')
        elif self.language in ['java', 'cpp', 'c', 'csharp']:
            return line.startswith('//') or line.startswith('/*') or line.startswith('*')
        return False

    def get_cyclomatic_complexity(self) -> Dict[str, Dict[str, Any]]:
        """Calculate cyclomatic complexity based on language"""
        results = {}
        
        if self.language == 'python':
            results = self._get_python_complexity()
        elif self.language == 'javascript':
            results = self._get_javascript_complexity()
        elif self.language == 'java':
            results = self._get_java_complexity()
        elif self.language == 'cpp':
            results = self._get_cpp_complexity()
        elif self.language == 'c':
            results = self._get_c_complexity()
        elif self.language == 'csharp':
            results = self._get_csharp_complexity()

        return results

    def _get_python_complexity(self) -> Dict[str, Dict[str, Any]]:
        """Get Python function complexity"""
        results = {}
        current_func = None
        current_complexity = 1
        func_line = 0

        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()

            # Find function definitions
            if stripped.startswith('def '):
                if current_func:
                    results[current_func] = {
                        'complexity': current_complexity,
                        'line': func_line
                    }
                current_func = self._extract_function_name(stripped, 'python')
                current_complexity = 1
                func_line = i

            # Count complexity keywords
            if current_func:
                for keyword in ['if ', 'elif ', 'except ', 'for ', 'while ', 'and ', 'or ', 'lambda', '?']:
                    if keyword in stripped:
                        current_complexity += stripped.count(keyword)

        if current_func:
            results[current_func] = {
                'complexity': current_complexity,
                'line': func_line
            }

        return results

    def _get_javascript_complexity(self) -> Dict[str, Dict[str, Any]]:
        """Get JavaScript function complexity"""
        results = {}
        current_func = None
        current_complexity = 1
        func_line = 0

        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()

            # Find function definitions
            if re.search(r'function\s+(\w+)|const\s+(\w+)\s*=\s*\(|let\s+(\w+)\s*=\s*\(', stripped):
                if current_func:
                    results[current_func] = {
                        'complexity': current_complexity,
                        'line': func_line
                    }
                current_func = self._extract_function_name(stripped, 'javascript')
                current_complexity = 1
                func_line = i

            # Count complexity keywords
            if current_func:
                for keyword in ['if ', 'else ', 'case ', 'switch', 'for ', 'while ', 'catch', '&&', '||', '?']:
                    if keyword in stripped:
                        current_complexity += stripped.count(keyword)

        if current_func:
            results[current_func] = {
                'complexity': current_complexity,
                'line': func_line
            }

        return results

    def _get_java_complexity(self) -> Dict[str, Dict[str, Any]]:
        """Get Java method complexity"""
        results = {}
        current_method = None
        current_complexity = 1
        method_line = 0

        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()

            # Find method definitions
            if re.search(r'(public|private|protected)?\s*(static)?\s*\w+\s+(\w+)\s*\(', stripped):
                if current_method:
                    results[current_method] = {
                        'complexity': current_complexity,
                        'line': method_line
                    }
                current_method = self._extract_function_name(stripped, 'java')
                current_complexity = 1
                method_line = i

            # Count complexity keywords
            if current_method:
                for keyword in ['if ', 'else ', 'case ', 'switch', 'for ', 'while ', 'catch', '&&', '||', '?']:
                    if keyword in stripped:
                        current_complexity += stripped.count(keyword)

        if current_method:
            results[current_method] = {
                'complexity': current_complexity,
                'line': method_line
            }

        return results

    def _get_cpp_complexity(self) -> Dict[str, Dict[str, Any]]:
        """Get C++ function complexity"""
        return self._get_c_like_complexity()

    def _get_c_complexity(self) -> Dict[str, Dict[str, Any]]:
        """Get C function complexity"""
        return self._get_c_like_complexity()

    def _get_csharp_complexity(self) -> Dict[str, Dict[str, Any]]:
        """Get C# method complexity"""
        results = {}
        current_method = None
        current_complexity = 1
        method_line = 0

        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()

            # Find method definitions
            if re.search(r'(public|private|protected)?\s*(static)?\s*\w+\s+(\w+)\s*\(', stripped):
                if current_method:
                    results[current_method] = {
                        'complexity': current_complexity,
                        'line': method_line
                    }
                current_method = self._extract_function_name(stripped, 'csharp')
                current_complexity = 1
                method_line = i

            # Count complexity keywords
            if current_method:
                for keyword in ['if ', 'else ', 'case ', 'switch', 'for ', 'while ', 'foreach', 'catch', '&&', '||', '?']:
                    if keyword in stripped:
                        current_complexity += stripped.count(keyword)

        if current_method:
            results[current_method] = {
                'complexity': current_complexity,
                'line': method_line
            }

        return results

    def _get_c_like_complexity(self) -> Dict[str, Dict[str, Any]]:
        """Generic complexity for C-like languages"""
        results = {}
        current_func = None
        current_complexity = 1
        func_line = 0
        brace_count = 0

        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()

            # Find function definitions (simple pattern for C/C++)
            if re.search(r'\w+\s+(\w+)\s*\([^)]*\)\s*\{', stripped):
                if current_func and brace_count == 0:
                    results[current_func] = {
                        'complexity': current_complexity,
                        'line': func_line
                    }
                current_func = self._extract_function_name(stripped, 'c')
                current_complexity = 1
                func_line = i

            # Count braces to track scope
            brace_count += stripped.count('{') - stripped.count('}')

            # Count complexity keywords
            if current_func:
                for keyword in ['if ', 'else ', 'case ', 'switch', 'for ', 'while ', 'do ', 'catch', '&&', '||', '?']:
                    if keyword in stripped:
                        current_complexity += stripped.count(keyword)

        if current_func:
            results[current_func] = {
                'complexity': current_complexity,
                'line': func_line
            }

        return results

    def _extract_function_name(self, line: str, language: str) -> str:
        """Extract function/method name from declaration"""
        if language == 'python':
            match = re.search(r'def\s+(\w+)', line)
            return match.group(1) if match else 'unknown'
        elif language == 'javascript':
            match = re.search(r'function\s+(\w+)|const\s+(\w+)|let\s+(\w+)', line)
            if match:
                return next(g for g in match.groups() if g)
            return 'unknown'
        elif language == 'java':
            match = re.search(r'\w+\s+(\w+)\s*\(', line)
            return match.group(1) if match else 'unknown'
        elif language == 'csharp':
            match = re.search(r'\w+\s+(\w+)\s*\(', line)
            return match.group(1) if match else 'unknown'
        elif language in ['c', 'cpp']:
            match = re.search(r'\w+\s+(\w+)\s*\(', line)
            return match.group(1) if match else 'unknown'
        return 'unknown'

    def get_halstead_metrics(self) -> Dict[str, float]:
        """Calculate Halstead complexity metrics"""
        # Count operators and operands
        operators = set()
        operands = set()
        operator_count = 0
        operand_count = 0
        
        # Common operators across languages
        operator_patterns = [
            r'[+\-*/%]',  # Arithmetic
            r'[<>=!]=?',  # Comparison/assignment
            r'[&|^~]',    # Bitwise
            r'&&|\|\|',   # Logical
            r'[(){}\[\];,.]',  # Structural
            r'if|else|while|for|do|case|switch|try|catch|finally|return|break|continue',  # Keywords
        ]
        
        for line in self.lines:
            # Skip comments and empty lines
            stripped = line.strip()
            if not stripped or self._is_comment_line(stripped):
                continue
            
            # Extract operators
            for pattern in operator_patterns:
                matches = re.findall(pattern, stripped)
                operator_count += len(matches)
                for match in matches:
                    operators.add(match)
            
            # Simple operand extraction (identifiers, numbers, strings)
            operand_matches = re.findall(r'\b[a-zA-Z_]\w*\b|\d+(?:\.\d+)?|["\'].*?["\']', stripped)
            operand_count += len(operand_matches)
            for match in operand_matches:
                operands.add(match)
        
        n1 = len(operators)  # Unique operators
        n2 = len(operands)   # Unique operands
        N1 = max(1, operator_count)  # Total operators
        N2 = max(1, operand_count)   # Total operands
        
        # Halstead metrics
        program_length = N1 + N2
        vocabulary = n1 + n2
        
        # Volume (proper Halstead formula: N * log2(n))
        if vocabulary > 1:
            volume = program_length * math.log2(vocabulary)
        else:
            volume = 0
        
        # Difficulty (proper Halstead formula: (n1/2) * (N2/n2))
        difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
        
        # Effort (E = D * V)
        effort = difficulty * volume
        
        # Time to program (in seconds, Stroud's number: E / 18)
        time_to_program = effort / 18 if effort > 0 else 0
        
        # Bugs (Halstead: E^(2/3) / 3000)
        bugs = effort ** (2/3) / 3000 if effort > 0 else 0
        
        return {
            'volume': round(volume, 2),
            'difficulty': round(difficulty, 2),
            'effort': round(effort, 2),
            'time_to_program': round(time_to_program, 2),
            'bugs': round(bugs, 4),
            'vocabulary': vocabulary,
            'program_length': program_length,
        }



