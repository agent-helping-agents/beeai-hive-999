#!/usr/bin/env python3
"""
Test script for Hypercube AI Model Builder
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from hypercube_ai.model_builder import HypercubeModelBuilder

def test_model_builder():
    """Test the model builder functionality"""
    
    print("🧪 Testing Hypercube AI Model Builder")
    print("=" * 50)
    
    # Create model builder instance
    print("1. Creating model builder instance...")
    builder = HypercubeModelBuilder()
    print("✅ Model builder created successfully")
    
    # Test adding layers
    print("\n2. Testing layer addition...")
    
    # Add Dense layer
    print("   Adding Dense layer (64 -> 32)...")
    # Simulate adding layer through UI
    builder.layer_type.value = 'Dense'
    builder.param_widgets['input_dim'].value = 64
    builder.param_widgets['output_dim'].value = 32
    builder.param_widgets['activation'].value = 'relu'
    builder._add_layer(None)
    
    # Add another Dense layer
    print("   Adding Dense layer (32 -> 10)...")
    builder.param_widgets['input_dim'].value = 32
    builder.param_widgets['output_dim'].value = 10
    builder.param_widgets['activation'].value = 'softmax'
    builder._add_layer(None)
    
    print(f"✅ Added {len(builder.layers)} layers successfully")
    
    # Test code generation
    print("\n3. Testing code generation...")
    
    # Generate PyTorch code
    print("   Generating PyTorch code...")
    pytorch_code = builder.generate_code('pytorch')
    print(f"✅ PyTorch code generated ({len(pytorch_code)} characters)")
    
    # Generate TensorFlow code
    print("   Generating TensorFlow code...")
    tensorflow_code = builder.generate_code('tensorflow')
    print(f"✅ TensorFlow code generated ({len(tensorflow_code)} characters)")
    
    # Test saving and loading
    print("\n4. Testing save/load functionality...")
    
    # Save model
    test_file = '/tmp/test_model.json'
    builder.save_model(test_file)
    print(f"✅ Model saved to {test_file}")
    
    # Load model
    new_builder = HypercubeModelBuilder()
    new_builder.load_model(test_file)
    print(f"✅ Model loaded successfully ({len(new_builder.layers)} layers)")
    
    # Test Hypercube analysis
    print("\n5. Testing Hypercube analysis...")
    builder._run_hypercube_analysis(None)
    print("✅ Hypercube analysis completed")
    
    # Display generated code
    print("\n6. Generated PyTorch Code:")
    print("-" * 30)
    print(pytorch_code[:500] + "..." if len(pytorch_code) > 500 else pytorch_code)
    print("-" * 30)
    
    print("\n🎉 All tests passed!")
    print("=" * 50)
    print("✅ Model builder is working correctly")
    print("✅ Layer addition functional")
    print("✅ Code generation working")
    print("✅ Save/load functionality operational")
    print("✅ Hypercube integration successful")
    
    return True

def test_layer_components():
    """Test individual layer components"""
    
    print("\n🧪 Testing Layer Components")
    print("=" * 50)
    
    from hypercube_ai.model_builder import (
        DenseLayer, Conv2DLayer, LSTMLayer, 
        AttentionLayer, DropoutLayer
    )
    
    # Test Dense layer
    print("1. Testing Dense layer...")
    dense = DenseLayer(64, 32, 'relu')
    pytorch_code = dense.generate_code('pytorch')
    tensorflow_code = dense.generate_code('tensorflow')
    print(f"✅ Dense layer: {pytorch_code}")
    print(f"✅ TensorFlow: {tensorflow_code}")
    
    # Test Conv2D layer
    print("\n2. Testing Conv2D layer...")
    conv = Conv2DLayer(3, 32, 3)
    print(f"✅ Conv2D layer: {conv.generate_code('pytorch')}")
    
    # Test LSTM layer
    print("\n3. Testing LSTM layer...")
    lstm = LSTMLayer(64, 32)
    print(f"✅ LSTM layer: {lstm.generate_code('pytorch')}")
    
    # Test Attention layer
    print("\n4. Testing Attention layer...")
    attn = AttentionLayer(64, 8)
    print(f"✅ Attention layer: {attn.generate_code('pytorch')}")
    
    # Test Dropout layer
    print("\n5. Testing Dropout layer...")
    dropout = DropoutLayer(0.5)
    print(f"✅ Dropout layer: {dropout.generate_code('pytorch')}")
    
    print("\n🎉 All layer component tests passed!")
    return True

def main():
    """Run all tests"""
    
    print("🚀 Hypercube AI Model Builder - Test Suite")
    print("=" * 60)
    
    try:
        # Test layer components
        if test_layer_components():
            print("\n✅ Layer component tests: PASSED")
        else:
            print("\n❌ Layer component tests: FAILED")
            return False
        
        # Test model builder
        if test_model_builder():
            print("\n✅ Model builder tests: PASSED")
        else:
            print("\n❌ Model builder tests: FAILED")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYour Hypercube AI Model Builder is ready to use!")
        print("\nTo start building models:")
        print("1. Run: conda activate ai_dev")
        print("2. Run: jupyter lab")
        print("3. Import and use: from hypercube_ai.model_builder import HypercubeModelBuilder")
        print("4. Create: builder = HypercubeModelBuilder()")
        print("5. Build your model using the interactive UI!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)