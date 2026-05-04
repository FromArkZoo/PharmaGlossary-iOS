import SwiftUI

struct Brand {
    let appStoreName: String
    let displayName: String
    let navigationTitle: String
    let subtitle: String
    let dataResource: String
    let primaryColor: Color
    let primaryDarkColor: Color
    let aboutBlurb: String

    static let current = Brand(
        appStoreName: "JB Pharma Glossary",
        displayName: "JB Pharma",
        navigationTitle: "JB Pharma Glossary",
        subtitle: "Decode pharma jargon, fast",
        dataResource: "glossary",
        primaryColor: PGColors.primary,
        primaryDarkColor: PGColors.primaryDark,
        aboutBlurb: "Quick-reference glossary for pharma and healthcare jargon — built for conferences, meetings, and the news."
    )
}
