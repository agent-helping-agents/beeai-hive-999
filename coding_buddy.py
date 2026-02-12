#!/usr/bin/env python3
"""
DeepSeek Coder Automation Wrapper
Automate coding tasks with Ollama + DeepSeek Coder
"""

import ollama
import sys
from typing import Optional

# Configuration
DEFAULT_MODEL = 'deepseek-coder'
DEFAULT_TIMEOUT = 120  # seconds

class CodingBuddy:
    """Your local AI coding assistant."""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.conversation_history = []
    
    def ask(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Ask a coding question and get a clean response."""
        
        messages = []
        
        # System prompt for cleaner outputs
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        
        # Add conversation context
        messages.extend(self.conversation_history[-5:])  # Keep last 5 exchanges
        
        # User prompt
        messages.append({'role': 'user', 'content': prompt})
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': 0.1,  # Low temp for consistent code
                    'top_k': 10,        # Focus on likely tokens
                    'num_predict': 2048, # Limit output length
                }
            )
            
            # Extract response
            reply = response['message']['content']
            
            # Store in history
            self.conversation_history.append({'role': 'user', 'content': prompt})
            self.conversation_history.append({'role': 'assistant', 'content': reply})
            
            return reply
            
        except Exception as e:
            return f"❌ Error: {e}"
    
    def generate_code(self, task: str, language: str = 'python') -> str:
        """Generate code for a specific task."""
        
        prompt = f"""
Write clean, working {language} code for the following task:

{task}

Requirements:
1. Working code only (no pseudo-code)
2. Include comments explaining complex parts
3. Handle common edge cases
4. Keep it simple and readable

Output ONLY the code in a markdown code block.
"""
        
        return self.ask(prompt, system_prompt="You are an expert programmer. Output ONLY code in markdown blocks. No explanations outside the code.")
    
    def explain_code(self, code: str) -> str:
        """Explain what a piece of code does."""
        prompt = f"Explain this code clearly:\n\n```{code}\n```"
        return self.ask(prompt)
    
    def fix_bug(self, code: str, error: str) -> str:
        """Fix a bug with the given error message."""
        prompt = f"""
Fix this code. Error message:
{error}

Code:
```{code}
```

Output the fixed code only.
"""
        return self.ask(prompt)
    
    def refactor(self, code: str, goal: str) -> str:
        """Refactor code to meet a goal."""
        prompt = f"""
Refactor this code to: {goal}

Original code:
```{code}
```

Output the refactored code only.
"""
        return self.ask(prompt)
    
    def write_tests(self, code: str, framework: str = 'pytest') -> str:
        """Write unit tests for code."""
        prompt = f"""
Write {framework} tests for this code:

```{code}
```

Output only the test code.
"""
        return self.ask(prompt)

def main():
    """CLI interface for Coding Buddy."""
    import argparse
    
    parser = argparse.ArgumentParser(description='DeepSeek Coder Automation')
    parser.add_argument('task', help='The coding task or question')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='Ollama model to use')
    parser.add_argument('--code', action='store_true', help='Generate code (specify language with --lang)')
    parser.add_argument('--lang', default='python', help='Programming language')
    parser.add_argument('--explain', action='store_true', help='Explain code from stdin')
    
    args = parser.parse_args()
    
    buddy = CodingBuddy(model=args.model)
    
    if args.explain:
        code = sys.stdin.read()
        result = buddy.explain_code(code)
    elif args.code:
        result = buddy.generate_code(args.task, args.lang)
    else:
        result = buddy.ask(args.task)
    
    print(result)

if __name__ == '__main__':
    main()
