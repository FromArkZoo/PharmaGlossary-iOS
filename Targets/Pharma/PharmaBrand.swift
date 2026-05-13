import SwiftUI

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
    primaryColor: Color(red: 0.545, green: 0.180, blue: 0.122),       // #8B2E1F oxblood
    primaryDarkColor: Color(red: 0.467, green: 0.137, blue: 0.094),   // deeper oxblood
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
    ),
    accentTint: Color(red: 0.784, green: 0.714, blue: 0.541)           // #C8B68A editorial complement
)

extension Brand {
    static let current: Brand = pharmaBrand
}
