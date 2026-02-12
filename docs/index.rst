Welcome to BeeAI Hive 999 documentation!
=========================================

A production-ready, full-screen terminal UI for a hybrid multi-agent system supporting both local (Ollama) and cloud (LangChain/LangSmith) backends.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules/agents
   modules/backend
   modules/tools
   modules/tui

Quick Start
-----------

.. code-block:: bash

   # Install dependencies
   pip install -e .

   # Run TUI
   python hive_tui_enhanced.py

   # Setup coding models
   python backend/ollama_coder.py setup

Features
--------

- **28+ Agents**: Queen Bee, 9 Workers, 9 Drones, 9 Foragers, Mantis Mail
- **9×9×9 Matrix**: 729 intersection nodes for blockchain × stakeholder × trend
- **Hybrid Backend**: Ollama (local) + LangChain (cloud)
- **Enhanced TUI**: Scrollable chat, bubbles, scrollbar, typing indicators
- **100% Offline Coding**: qwen2.5-coder:32b, deepseek-coder-v2:16b
- **Terminal 221b**: Sherlock Holmes-inspired Solana detective

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
