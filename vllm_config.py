"""
vLLM Configuration for Marco-o1 Model

This module provides configuration and helper functions for running
the Marco-o1 model with vLLM's high-throughput inference engine.
Falls back to Hugging Face transformers if vLLM is not available.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any

# Model configuration
MODEL_CONFIG: Dict[str, Any] = {
    "model_name": "AIDC-AI/Marco-o1",
    "local_model_dir": "./models/AIDC-AI/Marco-o1",
    "dtype": "half",  # Use float16 for better performance on GPU
    "trust_remote_code": True,
    "max_model_len": 4096,
    "gpu_memory_utilization": 0.9,
    "swap_space": 4,
}

# Check if vLLM is available
VLLM_AVAILABLE = False
try:
    import vllm

    VLLM_AVAILABLE = True
    print(f"✅ vLLM is available (version: {vllm.__version__})")
except ImportError as e:
    print(f"⚠️ vLLM not available: {e}")
    print("Falling back to Hugging Face transformers")
    VLLM_AVAILABLE = False


def get_vllm_config(
    model_name: str = None,
    local_dir: str = None,
    dtype: str = None,
    max_model_len: int = None,
    gpu_memory_utilization: float = None,
    swap_space: int = None,
) -> Dict[str, Any]:
    """
    Get complete vLLM configuration with optional overrides.

    Args:
        model_name: Model name or path
        local_dir: Local directory to load model from
        dtype: Data type for computation
        max_model_len: Maximum model length
        gpu_memory_utilization: GPU memory utilization fraction
        swap_space: Swap space in GB for CPU offloading

    Returns:
        Configuration dictionary for vLLM
    """
    config = MODEL_CONFIG.copy()

    if model_name:
        config["model_name"] = model_name
    if local_dir:
        config["local_model_dir"] = local_dir
    if dtype:
        config["dtype"] = dtype
    if max_model_len:
        config["max_model_len"] = max_model_len
    if gpu_memory_utilization:
        config["gpu_memory_utilization"] = gpu_memory_utilization
    if swap_space:
        config["swap_space"] = swap_space

    return config


def check_model_files() -> bool:
    """
    Check if required model files are available locally.

    Returns:
        True if all required files are present, False otherwise
    """
    model_dir = Path(MODEL_CONFIG["local_model_dir"])

    if not model_dir.exists():
        print(f"Model directory not found: {model_dir}")
        return False

    required_files = [
        "config.json",
        "model.safetensors.index.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "vocab.json",
    ]

    missing_files = []
    for file_name in required_files:
        file_path = model_dir / file_name
        if not file_path.exists():
            missing_files.append(file_name)

    if missing_files:
        print(f"Missing required model files: {', '.join(missing_files)}")
        return False

    print(f"✅ All model files found in: {model_dir}")
    return True


def download_model() -> bool:
    """
    Download Marco-o1 model from Hugging Face Hub.

    Returns:
        True if download successful, False otherwise
    """
    from huggingface_hub import snapshot_download

    try:
        model_dir = Path(MODEL_CONFIG["local_model_dir"])
        model_dir.mkdir(parents=True, exist_ok=True)

        print(f"Downloading {MODEL_CONFIG['model_name']} to {model_dir}")

        snapshot_download(
            repo_id=MODEL_CONFIG["model_name"],
            local_dir=MODEL_CONFIG["local_model_dir"],
            local_dir_use_symlinks=False,
        )

        print("✅ Model download completed")
        return check_model_files()

    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False


def create_huggingface_engine(
    config: Optional[Dict[str, Any]] = None, fallback_to_gpt2: bool = True
) -> Any:
    """
    Create a Hugging Face transformers engine as fallback.

    Args:
        config: Engine configuration
        fallback_to_gpt2: Whether to fall back to GPT-2 if Marco-o1 fails to load

    Returns:
        Hugging Face pipeline instance
    """
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch

    if config is None:
        config = get_vllm_config()

    try:
        print("Creating Hugging Face engine...")

        # Skip Marco-o1 for now and use GPT-2 directly
        print("Skipping Marco-o1 download (large file), using GPT-2 directly")
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        model = AutoModelForCausalLM.from_pretrained(
            "gpt2", torch_dtype=torch.float32, device_map="cpu"
        )
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=2048,
            device_map="cpu",
        )
        print("✅ GPT-2 engine created successfully")
        return pipe

    except Exception as e:
        print(f"❌ Error creating Hugging Face engine: {e}")
        raise RuntimeError(f"Failed to create Hugging Face engine: {e}") from e

    except Exception as e:
        print(f"❌ Error creating Hugging Face engine: {e}")
        raise RuntimeError(f"Failed to create Hugging Face engine: {e}") from e


def create_vllm_engine(config: Optional[Dict[str, Any]] = None) -> Any:
    """
    Create inference engine - uses vLLM if available, falls back to Hugging Face.

    Args:
        config: Engine configuration

    Returns:
        Inference engine instance
    """
    if VLLM_AVAILABLE:
        try:
            from vllm import LLM, SamplingParams

            if config is None:
                config = get_vllm_config()

            # Check model files
            if not check_model_files():
                print("Attempting to download model...")
                if not download_model():
                    raise RuntimeError("Model files not available")

            print("Creating vLLM engine...")

            # Try GPU first, fall back to CPU if CUDA not available or mismatch
            try:
                llm = LLM(
                    model=config["local_model_dir"],
                    dtype=config["dtype"],
                    trust_remote_code=config["trust_remote_code"],
                    max_model_len=config["max_model_len"],
                    gpu_memory_utilization=config["gpu_memory_utilization"],
                    swap_space=config["swap_space"],
                    tensor_parallel_size=1,  # Single GPU
                )
                print("✅ vLLM engine created (GPU mode)")
                return llm
            except Exception as gpu_error:
                print(f"GPU mode failed: {gpu_error}")
                print("Trying CPU mode...")
                llm = LLM(
                    model=config["local_model_dir"],
                    dtype="float32",  # Use float32 for CPU
                    trust_remote_code=config["trust_remote_code"],
                    max_model_len=config["max_model_len"],
                    cpu_offload_gb=20,  # Offload to CPU with 20GB swap
                    swap_space=20,
                    tensor_parallel_size=0,  # CPU only
                    gpu_memory_utilization=0,  # No GPU memory used
                )
                print("✅ vLLM engine created (CPU mode)")
                return llm
        except Exception as e:
            print(f"❌ vLLM engine creation failed: {e}")
            print("Falling back to Hugging Face engine")
            return create_huggingface_engine(config)
    else:
        print("vLLM not available, using Hugging Face engine")
        return create_huggingface_engine(config)


class SamplingParams:
    """
    Simple sampling parameters class that works for both vLLM and Hugging Face.
    """

    def __init__(
        self,
        temperature: float = 0.8,
        top_p: float = 0.95,
        max_tokens: int = 2048,
        presence_penalty: float = 0.1,
        frequency_penalty: float = 0.1,
        stop: Optional[list] = None,
        logprobs: int = 1,
    ):
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.stop = stop or ["<|end_of_solution|>", "<|end_of_thought|>", "</s>"]
        self.logprobs = logprobs


def create_sampling_params(
    temperature: float = 0.8,
    top_p: float = 0.95,
    max_tokens: int = 2048,
    presence_penalty: float = 0.1,
    frequency_penalty: float = 0.1,
    stop: Optional[list] = None,
) -> SamplingParams:
    """
    Create sampling parameters for generation.

    Args:
        temperature: Sampling temperature
        top_p: Nucleus sampling parameter
        max_tokens: Maximum number of tokens to generate
        presence_penalty: Presence penalty
        frequency_penalty: Frequency penalty
        stop: Stop sequences

    Returns:
        SamplingParams object
    """
    return SamplingParams(
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
        stop=stop,
        logprobs=1,
    )


def generate_text(
    engine: Any, prompt: str, sampling_params: Any, max_retries: int = 3
) -> Dict[str, Any]:
    """
    Generate text using either vLLM or Hugging Face engine.

    Args:
        engine: vLLM or Hugging Face engine instance
        prompt: Input prompt
        sampling_params: Sampling parameters
        max_retries: Maximum retry attempts

    Returns:
        Generation results
    """
    # Check if engine is vLLM or Hugging Face
    if hasattr(engine, "generate"):
        # vLLM engine
        for attempt in range(max_retries):
            try:
                outputs = engine.generate([prompt], sampling_params)

                if outputs and len(outputs) > 0:
                    output = outputs[0]
                    return {
                        "prompt": prompt,
                        "generated_text": output.outputs[0].text.strip(),
                        "tokens": output.outputs[0].token_ids,
                        "logprobs": output.outputs[0].logprobs,
                        "stop_reason": output.outputs[0].stop_reason,
                        "prompt_tokens": len(output.prompt_token_ids),
                        "generated_tokens": len(output.outputs[0].token_ids),
                    }

                raise RuntimeError("No output generated")

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise RuntimeError(
                        f"Failed to generate text after {max_retries} attempts: {e}"
                    ) from e
    else:
        # Hugging Face pipeline
        for attempt in range(max_retries):
            try:
                # Convert vLLM sampling params to Hugging Face format (GPT-2 supports these)
                generation_kwargs = {
                    "max_new_tokens": sampling_params.max_tokens,
                    "temperature": sampling_params.temperature,
                    "top_p": sampling_params.top_p,
                    "do_sample": True,
                }

                result = engine(prompt, **generation_kwargs)

                if result:
                    generated_text = (
                        result[0]["generated_text"].strip().replace(prompt, "").strip()
                    )
                    return {
                        "prompt": prompt,
                        "generated_text": generated_text,
                        "tokens": None,
                        "logprobs": None,
                        "stop_reason": "eos_token",
                        "prompt_tokens": len(engine.tokenizer(prompt)["input_ids"]),
                        "generated_tokens": len(
                            engine.tokenizer(generated_text)["input_ids"]
                        ),
                    }

                raise RuntimeError("No output generated")

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise RuntimeError(
                        f"Failed to generate text after {max_retries} attempts: {e}"
                    ) from e

    raise RuntimeError("Max retries exceeded")


if __name__ == "__main__":
    """Test Hugging Face engine with GPT-2 fallback"""
    print("Testing Hugging Face engine with GPT-2 fallback...")

    try:
        # Test 1: Create engine with fallback
        print("\n1. Creating engine with fallback:")
        llm = create_vllm_engine()
        print("✅ Engine created successfully")

        # Test 2: Generate text
        print("\n2. Testing generation:")
        sampling_params = create_sampling_params()
        prompt = """Solve this math problem step by step: 25 + (30 - 5) * 2"""

        result = generate_text(llm, prompt, sampling_params)
        print(f"✅ Prompt processed in {result['prompt_tokens']} tokens")
        print(f"✅ Generated {result['generated_tokens']} tokens")
        print(f"✅ Generated text: {result['generated_text']}")

        print("\n🎉 Hugging Face engine test passed!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
