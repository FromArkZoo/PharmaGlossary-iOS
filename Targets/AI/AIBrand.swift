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
    basicsAllowlist: ["Transformer", "GPU"],
    basicsSubtitle: "Foundational ML & hardware",
    policyConfig: PolicyConfig(
        displayName: "Frontier",
        subtitle: "Cutting-edge research & scaling",
        categories: ["Concepts", "Research"],
        excludedTerms: []
    ),
    accentTint: nil
)

extension Brand {
    static let current: Brand = aiBrand
}
