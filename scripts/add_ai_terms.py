"""Idempotently merge AI/ML + semiconductor terms into Targets/AI/Resources/glossary.json.

Mirrors scripts/add_basics.py — append-only, case-insensitive dedup against
existing terms, sort by (letter asc, term asc) on write. Each batch is a
Python list of entries built via the entry() helper, which enforces the
category + indication enums so we don't accidentally drift away from the
lenses defined in Targets/AI/AIBrand.swift.

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
# Architecture/Training/Inference/Eval/Alignment/Research/Concepts/Frontier/
# Models/Agents → Frontier lens. Hardware/Manufacturing/Memory/Interconnect/
# Packaging/Software/Infrastructure → Hardware lens. Industry/Regulation/
# Companies live outside lenses for now.
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
    """Build a Term dict. Letter derived from the first char of `term`.

    Args:
        term: display name, e.g. "Transformer"
        full: expanded form, e.g. "Mixture of Experts" — "" if N/A
        snappy: one-line summary shown italicised in the UI
        detail: 2-4 sentence body, generalist tone
        sources: list of source keys (should match aiBrand.sourceURLs for
                 linkification; will render as plain text if not)
        indications: list of domain tags from VALID_INDICATIONS
        category: single value from VALID_CATEGORIES
    """
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
# BATCH 1 — Core architectures + tokens (25 terms)
# ============================================================================
# Foundational ML architecture vocabulary plus the tokenization concepts
# needed to talk about LLMs. Mostly category="Architecture" with a few
# "Concepts" for tokenization. Indications skew NLP / Vision / Research.

BATCH_ARCHITECTURES = [
    entry(
        "Attention", "",
        "Mechanism letting a model weigh which other parts of its input matter for the current position.",
        "Introduced as a fix for the bottleneck in sequence-to-sequence models, attention lets a network learn dynamic, content-dependent connections rather than relying on fixed recurrence. The 2017 \"Attention Is All You Need\" paper showed that attention alone — no recurrence, no convolution — could match or beat the state of the art, kicking off the Transformer era.",
        ["Vaswani 2017"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Self-attention", "",
        "Attention where the queries, keys, and values all come from the same sequence.",
        "Self-attention lets each token in a sequence attend to every other token in the same sequence, producing context-aware representations in a single layer. It's the operation that makes Transformers parallelisable across sequence length, in contrast to RNNs which must process tokens one at a time.",
        ["Vaswani 2017"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Multi-head attention", "",
        "Running several attention operations in parallel with different learned projections, then concatenating.",
        "Each head can specialise — one might track syntactic structure, another long-range coreference. Modern frontier LLMs typically use 32–128 heads per layer, with variants like grouped-query attention (GQA) and multi-query attention (MQA) sharing key/value projections across heads to cut inference memory.",
        ["Vaswani 2017"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Encoder", "",
        "The part of a model that turns an input sequence into a vector representation.",
        "In encoder-decoder architectures (T5, original Transformer, BART) the encoder reads the input fully bidirectionally — every token sees every other — before passing rich representations to the decoder. BERT is an encoder-only model, designed for understanding tasks like classification and embedding generation rather than generation.",
        ["Vaswani 2017", "Google DeepMind"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Decoder", "",
        "The part of a model that generates an output sequence one token at a time.",
        "Decoders use causal (masked) self-attention so each position can only attend to earlier positions — necessary for left-to-right generation. GPT-family models, Claude, Llama, and Gemini are all decoder-only Transformers, having absorbed the encoder's job into a single autoregressive stack.",
        ["OpenAI"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Encoder-decoder", "",
        "Two-stack architecture: an encoder digests the input, a decoder generates the output conditioned on it.",
        "The original Transformer was encoder-decoder, designed for translation. T5, BART, and Whisper still use this shape. Most modern chat LLMs are decoder-only because they can be trained on more general next-token prediction, but encoder-decoder remains strong for tasks with a clear input→output mapping (translation, summarisation, speech recognition).",
        ["Vaswani 2017", "Google DeepMind"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Mixture of Experts", "MoE",
        "Architecture where each input is routed to a small subset of specialised sub-networks rather than the whole model.",
        "MoE separates total parameter count (large) from per-token compute (small). A router selects, say, 2 of 64 \"experts\" per token, so a 400B-parameter model might activate only 40B per forward pass. Mixtral, DeepSeek-V3, and (reportedly) GPT-4 all use MoE to scale capacity without exploding inference cost.",
        ["Mistral", "DeepSeek"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Sparse MoE", "",
        "MoE variant where only a few experts activate per token — the standard form in modern frontier models.",
        "Contrasted with \"dense MoE\" where all experts process every token (rarely used in practice). Sparse routing introduces training instability and load-balancing challenges, which papers like Switch Transformer and GShard worked through. The savings on inference are dramatic: 8× capacity at 1× compute is typical.",
        ["Google DeepMind"],
        indications=["Research"],
        category="Architecture",
    ),
    entry(
        "Diffusion model", "",
        "Generative model that learns to reverse a gradual noising process — turning noise into samples step by step.",
        "Forward process: take an image, add Gaussian noise over T steps until it's pure static. Train a network to invert one step. At inference, start from noise and denoise iteratively. DALL-E 3, Stable Diffusion, Flux, Midjourney, and Sora are all diffusion-based. Diffusion is now spreading to audio, video, and even language modelling.",
        ["OpenAI", "Stability AI"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "Latent diffusion", "",
        "Diffusion run in a compressed latent space rather than directly on pixels.",
        "An autoencoder compresses 512×512 images to, say, 64×64×4 latents; diffusion operates there; the autoencoder decodes back to pixels. Cuts memory and compute by 50×+ with little quality loss. Stable Diffusion's breakthrough was making latent diffusion practical at consumer scale — every modern image generator since has copied the trick.",
        ["Stability AI"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "Variational autoencoder", "VAE",
        "Generative model that learns a probabilistic mapping between data and a latent space.",
        "Trained to compress and reconstruct, but with a regularised latent space you can sample from. VAEs alone produce somewhat blurry samples, but they remain useful as the encoder/decoder for latent diffusion, and pop up everywhere quality-controlled compression is needed (audio codecs, biological sequence design).",
        ["Stanford CRFM"],
        indications=["Research"],
        category="Architecture",
    ),
    entry(
        "Generative adversarial network", "GAN",
        "Two-network setup: a generator creates fake samples, a discriminator tries to spot them, both improve.",
        "Goodfellow et al. (2014) launched the modern generative-modelling era with GANs. StyleGAN dominated face generation in the late 2010s, but training was famously brittle (mode collapse, instability). Diffusion has largely replaced GANs at the frontier, though GANs still win on speed: one forward pass instead of many denoising steps.",
        ["NVIDIA"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "Recurrent neural network", "RNN",
        "Network that processes a sequence one element at a time, carrying a hidden state between steps.",
        "RNNs dominated sequence modelling pre-2017 (machine translation, speech recognition). Their core weakness is sequential computation — you can't parallelise across the time dimension, so training is slow on long sequences and vanishing gradients make long-range learning hard. Transformers replaced them for most tasks, but RNN-like architectures are quietly returning via state space models (Mamba).",
        ["Stanford CRFM"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "LSTM", "Long Short-Term Memory",
        "RNN variant with gating mechanisms that lets gradients flow over long sequences.",
        "Introduced by Hochreiter & Schmidhuber in 1997 and dominant for sequence tasks through the 2010s. Three gates (input, forget, output) regulate how the hidden state updates. Google Translate ran on LSTMs in production before the Transformer takeover, and LSTMs remain relevant for resource-constrained on-device sequence tasks.",
        ["Stanford CRFM"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Convolutional neural network", "CNN",
        "Network that uses learned filters slid across an input, exploiting spatial structure.",
        "CNNs dominated computer vision from AlexNet (2012) through the late 2010s. Local receptive fields, weight sharing, and translation invariance made them naturally suited to images. Vision Transformers have since matched or beaten CNNs on most benchmarks, but CNNs remain the architecture of choice for resource-constrained deployment (mobile, embedded vision).",
        ["NVIDIA"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "ResNet", "Residual Network",
        "CNN with skip connections that let signal bypass layers — enabled training networks 100+ layers deep.",
        "Before ResNets (He et al., 2015), deeper networks paradoxically performed worse than shallower ones due to optimisation difficulties. Adding identity shortcuts solved this and unlocked very deep architectures. The residual idea (add input to transformed output) now appears in every Transformer block and is one of the most copied design patterns in modern deep learning.",
        ["Meta AI / FAIR"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "U-Net", "",
        "Encoder-decoder network with skip connections at every scale — the standard architecture for image-to-image tasks.",
        "Originally designed for biomedical image segmentation in 2015. The encoder downsamples, the decoder upsamples, and skip connections pass high-resolution features across. U-Net is now the workhorse of diffusion models — Stable Diffusion's denoising network is a U-Net — making it one of the most-used architectures by FLOP-hours.",
        ["Stability AI"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "Vision Transformer", "ViT",
        "Transformer applied directly to image patches, treating each patch as a token.",
        "Introduced by Google in 2020. Split an image into 16×16 patches, project each to an embedding, run a standard Transformer encoder. ViTs match or beat CNNs at scale, especially when pretrained on huge datasets. The architecture underpins modern vision-language models (CLIP, GPT-4o vision encoder) and image generators.",
        ["Google DeepMind"],
        indications=["Vision", "Research"],
        category="Architecture",
    ),
    entry(
        "CLIP", "Contrastive Language-Image Pretraining",
        "Model trained to align image and text embeddings — the basis for almost all modern multimodal systems.",
        "OpenAI's 2021 CLIP trained a vision encoder and a text encoder jointly on 400M image-caption pairs, with a contrastive loss pulling matched pairs together and pushing mismatched pairs apart. The resulting shared embedding space enables zero-shot classification, image search, and conditioning for image generators (Stable Diffusion uses CLIP for prompt encoding).",
        ["OpenAI"],
        indications=["Multimodal", "Research"],
        category="Architecture",
    ),
    entry(
        "Mamba", "",
        "Sequence model based on selective state space — competitive with Transformers but with linear-time inference.",
        "Released late 2023 by Gu & Dao. State space models maintain a compact recurrent state that's updated linearly per token, with selective gating chosen to match Transformer expressiveness. Promising on long-context tasks where Transformer's quadratic attention is prohibitive, though decoder-only Transformers remain dominant for general LLM work.",
        ["Stanford CRFM"],
        indications=["NLP", "Research"],
        category="Architecture",
    ),
    entry(
        "Token", "",
        "The atomic unit a language model processes — usually a word fragment of 3–4 characters.",
        "Models don't see characters or words directly; text is split into tokens by a tokenizer (BPE, SentencePiece). Common words like \"the\" become a single token; rare or compound words split into multiple. \"Context window\" is measured in tokens, API pricing is per-token, and a model's vocabulary size (typically 32k–256k) is the number of distinct tokens it knows.",
        ["OpenAI"],
        indications=["NLP"],
        category="Concepts",
    ),
    entry(
        "Tokenization", "",
        "Splitting text into tokens — the model's first preprocessing step.",
        "Modern LLMs use subword tokenizers (BPE, Unigram, SentencePiece) that balance vocabulary size against token length. The tokenizer is part of the model contract — \"GPT-4 tokens\" and \"Llama tokens\" aren't interchangeable. Tokenization quirks cause many weird model behaviours: poor arithmetic, struggle with character-level tasks, sensitivity to whitespace.",
        ["OpenAI"],
        indications=["NLP"],
        category="Concepts",
    ),
    entry(
        "Byte-Pair Encoding", "BPE",
        "Tokenizer training algorithm that iteratively merges the most frequent adjacent byte pairs.",
        "Start with single bytes as tokens. Repeatedly find the most common adjacent pair and add it as a new token. Stop at the target vocabulary size. GPT, Llama, and Mistral all use BPE variants. The simplicity is the strength: any string can be tokenized, including unseen characters, and the vocabulary adapts to the training corpus.",
        ["OpenAI"],
        indications=["NLP"],
        category="Concepts",
    ),
    entry(
        "Context window", "",
        "The maximum number of tokens a model can attend to at once.",
        "Bounded by self-attention's quadratic memory cost. Early GPT models had 2k–4k token windows; GPT-4 expanded to 128k; Claude 3.5 to 200k; Gemini 1.5 to 1M+ (with sparse attention tricks). Longer windows enable longer documents and chat histories but increase per-token inference cost and stress the model's ability to use context uniformly (\"lost in the middle\").",
        ["Anthropic", "OpenAI"],
        indications=["NLP"],
        category="Concepts",
    ),
    entry(
        "Positional encoding", "",
        "Information added to token embeddings so the model knows token order — Transformers have no built-in sequence sense.",
        "Original Transformer used fixed sinusoidal encodings. Modern models prefer learned variants like RoPE (rotary, GPT-NeoX/Llama) or ALiBi (linear bias, MPT). Positional encoding choice affects how well a model generalises to context lengths longer than it was trained on — important for long-context fine-tuning.",
        ["Meta AI / FAIR"],
        indications=["Research"],
        category="Architecture",
    ),
]


BATCHES = {
    1: BATCH_ARCHITECTURES,
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
