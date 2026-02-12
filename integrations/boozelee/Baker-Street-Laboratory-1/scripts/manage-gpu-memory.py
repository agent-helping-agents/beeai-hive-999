#!/usr/bin/env python3
"""
Baker Street Laboratory - GPU Memory Management
Intelligent model loading and unloading for 8GB GTX 1080
"""

import subprocess
import json
import time
import sys
from pathlib import Path

class BakerStreetGPUManager:
    def __init__(self):
        self.gpu_memory_limit = 8192  # 8GB in MB
        self.safety_margin = 1024     # 1GB safety margin
        self.available_memory = self.gpu_memory_limit - self.safety_margin
        
    def get_gpu_usage(self):
        """Get current GPU memory usage"""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                check=True
            )
            
            used, total = map(int, result.stdout.strip().split(', '))
            return used, total
            
        except Exception as e:
            print(f"Error getting GPU usage: {e}")
            return 0, self.gpu_memory_limit
    
    def get_running_ollama_models(self):
        """Get list of currently running Ollama models"""
        try:
            result = subprocess.run(
                ["ollama", "ps"],
                capture_output=True,
                text=True,
                check=True
            )
            
            models = []
            for line in result.stdout.split('\n')[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 1:
                        models.append(parts[0])
            
            return models
            
        except Exception as e:
            print(f"Error getting running models: {e}")
            return []
    
    def stop_model(self, model_name):
        """Stop a specific Ollama model"""
        try:
            subprocess.run(
                ["ollama", "stop", model_name],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ Stopped model: {model_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error stopping {model_name}: {e}")
            return False
    
    def optimize_for_longcontext(self):
        """Optimize GPU memory for long context model"""
        print("🧠 Optimizing GPU memory for baker-street-longcontext...")
        
        # Stop all running models first
        running_models = self.get_running_ollama_models()
        for model in running_models:
            if model != "baker-street-longcontext:latest":
                self.stop_model(model)
        
        # Wait for memory to clear
        time.sleep(3)
        
        used, total = self.get_gpu_usage()
        print(f"📊 GPU Memory: {used}MB used / {total}MB total")
        
        if used < self.available_memory:
            print("✅ Sufficient memory available for long context model")
            return True
        else:
            print("⚠️  Still insufficient memory. Consider using CPU mode.")
            return False
    
    def run_longcontext_cpu_mode(self, prompt):
        """Run long context model in CPU mode as fallback"""
        print("🔄 Running baker-street-longcontext in CPU mode...")
        
        try:
            # Set environment variable to force CPU usage
            env = {"CUDA_VISIBLE_DEVICES": ""}
            
            result = subprocess.run(
                ["ollama", "run", "baker-street-longcontext:latest"],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=60,
                env=env
            )
            
            if result.returncode == 0:
                print("✅ Long context model working in CPU mode")
                return True, result.stdout
            else:
                print(f"❌ CPU mode failed: {result.stderr}")
                return False, result.stderr
                
        except Exception as e:
            print(f"❌ Error in CPU mode: {e}")
            return False, str(e)
    
    def smart_model_rotation(self):
        """Implement smart model rotation based on time of day"""
        from datetime import datetime
        
        hour = datetime.now().hour
        
        # Morning: Long context for research analysis
        if 6 <= hour < 12:
            recommended = "baker-street-longcontext:latest"
        # Afternoon: Vision for document analysis
        elif 12 <= hour < 18:
            recommended = "baker-street-vision:latest"
        # Evening: Creative for report writing
        else:
            recommended = "baker-street-creative:latest"  # When available
        
        print(f"🕐 Time-based recommendation: {recommended}")
        return recommended
    
    def create_memory_config(self):
        """Create optimized memory configuration"""
        config = {
            "gpu_memory_limit_mb": self.gpu_memory_limit,
            "safety_margin_mb": self.safety_margin,
            "model_rotation_schedule": {
                "morning": "baker-street-longcontext:latest",
                "afternoon": "baker-street-vision:latest", 
                "evening": "baker-street-creative:latest"
            },
            "fallback_strategies": {
                "longcontext_cpu": True,
                "model_unloading": True,
                "memory_monitoring": True
            }
        }
        
        config_path = Path("config/gpu_memory_config.json")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"📄 Memory configuration saved to: {config_path}")
        return config

def main():
    """Main GPU management function"""
    print("🎮 BAKER STREET LABORATORY - GPU MEMORY MANAGER")
    print("=" * 50)
    
    manager = BakerStreetGPUManager()
    
    # Show current status
    used, total = manager.get_gpu_usage()
    print(f"📊 Current GPU Usage: {used}MB / {total}MB ({used/total*100:.1f}%)")
    
    running_models = manager.get_running_ollama_models()
    if running_models:
        print(f"🏃 Running Models: {', '.join(running_models)}")
    else:
        print("💤 No models currently running")
    
    # Create optimized configuration
    config = manager.create_memory_config()
    
    # Test long context model optimization
    if manager.optimize_for_longcontext():
        print("✅ GPU optimized for long context processing")
    else:
        print("⚠️  Using CPU fallback for long context model")
        
        # Test CPU mode
        test_prompt = "Test long context processing in CPU mode"
        success, response = manager.run_longcontext_cpu_mode(test_prompt)
        
        if success:
            print("✅ CPU fallback working correctly")
        else:
            print("❌ CPU fallback needs attention")
    
    # Show smart rotation recommendation
    recommended = manager.smart_model_rotation()
    
    print("\n🎭 GPU memory management configured for psychedelic detective research!")

if __name__ == "__main__":
    main()
