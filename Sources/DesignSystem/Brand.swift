import SwiftUI

struct BrandSource {
    let heading: String
    let items: [String]
}

struct PolicyConfig {
    let displayName: String
    let subtitle: String
    let categories: Set<String>
    let excludedTerms: Set<String>
}

struct Brand {
    let appStoreName: String
    let displayName: String
    let navigationTitle: String
    let titlePrefix: String       // serif bold ink, e.g. "JB"
    let titleBody: String         // serif italic accent, e.g. "Pharma"
    let subtitle: String
    let tagline: String?          // optional editorial one-liner; nil renders nothing
    let entryNoun: String         // "entries", "ratios", "ingredients"
    let dataResource: String
    let primaryColor: Color
    let primaryDarkColor: Color
    let bgColor: Color

    let urlScheme: String
    let aboutParagraphs: [String]
    let aboutDisclaimer: String
    let aboutSources: [BrandSource]
    let basicsAllowlist: Set<String>
    let basicsSubtitle: String
    let policyConfig: PolicyConfig

    /// Optional editorial tint for chip-count text on selected chips. When nil,
    /// PGColors.accentTint derives from primaryColor.lightened(by: 0.40).
    let accentTint: Color?

    // `static let current` is declared in each target's Targets/<Industry>/Brand.swift.
    // Exactly one target-specific file is compiled per build, so there's no duplicate.
}
