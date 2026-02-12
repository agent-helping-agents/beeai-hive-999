"""
Ollama Coder Integration - Local AI Coding Assistant

Provides direct Ollama integration for 100% offline coding:
- qwen2.5-coder:32b - Primary coding model (GPT-4o level)
- deepseek-coder-v2:16b - Complex algorithms & reasoning
- codellama:34b - Code generation & completion
- nomic-embed-text - Already in use for embeddings

Usage:
    from backend.ollama_coder import OllamaCoder, CodeSuggestion

    coder = OllamaCoder()
    suggestion = await coder.complete_code("def fibonacci(n):")
    print(suggestion.text)
"""

import asyncio
import json
import ollama
import subprocess
from typing import Optional, AsyncGenerator, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import time


class CodingModel(Enum):
    """Ollama models optimized for coding."""

    QWEN_CODER_32B = "qwen2.5-coder:32b"
    DEEPSEEK_CODER_V2 = "deepseek-coder-v2:16b-instruct"
    CODE_LLAMA_34B = "codellama:34b"
    CODE_LLAMA_7B = "codellama:7b"
    STARCODER2_15B = "starcoder2:15b"
    CODESTRAL = "codestral:latest"
    PHIND_CODELLAMA = "phind-codellama:34b"
    DEEPCODER = "deepseek-coder:33b"


@dataclass
class CodeSuggestion:
    """A code completion suggestion."""

    text: str
    language: str
    confidence: float
    model: str
    latency_ms: float


@dataclass
class CodeFix:
    """A code fix suggestion."""

    original: str
    fixed: str
    explanation: str
    severity: str  # error, warning, info
    line_number: Optional[int] = None


@dataclass
class CodeExplain:
    """Code explanation result."""

    summary: str
    details: str
    complexity: str
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None


class OllamaCoder:
    """
    Local Ollama-powered coding assistant.

    Replaces Claude Code/Goose for 100% offline development.
    """

    def __init__(
        self,
        model: CodingModel = CodingModel.QWEN_CODER_32B,
        host: str = "http://localhost:11434",
        timeout: float = 120.0,
    ):
        self.model = model
        self.host = host
        self.timeout = timeout
        self._client = None

    @property
    def client(self):
        """Lazy initialize Ollama client."""
        if self._client is None:
            self._client = ollama.Client(host=self.host)
        return self._client

    def is_available(self) -> bool:
        """Check if Ollama server is running."""
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def ensure_model(self) -> bool:
        """Ensure the coding model is pulled."""
        try:
            self.client.show(self.model.value)
            return True
        except Exception:
            print(f"Pulling {self.model.value}... (this may take a few minutes)")
            try:
                subprocess.run(
                    ["ollama", "pull", self.model.value], capture_output=True, text=True
                )
                return True
            except Exception as e:
                print(f"Failed to pull model: {e}")
                return False

    async def complete_code(
        self, prefix: str, language: Optional[str] = None, max_tokens: int = 256
    ) -> CodeSuggestion:
        """
        Generate code completion for the given prefix.

        Args:
            prefix: The code prefix to complete
            language: Optional language hint
            max_tokens: Maximum tokens to generate

        Returns:
            CodeSuggestion with completed code
        """
        start = time.time()

        prompt = self._build_completion_prompt(prefix, language)

        try:
            response = self.client.generate(
                model=self.model.value,
                prompt=prompt,
                options={
                    "num_predict": max_tokens,
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "stop": ["\n\n", "```", "\nclass ", "\ndef ", "\n#"],
                },
            )

            latency_ms = (time.time() - start) * 1000

            return CodeSuggestion(
                text=response["response"],
                language=language or self._detect_language(prefix),
                confidence=response.get("probs", [{}])[-1].get("prob", 0.8),
                model=self.model.value,
                latency_ms=latency_ms,
            )
        except Exception as e:
            raise RuntimeError(f"Code completion failed: {e}")

    async def stream_complete(
        self, prefix: str, language: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Stream code completion."""
        prompt = self._build_completion_prompt(prefix, language)

        try:
            response = self.client.generate(
                model=self.model.value,
                prompt=prompt,
                stream=True,
                options={"temperature": 0.2},
            )

            for chunk in response:
                yield chunk["response"]
        except Exception as e:
            raise RuntimeError(f"Streaming completion failed: {e}")

    async def explain_code(self, code: str, language: str = "python") -> CodeExplain:
        """Explain code in plain English."""
        prompt = f"""Explain the following {language} code:

```{language}
{code}
```

Provide:
1. A one-line summary
2. Detailed explanation of what it does
3. Time and space complexity (if applicable)
4. Any potential issues or improvements

Format as JSON:
{{
    "summary": "...",
    "details": "...",
    "complexity": "...",
    "time_complexity": "...",
    "space_complexity": "..."
}}
"""

        try:
            response = self.client.generate(
                model=self.model.value,
                prompt=prompt,
                format="json",
                options={"temperature": 0.3},
            )

            result = json.loads(response["response"])
            return CodeExplain(
                summary=result.get("summary", ""),
                details=result.get("details", ""),
                complexity=result.get("complexity", ""),
                time_complexity=result.get("time_complexity"),
                space_complexity=result.get("space_complexity"),
            )
        except json.JSONDecodeError:
            return CodeExplain(
                summary="Unable to parse explanation",
                details=response.get("response", "Error"),
                complexity="Unknown",
            )

    async def fix_code(
        self, code: str, error: Optional[str] = None, language: str = "python"
    ) -> List[CodeFix]:
        """Suggest fixes for code issues."""
        prompt = f"""Fix the following {language} code:

```{language}
{code}
```

{f"Error: {error}" if error else ""}

Identify and fix:
1. Syntax errors
2. Logical errors
3. Performance issues
4. Security vulnerabilities

Format as JSON array:
[
    {{
        "original": "problematic code",
        "fixed": "fixed code",
        "explanation": "why this fix is needed",
        "severity": "error|warning|info",
        "line_number": 5
    }}
]
"""

        try:
            response = self.client.generate(
                model=self.model.value,
                prompt=prompt,
                format="json",
                options={"temperature": 0.2},
            )

            fixes = json.loads(response["response"])
            return [
                CodeFix(
                    original=f.get("original", ""),
                    fixed=f.get("fixed", ""),
                    explanation=f.get("explanation", ""),
                    severity=f.get("severity", "info"),
                    line_number=f.get("line_number"),
                )
                for f in fixes
            ]
        except json.JSONDecodeError:
            return []

    async def generate_tests(
        self, code: str, language: str = "python", test_framework: str = "pytest"
    ) -> str:
        """Generate unit tests for code."""
        prompt = f"""Generate comprehensive unit tests for the following {language} code using {test_framework}:

```{language}
{code}
```

Requirements:
- Test all public functions
- Cover edge cases
- Use descriptive test names
- Include setup/teardown if needed
- Mock external dependencies
"""

        try:
            response = self.client.generate(
                model=self.model.value, prompt=prompt, options={"temperature": 0.3}
            )
            return response["response"]
        except Exception as e:
            raise RuntimeError(f"Test generation failed: {e}")

    async def refactor_code(
        self, code: str, goal: str, language: str = "python"
    ) -> str:
        """Refactor code to achieve a goal."""
        prompt = f"""Refactor the following {language} code to {goal}:

```{language}
{code}
```

Provide the complete refactored code with:
- Improved naming
- Better structure
- Added comments
- Preserved functionality
"""

        try:
            response = self.client.generate(
                model=self.model.value, prompt=prompt, options={"temperature": 0.4}
            )
            return response["response"]
        except Exception as e:
            raise RuntimeError(f"Refactoring failed: {e}")

    async def document_code(
        self, code: str, language: str = "python", style: str = "google"
    ) -> str:
        """Generate documentation for code."""
        prompt = f"""Add {style}-style documentation to the following {language} code:

```{language}
{code}
```

Include:
- Module docstring
- Class docstrings (if applicable)
- Function docstrings with Args/Returns/Raises
- Inline comments for complex logic
"""

        try:
            response = self.client.generate(
                model=self.model.value, prompt=prompt, options={"temperature": 0.3}
            )
            return response["response"]
        except Exception as e:
            raise RuntimeError(f"Documentation failed: {e}")

    def _build_completion_prompt(self, prefix: str, language: Optional[str]) -> str:
        """Build a prompt for code completion."""
        lang_hint = f" in {language}" if language else ""

        return f"""Complete the following code{lang_hint}:

```
{prefix}
```
Complete the code above. Return ONLY the completion, no explanations or markdown.
"""

    def _detect_language(self, code: str) -> str:
        """Detect programming language from code."""
        lang_patterns = {
            "python": ["def ", "import ", "from ", "class ", "print(", "if __name__"],
            "javascript": [
                "function ",
                "const ",
                "let ",
                "=>",
                "console.log",
                "import ",
            ],
            "typescript": ["interface ", "type ", ": ", "export ", "async "],
            "rust": ["fn ", "let mut ", "impl ", "-> ", "pub fn"],
            "go": ["func ", "package ", "import ", "var ", "type "],
            "java": ["public class ", "public static void ", "import ", "System.out."],
            "c": ["#include ", "int main()", "printf(", "struct "],
            "cpp": ["#include ", "std::", "using namespace ", "class "],
            "ruby": ["def ", "require ", "class ", "puts ", "end"],
            "php": ["<?php", "function ", "echo ", "class "],
            "swift": ["func ", "import ", "class ", "var ", "let "],
            "kotlin": ["fun ", "class ", "val ", "var ", "import "],
            "sql": ["SELECT ", "INSERT ", "UPDATE ", "DELETE ", "FROM "],
            "bash": ["#!/bin/bash", "echo ", "cd ", "export "],
            "solidity": ["pragma solidity", "contract ", "function ", "uint256"],
        }

        code_lower = code.lower()
        for lang, patterns in lang_patterns.items():
            for pattern in patterns:
                if pattern.lower() in code_lower:
                    return lang
        return "text"


class MultiModelCoder:
    """
    Use multiple coding models based on task type.
    """

    def __init__(self):
        self.qwen_coder = OllamaCoder(CodingModel.QWEN_CODER_32B)
        self.deepseek_coder = OllamaCoder(CodingModel.DEEPSEEK_CODER_V2)
        self.codellama = OllamaCoder(CodingModel.CODE_LLAMA_34B)

    async def complete(
        self, prefix: str, language: Optional[str] = None, complexity: str = "medium"
    ) -> CodeSuggestion:
        """Get code completion with appropriate model."""
        if complexity == "high":
            return await self.deepseek_coder.complete_code(prefix, language)
        return await self.qwen_coder.complete_code(prefix, language)

    async def explain(self, code: str, language: str = "python") -> CodeExplain:
        """Explain code using best model."""
        return await self.deepseek_coder.explain_code(code, language)

    async def fix(
        self, code: str, error: Optional[str] = None, language: str = "python"
    ) -> List[CodeFix]:
        """Fix code issues."""
        return await self.deepseek_coder.fix_code(code, error, language)


def setup_ollama_coding():
    """Setup Ollama for coding - pull models and verify."""
    print("🐝 Setting up Ollama for Coding...")
    print("-" * 40)

    models_to_pull = [
        (CodingModel.QWEN_CODER_32B, "Primary coding model - GPT-4o level"),
        (CodingModel.DEEPSEEK_CODER_V2, "Complex algorithms & reasoning"),
        (CodingModel.CODE_LLAMA_34B, "Code generation backup"),
    ]

    results = []
    for model, description in models_to_pull:
        print(f"\n📦 {model.value}")
        print(f"   {description}")

        coder = OllamaCoder(model)

        if not coder.is_available():
            print(f"   ⚠️  Ollama not running. Start with: ollama serve")
            results.append((model, False, "Ollama not running"))
            continue

        if not coder.ensure_model():
            print(f"   ❌ Failed to pull model")
            results.append((model, False, "Pull failed"))
            continue

        print(f"   ✅ Ready!")
        results.append((model, True, "Ready"))

    print("\n" + "=" * 40)
    print("Setup complete! You can now code 100% offline.")

    return all(r[1] for r in results)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_ollama_coding()
    else:
        coder = OllamaCoder()

        if not coder.is_available():
            print("❌ Ollama not running. Start with: ollama serve")
            sys.exit(1)

        print("🐝 Ollama Coder - 100% Offline Coding")
        print("-" * 40)
        print(f"Model: {coder.model.value}")
        print(f"Host: {coder.host}")

        async def demo():
            print("\n📝 Code Completion Demo:")
            suggestion = await coder.complete_code("def fibonacci(n):", "python")
            print(f"  {suggestion.text}")

        asyncio.run(demo())
