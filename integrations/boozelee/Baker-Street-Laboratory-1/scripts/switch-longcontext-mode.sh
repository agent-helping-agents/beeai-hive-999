#!/bin/bash
# Baker Street Laboratory - Model Switching Script

echo "🎭 BAKER STREET LABORATORY - MODEL SWITCHER"
echo "=========================================="

case "$1" in
    "gpu")
        echo "🎮 Switching to GPU mode (if available)..."
        export CUDA_VISIBLE_DEVICES=0
        echo "Using baker-street-longcontext:latest"
        ;;
    "cpu")
        echo "🖥️  Switching to CPU mode..."
        export CUDA_VISIBLE_DEVICES=""
        echo "Using baker-street-longcontext-cpu"
        ;;
    "auto")
        echo "🤖 Auto-detecting best mode..."
        GPU_MEM=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)
        if [ "$GPU_MEM" -gt 7000 ]; then
            echo "✅ Sufficient GPU memory available: ${GPU_MEM}MB"
            echo "Using GPU mode"
            export CUDA_VISIBLE_DEVICES=0
        else
            echo "⚠️  Limited GPU memory: ${GPU_MEM}MB"
            echo "Using CPU mode"
            export CUDA_VISIBLE_DEVICES=""
        fi
        ;;
    *)
        echo "Usage: $0 {gpu|cpu|auto}"
        echo "  gpu  - Force GPU mode"
        echo "  cpu  - Force CPU mode"  
        echo "  auto - Auto-detect best mode"
        exit 1
        ;;
esac

echo "🎭 Model switching complete!"
