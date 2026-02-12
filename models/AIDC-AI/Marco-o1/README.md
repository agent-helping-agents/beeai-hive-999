---
license: apache-2.0
library_name: transformers
inference: false
---
<p align="center">
    <img src="assets/logo.png" width="150" style="margin-bottom: 0.2;"/>

<p>

# 🍓 Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions

<!-- Broader Real-World Applications -->

<!-- # 🍓 Marco-o1: An Open Large Reasoning Model for Real-World Solutions -->

<!-- <h2 align="center"> <a href="https://github.com/AIDC-AI/Marco-o1/">Marco-o1</a></h2> -->
<!-- <h5 align="center"> If you appreciate our project, please consider giving us a star ⭐ on GitHub to stay updated with the latest developments.  </h2> -->
 

<div align="center">

<!-- **Affiliations:** -->

⭐ _**MarcoPolo Team**_ ⭐

[_**AI Business, Alibaba International Digital Commerce**_](https://aidc-ai.com)

[**Github**](https://github.com/AIDC-AI/Marco-o1)  🤗  [**Hugging Face**](https://huggingface.co/AIDC-AI/Marco-o1) 📝  [**Paper**](https://arxiv.org/abs/2411.14405) 🧑‍💻 [**Model**](https://huggingface.co/AIDC-AI/Marco-o1) 🗂️  [**Data**](https://github.com/AIDC-AI/Marco-o1/tree/main/data) 📽️  [**Demo**](https://huggingface.co/AIDC-AI/Marco-o1)

</div>

🎯 **Marco-o1** not only focuses on disciplines with standard answers, such as mathematics, physics, and coding—which are well-suited for reinforcement learning (RL)—but also places greater emphasis on **open-ended resolutions**. We aim to address the question: _"Can the o1 model effectively generalize to broader domains where clear standards are absent and rewards are challenging to quantify?"_

Currently, Marco-o1 Large Language Model (LLM) is powered by _Chain-of-Thought (CoT) fine-tuning_, _Monte Carlo Tree Search (MCTS)_, _reflection mechanisms_, and _innovative reasoning strategies_—optimized for complex real-world problem-solving tasks. 

⚠️ **Limitations:** <ins>We would like to emphasize that this research work is inspired by OpenAI's o1 (from which the name is also derived). This work aims to explore potential approaches to shed light on the currently unclear technical roadmap for large reasoning models. Besides, our focus is on open-ended questions, and we have observed interesting phenomena in multilingual applications. However, we must acknowledge that the current model primarily exhibits o1-like reasoning characteristics and its performance still fall short of a fully realized "o1" model. This is not a one-time effort, and we remain committed to continuous optimization and ongoing improvement.</ins>

![img.png](assets/img.png)

## 🚀 Highlights
Currently, our work is distinguished by the following highlights:

- 🍀 Fine-Tuning with CoT Data: We develop Marco-o1-CoT by performing full-parameter fine-tuning on the base model using open-source CoT dataset combined with our self-developed synthetic data.
- 🍀 Solution Space Expansion via MCTS: We integrate LLMs with MCTS (Marco-o1-MCTS), using the model's output confidence to guide the search and expand the solution space.
- 🍀 Reasoning Action Strategy: We implement novel reasoning action strategies and a reflection mechanism (Marco-o1-MCTS Mini-Step), including exploring different action granularities within the MCTS framework and prompting the model to self-reflect, thereby significantly enhancing the model's ability to solve complex problems.
- 🍀 Application in Translation Tasks: We are the first to apply Large Reasoning Models (LRM) to Machine Translation task, exploring inference time scaling laws in the multilingual and translation domain.

OpenAI recently introduced the groundbreaking o1 model, renowned for its exceptional reasoning capabilities. This model has demonstrated outstanding performance on platforms such as AIME, CodeForces, surpassing other leading models. Inspired by this success, we aimed to push the boundaries of LLMs even further, enhancing their reasoning abilities to tackle complex, real-world challenges.

🌍 Marco-o1 leverages advanced techniques like CoT fine-tuning, MCTS, and Reasoning Action Strategies to enhance its reasoning power. As shown in Figure 2, by fine-tuning Qwen2-7B-Instruct with a combination of the filtered Open-O1 CoT dataset, Marco-o1 CoT dataset, and Marco-o1 Instruction dataset, Marco-o1 improved its handling of complex tasks. MCTS allows exploration of multiple reasoning paths using confidence scores derived from softmax-applied log probabilities of the top-k alternative tokens, guiding the model to optimal solutions. Moreover, our reasoning action strategy involves varying the granularity of actions within steps and mini-steps to optimize search efficiency and accuracy.

<div align="center">
  <img src="assets/intro_2.jpg" alt="Figure Description or Alt Text" width="80%">
  <p><strong>Figure 2: </strong>The overview of Marco-o1.</p>
</div>

🌏 As shown in Figure 3, Marco-o1 achieved accuracy improvements of +6.17% on the MGSM (English) dataset and +5.60% on the MGSM (Chinese) dataset, showcasing enhanced reasoning capabilities. 

<div align="center">
  <img src="assets/results.jpg" alt="Figure Description or Alt Text" width="80%">
  <p><strong>Figure 3: </strong>The main results of Marco-o1.</p>
</div>

🌎 Additionally, in translation tasks, we demonstrate that Marco-o1 excels in translating slang expressions, such as translating "这个鞋拥有踩屎感" (literal translation: "This shoe offers a stepping-on-poop sensation.") to "This shoe has a comfortable sole," demonstrating its superior grasp of colloquial nuances.

<div align="center">
  <img src="assets/translation.jpg" alt="Figure Description or Alt Text" width="80%">
  <p><strong>Figure 4: </strong>The demostration of translation task using Marco-o1.</p>
</div>

For more information,please visit our [**Github**](https://github.com/AIDC-AI/Marco-o1).

## Usage

1. **Load Marco-o1-CoT model:** 
    ```
    # Load model directly
    from transformers import AutoTokenizer, AutoModelForCausalLM

    tokenizer = AutoTokenizer.from_pretrained("AIDC-AI/Marco-o1")
    model = AutoModelForCausalLM.from_pretrained("AIDC-AI/Marco-o1")
    ```

2. **Inference:** 

    Execute the inference script (you can give any customized inputs inside):
    ```
    ./src/talk_with_model.py

    # Use vLLM
    ./src/talk_with_model_vllm.py

    ```


# 👨🏻‍💻 Acknowledgement

## Main Contributors
From MarcoPolo Team, AI Business, Alibaba International Digital Commerce:
- Yu Zhao
- [Huifeng Yin](https://github.com/HuifengYin)
- Hao Wang
- [Longyue Wang](http://www.longyuewang.com)

## Citation

If you find Marco-o1 useful for your research and applications, please cite:

```
@misc{zhao2024marcoo1openreasoningmodels,
      title={Marco-o1: Towards Open Reasoning Models for Open-Ended Solutions}, 
      author={Yu Zhao and Huifeng Yin and Bo Zeng and Hao Wang and Tianqi Shi and Chenyang Lyu and Longyue Wang and Weihua Luo and Kaifu Zhang},
      year={2024},
      eprint={2411.14405},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2411.14405}, 
}
```

## LICENSE

This project is licensed under [Apache License Version 2](https://huggingface.co/datasets/choosealicense/licenses/blob/main/markdown/apache-2.0.md) (SPDX-License-identifier: Apache-2.0).

## DISCLAIMER

We used compliance checking algorithms during the training process, to ensure the compliance of the trained model and dataset to the best of our ability. Due to complex data and the diversity of language model usage scenarios, we cannot guarantee that the model is completely free of copyright issues or improper content. If you believe anything infringes on your rights or generates improper content, please contact us, and we will promptly address the matter.