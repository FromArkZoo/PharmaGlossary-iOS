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
            items: ["Cornell LII", "US Courts", "Supreme Court of the United States", "Library of Congress", "DOJ"]
        ),
        BrandSource(
            heading: "Specialised agencies",
            items: ["USPTO", "Copyright Office", "FTC", "SEC", "DOL", "EEOC", "OSHA", "EPA", "NLRB", "FCC"]
        ),
        BrandSource(
            heading: "Tax, bankruptcy, immigration",
            items: ["IRS", "Tax Court", "USCIS", "EOIR", "US Trustee Program"]
        ),
        BrandSource(
            heading: "Reference works",
            items: ["ABA Public Education", "Federal Rules of Civil Procedure", "Federal Rules of Evidence", "Federal Rules of Criminal Procedure", "UCC", "Restatement of Contracts", "Restatement of Torts"]
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
                "Affidavit", "Agency", "Alimony", "Annulment",
                "Answer", "Appeal", "Arraignment", "Assault",
                "Asylum", "At-will employment", "Attorney-client privilege", "Bail",
                "Battery", "Bill of Rights", "Breach", "Burden of proof",
                "Capacity", "Capital gains tax", "Cease and desist", "Chapter 7",
                "Chapter 11", "Chapter 13", "Child custody", "Child support guidelines",
                "Class action", "Common law", "Common-law marriage", "Complaint",
                "Compliance", "Consent decree", "Consideration", "Contract",
                "Conversion", "Copyright", "Corporation", "DMCA",
                "Damages", "Deed", "Defamation", "Defendant",
                "Deposition", "Discovery", "Divorce", "Double jeopardy",
                "Due process", "Easement", "Earned Income Tax Credit", "Eminent domain",
                "Employment agreement", "Enforcement action", "Equal protection", "Escrow",
                "Estate tax", "Fair use", "False imprisonment", "Federalism",
                "Felony", "Fifth Amendment", "First Amendment", "Fixture",
                "FMLA", "Force majeure", "Foreclosure", "Fourth Amendment",
                "Green card", "Guardianship", "Habeas corpus", "HIPAA",
                "Indemnity", "Indictment", "Infringement", "Joint custody",
                "Joint tenancy", "Judicial review", "Jurisdiction", "Landlord",
                "Lease", "Libel", "License", "Lien",
                "Liquidated damages", "LLC", "Living trust", "Living will",
                "Mens rea", "Minimum wage", "Miranda warning", "Misdemeanor",
                "Mortgage", "Motion", "Mutual assent", "Naturalization",
                "NDA", "Negligence", "Non-compete", "Notice-and-comment",
                "Offer", "Overtime", "Patent", "Patentable subject matter",
                "Paternity", "Plaintiff", "Plea bargain", "Power of attorney",
                "Prenuptial agreement", "Prior art", "Probable cause", "Probate",
                "Probation", "Proximate cause", "Public domain", "Punitive damages",
                "Real estate", "Regulation", "Removal proceedings", "Royalty",
                "Search warrant", "Separation of powers", "Settlement", "Sexual harassment",
                "Sixth Amendment", "Slander", "Specific performance", "Standing",
                "Statute", "Statute of frauds", "Statute of limitations", "Statutory damages",
                "Strict liability", "Subpoena", "Summons", "Tenant",
                "Title", "Title VII", "Tort", "Trade secret",
                "Trademark", "Trademark dilution", "Trespass", "Trust",
                "Unconscionable", "Venue", "Verdict", "Vicarious liability",
                "Visa", "Voidable", "Warranty", "Whistleblower",
                "Will", "Work for hire", "Wrongful termination",
                "Kelo v. New London", "Kickback", "Knock-and-announce rule",
                "X-mark",
                "Year-and-a-day rule", "Yellow-dog contract",
                "Zealous representation", "Zoning"
            ])
        ),
        LensConfig(
            id: "civil",
            glyph: "P",
            title: "Civil & Business",
            subtitle: "Contracts, torts, IP, business, employment",
            kind: .categoryFilter(
                categories: ["Contract", "Tort", "Property", "IP", "Procedure",
                             "Corporate", "Employment", "Tax", "Bankruptcy"],
                excludedTerms: []
            )
        ),
        LensConfig(
            id: "public",
            glyph: "C",
            title: "Public Law",
            subtitle: "Crime, constitution, regulation, immigration",
            kind: .categoryFilter(
                categories: ["Criminal", "Constitutional", "Regulatory", "Immigration"],
                excludedTerms: []
            )
        ),
        LensConfig(
            id: "family",
            glyph: "F",
            title: "Family",
            subtitle: "Marriage, custody, divorce",
            kind: .categoryFilter(
                categories: ["Family"],
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
        "OSHA":                              URL(string: "https://www.osha.gov")!,
        "EPA":                               URL(string: "https://www.epa.gov")!,
        "NLRB":                              URL(string: "https://www.nlrb.gov")!,
        "USCIS":                             URL(string: "https://www.uscis.gov")!,
        "EOIR":                              URL(string: "https://www.justice.gov/eoir")!,
        "Tax Court":                         URL(string: "https://www.ustaxcourt.gov")!,
        "US Trustee Program":                URL(string: "https://www.justice.gov/ust")!,
        "HUD":                               URL(string: "https://www.hud.gov")!,
        "Federal Reserve":                   URL(string: "https://www.federalreserve.gov")!,
        "FDIC":                              URL(string: "https://www.fdic.gov")!,
        "USDA":                              URL(string: "https://www.usda.gov")!,
        "FDA":                               URL(string: "https://www.fda.gov")!,
        "CFPB":                              URL(string: "https://www.consumerfinance.gov")!,
        "DHS":                               URL(string: "https://www.dhs.gov")!,
        "ICE":                               URL(string: "https://www.ice.gov")!,
        "FinCEN":                            URL(string: "https://www.fincen.gov")!,
        "GAO":                               URL(string: "https://www.gao.gov")!,
        "GSA":                               URL(string: "https://www.gsa.gov")!,
        "Bureau of Land Management":         URL(string: "https://www.blm.gov")!,
        "Department of the Interior":        URL(string: "https://www.doi.gov")!,
        "Federal Trade Commission":          URL(string: "https://www.ftc.gov")!,
        "State Department":                  URL(string: "https://www.state.gov")!,
        "NYSE":                              URL(string: "https://www.nyse.com")!,
        "WIPO":                              URL(string: "https://www.wipo.int")!,
        "Uniform Law Commission":            URL(string: "https://www.uniformlaws.org")!,
        "California Corporations Code":      URL(string: "https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=CORP")!,
        "Delaware Court of Chancery":        URL(string: "https://courts.delaware.gov/chancery/")!,
        "Federal Rules of Bankruptcy Procedure": URL(string: "https://www.law.cornell.edu/rules/frbp")!,
        // Reference works & rules
        "ABA Public Education":              URL(string: "https://www.americanbar.org/groups/public_education/")!,
        "Federal Rules of Civil Procedure":  URL(string: "https://www.law.cornell.edu/rules/frcp")!,
        "Federal Rules of Evidence":         URL(string: "https://www.law.cornell.edu/rules/fre")!,
        "Federal Rules of Criminal Procedure": URL(string: "https://www.law.cornell.edu/rules/frcrmp")!,
        "Federal Rules of Appellate Procedure": URL(string: "https://www.law.cornell.edu/rules/frap")!,
        "UCC":                               URL(string: "https://www.law.cornell.edu/ucc")!,
        "Internal Revenue Code":             URL(string: "https://www.law.cornell.edu/uscode/text/26")!,
        "Bankruptcy Code":                   URL(string: "https://www.law.cornell.edu/uscode/text/11")!,
        "Immigration and Nationality Act":   URL(string: "https://www.law.cornell.edu/uscode/text/8/chapter-12")!,
        "Restatement of Contracts":          URL(string: "https://www.ali.org/publications/series/restatements/")!,
        "Restatement of Torts":              URL(string: "https://www.ali.org/publications/series/restatements/")!,
        "ALI":                               URL(string: "https://www.ali.org")!,
        "Justia":                            URL(string: "https://www.justia.com")!
    ]
)

extension Brand {
    static let current: Brand = lawBrand
}
