#!/usr/bin/env python3
"""
Terminal 221B v2.0 - Multi-LLM Support Engine
Support for Cohete, Mistral, Dolphin, Llama 2, and others

Local inference with model switching and performance optimization
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, List
import torch
import psutil
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════════════════
# AVAILABLE MODELS
# ═══════════════════════════════════════════════════════════════════════════

class ModelType(Enum):
    """Available LLM models"""
    COHETE_7B = "ehartford/cohete-7b-instruct"
    MISTRAL_7B_V2 = "mistralai/Mistral-7B-Instruct-v0.2"
    DOLPHIN_MISTRAL = "cognitivecomputations/dolphin-2.9-mistral-7b"
    LLAMA2_7B = "meta-llama/Llama-2-7b-chat-hf"
    NEURAL_CHAT_7B = "Intel/neural-chat-7b-v3-3"
    NEURAL_MONO = "microsoft/phi-2"  # Smaller, optimized alternative

@dataclass
class ModelConfig:
    """Configuration for an LLM model"""
    model_type: ModelType
    model_name: str
    size_gb: float
    quantization: str
    best_for: str
    requires_auth: bool
    optimal_device: str  # "cuda", "cpu", "intel_xpu"
    max_context: int
    speed_rating: str  # "FAST", "MEDIUM", "SLOW"
    quality_rating: str  # "EXCELLENT", "VERY_GOOD", "GOOD"
    uncensored: bool
    
# Model configurations
MODEL_CONFIGS = {
    ModelType.COHETE_7B: ModelConfig(
        model_type=ModelType.COHETE_7B,
        model_name="cohete-7b-instruct",
        size_gb=3.5,
        quantization="Q4_K_M",
        best_for="General-purpose bounty analysis, fast responses",
        requires_auth=False,
        optimal_device="cpu",
        max_context=8192,
        speed_rating="FAST",
        quality_rating="EXCELLENT",
        uncensored=True
    ),
    
    ModelType.MISTRAL_7B_V2: ModelConfig(
        model_type=ModelType.MISTRAL_7B_V2,
        model_name="Mistral-7B-Instruct-v0.2",
        size_gb=3.5,
        quantization="Q4_K_M",
        best_for="Code analysis, technical depth, reasoning",
        requires_auth=False,
        optimal_device="cpu",
        max_context=32768,
        speed_rating="FAST",
        quality_rating="VERY_GOOD",
        uncensored=False
    ),
    
    ModelType.DOLPHIN_MISTRAL: ModelConfig(
        model_type=ModelType.DOLPHIN_MISTRAL,
        model_name="dolphin-2.9-mistral-7b",
        size_gb=4.0,
        quantization="Q4_K_M",
        best_for="Complex vulnerability analysis, uncensored reasoning",
        requires_auth=False,
        optimal_device="cuda",
        max_context=32768,
        speed_rating="MEDIUM",
        quality_rating="EXCELLENT",
        uncensored=True
    ),
    
    ModelType.LLAMA2_7B: ModelConfig(
        model_type=ModelType.LLAMA2_7B,
        model_name="Llama-2-7b-chat",
        size_gb=3.2,
        quantization="Q4_K_M",
        best_for="Fallback option, general dialogue",
        requires_auth=True,  # Requires Meta license acceptance
        optimal_device="cpu",
        max_context=4096,
        speed_rating="MEDIUM",
        quality_rating="GOOD",
        uncensored=False
    ),
    
    ModelType.NEURAL_CHAT_7B: ModelConfig(
        model_type=ModelType.NEURAL_CHAT_7B,
        model_name="neural-chat-7b-v3-3",
        size_gb=3.3,
        quantization="Q4_K_M",
        best_for="Intel CPU optimization",
        requires_auth=False,
        optimal_device="intel_xpu",
        max_context=4096,
        speed_rating="FAST",
        quality_rating="GOOD",
        uncensored=False
    ),
}

# ═══════════════════════════════════════════════════════════════════════════
# SYSTEM DETECTION
# ═══════════════════════════════════════════════════════════════════════════

class SystemDetector:
    """Detect system capabilities for optimal model selection"""
    
    @staticmethod
    def get_gpu_info() -> Dict:
        """Get GPU information"""
        try:
            if torch.cuda.is_available():
                return {
                    "available": True,
                    "device": "cuda",
                    "device_name": torch.cuda.get_device_name(0),
                    "vram_total_gb": torch.cuda.get_device_properties(0).total_memory / 1e9,
                    "vram_free_gb": torch.cuda.mem_get_info()[0] / 1e9,
                    "compute_capability": torch.cuda.get_device_capability(0),
                }
            elif torch.backends.mps.is_available():  # Apple Metal Performance Shaders
                return {
                    "available": True,
                    "device": "mps",
                    "device_name": "Apple Metal (MPS)",
                    "vram_total_gb": None,
                    "vram_free_gb": None,
                }
            else:
                return {"available": False, "device": "cpu"}
        except Exception as e:
            return {"available": False, "device": "cpu", "error": str(e)}
    
    @staticmethod
    def get_cpu_info() -> Dict:
        """Get CPU information"""
        return {
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
            "cpu_freq_ghz": psutil.cpu_freq().max / 1000,
            "brand": SystemDetector._detect_cpu_brand(),
        }
    
    @staticmethod
    def _detect_cpu_brand() -> str:
        """Detect CPU brand (Intel/AMD/Apple Silicon)"""
        import platform
        system = platform.system()
        if system == "Darwin":
            return "Apple Silicon"
        try:
            import subprocess
            info = subprocess.check_output("lscpu").decode()
            if "Intel" in info:
                return "Intel"
            elif "AMD" in info:
                return "AMD"
        except:
            pass
        return "Unknown"
    
    @staticmethod
    def get_ram_info() -> Dict:
        """Get RAM information"""
        vm = psutil.virtual_memory()
        return {
            "total_gb": vm.total / 1e9,
            "available_gb": vm.available / 1e9,
            "used_gb": vm.used / 1e9,
            "percent_used": vm.percent,
        }
    
    @staticmethod
    def recommend_model() -> ModelType:
        """Recommend best model based on system specs"""
        gpu = SystemDetector.get_gpu_info()
        cpu = SystemDetector.get_cpu_info()
        ram = SystemDetector.get_ram_info()
        
        # CUDA GPU with good VRAM
        if gpu["available"] and gpu["device"] == "cuda":
            if gpu["vram_free_gb"] > 6:
                return ModelType.DOLPHIN_MISTRAL  # Best quality
            elif gpu["vram_free_gb"] > 4:
                return ModelType.MISTRAL_7B_V2  # Good balance
            else:
                return ModelType.COHETE_7B  # Lightweight
        
        # Apple Metal
        elif gpu["available"] and gpu["device"] == "mps":
            return ModelType.MISTRAL_7B_V2  # MPS optimized
        
        # Intel CPU
        elif "Intel" in cpu["brand"]:
            return ModelType.NEURAL_CHAT_7B  # Intel optimized
        
        # Generic CPU
        else:
            if ram["available_gb"] > 12:
                return ModelType.COHETE_7B  # Best CPU performance
            else:
                return ModelType.NEURAL_MONO  # Minimal memory
        
        return ModelType.COHETE_7B  # Safe default

# ═══════════════════════════════════════════════════════════════════════════
# MULTI-LLM ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class MultiLLMEngine:
    """
    Multi-LLM inference engine with model switching
    
    Features:
    - Load any model configuration
    - Switch between models efficiently
    - Performance tracking
    - Automatic device selection
    - RAM-efficient loading
    """
    
    def __init__(self):
        self.current_model = None
        self.current_model_type = None
        self.pipeline = None
        self.device = self._select_device()
        self.performance_log = []
        
    def _select_device(self) -> str:
        """Select optimal device for inference"""
        gpu = SystemDetector.get_gpu_info()
        if gpu["available"]:
            return gpu["device"]
        return "cpu"
    
    def load_model(self, model_type: ModelType) -> bool:
        """Load a specific model"""
        try:
            config = MODEL_CONFIGS[model_type]
            print(f"\n📥 Loading {config.model_name}...")
            print(f"   Device: {self.device}")
            print(f"   Size: {config.size_gb}GB")
            print(f"   Quantization: {config.quantization}")
            
            self.pipeline = pipeline(
                "text-generation",
                model=config.model_type.value,
                torch_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                model_kwargs={
                    "load_in_8bit": self.device == "cuda",
                    "trust_remote_code": True,
                }
            )
            
            self.current_model = config
            self.current_model_type = model_type
            
            print(f"✅ Model loaded successfully!\n")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load model: {str(e)}\n")
            return False
    
    def switch_model(self, model_type: ModelType) -> bool:
        """Switch to a different model"""
        if self.current_model_type == model_type:
            print(f"ℹ️  Model {self.current_model.model_name} already loaded\n")
            return True
        
        # Unload current model
        if self.pipeline is not None:
            del self.pipeline
            if self.device == "cuda":
                torch.cuda.empty_cache()
        
        # Load new model
        return self.load_model(model_type)
    
    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """Generate text using current model"""
        if self.pipeline is None:
            return "Error: No model loaded"
        
        try:
            response = self.pipeline(
                prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.95,
                top_k=50,
            )
            return response[0]["generated_text"]
        except Exception as e:
            return f"Error during generation: {str(e)}"
    
    def chat(self, system_prompt: str, user_message: str, max_tokens: int = 1024) -> str:
        """Chat-style generation with system prompt"""
        formatted_prompt = f"""<|system|>{system_prompt}</|system|>
<|user|>{user_message}</|user|>
<|assistant|>"""
        
        response = self.generate(formatted_prompt, max_tokens)
        return response.split("<|assistant|>")[-1].strip()
    
    def list_available_models(self) -> str:
        """List all available models with system recommendations"""
        output = "\n╔════════════════════════════════════════════════════════════════════════════╗\n"
        output += "║              🤖 AVAILABLE LLM MODELS                                    ║\n"
        output += "╚════════════════════════════════════════════════════════════════════════════╝\n\n"
        
        gpu = SystemDetector.get_gpu_info()
        cpu = SystemDetector.get_cpu_info()
        ram = SystemDetector.get_ram_info()
        
        output += f"🖥️  System Info:\n"
        output += f"   GPU: {'Available (' + gpu['device_name'] + ')' if gpu['available'] else 'None'}\n"
        output += f"   CPU: {cpu['brand']} ({cpu['cores']} cores)\n"
        output += f"   RAM: {ram['available_gb']:.1f}GB available\n\n"
        
        recommended = SystemDetector.recommend_model()
        
        for idx, (model_type, config) in enumerate(MODEL_CONFIGS.items(), 1):
            is_recommended = "✓" if model_type == recommended else " "
            is_current = "●" if self.current_model_type == model_type else "○"
            
            output += f"[{is_recommended}{is_current}] {idx}. {config.model_name}\n"
            output += f"     Role: {config.best_for}\n"
            output += f"     Size: {config.size_gb}GB | Speed: {config.speed_rating} | Quality: {config.quality_rating}\n"
            output += f"     Uncensored: {'Yes ⚡' if config.uncensored else 'No'}\n\n"
        
        return output
    
    def get_current_model_info(self) -> Dict:
        """Get info about currently loaded model"""
        if self.current_model is None:
            return {"status": "No model loaded"}
        
        return {
            "name": self.current_model.model_name,
            "size_gb": self.current_model.size_gb,
            "speed": self.current_model.speed_rating,
            "quality": self.current_model.quality_rating,
            "uncensored": self.current_model.uncensored,
            "device": self.device,
        }


# ═══════════════════════════════════════════════════════════════════════════
# INTERACTIVE CLI FOR MODEL TESTING
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    print("\n╔════════════════════════════════════════════════════════════════════════════╗")
    print("║           Terminal 221B v2.0 - Multi-LLM Engine                         ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    # Initialize engine
    engine = MultiLLMEngine()
    
    # Show available models
    print(engine.list_available_models())
    
    # Detect system and recommend
    recommended = SystemDetector.recommend_model()
    config = MODEL_CONFIGS[recommended]
    print(f"🎯 Recommended Model: {config.model_name}\n")
    
    # Interactive mode
    print("Loading recommended model...\n")
    engine.load_model(recommended)
    
    # Chat loop
    print("💬 Enter 'quit' to exit, 'switch' to change models\n")
    
    system_prompt = """You are a helpful security expert analyzing vulnerabilities.
    Be concise, technical, and actionable in your responses."""
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == "quit":
                print("\nGoodbye! 👋\n")
                break
            elif user_input.lower() == "switch":
                print(engine.list_available_models())
                choice = input("Select model number: ").strip()
                try:
                    model_type = list(MODEL_CONFIGS.keys())[int(choice) - 1]
                    engine.switch_model(model_type)
                except (ValueError, IndexError):
                    print("Invalid choice\n")
                continue
            elif not user_input:
                continue
            
            print(f"\n{engine.current_model.model_name}:")
            response = engine.chat(system_prompt, user_input)
            print(f"{response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋\n")
            break
        except Exception as e:
            print(f"Error: {str(e)}\n")
