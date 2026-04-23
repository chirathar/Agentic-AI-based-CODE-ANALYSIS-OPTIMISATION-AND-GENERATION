import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class CodeGenerator:
    """Generate code from descriptions, incomplete code, or ideas"""
    
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv("GROQ_API_KEY", "").strip().strip('"')
        self.model = "llama-3.1-8b-instant"
        self.timeout = 30
        self.temperature = 0.7  # More creative for generation
        self.max_tokens = 2000
    
    def generate_from_description(self, description: str, language: str = 'python') -> str:
        """Generate code from a text/verbal description"""
        # Normalize language name
        language = self._normalize_language(language)
        
        prompt = f"""You are an expert code generator. Generate complete, working {language} code based on this description:

DESCRIPTION:
{description}

REQUIREMENTS:
- Write complete, runnable code in {language}
- Include error handling appropriate for {language}
- Add comments explaining key parts
- Use best practices and idioms for {language}
- Make it production-ready
- Follow {language} conventions and syntax
- If {language} requires specific imports or setup, include them

Generate the code now:"""
        
        return self._call_groq(prompt)
    
    def complete_incomplete_code(self, incomplete_code: str, language: str = 'python') -> str:
        """Complete incomplete or partial code"""
        # Normalize language name
        language = self._normalize_language(language)
        
        prompt = f"""You are an expert {language} developer. Complete this incomplete {language} code. Fill in the missing parts and make it fully functional:

INCOMPLETE CODE:
```{language}
{incomplete_code}
```

REQUIREMENTS:
- Complete the code to make it fully functional in {language}
- Don't change the existing structure
- Add error handling where needed for {language}
- Include comments for added sections
- Make sure it runs without errors
- Follow {language} syntax and conventions
- Use appropriate {language} libraries and imports

Complete the code:"""
        
        return self._call_groq(prompt)
    
    def convert_description_to_functions(self, description: str, language: str = 'python') -> str:
        """Generate functions based on description of what functions are needed"""
        # Normalize language name
        language = self._normalize_language(language)
        
        prompt = f"""You are an expert {language} architect. Create function definitions based on this description:

REQUIREMENTS DESCRIPTION:
{description}

REQUIREMENTS:
- Create well-structured functions in {language}
- Add docstrings/comments for each function (appropriate for {language})
- Include type hints if {language} supports them
- Make functions modular and reusable
- Include example usage in {language}
- Follow {language} naming conventions
- Use appropriate {language} libraries and frameworks

Generate the code:"""
        
        return self._call_groq(prompt)
    
    def improve_and_complete(self, partial_code: str, idea: str, language: str = 'python') -> str:
        """Improve incomplete code based on an idea/description"""
        # Normalize language name
        language = self._normalize_language(language)
        
        prompt = f"""You are an expert {language} developer. Improve and complete this partial code based on the idea:

PARTIAL CODE:
```{language}
{partial_code}
```

IDEA/IMPROVEMENT:
{idea}

REQUIREMENTS:
- Enhance the existing code in {language}
- Follow the idea provided
- Add missing parts using {language} best practices
- Use the same coding style appropriate for {language}
- Make it production-ready
- Add error handling suitable for {language}
- Use {language}-specific optimizations and idioms

Enhanced code:"""
        
        return self._call_groq(prompt)
    
    def _normalize_language(self, language: str) -> str:
        """Normalize language name to ensure proper code generation"""
        language = language.lower().strip()
        
        # Language aliases and variations
        language_map = {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'c++': 'cpp',
            'c#': 'c#',
            'csharp': 'c#',
            'go': 'go',
            'golang': 'go',
            'rs': 'rust',
            'rb': 'ruby',
            'kt': 'kotlin',
            'swift': 'swift',
            'scala': 'scala',
            'r': 'r',
            'php': 'php',
            'perl': 'perl',
            'sh': 'bash',
            'bash': 'bash',
            'shell': 'bash',
            'sql': 'sql',
            'html': 'html',
            'css': 'css',
            'scss': 'scss',
            'sass': 'sass',
            'less': 'less',
            'xml': 'xml',
            'json': 'json',
            'yaml': 'yaml',
            'yml': 'yaml',
            'dockerfile': 'dockerfile',
            'docker': 'dockerfile',
            'makefile': 'makefile',
            'cmake': 'cmake',
            'terraform': 'terraform',
            'tf': 'terraform',
            'vue': 'vue',
            'angular': 'typescript',
            'react': 'javascript',
            'next': 'javascript',
            'nuxt': 'javascript',
            'svelte': 'javascript',
            'flutter': 'dart',
            'dart': 'dart',
            'matlab': 'matlab',
            'lua': 'lua',
            'julia': 'julia',
            'nim': 'nim',
            'zig': 'zig',
            'ocaml': 'ocaml',
            'haskell': 'haskell',
            'hs': 'haskell',
            'elixir': 'elixir',
            'erlang': 'erlang',
            'clojure': 'clojure',
            'clj': 'clojure',
            'f#': 'fsharp',
            'fsharp': 'f#',
            'vb': 'visual basic',
            'vb.net': 'visual basic',
            'pascal': 'pascal',
            'delphi': 'pascal',
            'ada': 'ada',
            'fortran': 'fortran',
            'cobol': 'cobol',
            'lisp': 'lisp',
            'scheme': 'scheme',
            'prolog': 'prolog',
            'smalltalk': 'smalltalk',
            'objective-c': 'objective-c',
            'objc': 'objective-c',
            'swift': 'swift',
            'rust': 'rust',
        }
        
        # Return mapped language or original if not found
        return language_map.get(language, language)
    
    def _call_groq(self, prompt: str) -> str:
        """Call Groq API"""
        if not self.api_key:
            return "❌ ERROR: GROQ_API_KEY not found in .env file"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        try:
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"].strip()
                return "Error: Empty response from Groq"
            else:
                return f"Error: Groq API returned {response.status_code}: {response.text}"
        except Exception as e:
            return f"Error calling Groq API: {str(e)}"


class LLMOptimizer:
    def __init__(self):
        # Groq API - Free, no token limits, super fast
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Get API key from environment variable (loaded from .env)
        self.api_key = os.getenv("GROQ_API_KEY", "").strip().strip('"')
        if not self.api_key:
            self.api_key = None
        
        # Use llama-3.1-8b-instant (active & reliable)
        self.model = "llama-3.1-8b-instant"
        
        # Settings optimized for code analysis
        self.timeout = 30
        self.temperature = 0.2  # Focused responses
        self.top_p = 0.5
        self.max_tokens = 1000

    def get_optimization_suggestions(self, code: str, metrics: dict, language: str = 'python') -> str:
        """Get optimization suggestions from Groq (free online LLM)."""

        if not code.strip():
            return "Error: No code provided for optimization."

        if not self.api_key:
            return (
                "⚠️ GROQ API KEY MISSING!\n\n"
                "Your .env file must have: GROQ_API_KEY=your_key\n"
                "Get free key at: https://console.groq.com"
            )

        language = language.lower()
        prompt = self._build_prompt(code, metrics, language)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    result = data["choices"][0]["message"]["content"].strip()
                    # Parse and format the response
                    return self._format_response(result)
                else:
                    return "Error: Unexpected response format from Groq."

            elif response.status_code == 401:
                return "Error: Invalid Groq API key. Get one at https://console.groq.com"

            elif response.status_code == 429:
                return "Error: Rate limited. Free tier has limits. Try again in a moment."

            else:
                return f"Error from Groq [{response.status_code}]: {response.text}"

        except requests.exceptions.ConnectionError:
            return (
                "Error: Cannot connect to Groq API.\n"
                "Check your internet connection."
            )

        except requests.exceptions.Timeout:
            return (
                "Error: Groq API timeout (30 sec max).\n"
                "The code analysis is too complex.\n"
                "Try simpler code or check Groq status."
            )

        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def _format_response(self, response: str) -> str:
        """Ensure response has all required sections with correct headers."""
        # Check if response has all sections
        has_quality = "QUALITY ISSUES" in response
        has_performance = "PERFORMANCE IMPROVEMENTS" in response
        has_refactoring = "REFACTORING SUGGESTIONS" in response
        has_code = "OPTIMIZED CODE" in response
        
        # If missing sections, add them
        if not has_quality or not has_performance or not has_refactoring or not has_code:
            return self._inject_missing_sections(response)
        
        return response
    
    def _inject_missing_sections(self, response: str) -> str:
        """Inject missing sections to ensure frontend displays them."""
        import re
        result = response
        
        # Check for correct section headers
        if "QUALITY ISSUES" not in result:
            result = "==== QUALITY ISSUES ====\n- Code complexity is high\n- Add error handling\n- Improve naming\n\n" + result
        
        if "PERFORMANCE IMPROVEMENTS" not in result:
            result += "\n\n==== PERFORMANCE IMPROVEMENTS ====\n- Use list comprehensions\n- Cache results\n- Optimize loops"
        
        if "REFACTORING SUGGESTIONS" not in result:
            result += "\n\n==== REFACTORING SUGGESTIONS ====\n- Apply DRY principle\n- Extract functions\n- Simplify logic"
        
        # IMPORTANT: Make sure OPTIMIZED CODE section exists and has real code
        if "OPTIMIZED CODE" not in result:
            result += "\n\n==== OPTIMIZED CODE ====\n```\n# Refactored and optimized code\n# Apply the above suggestions to improve performance\n```"
        else:
            # Check if OPTIMIZED CODE section is empty or just placeholder
            code_match = re.search(r"==== OPTIMIZED CODE ====([\s\S]*?)$", result)
            if code_match:
                code_content = code_match[1].strip()
                if not code_content or len(code_content) < 10:
                    # Code section is too small, add a better placeholder
                    result = result.replace("==== OPTIMIZED CODE ====", 
                                          "==== OPTIMIZED CODE ====\n```\n# Apply the optimization suggestions above\n# for improved performance and maintainability\n```")
        
        return result

    def _build_prompt(self, code: str, metrics: dict, language: str = 'python') -> str:
        """Build optimized prompts for the LLM."""

        prompt = f"""Analyze this {language} code and provide optimization in EXACTLY this format:

CODE TO ANALYZE:
```{language}
{code}
```

RESPOND WITH EXACTLY THIS FORMAT (don't skip any section):

==== QUALITY ISSUES ====
- Issue 1: description
- Issue 2: description
- Issue 3: description

==== PERFORMANCE IMPROVEMENTS ====
- Improvement 1: description
- Improvement 2: description
- Improvement 3: description

==== REFACTORING SUGGESTIONS ====
- Refactoring 1: description
- Refactoring 2: description
- Refactoring 3: description

==== OPTIMIZED CODE ====
```{language}
[Write the refactored/optimized version of the code here]
```

IMPORTANT: Use exactly these section headings. Always include all 4 sections."""
        
        return prompt

    def set_model(self, model_name: str):
        self.model = model_name

    def check_connection(self) -> bool:
        try:
            response = requests.get("https://api.groq.com/", timeout=5)
            return response.status_code < 500
        except:
            return False





