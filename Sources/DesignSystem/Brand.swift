import SwiftUI

struct BrandSource {
    let heading: String
    let items: [String]
}

/// One lens card on the filter sheet. Each industry defines its own array
/// of lenses (1+) — Pharma has Basics + Policy, AI has Basics + Frontier +
/// Hardware, future industries can have any number.
struct LensConfig: Hashable {
    let id: String              // route identifier, e.g. "basics", "frontier"
    let glyph: String           // single char rendered on the lens card
    let title: String           // displayed on the card + as the destination nav title
    let subtitle: String        // descriptive line on the card
    let kind: LensKind
}

enum LensKind: Hashable {
    /// Pull a curated set of terms by exact-name match. Use for "Basics"-style
    /// lenses where the slice doesn't align with the `category` enum.
    case allowlist(Set<String>)

    /// Pull terms whose `category` is in the categories set, minus any term
    /// names in `excludedTerms`. Use for category-aligned slices (Policy,
    /// Hardware, Frontier research, etc.).
    case categoryFilter(categories: Set<String>, excludedTerms: Set<String>)
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

    /// Ordered list of lenses shown on the filter sheet. Order = display order.
    let lenses: [LensConfig]

    /// Optional editorial tint for chip-count text on selected chips. When nil,
    /// PGColors.accentTint derives from primaryColor.lightened(by: 0.40).
    let accentTint: Color?

    /// Keys MUST match exactly: either a value in glossary.json's `sources`
    /// array (per-term footer) OR the abbreviation prefix / full item in a
    /// BrandSource (About view). Lookup is by full-string equality. Missing
    /// keys fall through to plain text — no crash, no broken UI.
    let sourceURLs: [String: URL]

    // `static let current` is declared in each target's Targets/<Industry>/Brand.swift.
    // Exactly one target-specific file is compiled per build, so there's no duplicate.
}
