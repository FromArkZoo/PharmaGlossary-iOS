import SwiftUI

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
    let aboutBlurb: String

    static let current = Brand(
        appStoreName: "JB Pharma Glossary",
        displayName: "JB Pharma",
        navigationTitle: "JB Pharma",
        titlePrefix: "JB",
        titleBody: "Pharma",
        subtitle: "decoding pharma jargon",
        tagline: nil,
        entryNoun: "entries",
        dataResource: "glossary",
        primaryColor: PGColors.accent,
        primaryDarkColor: PGColors.accentDark,
        bgColor: PGColors.bg,
        aboutBlurb: "Quick-reference glossary for pharma and healthcare jargon — built for conferences, meetings, and the news."
    )
}
