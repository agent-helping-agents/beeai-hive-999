# Hive 999 — Setup Guide

## Prerequisites

- Ubuntu Linux with Python 3.11+
- NVIDIA GPU with CUDA 12.2 (optional but recommended for ONNX)
- Ollama installed and running (`curl -fsSL https://ollama.ai/install.sh | sh`)

## Step 1: Pull Ollama Models

```bash
ollama pull granite3.3:8b
ollama pull llama3.2:3b
```

## Step 2: Create Virtual Environment

```bash
cd ~/beeai-hive-999
python3 -m venv .venv
source .venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install \
    beeai-framework \
    chromadb \
    pyyaml \
    prompt_toolkit

# Optional: GPU-accelerated ONNX for faster embeddings
pip install onnxruntime-gpu
# If no NVIDIA GPU, use CPU version:
# pip install onnxruntime
```

## Step 4: Generate the Matrix

```bash
python data/matrix/generate_matrix.py
# Creates data/matrix/matrix_729.json (729 nodes)
```

## Step 5: Embed into ChromaDB

```bash
python data/embeddings/embed_matrix.py
# Creates data/vectors/hive_vectors/ with collection "matrix_999"
```

## Step 6: Launch

### Option A: Full TUI
```bash
python main.py
# or
bash run.sh
```

### Option B: Simple REPL
```bash
python main.py --repl
```

### Option C: Single Query
```bash
python main.py --query "What are the RegTech implications of Ethereum for Government Agencies?"
```

## Step 7: (Optional) Install as systemd Service

```bash
sudo cp config/beeai-hive.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable beeai-hive
sudo systemctl start beeai-hive

# Check status
sudo systemctl status beeai-hive
journalctl -u beeai-hive -f
```

## Quick Start (All-in-One)

```bash
cd ~/beeai-hive-999
bash run.sh
```

The `run.sh` script handles all checks automatically.
