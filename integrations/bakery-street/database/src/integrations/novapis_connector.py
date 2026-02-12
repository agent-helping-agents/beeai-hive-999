"""
NovAPIS Framework Integration
🔒 PRIVATE - PROPRIETARY
© 2025 Baker Street Laboratory

Connects Energetic Lexicon to NovAPIS Python framework.
NovAPIS provides deep code analysis and concept extraction capabilities.
"""

import subprocess
import json
import logging
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class NovAPISConnector:
    """
    Connector for NovAPIS Framework

    NovAPIS is a proprietary Python framework for code analysis.
    This connector provides:
    - Repository analysis and ingestion
    - Concept extraction from code
    - Dependency graph generation
    - Code pattern recognition
    """

    def __init__(self, novapis_path: str = "./novapis"):
        """
        Initialize NovAPIS connector

        Args:
            novapis_path: Path to NovAPIS installation
        """
        self.novapis_path = Path(novapis_path)

        if not self.novapis_path.exists():
            logger.warning(f"NovAPIS path not found: {novapis_path}")

        logger.info(f"Initialized NovAPIS connector: {novapis_path}")

    def ingest_repository(
        self,
        repo_url: str,
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Use NovAPIS to analyze and ingest repository

        NovAPIS provides deep code analysis capabilities for extracting
        concepts, patterns, and relationships from source code.

        Args:
            repo_url: Git repository URL
            output_format: Output format (json, yaml, db)

        Returns:
            dict: {
                'repository': str,
                'concepts': List[str],
                'dependencies': List[str],
                'patterns': List[str],
                'metrics': dict
            }
        """
        logger.info(f"Ingesting repository: {repo_url}")

        try:
            result = subprocess.run([
                'python',
                str(self.novapis_path / 'analyze.py'),
                '--repo', repo_url,
                '--output', output_format
            ], capture_output=True, text=True, timeout=300)

            if result.returncode != 0:
                logger.error(f"NovAPIS failed: {result.stderr}")
                return {
                    'repository': repo_url,
                    'concepts': [],
                    'dependencies': [],
                    'patterns': [],
                    'metrics': {},
                    'error': result.stderr
                }

            return json.loads(result.stdout)

        except subprocess.TimeoutExpired:
            logger.error("NovAPIS timeout (300s)")
            return {
                'repository': repo_url,
                'error': 'Timeout'
            }

        except json.JSONDecodeError as e:
            logger.error(f"NovAPIS JSON parse error: {e}")
            return {
                'repository': repo_url,
                'error': 'Invalid JSON output'
            }

        except Exception as e:
            logger.error(f"NovAPIS error: {e}")
            return {
                'repository': repo_url,
                'error': str(e)
            }

    def extract_concepts(
        self,
        code: str,
        language: str = "python"
    ) -> List[str]:
        """
        Extract concepts from code using NovAPIS

        Analyzes source code to identify key concepts, classes, and patterns.

        Args:
            code: Source code string
            language: Programming language

        Returns:
            list: Extracted concept names
        """
        logger.info(f"Extracting concepts from {language} code")

        try:
            result = subprocess.run([
                'python',
                str(self.novapis_path / 'extract_concepts.py'),
                '--language', language,
                '--input', '-'
            ], input=code, capture_output=True, text=True, timeout=60)

            if result.returncode != 0:
                logger.error(f"Concept extraction failed: {result.stderr}")
                return []

            data = json.loads(result.stdout)
            return data.get('concepts', [])

        except Exception as e:
            logger.error(f"Concept extraction error: {e}")
            return []

    def analyze_dependencies(
        self,
        project_path: str
    ) -> Dict[str, List[str]]:
        """
        Analyze project dependencies using NovAPIS

        Generates dependency graph and identifies critical components.

        Args:
            project_path: Path to project directory

        Returns:
            dict: {
                'direct': List[str],
                'transitive': List[str],
                'critical': List[str]
            }
        """
        logger.info(f"Analyzing dependencies: {project_path}")

        try:
            result = subprocess.run([
                'python',
                str(self.novapis_path / 'dependencies.py'),
                '--project', project_path,
                '--format', 'json'
            ], capture_output=True, text=True, timeout=120)

            if result.returncode != 0:
                logger.error(f"Dependency analysis failed: {result.stderr}")
                return {
                    'direct': [],
                    'transitive': [],
                    'critical': []
                }

            return json.loads(result.stdout)

        except Exception as e:
            logger.error(f"Dependency analysis error: {e}")
            return {
                'direct': [],
                'transitive': [],
                'critical': []
            }

    def detect_patterns(
        self,
        code: str,
        pattern_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Detect design patterns and code patterns using NovAPIS

        Args:
            code: Source code
            pattern_types: Specific patterns to detect (None = all)

        Returns:
            list: [{
                'pattern': str,
                'location': str,
                'confidence': float
            }]
        """
        logger.info("Detecting code patterns")

        try:
            args = [
                'python',
                str(self.novapis_path / 'pattern_detection.py'),
                '--input', '-'
            ]

            if pattern_types:
                args.extend(['--patterns', ','.join(pattern_types)])

            result = subprocess.run(
                args,
                input=code,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                logger.error(f"Pattern detection failed: {result.stderr}")
                return []

            data = json.loads(result.stdout)
            return data.get('patterns', [])

        except Exception as e:
            logger.error(f"Pattern detection error: {e}")
            return []

    def health_check(self) -> bool:
        """
        Check if NovAPIS is available

        Returns:
            bool: True if NovAPIS can be executed
        """
        if not self.novapis_path.exists():
            return False

        try:
            result = subprocess.run([
                'python',
                str(self.novapis_path / 'version.py')
            ], capture_output=True, timeout=5)

            return result.returncode == 0

        except Exception:
            return False

    def __repr__(self):
        return f"<NovAPISConnector(path='{self.novapis_path}')>"
