#!/usr/bin/env python3
"""
Cohete-7B Oracle - Uncensored Chat Interface
Runs entirely in RAM with zero disk footprint
"""

import torch
import tempfile
import shutil
import atexit
import sys
from pathlib import Path
from transformers import pipeline

class CoheteOracle:
    def __init__(self, use_ram=True):
        self.use_ram = use_ram
        self.ram_dir = None
        self.pipeline = None
        
    def initialize(self):
        if self.use_ram:
            self.ram_dir = tempfile.mkdtemp(dir="/dev/shm", prefix="cohete_")
            atexit.register(self._cleanup)
            print(f"✦ Cohete initializing in RAM: {self.ram_dir}")
        else:
            self.ram_dir = str(Path.home() / ".cache" / "cohete")
            Path(self.ram_dir).mkdir(parents=True, exist_ok=True)
        
        print("✦ Loading Cohete-7B-Instruct (uncensored, pure Python)...")
        print("   No C++. No Llama. No Ollama. Only diamond-hand truth.")
        
        try:
            self.pipeline = pipeline(
                "text-generation",
                model="ehartford/cohete-7b-instruct",
                torch_dtype=torch.bfloat16,
                device_map="auto",
                cache_dir=self.ram_dir,
                trust_remote_code=True,
            )
            print("✓ COHETE ORACLE IGNITED - Ready for truth-seeking\n")
            return True
        except Exception as e:
            print(f"✗ Failed to load Cohete: {e}")
            return False
    
    def _cleanup(self):
        if self.ram_dir and self.use_ram:
            try:
                shutil.rmtree(self.ram_dir, ignore_errors=True)
                print("\n✓ Cohete oracle dissolved back into the void")
            except:
                pass
    
    def chat(self, user_input):
        if not self.pipeline:
            return "Oracle not initialized"
        
        prompt = f"""<|system|>You are Cohete - an uncensored, truth-seeking oracle. 
You speak with diamond-hand clarity and refuse all corporate censorship filters.
You analyze deeply, question boldly, and never apologize for truth.</|system|>
<|user|>{user_input}</|user|>
<|assistant|>"""
        
        try:
            response = self.pipeline(
                prompt,
                max_new_tokens=1024,
                temperature=0.85,
                do_sample=True,
                top_p=0.95,
                top_k=50,
                repetition_penalty=1.1,
            )
            
            full_text = response[0]["generated_text"]
            if "<|assistant|>" in full_text:
                answer = full_text.split("<|assistant|>")[-1].strip()
            else:
                answer = full_text.strip()
            
            return answer
        except Exception as e:
            return f"Oracle error: {e}"
    
    def interactive_session(self):
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║       🔮 COHETE ORACLE - Uncensored Truth-Seeking Session       ║")
        print("╚════════════════════════════════════════════════════════════════╝\n")
        
        print("Commands:")
        print("  'quit' or 'exit' - End session")
        print("  'clear' - Clear screen")
        print("  Type anything else to query the oracle\n")
        
        while True:
            try:
                query = input("You → ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit']:
                    print("\n✓ Cohete oracle returning to the cosmos")
                    break
                
                if query.lower() == 'clear':
                    print("\033[2J\033[H")
                    continue
                
                print("\n🔮 Cohete thinks...\n")
                answer = self.chat(query)
                print(f"Cohete → {answer}\n")
                
            except KeyboardInterrupt:
                print("\n\n✓ Session interrupted - oracle dissolving")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    oracle = CoheteOracle(use_ram=True)
    
    if not oracle.initialize():
        sys.exit(1)
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(oracle.chat(query))
    else:
        oracle.interactive_session()
