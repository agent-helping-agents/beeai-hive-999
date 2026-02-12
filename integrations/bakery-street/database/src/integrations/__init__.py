"""
Energetic Lexicon - External Tool Integrations
🔒 PRIVATE - PROPRIETARY
© 2025 Baker Street Laboratory

Connectors for:
- PRIMAX (Proprietary AI framework)
- NovAPIS (Proprietary Python framework)
- Dream Script (Self-evolving templates)
- Amphetamemes (Template system)
- AgenticSeek (GPL-3.0, isolated)
"""

__all__ = [
    'PRIMAXClient',
    'NovAPISConnector',
    'DreamScriptExecutor',
    'AmphetamemesConnector',
]

# Import proprietary connectors
try:
    from .primax_client import PRIMAXClient
except ImportError:
    PRIMAXClient = None

try:
    from .novapis_connector import NovAPISConnector
except ImportError:
    NovAPISConnector = None

try:
    from .dreamscript_executor import DreamScriptExecutor
except ImportError:
    DreamScriptExecutor = None

try:
    from .amphetamemes_connector import AmphetamemesConnector
except ImportError:
    AmphetamemesConnector = None
