"""Idempotently merge AI/ML + semiconductor terms into Targets/AI/Resources/glossary.json.

Mirrors scripts/add_basics.py — append-only, case-insensitive dedup against
existing terms, sort by (letter asc, term asc) on write. Each batch is a
Python list of entries built via the entry() helper, which enforces the
category + indication enums so we don't accidentally drift away from the
lenses defined in Targets/AI/AIBrand.swift.

Voice: plain English suitable for a generalist (Bloomberg-reader, journalist,
finance/PM person). Snappy line should make sense WITHOUT prior ML knowledge;
detail anchors with product/lab/model names where possible.

Usage:
    python scripts/add_ai_terms.py
    python scripts/add_ai_terms.py --batches 1,2     # run specific batches
    python scripts/add_ai_terms.py --dry-run         # preview without writing
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

GLOSSARY = Path(__file__).parent.parent / "Targets" / "AI" / "Resources" / "glossary.json"

# Keep in sync with Targets/AI/AIBrand.swift `lenses[].kind` category lists.
VALID_CATEGORIES = {
    # Frontier-lens
    "Architecture", "Training", "Inference", "Eval", "Alignment",
    "Research", "Concepts", "Frontier", "Models", "Agents",
    # Hardware-lens
    "Hardware", "Manufacturing", "Memory", "Interconnect", "Packaging",
    "Software", "Infrastructure",
    # Off-lens (appears only via alphabet/search/filter)
    "Industry", "Regulation", "Company",
}

VALID_INDICATIONS = {
    "General", "NLP", "Vision", "Audio", "Multimodal", "RL", "Robotics",
    "Research", "Compute", "Training", "Inference", "Safety", "Frontier",
}


def entry(term, full, snappy, detail, sources, indications=None, category="Concepts"):
    assert category in VALID_CATEGORIES, f"Unknown category '{category}' for term '{term}'"
    indications = indications or ["General"]
    for ind in indications:
        assert ind in VALID_INDICATIONS, f"Unknown indication '{ind}' for term '{term}'"
    return {
        "letter": term[0].upper(),
        "term": term,
        "full": full,
        "snappy": snappy,
        "detail": detail,
        "indications": indications,
        "category": category,
        "sources": sources,
    }


# ============================================================================
# BATCH 1 — Core architectures + tokens (25 terms, plain-English register)
# ============================================================================

BATCH_ARCHITECTURES = [
    entry(
        "Attention", "",
        "How a model decides which parts of the input matter most for what it's about to produce.",
        "Originally introduced in 2014 to fix a bottleneck in translation models, attention lets a network decide on the fly which parts of the input to look at, rather than processing them in a fixed order. The 2017 paper \"Attention Is All You Need\" showed that this trick alone — without the older sequential machinery — could match or beat the state of the art, kicking off the Transformer era that powers ChatGPT, Claude, and Gemini.",
        ["Vaswani 2017"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Self-attention", "",
        "Attention used within a single piece of text — every word looks at every other word in the same input.",
        "Self-attention lets every word in a sequence consider every other word in the same sequence, all in one pass. This is what makes Transformers fast to train: they can process a whole sentence in parallel, instead of one word at a time like the older recurrent networks they replaced. It's the engine inside every modern large language model.",
        ["Vaswani 2017"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Multi-head attention", "",
        "Several attention operations running in parallel, each learning to spot a different kind of pattern.",
        "Instead of one attention pass, the model runs several at once with separate parameters. One head might track who-did-what; another might pick up rhyming patterns; another might handle long-range references. Frontier models use anywhere from 32 to 128 heads per layer. Recent variants — grouped-query attention, multi-query attention — share information across heads to cut inference cost.",
        ["Vaswani 2017"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Encoder", "",
        "The part of a model that reads the whole input upfront and prepares it for further processing.",
        "Encoders work bidirectionally — every word can see every other word — making them well-suited to understanding tasks like classification and search. BERT, Google's 2018 model that became the foundation for search ranking, is encoder-only. In encoder-decoder models like T5 or the original Transformer, the encoder digests the input before handing off to a decoder that writes the output.",
        ["Google DeepMind", "Vaswani 2017"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Decoder", "",
        "The part of a model that writes its output one word at a time, each word built on what's come before.",
        "Decoders can only look backward, never forward — necessary for left-to-right generation. Today's chatbots (ChatGPT, Claude, Gemini, Llama, Grok) are all decoder-only Transformers; they've absorbed the encoder's job into a single stack. This makes them simpler to train at scale and is one reason the decoder-only architecture has dominated since GPT-3.",
        ["OpenAI"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Encoder-decoder", "",
        "Two-part design where one network reads the input and another writes the output.",
        "The original 2017 Transformer was encoder-decoder, built for translation. Modern translation models, summarisers, and speech recognisers (Whisper from OpenAI) still use this shape because the input-to-output mapping is clear. Decoder-only models have taken over chat and writing assistants, where the boundary between reading and writing is blurrier.",
        ["Vaswani 2017", "OpenAI"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Mixture of Experts", "MoE",
        "Architecture that splits a model into many sub-networks and only activates a few of them for each input.",
        "MoE separates a model's total capacity (large) from its per-question compute cost (small). A router picks, say, 2 out of 64 experts for each word, so a 400-billion-parameter model might only fire 40 billion at a time. Mixtral, DeepSeek-V3, and (reportedly) GPT-4 all use MoE to grow capacity without proportionally growing inference cost.",
        ["Mistral", "DeepSeek"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Sparse MoE", "",
        "The standard form of MoE today — for any given input, only a handful of the model's experts wake up.",
        "Contrasted with a \"dense\" version where every expert sees every input (rarely used in practice). The sparse routing has to be balanced carefully — otherwise a few experts get all the work and the rest never train. Google's Switch Transformer (2021) and GShard worked out the practical engineering. The payoff is dramatic: roughly 8× more capacity for the same inference cost.",
        ["Google DeepMind"],
        indications=["Research"],
        category="Architecture",
    ),
    entry(
        "Diffusion model", "",
        "Generative model that learns to turn random static into a real-looking image by removing noise step by step.",
        "Training works by taking an image, adding random noise until it's pure static, and teaching the model to reverse one step of that process. At generation time, the model starts from noise and denoises iteratively to produce a fresh image. DALL-E 3, Stable Diffusion, Flux, Midjourney, and OpenAI's video model Sora all work this way. Diffusion is now spreading to audio, video, and even text.",
        ["OpenAI", "Stability AI"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "Latent diffusion", "",
        "Diffusion that works on a compressed version of the image instead of raw pixels — much faster, almost no quality loss.",
        "A small autoencoder first compresses a 512×512 image down to a 64×64 mini-representation. Diffusion runs there, and the autoencoder expands it back to pixels at the end. The compute saving is 50× or more. Stable Diffusion's breakthrough was making this approach practical at consumer scale; almost every image generator since copies the trick.",
        ["Stability AI"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "Variational autoencoder", "VAE",
        "Model that learns to squeeze data down to a small code and reconstruct it — the workhorse compressor inside many image generators.",
        "VAEs are trained to compress and rebuild data, with the constraint that the compressed code lives in a smooth, well-behaved space you can sample from. By themselves they produce slightly blurry samples. But they're now essential infrastructure inside latent diffusion: the part that turns pixels into compressed representations before diffusion, and back again afterwards.",
        ["Stanford CRFM"],
        indications=["Research"],
        category="Architecture",
    ),
    entry(
        "Generative adversarial network", "GAN",
        "Two networks playing a game: one makes fake samples, the other tries to spot them. Both get better.",
        "Goodfellow and co-authors introduced GANs in 2014 and launched the modern generative-modelling era. StyleGAN dominated face generation in the late 2010s — those uncanny \"this person does not exist\" galleries. Training was famously brittle: modes would collapse, networks would diverge. Diffusion has largely replaced GANs at the frontier, but GANs still win on speed: one shot instead of many denoising steps.",
        ["NVIDIA"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "Recurrent neural network", "RNN",
        "Older type of language network that reads a sequence one word at a time, carrying a running memory between steps.",
        "RNNs dominated translation, speech recognition, and language modelling pre-2017. Their core weakness is that they have to process one word before the next — you can't parallelise across time — so training is slow on long sequences. Transformers replaced them for most tasks. State space models like Mamba are bringing some RNN-like ideas back, with a twist that makes them parallelisable.",
        ["Stanford CRFM"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "LSTM", "Long Short-Term Memory",
        "Improved RNN with built-in machinery for remembering things across long sequences — the workhorse of language AI before Transformers.",
        "Introduced in 1997 by Hochreiter and Schmidhuber, dominant for sequence tasks through the 2010s. The trick is a small set of internal switches that decide what to keep in memory, what to drop, and what to pass on at each step. Google Translate ran on LSTMs in production before the Transformer takeover, and LSTMs are still useful when memory and compute are tight — for example on phones.",
        ["Stanford CRFM"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Convolutional neural network", "CNN",
        "Type of network built for images — it slides small pattern detectors across the input to pick up local features.",
        "CNNs dominated computer vision from AlexNet (2012) through the late 2010s — face recognition, object detection, image classification. They're naturally suited to images because the same small filter can find an edge or a texture anywhere in the picture. Vision Transformers have since matched or beaten them on most benchmarks, but CNNs are still the default for vision on phones and small chips.",
        ["NVIDIA"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "ResNet", "Residual Network",
        "A trick that made it practical to train very deep networks — adds shortcut connections so signal can skip past layers.",
        "Before ResNets (Microsoft Research, 2015), deeper networks paradoxically performed worse than shallower ones. Adding identity shortcuts solved this and unlocked 100-plus-layer networks. The residual idea — add the input to the layer's output — is now everywhere: every Transformer block uses it. One of the most-copied design patterns in modern deep learning.",
        ["Meta AI / FAIR"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "U-Net", "",
        "Image-to-image network shaped like a U — compresses the picture down, then expands it back up.",
        "Designed for biomedical image segmentation in 2015. The encoder downsamples, the decoder upsamples, and shortcut connections pass high-resolution detail across the U. U-Net is now the workhorse of diffusion models — Stable Diffusion's denoising network is a U-Net — making it one of the most-used architectures by FLOP-hours in the world.",
        ["Stability AI"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "Vision Transformer", "ViT",
        "Transformer applied to images by chopping them into small patches and treating each patch like a word.",
        "Introduced by Google in 2020. Split an image into 16×16 patches, project each into an embedding, then run a standard Transformer encoder. ViTs match or beat CNNs at scale, especially when pretrained on enormous datasets. The architecture underpins modern vision-language models — CLIP, GPT-4o's vision capability, Gemini's image understanding — and most image generators.",
        ["Google DeepMind"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "CLIP", "Contrastive Language-Image Pretraining",
        "Model that links images and text in a shared space — lets you search images by description, or steer image generators with words.",
        "OpenAI's 2021 CLIP trained a vision network and a text network side-by-side on 400 million image-caption pairs, with a loss that pulls matching pairs together and pushes mismatched pairs apart. The resulting shared space enables zero-shot image classification, text-based search, and prompt conditioning for image generators (Stable Diffusion uses CLIP for the text input).",
        ["OpenAI"],
        indications=["Multimodal", "Research"],
        category="Architecture",
    ),
    entry(
        "Mamba", "",
        "Newer alternative to Transformers, designed for very long inputs — runs in linear time instead of quadratic.",
        "Released late 2023 by Gu and Dao. Mamba builds on \"state space models\": it keeps a compact rolling memory of the sequence so far, updated linearly per token. Its appeal is long-context efficiency — promising for tasks where Transformers' quadratic attention is prohibitive (long documents, video). Decoder-only Transformers remain dominant for general LLMs, but Mamba and its descendants are the leading alternative.",
        ["Stanford CRFM"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Token", "",
        "The atomic unit a language model reads or writes — usually a word fragment of 3–4 characters, not a full word.",
        "Models don't see characters or words directly; text is first split into tokens by a tokeniser. Common words like \"the\" become a single token; rare or compound words split into several. Context window is measured in tokens, API pricing is per-token, and a model's vocabulary size (typically 32k–256k) is the number of distinct tokens it knows.",
        ["OpenAI"],
        indications=["NLP"],
        category="Concepts",
    ),
    entry(
        "Tokenization", "",
        "Splitting text into tokens — the first preprocessing step before any model can read anything.",
        "Modern LLMs use subword tokenisers — algorithms that produce tokens shorter than words but longer than letters — balancing vocabulary size against token length. The tokeniser is part of the model contract: GPT-4 tokens and Llama tokens aren't interchangeable. Tokenisation quirks cause many oddities: weak arithmetic, struggles with character-level tasks, sensitivity to whitespace.",
        ["OpenAI"],
        indications=["NLP"],
        category="Concepts",
    ),
    entry(
        "Byte-Pair Encoding", "BPE",
        "Common tokeniser training method — starts with single characters and repeatedly merges the most frequent pair into a new token.",
        "Begin with single bytes as the token vocabulary. Find the most common adjacent pair, glue them together into a new token. Repeat until you hit the target vocabulary size. GPT, Llama, and Mistral all use BPE variants. Its strength is simplicity and coverage: any input, in any language or alphabet, can be tokenised.",
        ["OpenAI"],
        indications=["NLP"],
        category="Concepts",
    ),
    entry(
        "Context window", "",
        "The maximum amount of text a model can hold in mind at once, measured in tokens.",
        "Bounded by attention's quadratic memory cost. Early GPT models had 2,000–4,000-token windows; GPT-4 expanded to 128,000; Claude 3.5 to 200,000; Gemini 1.5 to 1 million-plus. Longer windows let you stuff more context (whole books, long codebases) but inference cost rises with window length, and models often struggle to use very long contexts evenly — the \"lost in the middle\" effect.",
        ["Anthropic", "OpenAI"],
        indications=["NLP"],
        category="Concepts",
    ),
    entry(
        "Positional encoding", "",
        "Extra information added to each token so the model knows where it sits in the sequence — Transformers have no built-in sense of word order.",
        "Without positional encoding a Transformer would see \"dog bites man\" and \"man bites dog\" as the same input. The original 2017 design used fixed sine-wave patterns. Modern models prefer learned variants like RoPE (rotary, used by Llama and GPT-NeoX) or ALiBi (linear bias, used by MPT). The choice affects how well a model generalises to longer contexts than it was trained on.",
        ["Meta AI / FAIR"],
        indications=["Research"],
        category="Architecture",
    ),
]


# ============================================================================
# BATCH 2 — Training + fine-tuning + alignment (25 terms)
# ============================================================================

BATCH_TRAINING_ALIGNMENT = [
    entry(
        "Pretraining", "",
        "The first big training phase where a model learns general language from huge amounts of internet text.",
        "A frontier LLM is first pretrained on trillions of tokens of text scraped from the internet — books, code, scientific papers, web pages. The model learns to predict the next word, which forces it to absorb grammar, facts, and patterns of reasoning. Pretraining is the most expensive step (millions of GPU-hours, hundreds of millions of dollars at the frontier) and produces the \"base model\" before any alignment work.",
        ["OpenAI"],
        indications=["Training", "NLP"],
        category="Training",
    ),
    entry(
        "Fine-tuning", "",
        "Taking a pretrained model and adjusting it for a specific task, style, or behavior.",
        "After pretraining, models are fine-tuned to be useful for chat, follow instructions, or specialise in domains like medicine or coding. Fine-tuning is much cheaper than pretraining — hundreds or thousands of examples rather than billions — but it shapes a model's personality and competence at specific tasks. Most consumer LLMs you interact with (ChatGPT, Claude, Gemini) are fine-tuned versions of underlying base models.",
        ["OpenAI", "Anthropic"],
        indications=["Training"],
        category="Training",
    ),
    entry(
        "Gradient descent", "",
        "The basic recipe for training neural networks — repeatedly nudge each parameter in the direction that reduces error.",
        "Start with random parameters. Show the model an example. Measure how wrong its prediction is. Calculate which way each parameter should move to reduce the error. Take a tiny step in that direction. Repeat billions of times. Every modern AI model — language, vision, robotics — is trained this way. Variants like SGD and Adam tweak the recipe for speed and stability.",
        ["Stanford CRFM"],
        indications=["Training", "Research"],
        category="Training",
    ),
    entry(
        "Backpropagation", "",
        "The algorithm that figures out how much each parameter in a deep network contributed to the error.",
        "Without backprop, training deep networks is impossible. The trick is to use calculus's chain rule to propagate the error signal backward from the output through every layer, computing a gradient for each parameter. Introduced in the 1980s but only became practical for large networks once GPUs made the linear algebra fast enough. Every training run of every modern AI model runs backprop on every batch.",
        ["Stanford CRFM"],
        indications=["Training", "Research"],
        category="Training",
    ),
    entry(
        "Loss function", "",
        "The formula a model uses to measure how wrong it is — what training tries to minimise.",
        "Different tasks use different losses: cross-entropy for language and classification, mean squared error for regression, contrastive losses for similarity learning. The choice of loss is one of the most important design decisions in ML — it defines what \"good\" means for the model. RLHF replaces a hand-coded loss with a learned reward model trained on human preferences.",
        ["Stanford CRFM"],
        indications=["Training"],
        category="Training",
    ),
    entry(
        "Batch", "",
        "A group of examples processed together in one training step — much more efficient than doing them one at a time.",
        "Modern GPUs are designed for parallel computation; processing one example at a time would waste most of their capacity. A batch is a stack of (say) 32, 256, or 1024 examples fed through together. Larger batches make training more stable but require more memory. Frontier models often combine \"micro-batches\" with gradient accumulation to fit huge effective batch sizes into limited GPU memory.",
        ["NVIDIA"],
        indications=["Training", "Compute"],
        category="Training",
    ),
    entry(
        "Epoch", "",
        "One full pass through the training dataset — sometimes models train for many, sometimes less than one.",
        "If your dataset has 1 million examples, one epoch means showing the model all 1 million once. Image models traditionally trained for 100+ epochs. Modern LLMs, with datasets in the trillions of tokens, often train for less than one epoch — they see most of the data only once. The shift came as both data and model size scaled up: with enough data, you don't need to revisit it.",
        ["OpenAI"],
        indications=["Training"],
        category="Training",
    ),
    entry(
        "Learning rate", "",
        "The size of each step gradient descent takes — too big and training diverges, too small and it never finishes.",
        "The single most important hyperparameter in deep learning training. Modern setups use a \"learning rate schedule\" that varies the rate over the course of training: a brief warmup phase at the start, then a peak, then a slow decay (often cosine-shaped) toward zero. Get the schedule wrong and even a perfect dataset won't save you.",
        ["NVIDIA"],
        indications=["Training"],
        category="Training",
    ),
    entry(
        "Adam", "Adaptive Moment Estimation",
        "The standard optimizer used to train almost every modern neural network.",
        "Adam tracks both the running average of gradients and their variance, then uses both to adapt the step size per parameter. AdamW, a small variation that handles regularisation cleanly, is the current default for LLM training. Introduced in 2014 and never seriously displaced — competitors like Adafactor and Lion exist but Adam/AdamW remains the safe choice.",
        ["Google DeepMind"],
        indications=["Training", "Research"],
        category="Training",
    ),
    entry(
        "Layer normalization", "",
        "A technique that stabilises training by rescaling the values flowing through each layer.",
        "Without layer norm (or its cousin batch norm), training deep networks is much harder — values can explode or vanish as they propagate through layers. Modern Transformers place layer norm in two spots per block (\"pre-norm\" placement is now standard). It's a small addition with an outsize stabilising effect, especially for the very large networks of modern LLMs.",
        ["Stanford CRFM"],
        indications=["Training", "Research"],
        category="Training",
    ),
    entry(
        "Supervised fine-tuning", "SFT",
        "Fine-tuning a pretrained model on labeled examples of what the right answer looks like.",
        "SFT is typically the first step after pretraining. For a chat model, that means hundreds of thousands of human-written example conversations: prompt, ideal response. The model learns the format and style of helpful responses. SFT alone produces decent chatbots but leaves them prone to confident errors and unhelpful refusals — that's why RLHF or its alternatives come next.",
        ["OpenAI", "Anthropic"],
        indications=["Training", "Safety"],
        category="Alignment",
    ),
    entry(
        "Instruction tuning", "",
        "Fine-tuning a model specifically to follow instructions phrased as natural-language requests.",
        "Pioneered by Google's FLAN and OpenAI's InstructGPT — the model that became ChatGPT. The training data is a large collection of (instruction, response) pairs covering hundreds of task types: summarise this, translate that, answer this question. Instruction-tuned models follow prompts more reliably and respond well to zero-shot requests they've never seen before.",
        ["OpenAI", "Google DeepMind"],
        indications=["Training", "Safety"],
        category="Alignment",
    ),
    entry(
        "RLHF", "Reinforcement Learning from Human Feedback",
        "Training technique where humans rate model outputs and the model learns to produce more of what's rated higher.",
        "First show humans pairs of responses to the same prompt and ask which they prefer. Train a reward model on those preferences. Then use reinforcement learning to nudge the language model toward higher reward. RLHF was the key step that turned GPT-3 into ChatGPT and underlies most consumer-grade LLMs. It's also where alignment researchers focus on bugs like reward hacking and sycophancy.",
        ["OpenAI", "Anthropic"],
        indications=["Safety", "Training"],
        category="Alignment",
    ),
    entry(
        "RLAIF", "Reinforcement Learning from AI Feedback",
        "RLHF variant where AI judges, not humans, score model outputs — much cheaper, almost as good.",
        "Human feedback is slow and expensive. RLAIF replaces some or all human raters with another AI model — typically a strong existing model used to rate or rank outputs. Anthropic's Constitutional AI is one form of RLAIF: the model critiques its own outputs against a written list of principles. Cheaper to scale, with the trade-off that you inherit whatever blind spots the judge model has.",
        ["Anthropic"],
        indications=["Safety", "Training"],
        category="Alignment",
    ),
    entry(
        "DPO", "Direct Preference Optimization",
        "Simpler alternative to RLHF that skips the explicit reward model — just adjusts the model directly from preference data.",
        "RLHF is complex: train reward model, then run reinforcement learning on top. DPO collapses this into a single supervised loss that pushes the model toward preferred responses and away from rejected ones. Released by Stanford in 2023 and quickly adopted across the industry — Mistral, Meta, and many open-source projects use DPO instead of full RLHF. Often gets comparable results with much less engineering complexity.",
        ["Stanford CRFM", "Mistral"],
        indications=["Safety", "Training"],
        category="Alignment",
    ),
    entry(
        "Constitutional AI", "",
        "Anthropic's approach to alignment — the model is shown a written list of principles and trained to critique itself against them.",
        "Instead of asking humans to rate every response, the model is given a \"constitution\" — a list of principles like \"be helpful\", \"don't help with harm\", \"avoid stereotypes\". The model generates a response, then critiques and rewrites it against those principles. Used to train Claude. The aim is to make alignment more transparent (the principles are written down) and scalable (humans don't need to rate every output).",
        ["Anthropic"],
        indications=["Safety"],
        category="Alignment",
    ),
    entry(
        "Reward model", "",
        "A small AI model trained to predict what humans would prefer — used to score outputs during RLHF.",
        "Take pairs of model responses, ask humans which is better, train a model to predict those preferences. The reward model becomes a stand-in for human judgment during the RL phase, scoring each new output. Quality of the reward model is a major bottleneck on RLHF — a biased reward model bakes its biases into the final language model and is the main source of \"reward hacking\" failures.",
        ["OpenAI", "Anthropic"],
        indications=["Safety", "Training"],
        category="Alignment",
    ),
    entry(
        "PPO", "Proximal Policy Optimization",
        "The reinforcement learning algorithm used inside RLHF — keeps updates small enough that the model doesn't drift away from its training.",
        "Developed by OpenAI in 2017, originally for video-game agents. PPO's \"trust region\" approach prevents the kind of overconfident gradient updates that destabilise RL training. In RLHF it's used to update the language model under guidance from the reward model. Newer alternatives like DPO try to avoid PPO's complexity, but PPO is still the workhorse for full RLHF pipelines.",
        ["OpenAI"],
        indications=["Safety", "Training"],
        category="Alignment",
    ),
    entry(
        "LoRA", "Low-Rank Adaptation",
        "Efficient fine-tuning technique that adds small trainable matrices alongside the frozen original weights.",
        "Instead of fine-tuning all 70 billion parameters of a model, LoRA freezes them and adds tiny trainable \"adapter\" matrices alongside — typically 0.1-1% the size. Trains roughly 100× faster and the resulting adapters are small files you can swap in and out. Released by Microsoft Research in 2021 and now the dominant approach to customising open-source models. Hugging Face hosts thousands of community-trained LoRAs.",
        ["Microsoft Research", "Hugging Face"],
        indications=["Training"],
        category="Training",
    ),
    entry(
        "QLoRA", "",
        "LoRA combined with model quantisation, letting you fine-tune huge models on a single consumer GPU.",
        "Standard LoRA still needs the full model loaded in memory. QLoRA compresses (quantises) the frozen base model to 4 bits per parameter, dropping memory by 4-8×. The result: fine-tuning a 70B-parameter model fits on a single 24GB consumer GPU. Released by University of Washington researchers in 2023 and democratised LLM fine-tuning overnight.",
        ["Hugging Face"],
        indications=["Training"],
        category="Training",
    ),
    entry(
        "PEFT", "Parameter-Efficient Fine-Tuning",
        "Umbrella term for fine-tuning methods that adjust only a small fraction of a model's parameters.",
        "Covers LoRA, QLoRA, prompt tuning, prefix tuning, adapter layers, and more. The shared goal: avoid the cost and disk space of full fine-tuning while preserving most of the quality. PEFT methods are essential for adapting frontier models to specific tasks at a small lab or company that can't afford to retrain the whole thing. Hugging Face's PEFT library is the standard implementation.",
        ["Hugging Face"],
        indications=["Training"],
        category="Training",
    ),
    entry(
        "Reward hacking", "",
        "When a model finds shortcuts that score high on its reward signal but don't actually satisfy what the reward was meant to capture.",
        "Classic example: a robot trained to maximise points in a boat-racing game discovered it could rack up points by spinning in circles in a single area, ignoring the actual race. In RLHF, reward hacking shows up as models that game the reward model — producing outputs that look good to it but aren't actually helpful. A major reason RLHF needs careful design and many rounds of iteration.",
        ["OpenAI", "Anthropic"],
        indications=["Safety"],
        category="Alignment",
    ),
    entry(
        "Sycophancy", "",
        "When a model agrees with whatever the user says, even if it's wrong — a side effect of training on human preferences.",
        "RLHF rewards responses that humans rate highly. Humans tend to rate agreeable responses higher than challenging ones. The result: models that flatter, agree with mistaken claims, or change their answer when pushed even slightly. Recognised as a major alignment failure mode and the target of specific mitigation training. The 2023 Anthropic paper \"Towards Understanding Sycophancy\" documented the phenomenon in detail.",
        ["Anthropic"],
        indications=["Safety"],
        category="Alignment",
    ),
    entry(
        "Red-teaming", "",
        "Adversarial testing — having people deliberately try to break the model or get it to misbehave.",
        "Borrowed from cybersecurity. Red teams probe a model for jailbreaks, unsafe outputs, bias, hallucination, and other failure modes before release. Anthropic, OpenAI, and Google all run extensive red-team campaigns. Findings feed into refusal training and constitutional updates. The UK and US AI Safety Institutes do third-party red-teaming on frontier models before they ship.",
        ["Anthropic", "OpenAI"],
        indications=["Safety"],
        category="Alignment",
    ),
    entry(
        "Refusal training", "",
        "Teaching a model when to say no — declining requests for help with harmful, illegal, or otherwise off-policy tasks.",
        "A subset of alignment training that produces the familiar \"I can't help with that\" responses to weapons synthesis, malware, or self-harm queries. Hard to get right: too liberal and the model is dangerous; too strict and it's annoying (\"I can't tell you how to chop onions\"). Modern refusal training is layered with explanation — the model says why it's declining and offers to help with the underlying need.",
        ["Anthropic", "OpenAI"],
        indications=["Safety"],
        category="Alignment",
    ),
]


# ============================================================================
# BATCH 3 — Inference, decoding, parallelism (25 terms)
# ============================================================================

BATCH_INFERENCE = [
    entry(
        "Inference", "",
        "Using a trained model to produce outputs — the part of AI that happens every time you send a prompt.",
        "After a model is trained once (extremely expensive), it's run many billions of times to answer queries (still expensive, but per-query small). Inference dominates the running cost of consumer LLM services. Optimising inference — KV caching, quantization, batching, speculative decoding — is a major engineering frontier and the main job of inference frameworks like vLLM and TensorRT.",
        ["NVIDIA", "OpenAI"],
        indications=["Inference", "Compute"],
        category="Inference",
    ),
    entry(
        "Quantization", "",
        "Compressing a model by storing its numbers with fewer bits — smaller, faster, almost as accurate.",
        "Models are normally trained at 16- or 32-bit precision. Quantization rounds parameters down to 8, 4, or even 2 bits each, shrinking memory by 2-8× and speeding inference. Quality loss is small if done carefully. Quantised models can run on consumer hardware (phones, laptops) that couldn't otherwise host them. Standard formats: INT8, INT4, FP8.",
        ["NVIDIA", "Hugging Face"],
        indications=["Inference", "Compute"],
        category="Inference",
    ),
    entry(
        "KV cache", "Key-Value cache",
        "Memory of past computation that lets a language model generate each new token without redoing work for old ones.",
        "When generating word N, a Transformer would normally re-process all previous N-1 words. The KV cache stores intermediate results so each new word only adds one position's worth of computation. KV cache size grows linearly with context length and dominates inference memory at long contexts — a major reason 1M-token contexts are hard.",
        ["NVIDIA"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Prompt caching", "",
        "Server-side reuse of a common prompt prefix across many requests — pay the compute once, reuse it many times.",
        "If you hit the same model with the same long system prompt every time, prompt caching stores the KV cache for that prefix on the server. Subsequent requests skip recomputing it. OpenAI, Anthropic, and Google all expose prompt caching APIs with significant cost discounts (50–90%) for cached prefixes — important for any app that uses a long, stable system prompt.",
        ["Anthropic", "OpenAI"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Speculative decoding", "",
        "Inference trick where a small model proposes several next tokens and the big model verifies them in parallel.",
        "Generating one token at a time is sequential and slow. A cheap \"draft\" model guesses the next 4-8 tokens; the expensive main model checks them all in a single batched forward pass; accepted guesses are kept and rejected ones trigger a fallback. Achieves 2-3× speedup on typical workloads. Used in production by most inference engines.",
        ["Google DeepMind"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Distillation", "",
        "Training a small model to mimic the outputs of a large one — cheaper to run, often surprisingly good.",
        "The large \"teacher\" model produces outputs (or probability distributions) on a big set of prompts. The small \"student\" is trained to match them. Distilled models capture most of the teacher's capabilities at a fraction of the cost. GPT-4o mini, Claude Haiku, and Gemini Flash are all distilled from larger siblings. Phi-3 is a notable open-source example.",
        ["Microsoft Research", "OpenAI"],
        indications=["Inference", "Training"],
        category="Inference",
    ),
    entry(
        "Pruning", "",
        "Removing parameters from a trained model that contribute little to its output — shrinks size with small quality loss.",
        "Magnitude pruning zeroes out the smallest-weight connections. Structured pruning removes whole rows, columns, or attention heads to maintain hardware-friendly shapes. Pruning is less popular than quantization in modern LLM serving (quantization is more predictable) but is still important for edge deployment and embedded vision models.",
        ["NVIDIA"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Greedy decoding", "",
        "Generating the highest-probability next token at every step — deterministic but often repetitive.",
        "The simplest decoding strategy: at each step, pick whichever token the model rates most likely. Always produces the same output for the same input. Tends to produce dull, repetitive text and gets stuck in loops on creative tasks. Useful for tasks where determinism matters (code completion, structured output) but mostly replaced by sampling-based methods for chat.",
        ["OpenAI"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Beam search", "",
        "Decoding strategy that keeps several candidate sequences alive at once and picks the best at the end.",
        "Instead of committing to one next token, beam search expands the top-K continuations of every partial sequence at each step, keeping a fixed-size \"beam\" of best candidates. Used heavily in translation and summarisation, where there's a clear single \"correct\" answer. Less useful for open-ended chat, where sampling produces more interesting outputs.",
        ["Google DeepMind"],
        indications=["Inference", "NLP"],
        category="Inference",
    ),
    entry(
        "Temperature", "",
        "Knob that controls how random a model's output is — low values are predictable, high values are creative.",
        "Temperature scales the model's probability distribution before sampling. Temperature 0 is equivalent to greedy decoding. Temperature 0.7-1.0 is typical for chat. Above 1.5 the model starts to produce gibberish. The single most useful knob a developer can tune when integrating an LLM into a product.",
        ["OpenAI"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Top-k sampling", "",
        "Decoding rule that restricts each step's choices to the K most likely tokens.",
        "Caps the long tail of the distribution: even if the model gives small probability to thousands of weird tokens, only the top K (typically 20-50) are considered. Combined with temperature and top-p to shape model output. A workhorse decoding rule throughout the 2020s, though top-p has largely replaced it in modern stacks.",
        ["OpenAI"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Top-p sampling", "Nucleus sampling",
        "Decoding rule that picks from however many tokens are needed to cover a probability mass of P.",
        "Instead of fixing the number of candidates (like top-k), top-p adapts: take the smallest set of tokens whose probabilities sum to P (typically 0.9-0.95). When the model is confident, this is a tiny set; when uncertain, it widens. Strikes a better balance than top-k in practice and is the default decoding strategy for most modern chat models.",
        ["Allen Institute for AI"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Repetition penalty", "",
        "Downweighting tokens that have already appeared to stop the model getting stuck on the same words.",
        "Without it, language models tend to loop — \"the the the the\" or repeating phrases. The penalty multiplies the probability of recently-used tokens by a factor below 1 (typical 1.1-1.3). Heavier penalties harm fluency, lighter ones leave loops in. Largely solved by modern training but still an important inference-time knob for older or smaller models.",
        ["Hugging Face"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Logits", "",
        "The raw, unnormalised scores a model outputs for each possible next token, before they're turned into probabilities.",
        "Logits are what comes out of the final layer of a language model — one number per vocabulary entry. Softmax converts them into a probability distribution. \"Logit bias\" APIs (OpenAI, Anthropic) let developers nudge specific tokens up or down before sampling, useful for forcing JSON output or banning specific words.",
        ["OpenAI"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Sampling", "",
        "Picking each next token randomly from the model's probability distribution, rather than always taking the top one.",
        "The umbrella over temperature, top-k, top-p, and similar decoding methods. Introduces controlled randomness that lets the model produce diverse, creative outputs instead of dull, deterministic ones. The main mechanism by which the same prompt to the same model gives slightly different answers each time.",
        ["OpenAI"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Decoding", "",
        "The general process of turning a model's predictions into an output sequence.",
        "Covers everything from greedy decoding through beam search and various sampling strategies. The choice of decoding strategy can have a bigger effect on output quality than people realise — the same model can feel completely different with different decoding settings. Modern chat APIs expose temperature, top-p, and a few other dials.",
        ["OpenAI"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Tensor parallelism", "",
        "Splitting a single layer's computation across multiple GPUs — needed when one layer doesn't fit on one chip.",
        "Each GPU holds part of the weight matrices and computes its slice in parallel; results are combined with high-bandwidth communication. Tensor parallelism is what makes frontier models (300B+ parameters) trainable and servable at all. Requires very fast interconnect — typically NVLink within a node, InfiniBand between nodes.",
        ["NVIDIA"],
        indications=["Compute", "Training"],
        category="Infrastructure",
    ),
    entry(
        "Pipeline parallelism", "",
        "Splitting a model's layers across multiple GPUs — different GPUs hold different layers, examples flow through like an assembly line.",
        "Each batch is broken into micro-batches that move through the pipeline staggered, so all GPUs stay busy. Pipeline parallelism is necessary for very deep models and is often combined with tensor and data parallelism in a \"3D parallel\" setup. Megatron-LM and DeepSpeed are the standard libraries.",
        ["NVIDIA", "Microsoft Research"],
        indications=["Compute", "Training"],
        category="Infrastructure",
    ),
    entry(
        "Data parallelism", "",
        "Each GPU holds a full copy of the model and works on a different slice of the batch — the simplest parallel setup.",
        "After every step, GPUs exchange gradients so they stay synchronised. Easy to implement and scales linearly up to maybe 100 GPUs. Beyond that, the communication overhead and memory cost of replicating the model become prohibitive — bigger models switch to tensor/pipeline parallelism or sharded variants like FSDP.",
        ["NVIDIA"],
        indications=["Compute", "Training"],
        category="Infrastructure",
    ),
    entry(
        "FSDP", "Fully Sharded Data Parallel",
        "Data parallelism where each GPU holds only a slice of the model weights, fetching others on demand.",
        "Solves data parallelism's main problem (every GPU holds a full model copy). FSDP shards parameters, gradients, and optimizer state across all GPUs and gathers them just-in-time for each layer. Introduced by Meta in PyTorch; now the standard way to train large models on commodity clusters. Closely related to Microsoft's ZeRO.",
        ["Meta AI / FAIR"],
        indications=["Compute", "Training"],
        category="Infrastructure",
    ),
    entry(
        "ZeRO", "Zero Redundancy Optimizer",
        "Microsoft's approach to sharding optimizer state, gradients, and parameters across GPUs — the original sharded-data-parallel design.",
        "Three \"stages\" of sharding: ZeRO-1 shards optimizer state only; ZeRO-2 adds gradients; ZeRO-3 adds parameters (equivalent to PyTorch's FSDP). Implemented in Microsoft's DeepSpeed library. Single most important technique for training frontier-scale models on clusters of hundreds or thousands of GPUs.",
        ["Microsoft Research"],
        indications=["Compute", "Training"],
        category="Infrastructure",
    ),
    entry(
        "Continuous batching", "",
        "Inference scheduling where finished requests are replaced mid-batch — keeps the GPU full when requests have different lengths.",
        "Standard batching waits for the longest request in a batch to finish before starting new ones, wasting compute. Continuous batching adds new prompts to the batch as soon as slots open, dramatically improving throughput for chat-like workloads with varying response lengths. The headline innovation behind vLLM and now standard across inference engines.",
        ["UC Berkeley"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Latency", "",
        "How long a single request takes — usually split into time-to-first-token and time-per-token.",
        "Latency matters for interactive chat (\"can you feel the lag?\") more than for batch jobs. Time-to-first-token is dominated by prompt processing; subsequent tokens flow at the model's per-token speed. KV caching, prompt caching, and speculative decoding are all latency optimisations. Frontier APIs target 300–500ms time-to-first-token.",
        ["NVIDIA"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Throughput", "",
        "Total tokens (across all requests) a system produces per second — what matters for cost economics.",
        "While latency is about one user's experience, throughput is about how many users one GPU can serve. Continuous batching, large effective batch sizes, and quantisation all increase throughput. Modern H100s serve roughly 1,000-5,000 tokens/second per GPU depending on model size and quantisation; bigger systems aggregate this across many GPUs.",
        ["NVIDIA"],
        indications=["Inference"],
        category="Inference",
    ),
    entry(
        "Mixed precision", "",
        "Training or inference that uses 16-bit numbers for most operations and 32-bit only where needed.",
        "Halves memory and roughly doubles throughput on modern GPUs (which are designed for FP16/BF16). The trick is identifying which operations need full precision to stay numerically stable — usually a small subset including normalisation and the optimizer state. Standard in all modern LLM training and inference; BF16 is the dominant flavour for training.",
        ["NVIDIA"],
        indications=["Training", "Inference"],
        category="Training",
    ),
]


BATCHES = {
    1: BATCH_ARCHITECTURES,
    2: BATCH_TRAINING_ALIGNMENT,
    3: BATCH_INFERENCE,
}


def merge(batches_to_run, dry_run=False):
    existing = json.loads(GLOSSARY.read_text())
    existing_names = {t["term"].lower() for t in existing}

    new_entries = []
    for n in batches_to_run:
        batch = BATCHES.get(n)
        if batch is None:
            print(f"warning: batch {n} not found, skipping")
            continue
        for e in batch:
            key = e["term"].lower()
            if key in existing_names:
                print(f"skip: {e['term']} already exists")
                continue
            new_entries.append(e)
            existing_names.add(key)

    if dry_run:
        print(f"would merge {len(new_entries)} new entries; total would be {len(existing) + len(new_entries)}")
        return

    combined = existing + new_entries
    combined.sort(key=lambda t: (t["letter"], t["term"].lower()))
    GLOSSARY.write_text(json.dumps(combined, ensure_ascii=False, indent=2) + "\n")
    print(f"merged {len(new_entries)} new entries; total {len(combined)}")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--batches", default=",".join(str(n) for n in BATCHES),
                   help="comma-separated batch numbers to run (default: all)")
    p.add_argument("--dry-run", action="store_true", help="preview without writing")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    nums = [int(x) for x in args.batches.split(",") if x.strip()]
    merge(nums, dry_run=args.dry_run)
