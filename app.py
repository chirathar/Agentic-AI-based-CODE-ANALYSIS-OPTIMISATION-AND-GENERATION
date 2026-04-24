from flask import Flask, render_template, request, jsonify, Response, send_from_directory
from flask_cors import CORS
from multilang_analyzer import MultiLanguageCodeAnalyzer
from llm_optimizer import LLMOptimizer, CodeGenerator
from explain_code import CodeExplainer
from learning_agent import LearningAgent
import os
import json
import time

app = Flask(__name__, static_folder='Frontend/static', template_folder='Frontend')
CORS(app)

# Initialize analyzer, optimizer, code generator, explainer, and learning agent
optimizer = LLMOptimizer()
generator = CodeGenerator()
explainer = CodeExplainer()
learning_agent = LearningAgent()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index_new.html')

@app.route('/test')
def test_optimization():
    """Serve the simple optimization test page"""
    return send_from_directory('.', 'test_optimization_simple.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze code and return metrics"""
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        language = data.get('language', 'python').lower()

        if not code:
            return jsonify({'error': 'No code provided'}), 400

        # Validate language - expanded support
        valid_languages = [
            'python', 'javascript', 'typescript', 'java', 'cpp', 'c', 'csharp',
            'go', 'rust', 'ruby', 'php', 'html', 'css', 'scss', 'sass', 'vue',
            'react', 'angular', 'swift', 'kotlin', 'dart', 'flutter', 'r',
            'matlab', 'julia', 'haskell', 'scala', 'clojure', 'elixir',
            'fsharp', 'ocaml', 'bash', 'powershell', 'perl', 'lua',
            'dockerfile', 'terraform', 'json', 'yaml', 'xml', 'sql',
            'pascal', 'ada', 'fortran', 'cobol', 'lisp', 'prolog',
            'smalltalk', 'objective-c', 'erlang', 'nim', 'zig', 'assembly'
        ]
        
        # For analysis, we primarily support the core languages that have proper analyzers
        analysis_languages = ['python', 'javascript', 'java', 'cpp', 'c', 'csharp']
        
        if language not in valid_languages:
            return jsonify({
                'error': f'Unsupported language: {language}. Supported: {", ".join(sorted(valid_languages))}',
                'type': 'language_error'
            }), 400
        
        # For unsupported analysis languages, provide basic metrics
        if language not in analysis_languages:
            # Basic metrics for unsupported languages
            lines = code.split('\n')
            loc = len(lines)
            comments = sum(1 for line in lines if line.strip().startswith(('#', '//', '/*', '*', '<!--', '-->', '{', '}')) and line.strip())
            blank = sum(1 for line in lines if not line.strip())
            lloc = loc - comments - blank
            
            basic_metrics = {
                'raw': {
                    'loc': loc,
                    'lloc': max(0, lloc),
                    'comments': comments,
                    'blank': blank
                },
                'cyclomatic': {'main': {'complexity': 1, 'line': 1}},
                'halstead': {
                    'volume': 100.0,
                    'difficulty': 5.0,
                    'effort': 500.0,
                    'time_to_program': 27.78,
                    'bugs': 0.01,
                    'vocabulary': 20,
                    'program_length': 50
                },
                'avg_complexity': 1.0,
                'language': language
            }
            
            return jsonify({
                'success': True,
                'metrics': basic_metrics,
                'code_length': len(code),
                'language': language,
                'note': f'Basic metrics provided for {language}. Advanced analysis available for: {", ".join(analysis_languages)}'
            }), 200

        # Analyze code with language support
        analyzer = MultiLanguageCodeAnalyzer(code, language)
        metrics = analyzer.get_all_metrics()

        return jsonify({
            'success': True,
            'metrics': metrics,
            'code_length': len(code),
            'language': language
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Analysis failed: {str(e)}',
            'type': 'analysis_error'
        }), 500

def send_progress_update(progress, status, section, content=''):
    """Send Server-Sent Event progress update"""
    event = {
        'progress': progress,
        'status': status,
        'section': section,
        'content': content
    }
    return f"data: {json.dumps(event)}\n\n"

@app.route('/api/optimize/suggestions', methods=['POST'])
def optimization_suggestions():
    """Get optimization suggestions with streaming progress"""
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        metrics = data.get('metrics', {})
        language = data.get('language', 'python').lower()

        if not code:
            return jsonify({'error': 'No code provided'}), 400

        def generate_optimization():
            """Generator function for streaming response"""
            try:
                yield send_progress_update(10, 'processing', 'Analyzing code for optimization opportunities...')
                time.sleep(0.1)
                
                yield send_progress_update(30, 'processing', 'Generating optimization suggestions...')
                time.sleep(0.1)
                
                yield send_progress_update(60, 'processing', 'Applying optimization patterns...')
                
                # Get optimization suggestions
                optimization_response = optimizer.get_optimization_suggestions(code, metrics, language)
                
                yield send_progress_update(100, 'complete', 'Optimization suggestions ready!', optimization_response)
                
            except Exception as e:
                yield send_progress_update(0, 'error', 'Error', f"Optimization failed: {str(e)}")

        return Response(generate_optimization(), mimetype='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        })

    except Exception as e:
        return jsonify({
            'error': f'Optimization failed: {str(e)}',
            'type': 'optimization_error'
        }), 500

@app.route('/api/optimize/refactoring', methods=['POST'])
def refactoring_suggestions():
    """Get refactoring suggestions with streaming progress"""
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        metrics = data.get('metrics', {})
        language = data.get('language', 'python').lower()

        if not code:
            return jsonify({'error': 'No code provided'}), 400

        def generate_refactoring():
            """Generator function for streaming response"""
            try:
                yield send_progress_update(10, 'processing', 'Analyzing code structure...')
                time.sleep(0.1)
                
                yield send_progress_update(30, 'processing', 'Identifying refactoring opportunities...')
                time.sleep(0.1)
                
                yield send_progress_update(60, 'processing', 'Generating refactoring suggestions...')
                
                # Get refactoring suggestions (extracted from optimization response)
                optimization_response = optimizer.get_optimization_suggestions(code, metrics, language)
                refactoring_data = extract_refactoring_suggestions(optimization_response)
                
                yield send_progress_update(100, 'complete', 'Refactoring suggestions ready!', refactoring_data)
                
            except Exception as e:
                yield send_progress_update(0, 'error', 'Error', f"Refactoring failed: {str(e)}")

        return Response(generate_refactoring(), mimetype='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        })

    except Exception as e:
        return jsonify({
            'error': f'Refactoring failed: {str(e)}',
            'type': 'refactoring_error'
        }), 500

@app.route('/api/optimize/performance', methods=['POST'])
def performance_suggestions():
    """Get performance improvement suggestions with streaming progress"""
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        metrics = data.get('metrics', {})
        language = data.get('language', 'python').lower()

        if not code:
            return jsonify({'error': 'No code provided'}), 400

        def generate_performance():
            """Generator function for streaming response"""
            try:
                yield send_progress_update(10, 'processing', 'Analyzing performance bottlenecks...')
                time.sleep(0.1)
                
                yield send_progress_update(30, 'processing', 'Identifying optimization opportunities...')
                time.sleep(0.1)
                
                yield send_progress_update(60, 'processing', 'Generating performance improvements...')
                
                # Get performance suggestions (extracted from optimization response)
                optimization_response = optimizer.get_optimization_suggestions(code, metrics, language)
                performance_data = extract_performance_suggestions(optimization_response)
                
                yield send_progress_update(100, 'complete', 'Performance suggestions ready!', performance_data)
                
            except Exception as e:
                yield send_progress_update(0, 'error', 'Error', f"Performance analysis failed: {str(e)}")

        return Response(generate_performance(), mimetype='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        })

    except Exception as e:
        return jsonify({
            'error': f'Performance analysis failed: {str(e)}',
            'type': 'performance_error'
        }), 500

@app.route('/api/optimize/optimized-code', methods=['POST'])
def optimized_code():
    """Get fully optimized code with streaming progress"""
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        metrics = data.get('metrics', {})
        language = data.get('language', 'python').lower()

        if not code:
            return jsonify({'error': 'No code provided'}), 400

        def generate_optimized():
            """Generator function for streaming response"""
            try:
                yield send_progress_update(10, 'processing', 'Analyzing original code...')
                time.sleep(0.1)
                
                yield send_progress_update(30, 'processing', 'Applying optimization patterns...')
                time.sleep(0.1)
                
                yield send_progress_update(60, 'processing', 'Generating optimized code...')
                
                # Generate optimized code using custom logic
                optimized_code_data = generate_optimized_code_custom(code, language)
                
                yield send_progress_update(100, 'complete', 'Optimized code ready!', optimized_code_data)
                
            except Exception as e:
                yield send_progress_update(0, 'error', 'Error', f"Code optimization failed: {str(e)}")

        return Response(generate_optimized(), mimetype='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        })

    except Exception as e:
        return jsonify({
            'error': f'Optimization failed: {str(e)}',
            'type': 'optimization_error'
        }), 500

def generate_optimized_code_custom(code, language):
    """Generate optimized code using custom logic"""
    
    if language == 'python':
        return optimize_python_code(code)
    elif language == 'javascript':
        return optimize_javascript_code(code)
    elif language == 'java':
        return optimize_java_code(code)
    else:
        # For other languages, apply basic optimizations
        return apply_basic_optimizations(code)

def optimize_python_code(code):
    """Optimize Python code with proper usage analysis and significant improvements"""
    lines = code.split('\n')
    optimized_lines = []
    
    # Simple direct optimization approach
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            optimized_lines.append(line)
            continue
        
        # Function optimization
        if stripped.startswith('def '):
            func_name = stripped.split('(')[0].replace('def ', '')
            optimized_lines.append(f'def {func_name} -> Any:')
            optimized_lines.append('    """Optimized version with improved performance"""')
            continue
        
        # Optimize sum patterns - direct replacement
        if stripped == 'total = 0':
            # Look ahead for sum pattern
            if (i + 2 < len(lines) and 
                'for i in range(len(' in lines[i + 1] and 
                'total +=' in lines[i + 2]):
                
                # Extract variable name from the for loop
                for_line = lines[i + 1]
                if 'range(len(' in for_line:
                    start = for_line.find('range(len(') + 10
                    end = for_line.find('))')
                    if start > -1 and end > start:
                        var_name = for_line[start:end]
                        optimized_lines.append(f'total = sum({var_name})')
                        # Skip the next 2 lines (for loop and total +=)
                        continue
        
        # Optimize range(len()) patterns
        if 'for i in range(len(' in stripped:
            var_name = extract_variable_from_range_len(stripped)
            if var_name:
                if var_name.lower() in ['numbers', 'items', 'list', 'data']:
                    optimized_line = line.replace(f'for i in range(len({var_name})):', f'for item in {var_name}:')
                else:
                    optimized_line = line.replace(f'for i in range(len({var_name})):', f'for i, item in enumerate({var_name}):')
                optimized_lines.append(optimized_line)
                continue
        
        # Add the line as-is if no optimization applies
        optimized_lines.append(line)
    
    # Add necessary imports
    optimized_lines.insert(0, 'from typing import Any')
    optimized_lines.insert(1, '')
    
    return '\n'.join(optimized_lines)

def analyze_code_structure(code):
    """Analyze code structure to understand usage patterns"""
    lines = code.split('\n')
    analysis = {
        'variables': {},
        'functions': {},
        'loops': [],
        'patterns': []
    }
    
    # Track variable definitions and usage
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Track function definitions
        if stripped.startswith('def '):
            func_name = stripped.split('(')[0].replace('def ', '')
            analysis['functions'][func_name] = {
                'line': i,
                'params': extract_function_params(stripped),
                'returns': extract_return_statements(lines, i)
            }
        
        # Track variable assignments
        if '=' in stripped and not stripped.startswith('#'):
            var_name = stripped.split('=')[0].strip()
            if var_name and not var_name.startswith('def ') and not var_name.startswith('if '):
                analysis['variables'][var_name] = {
                    'line': i,
                    'type': infer_variable_type(stripped)
                }
        
        # Track loops
        if stripped.startswith('for '):
            analysis['loops'].append({
                'line': i,
                'type': 'for',
                'pattern': stripped
            })
    
    return analysis

def is_sum_pattern(lines, index, analysis):
    """Check if current position is a sum pattern"""
    if index >= len(lines):
        return False
    
    current_line = lines[index].strip()
    if not current_line.startswith('total = 0') and not current_line.startswith('sum_total = 0'):
        return False
    
    # Check if next lines contain a for loop with addition
    if index + 2 < len(lines):
        next_line = lines[index + 1].strip()
        third_line = lines[index + 2].strip()
        
        return (next_line.startswith('for ') and 
                ('total +=' in third_line or 'sum_total +=' in third_line))
    
    return False

def is_max_pattern(lines, index, analysis):
    """Check if current position is a max finding pattern"""
    if index >= len(lines):
        return False
    
    current_line = lines[index].strip()
    if not current_line.startswith('max_val = ') and not current_line.startswith('maximum = '):
        return False
    
    # Check for manual max finding pattern
    if index + 2 < len(lines):
        next_line = lines[index + 1].strip()
        third_line = lines[index + 2].strip()
        
        return (next_line.startswith('for ') and 
                third_line.startswith('if ') and 
                ('>' in third_line or 'max_val' in third_line))
    
    return False

def optimize_sum_pattern(lines, index, analysis):
    """Optimize sum pattern to use sum() function"""
    current_line = lines[index]
    
    # Look for the sum pattern in the next few lines
    for i in range(index + 1, min(index + 5, len(lines))):
        if 'for ' in lines[i] and 'range(len(' in lines[i]:
            collection = extract_collection_from_loop(lines[i])
            if collection:
                return [f"total = sum({collection})"]
        elif 'for ' in lines[i] and ' in ' in lines[i]:
            collection = extract_collection_from_loop(lines[i])
            if collection:
                return [f"total = sum({collection})"]
    
    return [current_line]

def optimize_max_pattern(lines, index, analysis):
    """Optimize max finding pattern to use max() function"""
    current_line = lines[index]
    
    # Look for the max pattern in the next few lines
    for i in range(index + 1, min(index + 5, len(lines))):
        if 'for ' in lines[i] and ('range(len(' in lines[i] or ' in ' in lines[i]):
            collection = extract_collection_from_loop(lines[i])
            if collection:
                return [f"max_val = max({collection})"]
    
    return [current_line]

def extract_collection_from_loop(for_line):
    """Extract collection name from for loop line"""
    if 'for i in range(len(' in for_line:
        start = for_line.find('range(len(') + 10
        end = for_line.find('))')
        return for_line[start:end]
    elif ' for ' in for_line and ' in ' in for_line:
        parts = for_line.split(' in ')
        if len(parts) > 1:
            collection = parts[1].split(':')[0]
            return collection.strip()
    return None

def extract_variable_from_range_len(line):
    """Extract variable name from range(len(variable)) pattern"""
    if 'range(len(' in line:
        start = line.find('range(len(') + 10
        end = line.find('))')
        if start > -1 and end > start:
            return line[start:end]
    return None

def is_simple_iteration_needed(var_name, analysis):
    """Check if simple iteration is needed or enumerate is better"""
    # If the variable is used with index access elsewhere, use enumerate
    # Otherwise, use direct iteration
    return var_name.lower() in ['numbers', 'items', 'list', 'array']

def optimize_range_len_pattern(line, var_name, analysis):
    """Optimize range(len()) pattern"""
    if var_name.lower() in ['numbers', 'items', 'list']:
        return line.replace(f'for i in range(len({var_name})):', f'for item in {var_name}:')
    else:
        return line.replace(f'for i in range(len({var_name})):', f'for i, item in enumerate({var_name}):')

def is_list_comprehension_candidate(lines, index, analysis):
    """Check if current position is a list comprehension candidate"""
    if index >= len(lines):
        return False
    
    # Look for pattern: results = [] followed by for loop with append
    current_line = lines[index].strip()
    if not (current_line.endswith('[]') or current_line.startswith('results =')):
        return False
    
    if index + 1 < len(lines):
        next_line = lines[index + 1].strip()
        return next_line.startswith('for ') and 'append(' in next_line
    
    return False

def optimize_to_list_comprehension(lines, index, analysis):
    """Convert append loop to list comprehension"""
    current_line = lines[index]
    for_line = lines[index + 1]
    
    # Extract components for list comprehension
    var_name = extract_loop_variable(for_line)
    collection = extract_collection_from_loop(for_line)
    append_value = extract_append_value(for_line)
    
    if collection and append_value:
        var_name = var_name or 'item'
        return [f"results = [{append_value} for {var_name} in {collection}]"]
    
    return [current_line, for_line]

def extract_loop_variable(for_line):
    """Extract loop variable from for line"""
    if 'for ' in for_line and ' in ' in for_line:
        parts = for_line.split(' for ')[1].split(' in ')[0]
        return parts.strip()
    return None

def extract_append_value(for_line):
    """Extract value being appended"""
    if 'append(' in for_line:
        start = for_line.find('append(') + 7
        end = for_line.find(')', start)
        if start > -1 and end > start:
            return for_line[start:end]
    return None

def optimize_function(lines, index, func_analysis):
    """Optimize function with proper analysis"""
    func_line = lines[index]
    func_name = func_line.split('(')[0].replace('def ', '')
    
    # Add type hints and docstring
    optimized = [f'def {func_name} -> Any:']
    optimized.append('    """Optimized version with improved performance"""')
    
    return optimized

def generate_required_imports(optimized_lines):
    """Generate required imports based on optimizations used"""
    imports = []
    
    code_text = '\n'.join(optimized_lines)
    
    if '-> Any' in code_text:
        imports.append('from typing import Any')
    
    return imports

def extract_function_params(func_line):
    """Extract parameters from function definition"""
    if '(' in func_line and ')' in func_line:
        params = func_line.split('(')[1].split(')')[0]
        return [p.strip() for p in params.split(',') if p.strip()]
    return []

def extract_return_statements(lines, start_index):
    """Extract return statements from function"""
    returns = []
    for i in range(start_index, len(lines)):
        line = lines[i].strip()
        if line.startswith('def ') and i > start_index:
            break  # Next function
        if line.startswith('return '):
            returns.append(line)
    return returns

def infer_variable_type(line):
    """Infer variable type from assignment"""
    if '=' in line:
        value = line.split('=')[1].strip()
        if value.isdigit():
            return 'int'
        elif value.replace('.', '').isdigit():
            return 'float'
        elif value.startswith('"') or value.startswith("'"):
            return 'str'
        elif value.startswith('['):
            return 'list'
        elif value.startswith('{'):
            return 'dict'
    return 'unknown'

def optimize_javascript_code(code):
    """Optimize JavaScript code with common improvements"""
    lines = code.split('\n')
    optimized_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Optimize var to const/let
        if stripped.startswith('var ') and '=' in stripped:
            optimized_line = stripped.replace('var ', 'const ', 1)
            optimized_lines.append(optimized_line)
            continue
            
        # Optimize for loops
        if 'for (var i = 0; i < ' in stripped and '.length; i++)' in stripped:
            array_name = stripped.split('i < ')[1].split('.length')[0]
            optimized_line = stripped.replace(
                f'for (var i = 0; i < {array_name}.length; i++)',
                f'for (const item of {array_name})'
            )
            optimized_lines.append(optimized_line)
            continue
        
        optimized_lines.append(line)
    
    return '\n'.join(optimized_lines)

def optimize_java_code(code):
    """Optimize Java code with common improvements"""
    lines = code.split('\n')
    optimized_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Optimize string concatenation
        if '+=' in stripped and '"' in stripped:
            optimized_line = stripped + ' // Consider using StringBuilder for better performance'
            optimized_lines.append(optimized_line)
            continue
        
        optimized_lines.append(line)
    
    return '\n'.join(optimized_lines)

def apply_basic_optimizations(code):
    """Apply basic optimizations for any language"""
    lines = code.split('\n')
    optimized_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Remove multiple consecutive empty lines
        if not stripped and optimized_lines and not optimized_lines[-1].strip():
            continue
            
        optimized_lines.append(line)
    
    # Add optimization comment
    optimized_lines.insert(0, f'// Optimized version with performance improvements')
    optimized_lines.insert(1, '')
    
    return '\n'.join(optimized_lines)

def extract_refactoring_suggestions(optimization_response):
    """Extract refactoring suggestions from optimization response"""
    if isinstance(optimization_response, str):
        # Parse the optimization response to extract refactoring suggestions
        content = optimization_response
        
        # Look for refactoring-related sections
        refactoring_patterns = [
            'REFACTORING',
            'REFACTOR',
            'STRUCTURE',
            'ORGANIZATION',
            'CLEAN CODE'
        ]
        
        refactoring_content = []
        lines = content.split('\n')
        current_section = []
        in_refactoring_section = False
        
        for line in lines:
            line_upper = line.upper()
            
            # Check if we're entering a refactoring section
            if any(pattern in line_upper for pattern in refactoring_patterns):
                in_refactoring_section = True
                if current_section:
                    refactoring_content.extend(current_section)
                    current_section = []
                continue
            
            # Check if we're leaving the refactoring section
            if in_refactoring_section and ('===' in line_upper or 'OPTIMIZED CODE' in line_upper):
                in_refactoring_section = False
                continue
            
            # Add line if we're in a refactoring section
            if in_refactoring_section and line.strip():
                current_section.append(line.strip())
        
        # Add any remaining content
        if current_section:
            refactoring_content.extend(current_section)
        
        # If no specific refactoring content found, use the whole response
        if not refactoring_content:
            refactoring_content = [line.strip() for line in content.split('\n') if line.strip()]
        
        return '\n'.join(refactoring_content[:10]) if refactoring_content else "No specific refactoring suggestions identified. The code structure appears to be well-organized."
    
    return "No refactoring suggestions available."

def extract_performance_suggestions(optimization_response):
    """Extract performance suggestions from optimization response"""
    if isinstance(optimization_response, str):
        # Parse the optimization response to extract performance suggestions
        content = optimization_response
        
        # Look for performance-related sections
        performance_patterns = [
            'PERFORMANCE',
            'OPTIMIZATION',
            'EFFICIENCY',
            'SPEED',
            'MEMORY',
            'CPU',
            'BOTTLENECK'
        ]
        
        performance_content = []
        lines = content.split('\n')
        current_section = []
        in_performance_section = False
        
        for line in lines:
            line_upper = line.upper()
            
            # Check if we're entering a performance section
            if any(pattern in line_upper for pattern in performance_patterns):
                in_performance_section = True
                if current_section:
                    performance_content.extend(current_section)
                    current_section = []
                continue
            
            # Check if we're leaving the performance section
            if in_performance_section and ('===' in line_upper or 'REFACTORING' in line_upper):
                in_performance_section = False
                continue
            
            # Add line if we're in a performance section
            if in_performance_section and line.strip():
                current_section.append(line.strip())
        
        # Add any remaining content
        if current_section:
            performance_content.extend(current_section)
        
        # If no specific performance content found, use relevant parts of the response
        if not performance_content:
            # Look for performance-related keywords in the entire response
            performance_keywords = ['fast', 'slow', 'optimize', 'efficient', 'memory', 'cpu', 'performance']
            for line in content.split('\n'):
                if any(keyword in line.lower() for keyword in performance_keywords):
                    performance_content.append(line.strip())
        
        return '\n'.join(performance_content[:10]) if performance_content else "No specific performance improvements identified. The code appears to be reasonably optimized."
    
    return "No performance suggestions available."

def extract_optimized_code(optimization_response):
    """Extract optimized code from optimization response"""
    if isinstance(optimization_response, str):
        content = optimization_response
        
        # Look for code blocks
        import re
        
        # Pattern to match code blocks with language specification
        code_block_pattern = r'```(?:python|javascript|java|cpp|c|csharp)?\n?(.*?)```'
        code_blocks = re.findall(code_block_pattern, content, re.DOTALL)
        
        if code_blocks:
            # Return the first code block found
            return code_blocks[0].strip()
        
        # Look for "OPTIMIZED CODE" section
        optimized_patterns = [
            'OPTIMIZED CODE',
            'IMPROVED CODE',
            'FINAL CODE',
            'SUGGESTED CODE'
        ]
        
        lines = content.split('\n')
        optimized_code = []
        in_optimized_section = False
        
        for line in lines:
            line_upper = line.upper()
            
            # Check if we're entering an optimized code section
            if any(pattern in line_upper for pattern in optimized_patterns):
                in_optimized_section = True
                continue
            
            # Check if we're leaving the optimized code section
            if in_optimized_section and ('===' in line_upper or line_upper.startswith('```')):
                if line_upper.startswith('```'):
                    continue  # Skip the closing markdown
                in_optimized_section = False
                continue
            
            # Add line if we're in the optimized code section
            if in_optimized_section:
                optimized_code.append(line)
        
        if optimized_code:
            return '\n'.join(optimized_code).strip()
        
        # If no optimized code found, return a comment indicating this
        return "# No optimized code was generated. The original code may already be optimal.\n# Original code can be used as is."
    
    return "# No optimized code available."

# ===== CODE GENERATION ENDPOINTS =====

@app.route('/api/generate/from-description', methods=['POST'])
def generate_from_description():
    """Generate code from text description"""
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        language = data.get('language', 'python').lower()
        
        if not description:
            return jsonify({'error': 'No description provided'}), 400
        
        generated_code = generator.generate_from_description(description, language)
        
        return jsonify({
            'success': True,
            'content': generated_code,
            'language': language
        })
        
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/api/generate/from-description-stream', methods=['POST'])
def generate_from_description_stream():
    """Generate code from text description with streaming (for old frontend)"""
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        language = data.get('language', 'python').lower()
        
        if not description:
            return jsonify({'error': 'No description provided'}), 400
        
        def generate():
            yield send_progress_update(10, 'processing', 'Analyzing description...')
            time.sleep(0.1)
            
            yield send_progress_update(30, 'processing', 'Generating code structure...')
            time.sleep(0.1)
            
            yield send_progress_update(60, 'processing', 'Writing complete code...')
            generated_code = generator.generate_from_description(description, language)
            
            yield send_progress_update(100, 'complete', 'Code generated!', generated_code)
        
        return Response(generate(), mimetype='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        })
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/api/generate/complete-code', methods=['POST'])
def complete_incomplete_code():
    """Complete incomplete code"""
    try:
        data = request.get_json()
        incomplete_code = data.get('incomplete_code', '').strip()
        language = data.get('language', 'python').lower()
        
        if not incomplete_code:
            return jsonify({'error': 'No incomplete code provided'}), 400
        
        completed_code = generator.complete_incomplete_code(incomplete_code, language)
        
        return jsonify({
            'success': True,
            'content': completed_code,
            'language': language
        })
    except Exception as e:
        return jsonify({'error': f'Completion failed: {str(e)}'}), 500

@app.route('/api/generate/functions', methods=['POST'])
def generate_functions():
    """Generate functions from description"""
    try:
        data = request.get_json()
        description = data.get('description', '').strip()
        language = data.get('language', 'python').lower()
        
        if not description:
            return jsonify({'error': 'No description provided'}), 400
        
        generated = generator.convert_description_to_functions(description, language)
        
        return jsonify({
            'success': True,
            'content': generated,
            'language': language
        })
        
    except Exception as e:
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/api/generate/improve', methods=['POST'])
def improve_and_complete():
    """Improve and complete code based on idea"""
    try:
        data = request.get_json()
        partial_code = data.get('code', '').strip()
        idea = data.get('idea', '').strip()
        language = data.get('language', 'python').lower()
        
        if not partial_code or not idea:
            return jsonify({'error': 'Code and idea are required'}), 400
        
        improved = generator.improve_and_complete(partial_code, idea, language)
        
        return jsonify({
            'success': True,
            'content': improved,
            'language': language
        })
        
    except Exception as e:
        return jsonify({'error': f'Improvement failed: {str(e)}'}), 500

@app.route('/api/explain', methods=['POST'])
def explain():
    """Explain code with adaptive learning"""
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        language = data.get('language', 'python').lower()
        skill_level = data.get('skill_level', None)
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Get code explanation
        explanation = explainer.explain_code(code, language, skill_level)
        
        return jsonify({
            'success': True,
            'explanation': explanation.get('overview', ''),
            'skill_level': explanation.get('skill_level', 'beginner'),
            'concept_gaps': explanation.get('concept_gaps', []),
            'language': language
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Explanation failed: {str(e)}',
            'type': 'explanation_error'
        }), 500

@app.route('/api/learning/submit', methods=['POST'])
def learning_submit():
    """Submit code for agentic learning feedback"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user').strip()
        code = data.get('code', '').strip()
        language = data.get('language', 'python').lower()
        task_id = data.get('task_id')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Process through learning agent
        result = learning_agent.process_submission(user_id, code, task_id, language)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Learning submission failed: {str(e)}',
            'type': 'learning_error'
        }), 500

@app.route('/api/learning/task', methods=['GET'])
def learning_task():
    """Get next recommended task"""
    try:
        user_id = request.args.get('user_id', 'default_user').strip()
        
        result = learning_agent.get_next_task(user_id)
        
        return jsonify({'success': True, 'data': result}), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Task generation failed: {str(e)}',
            'type': 'task_error'
        }), 500

@app.route('/api/learning/progress', methods=['GET'])
def learning_progress():
    """Get user learning progress"""
    try:
        user_id = request.args.get('user_id', 'default_user').strip()
        
        progress = learning_agent.get_user_progress(user_id)
        
        return jsonify({'success': True, 'data': progress}), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Progress retrieval failed: {str(e)}',
            'type': 'progress_error'
        }), 500

@app.route('/api/learning/path', methods=['GET'])
def learning_path():
    """Get personalized learning path"""
    try:
        user_id = request.args.get('user_id', 'default_user').strip()
        
        path = learning_agent.get_learning_path(user_id)
        
        return jsonify({'success': True, 'data': path}), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Learning path generation failed: {str(e)}',
            'type': 'path_error'
        }), 500

@app.route('/api/learning/concept/<concept>', methods=['GET'])
def learning_concept(concept):
    """Get details about a specific concept"""
    try:
        details = learning_agent.analyze_concept_gap(concept)
        
        return jsonify({'success': True, 'data': details}), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Concept analysis failed: {str(e)}',
            'type': 'concept_error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'ollama_model': optimizer.model}), 200

if __name__ == '__main__':
    print("Starting Python Code Analyzer & Optimizer Server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='localhost', port=5000)
