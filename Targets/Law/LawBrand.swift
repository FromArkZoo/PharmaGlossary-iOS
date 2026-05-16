import SwiftUI

let lawBrand = Brand(
    appStoreName: "JB Law",
    displayName: "JB Law",
    navigationTitle: "JB Law",
    titlePrefix: "JB",
    titleBody: "Law",
    subtitle: "decoding legal jargon",
    tagline: nil,
    entryNoun: "entries",
    dataResource: "glossary",
    primaryColor: Color(red: 0.122, green: 0.302, blue: 0.227),       // #1F4D3A deep law-book green
    primaryDarkColor: Color(red: 0.078, green: 0.212, blue: 0.149),   // deeper green
    bgColor: PGColors.bg,
    urlScheme: "law",
    aboutParagraphs: [
        "JB Law is a generalist's reference for the language of US law — the words you encounter in contracts, leases, employment agreements, news headlines, and any time you talk to a lawyer.",
        "Entries summarise publicly available material from courts, agencies, and reference works. They are written for orientation in plain English, not as legal advice."
    ],
    aboutDisclaimer: "Educational reference. Not legal advice. Laws vary by jurisdiction.",
    aboutSources: [
        BrandSource(
            heading: "Federal & courts",
            items: ["Cornell LII", "US Courts", "Supreme Court of the United States", "Library of Congress"]
        ),
        BrandSource(
            heading: "Specialised agencies",
            items: ["USPTO", "Copyright Office", "FTC", "SEC", "DOL", "EEOC"]
        ),
        BrandSource(
            heading: "Reference works",
            items: ["ABA Public Education", "Federal Rules of Civil Procedure", "Federal Rules of Evidence", "UCC", "Restatement of Contracts"]
        )
    ],
    lenses: [
        LensConfig(
            id: "basics",
            glyph: "B",
            title: "Basics",
            subtitle: "Foundational legal terms",
            kind: .allowlist([
                "Acceptance", "Actus reus", "Administrative law", "Adverse possession",
                "Affidavit", "Agency", "Answer", "Appeal",
                "Arraignment", "Assault", "Bail", "Battery",
                "Bill of Rights", "Breach", "Burden of proof", "Capacity",
                "Cease and desist", "Class action", "Complaint", "Compliance",
                "Consent decree", "Consideration", "Contract", "Conversion",
                "Copyright", "DMCA", "Damages", "Deed",
                "Defamation", "Defendant", "Deposition", "Discovery",
                "Double jeopardy", "Due process", "Easement", "Eminent domain",
                "Enforcement action", "Equal protection", "Escrow", "Fair use",
                "False imprisonment", "Federalism", "Felony", "Fifth Amendment",
                "First Amendment", "Fixture", "Force majeure", "Foreclosure",
                "Fourth Amendment", "GDPR", "HIPAA", "Habeas corpus",
                "Indemnity", "Indictment", "Infringement", "Joint tenancy",
                "Judicial review", "Jurisdiction", "Landlord", "Lease",
                "Libel", "License", "Lien", "Liquidated damages",
                "Mens rea", "Miranda warning", "Misdemeanor", "Mortgage",
                "Motion", "Mutual assent", "NDA", "Negligence",
                "Notice-and-comment", "Offer", "Patent", "Patentable subject matter",
                "Plaintiff", "Plea bargain", "Prior art", "Probable cause",
                "Probation", "Proximate cause", "Public domain", "Punitive damages",
                "Real estate", "Regulation", "Royalty", "Search warrant",
                "Separation of powers", "Settlement", "Sixth Amendment", "Slander",
                "Specific performance", "Standing", "Statute", "Statute of frauds",
                "Statute of limitations", "Statutory damages", "Strict liability", "Subpoena",
                "Summons", "Tenant", "Title", "Tort",
                "Trade secret", "Trademark", "Trademark dilution", "Trespass",
                "Unconscionable", "Venue", "Verdict", "Vicarious liability",
                "Voidable", "Warranty", "Work for hire",
                "Kelo v. New London", "Kickback", "Knock-and-announce rule",
                "X-mark",
                "Year-and-a-day rule", "Yellow-dog contract",
                "Zealous representation", "Zoning"
            ])
        ),
        LensConfig(
            id: "practice",
            glyph: "P",
            title: "Practice",
            subtitle: "Contracts, IP, property, torts, procedure",
            kind: .categoryFilter(
                categories: ["Contract", "IP", "Property", "Tort", "Procedure"],
                excludedTerms: []
            )
        ),
        LensConfig(
            id: "public",
            glyph: "C",
            title: "Public Law",
            subtitle: "Crime, constitution, regulation",
            kind: .categoryFilter(
                categories: ["Criminal", "Constitutional", "Regulatory"],
                excludedTerms: []
            )
        )
    ],
    accentTint: nil,
    sourceURLs: [
        // Federal & courts
        "Cornell LII":                       URL(string: "https://www.law.cornell.edu")!,
        "US Courts":                         URL(string: "https://www.uscourts.gov")!,
        "Supreme Court of the United States":URL(string: "https://www.supremecourt.gov")!,
        "Library of Congress":               URL(string: "https://www.loc.gov")!,
        "DOJ":                               URL(string: "https://www.justice.gov")!,
        // Specialised agencies
        "USPTO":                             URL(string: "https://www.uspto.gov")!,
        "Copyright Office":                  URL(string: "https://www.copyright.gov")!,
        "FTC":                               URL(string: "https://www.ftc.gov")!,
        "SEC":                               URL(string: "https://www.sec.gov")!,
        "DOL":                               URL(string: "https://www.dol.gov")!,
        "EEOC":                              URL(string: "https://www.eeoc.gov")!,
        "FCC":                               URL(string: "https://www.fcc.gov")!,
        "IRS":                               URL(string: "https://www.irs.gov")!,
        // Reference works & rules
        "ABA Public Education":              URL(string: "https://www.americanbar.org/groups/public_education/")!,
        "Federal Rules of Civil Procedure":  URL(string: "https://www.law.cornell.edu/rules/frcp")!,
        "Federal Rules of Evidence":         URL(string: "https://www.law.cornell.edu/rules/fre")!,
        "UCC":                               URL(string: "https://www.law.cornell.edu/ucc")!,
        "Restatement of Contracts":          URL(string: "https://www.ali.org/publications/series/restatements/")!,
        "ALI":                               URL(string: "https://www.ali.org")!,
        "Justia":                            URL(string: "https://www.justia.com")!
    ]
)

extension Brand {
    static let current: Brand = lawBrand
}
