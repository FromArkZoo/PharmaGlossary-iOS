import SwiftUI

let aiBrand = Brand(
    appStoreName: "JB AI Glossary",
    displayName: "JB AI",
    navigationTitle: "JB AI",
    titlePrefix: "JB",
    titleBody: "AI",
    subtitle: "decoding AI & silicon",
    tagline: nil,
    entryNoun: "entries",
    dataResource: "glossary",
    primaryColor: Color(red: 0.122, green: 0.310, blue: 0.800),       // #1F4FCC electric blue
    primaryDarkColor: Color(red: 0.094, green: 0.235, blue: 0.616),   // deeper blue
    bgColor: PGColors.bg,
    urlScheme: "ai",
    aboutParagraphs: [
        "JB AI is a generalist's reference for the language of AI, machine learning, and the silicon underneath — the jargon you encounter in research papers, earnings calls, and tech news.",
        "Entries summarize publicly available information from papers, labs, and hardware vendors. They are written for orientation, not for engineering or investment decisions."
    ],
    aboutDisclaimer: "This is reference material. It is not engineering or investment advice.",
    aboutSources: [
        BrandSource(
            heading: "Research / labs",
            items: ["OpenAI", "Anthropic", "Google DeepMind", "Meta AI / FAIR", "Stanford CRFM", "Allen Institute for AI"]
        ),
        BrandSource(
            heading: "Hardware vendors",
            items: ["NVIDIA", "AMD", "Intel", "TSMC", "ASML", "Apple Silicon"]
        ),
        BrandSource(
            heading: "Standards & community",
            items: ["IEEE", "ACM", "MLCommons", "Open Compute Project"]
        )
    ],
    lenses: [
        LensConfig(
            id: "basics",
            glyph: "B",
            title: "Basics",
            subtitle: "Foundational ML & hardware",
            kind: .allowlist(["Transformer", "GPU"])
        ),
        LensConfig(
            id: "frontier",
            glyph: "F",
            title: "Frontier",
            subtitle: "ML, models, research & scaling",
            kind: .categoryFilter(
                categories: ["Architecture", "Training", "Inference", "Eval",
                             "Alignment", "Research", "Concepts", "Frontier",
                             "Models", "Agents"],
                excludedTerms: []
            )
        ),
        LensConfig(
            id: "hardware",
            glyph: "H",
            title: "Hardware",
            subtitle: "Chips, fabs, memory, interconnect, stack",
            kind: .categoryFilter(
                categories: ["Hardware", "Manufacturing", "Memory",
                             "Interconnect", "Packaging", "Software",
                             "Infrastructure"],
                excludedTerms: []
            )
        )
    ],
    accentTint: nil,
    sourceURLs: [
        // Research / labs
        "OpenAI":               URL(string: "https://openai.com")!,
        "Anthropic":            URL(string: "https://www.anthropic.com")!,
        "Google DeepMind":      URL(string: "https://deepmind.google")!,
        "DeepMind":             URL(string: "https://deepmind.google")!,
        "Meta AI / FAIR":       URL(string: "https://ai.meta.com")!,
        "Stanford CRFM":        URL(string: "https://crfm.stanford.edu")!,
        "Allen Institute for AI": URL(string: "https://allenai.org")!,
        "Mistral":              URL(string: "https://mistral.ai")!,
        "DeepSeek":             URL(string: "https://www.deepseek.com")!,
        "Stability AI":         URL(string: "https://stability.ai")!,
        "Hugging Face":         URL(string: "https://huggingface.co")!,
        "Microsoft Research":   URL(string: "https://www.microsoft.com/en-us/research/")!,
        "Google Research":      URL(string: "https://research.google")!,
        "Cohere":               URL(string: "https://cohere.com")!,
        "xAI":                  URL(string: "https://x.ai")!,
        "Apple":                URL(string: "https://www.apple.com")!,
        "MIT":                  URL(string: "https://www.mit.edu")!,
        "UC Berkeley":          URL(string: "https://www.berkeley.edu")!,
        "EleutherAI":           URL(string: "https://www.eleuther.ai")!,
        "Together AI":          URL(string: "https://www.together.ai")!,
        // Hardware vendors
        "NVIDIA":               URL(string: "https://www.nvidia.com")!,
        "AMD":                  URL(string: "https://www.amd.com")!,
        "Intel":                URL(string: "https://www.intel.com")!,
        "TSMC":                 URL(string: "https://www.tsmc.com")!,
        "ASML":                 URL(string: "https://www.asml.com")!,
        "Apple Silicon":        URL(string: "https://www.apple.com/mac/m-series/")!,
        "Cerebras":             URL(string: "https://www.cerebras.net")!,
        "Groq":                 URL(string: "https://groq.com")!,
        "SambaNova":            URL(string: "https://sambanova.ai")!,
        "Samsung":              URL(string: "https://semiconductor.samsung.com")!,
        "SK Hynix":             URL(string: "https://www.skhynix.com")!,
        "Micron":               URL(string: "https://www.micron.com")!,
        "Qualcomm":             URL(string: "https://www.qualcomm.com")!,
        "ARM":                  URL(string: "https://www.arm.com")!,
        "Synopsys":             URL(string: "https://www.synopsys.com")!,
        "Cadence":              URL(string: "https://www.cadence.com")!,
        // Standards & community
        "IEEE":                 URL(string: "https://www.ieee.org")!,
        "ACM":                  URL(string: "https://www.acm.org")!,
        "MLCommons":            URL(string: "https://mlcommons.org")!,
        "Open Compute Project": URL(string: "https://www.opencompute.org")!,
        // Foundational papers
        "Vaswani 2017":         URL(string: "https://arxiv.org/abs/1706.03762")!,
    ]
)

extension Brand {
    static let current: Brand = aiBrand
}
