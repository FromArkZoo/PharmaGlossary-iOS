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

extension Brand {
    /// Keys MUST match exactly: either a value in glossary.json's `sources`
    /// array (per-term footer) OR the abbreviation prefix in a BrandSource
    /// item (About view). Lookup is by full-string equality. Missing keys
    /// fall through to plain text — no crash, no broken UI.
    static let sourceURLs: [String: URL] = [
        "NCI Dictionary of Cancer Terms": URL(string: "https://www.cancer.gov/publications/dictionaries/cancer-terms")!,
        "FDA":              URL(string: "https://www.fda.gov")!,
        "NIH":              URL(string: "https://www.nih.gov")!,
        "NIH MedlinePlus":  URL(string: "https://medlineplus.gov")!,
        "CMS Glossary":     URL(string: "https://www.cms.gov/apps/glossary")!,
        "NHGRI":            URL(string: "https://www.genome.gov")!,
        "NIH NIMH":         URL(string: "https://www.nimh.nih.gov")!,
        "CDC":              URL(string: "https://www.cdc.gov")!,
        "WHO":              URL(string: "https://www.who.int")!,
        "NIH NIA":          URL(string: "https://www.nia.nih.gov")!,
        "ICH GCP":          URL(string: "https://www.ich.org/page/efficacy-guidelines")!,
        "HRSA":             URL(string: "https://www.hrsa.gov")!,
        "ISPOR":            URL(string: "https://www.ispor.org")!,
        "ICER":             URL(string: "https://icer.org")!,
        "ICH E9":           URL(string: "https://www.ich.org/page/efficacy-guidelines")!,
        "CMS":              URL(string: "https://www.cms.gov")!,
        "EMA":              URL(string: "https://www.ema.europa.eu")!,
        "ICH":              URL(string: "https://www.ich.org")!,
        "NCI":              URL(string: "https://www.cancer.gov")!,
    ]
}
