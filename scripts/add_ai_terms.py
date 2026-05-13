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
