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

    static let current = pharmaBrand
}

let pharmaBrand = Brand(
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
    urlScheme: "pharma",
    aboutParagraphs: [
        "JB Pharma is a generalist's reference for the language of pharma and healthcare — the jargon you encounter in news, earnings calls, regulatory filings, and conferences.",
        "Entries summarize publicly available information from the authoritative sources listed below. They are written for orientation, not for clinical decision-making."
    ],
    aboutDisclaimer: "This is reference material. It is not medical advice.",
    aboutSources: [
        BrandSource(
            heading: "US health agencies",
            items: ["FDA — Food and Drug Administration",
                    "NIH — National Institutes of Health",
                    "NCI — National Cancer Institute",
                    "NHGRI — National Human Genome Research Institute",
                    "CDC — Centers for Disease Control and Prevention",
                    "CMS — Centers for Medicare & Medicaid Services",
                    "HRSA — Health Resources and Services Administration"]
        ),
        BrandSource(
            heading: "International",
            items: ["WHO — World Health Organization",
                    "EMA — European Medicines Agency",
                    "ICH — International Council for Harmonisation"]
        ),
        BrandSource(
            heading: "Health economics & access",
            items: ["ICER — Institute for Clinical and Economic Review",
                    "ISPOR — Professional Society for Health Economics and Outcomes Research"]
        )
    ],
    basicsAllowlist: [
        // Already present
        "RNA", "Mutation", "siRNA", "Ligand", "Receptor", "Agonist", "Antagonist",
        "MAb", "Apoptosis", "Insulin",
        // Mol bio
        "DNA", "Gene", "Genome", "Chromosome", "Allele", "Codon", "Nucleotide",
        "Base Pair", "Transcription", "Translation",
        "mRNA", "tRNA", "rRNA", "miRNA",
        // Protein/enzyme
        "Protein", "Peptide", "Amino Acid", "Alanine", "Glycine", "Lysine",
        "Enzyme", "Antibody", "Antigen", "Epitope", "Immunoglobulin",
        // Cell
        "Cell", "Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum",
        "Golgi Apparatus", "Cytoplasm", "Cell Membrane", "Mitosis", "Meiosis",
        // Chemistry
        "Atom", "Molecule", "Ion", "Isotope", "Isomer", "Polymer", "Monomer",
        "Hydrogen Bond", "Covalent Bond", "Acid", "Base", "pH", "Buffer",
        // Physiology
        "Hormone", "Neurotransmitter", "Cytokine", "Chemokine", "Lipid",
        "Fatty Acid", "Cholesterol", "Triglyceride", "Carbohydrate", "Glucose",
        "Glycogen", "Metabolism", "ATP", "Glycolysis", "Krebs Cycle"
    ],
    basicsSubtitle: "Foundational biology & chemistry",
    policyConfig: PolicyConfig(
        displayName: "Policy",
        subtitle: "Regulation, pricing, access",
        categories: ["Regulatory", "Commercial / Market Access"],
        excludedTerms: ["MSL", "Loss of Exclusivity", "Patent Cliff", "NCI", "HEOR", "Gross-to-Net", "Phase 4"]
    )
)
