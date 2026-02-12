#!/usr/bin/env python3
"""
Explore Ollama alternatives for research & investigating hypercube setting.

This script explores various inference options for the BeeAI Hive 999
system in a research and investigating hypercube environment.
"""

import sys
import os
import asyncio
import subprocess

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def check_ollama_models():
    """Check available Ollama models."""
    print("=== Available Ollama Models ===")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Error: ollama command not available")
    except Exception as e:
        print(f"Error checking Ollama models: {e}")
    print()


async def check_ollama_running():
    """Check if Ollama service is running."""
    print("=== Ollama Service Status ===")
    try:
        result = subprocess.run(["ollama", "ps"], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Ollama service not running")
    except Exception as e:
        print(f"Error checking Ollama service: {e}")
    print()


async def explore_ollama_alternatives():
    """Explore alternative inference options."""
    print("=== Exploring Ollama Alternatives ===")

    alternatives = [
        {
            "name": "Ollama Local (Current)",
            "description": "Ollama running locally with various models",
            "status": "Available"
            if os.path.exists("/usr/bin/ollama")
            else "Not Installed",
        },
        {
            "name": "Hugging Face Transformers",
            "description": "Run models locally using Hugging Face Transformers library",
            "status": "Available"
            if os.system("python -c 'import transformers' 2>/dev/null") == 0
            else "Not Installed",
        },
        {
            "name": "PyTorch Direct",
            "description": "Direct PyTorch inference (requires GPU)",
            "status": "Available"
            if os.system("python -c 'import torch' 2>/dev/null") == 0
            else "Not Installed",
        },
        {
            "name": "TensorFlow",
            "description": "TensorFlow/Keras inference",
            "status": "Available"
            if os.system("python -c 'import tensorflow' 2>/dev/null") == 0
            else "Not Installed",
        },
        {
            "name": "ONNX Runtime",
            "description": "ONNX Runtime for optimized inference",
            "status": "Available"
            if os.system("python -c 'import onnxruntime' 2>/dev/null") == 0
            else "Not Installed",
        },
        {
            "name": "JAX",
            "description": "JAX for high-performance numerical computation",
            "status": "Available"
            if os.system("python -c 'import jax' 2>/dev/null") == 0
            else "Not Installed",
        },
        {
            "name": "Gradio",
            "description": "Gradio for easy model interfaces",
            "status": "Available"
            if os.system("python -c 'import gradio' 2>/dev/null") == 0
            else "Not Installed",
        },
        {
            "name": "FastAPI",
            "description": "FastAPI for REST API endpoints",
            "status": "Available"
            if os.system("python -c 'import fastapi' 2>/dev/null") == 0
            else "Not Installed",
        },
        {
            "name": "Flask",
            "description": "Flask for simple web applications",
            "status": "Available"
            if os.system("python -c 'import flask' 2>/dev/null") == 0
            else "Not Installed",
        },
        {
            "name": "Ray Serve",
            "description": "Ray Serve for distributed model serving",
            "status": "Available"
            if os.system("python -c 'import ray' 2>/dev/null") == 0
            else "Not Installed",
        },
    ]

    for idx, alt in enumerate(alternatives, 1):
        status = "✅" if "Available" in alt["status"] else "❌"
        print(f"{idx:2}. {status} {alt['name']}")
        print(f"    {alt['description']}")
        print(f"    Status: {alt['status']}")
        print()


async def explore_cloud_options():
    """Explore cloud inference options."""
    print("=== Cloud Inference Options ===")

    cloud_options = [
        {
            "name": "OpenAI API",
            "description": "OpenAI GPT-4, GPT-3.5 API access",
            "key": "OPENAI_API_KEY",
            "status": os.environ.get("OPENAI_API_KEY") is not None,
        },
        {
            "name": "Anthropic API",
            "description": "Anthropic Claude 3 API access",
            "key": "ANTHROPIC_API_KEY",
            "status": os.environ.get("ANTHROPIC_API_KEY") is not None,
        },
        {
            "name": "Google Vertex AI",
            "description": "Google Cloud Vertex AI",
            "key": "GOOGLE_APPLICATION_CREDENTIALS",
            "status": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is not None,
        },
        {
            "name": "AWS Bedrock",
            "description": "Amazon Bedrock API",
            "key": "AWS_ACCESS_KEY_ID",
            "status": os.environ.get("AWS_ACCESS_KEY_ID") is not None,
        },
        {
            "name": "Azure OpenAI",
            "description": "Azure OpenAI service",
            "key": "AZURE_OPENAI_KEY",
            "status": os.environ.get("AZURE_OPENAI_KEY") is not None,
        },
        {
            "name": "Hugging Face Inference Endpoints",
            "description": "Hugging Face Inference API",
            "key": "HUGGING_FACE_HUB_TOKEN",
            "status": os.environ.get("HUGGING_FACE_HUB_TOKEN") is not None,
        },
        {
            "name": "Replicate API",
            "description": "Replicate AI platform",
            "key": "REPLICATE_API_TOKEN",
            "status": os.environ.get("REPLICATE_API_TOKEN") is not None,
        },
    ]

    for idx, option in enumerate(cloud_options, 1):
        status = "✅" if option["status"] else "❌"
        print(f"{idx:2}. {status} {option['name']}")
        print(f"    {option['description']}")
        print(f"    Status: {'Configured' if option['status'] else 'Not Configured'}")
        print()


async def check_gpu_availability():
    """Check GPU availability for local inference."""
    print("=== GPU Availability ===")

    try:
        import torch

        if torch.cuda.is_available():
            print(f"CUDA Available: ✅ {torch.cuda.get_device_name(0)}")
            print(f"CUDA Version: {torch.version.cuda}")
            print(
                f"CUDA Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB"
            )
        elif torch.backends.mps.is_available():
            print("MPS Available: ✅ Apple Silicon GPU")
        else:
            print("No GPU Available: ❌ Using CPU only")
    except ImportError:
        print("PyTorch not available, checking NVIDIA-SMI...")
        try:
            result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
            if result.returncode == 0:
                print("NVIDIA GPU Available: ✅")
                print(result.stdout.split("\n")[0])
            else:
                print("No NVIDIA GPU detected")
        except:
            print("No GPU information available")

    print()


async def main():
    """Main function to explore inference options."""
    print("🚀 BeeAI Hive 999 - Inference Options Exploration")
    print("=" * 70)
    print()

    await check_ollama_models()
    await check_ollama_running()
    await explore_ollama_alternatives()
    await explore_cloud_options()
    await check_gpu_availability()

    print("=" * 70)
    print("📊 Summary")
    print("=" * 70)
    print()
    print("Recommended Setup for Research & Investigation Hypercube:")
    print("1. **Ollama Local**: Use for quick prototyping and debugging")
    print("2. **Hugging Face Transformers**: For detailed model exploration")
    print("3. **PyTorch/TensorFlow**: For custom research and model modification")
    print("4. **Cloud APIs**: For heavy-duty analysis and benchmarking")
    print()
    print("Key Models to Explore:")
    print("- marco-o1:latest (For reasoning and analysis)")
    print("- llama3.2:latest (For general purpose tasks)")
    print("- deepseek-r1:8b (For deep reasoning)")
    print("- qwen2.5-coder:32b (For coding and technical tasks)")
    print("- nomic-embed-text (For embeddings and search)")
    print()
    print("💡 Tips:")
    print("- Use 'ollama pull <model>' to download new models")
    print("- Check config/hive_config.py for model configuration")
    print("- Use the TUI to test different models interactively")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExploration canceled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        print(traceback.format_exc())
        sys.exit(1)
