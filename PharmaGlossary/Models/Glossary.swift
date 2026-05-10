import Foundation

struct Term: Codable, Identifiable, Hashable {
    let letter: String
    let term: String
    let full: String
    let snappy: String
    let detail: String
    let indications: [String]
    let category: String
    let sources: [String]

    var id: String { "\(letter)::\(term)" }

    var hasFull: Bool { !full.isEmpty }
    var hasSnappy: Bool { !snappy.isEmpty }
    var hasCategory: Bool { !category.isEmpty }
    var hasSources: Bool { !sources.isEmpty }

    var shareText: String {
        var s = term
        if hasFull { s += " (\(full))" }
        if hasSnappy { s += "\n\n\(snappy)" }
        s += "\n\n\(detail)"
        return s
    }
}

struct FilterState: Equatable {
    var indications: Set<String> = []
    var categories: Set<String> = []

    var isActive: Bool { !indications.isEmpty || !categories.isEmpty }

    var summary: String {
        let parts = indications.sorted() + categories.sorted()
        return parts.joined(separator: " · ")
    }
}

@MainActor
final class GlossaryStore: ObservableObject {
    @Published private(set) var allTerms: [Term] = []
    @Published private(set) var byLetter: [String: [Term]] = [:]
    @Published private(set) var letters: [String] = []
    @Published private(set) var favorites: Set<String> = []

    var detailCache: [String: AttributedString] = [:]

    private let favoritesKey = "pg.favorites.v1"

    static let policyCategories: Set<String> = ["Regulatory", "Commercial / Market Access"]
    static let policyExcludedTerms: Set<String> = [
        "MSL", "Loss of Exclusivity", "Patent Cliff", "NCI", "HEOR", "Gross-to-Net", "Phase 4"
    ]

    /// Foundational biology/chemistry concepts. Curated list, mirrors the Policy
    /// lens pattern (allowlist rather than category filter) so we can scope it
    /// precisely without changing the data schema.
    static let basicsAllowlist: Set<String> = [
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
    ]

    var alphabetLetters: [String] {
        letters.filter { $0.range(of: "^[A-Z]$", options: .regularExpression) != nil }
    }

    var policyTerms: [Term] {
        allTerms
            .filter { Self.policyCategories.contains($0.category) && !Self.policyExcludedTerms.contains($0.term) }
            .sorted { $0.term.localizedCaseInsensitiveCompare($1.term) == .orderedAscending }
    }

    var basicsTerms: [Term] {
        allTerms
            .filter { Self.basicsAllowlist.contains($0.term) }
            .sorted { $0.term.localizedCaseInsensitiveCompare($1.term) == .orderedAscending }
    }

    init() {
        load()
        loadFavorites()
    }

    // MARK: - Favorites

    private func loadFavorites() {
        let stored = UserDefaults.standard.stringArray(forKey: favoritesKey) ?? []
        favorites = Set(stored)
    }

    private func persistFavorites() {
        UserDefaults.standard.set(Array(favorites).sorted(), forKey: favoritesKey)
    }

    func toggleFavorite(_ term: Term) {
        if favorites.contains(term.term) {
            favorites.remove(term.term)
        } else {
            favorites.insert(term.term)
        }
        persistFavorites()
    }

    func isFavorited(_ term: Term) -> Bool {
        favorites.contains(term.term)
    }

    var favoriteTerms: [Term] {
        allTerms
            .filter { favorites.contains($0.term) }
            .sorted { $0.term.localizedCaseInsensitiveCompare($1.term) == .orderedAscending }
    }

    private func load() {
        guard let url = Bundle.main.url(forResource: Brand.current.dataResource, withExtension: "json") else {
            assertionFailure("\(Brand.current.dataResource).json missing from bundle")
            return
        }
        do {
            let data = try Data(contentsOf: url)
            let terms = try JSONDecoder().decode([Term].self, from: data)
            self.allTerms = terms
            self.byLetter = Dictionary(grouping: terms, by: { $0.letter })
            self.letters = byLetter.keys.sorted()
            prewarmDetailCache(terms: terms)
        } catch {
            assertionFailure("Failed to decode \(Brand.current.dataResource).json: \(error)")
        }
    }

    /// Build every term's `attributedDetail` off the main thread, then bulk-merge
    /// into the cache so the first link tap doesn't pay the regex cost.
    private func prewarmDetailCache(terms: [Term]) {
        Task.detached(priority: .utility) { [weak self] in
            var built: [String: AttributedString] = [:]
            built.reserveCapacity(terms.count)
            for term in terms {
                built[term.id] = Self.computeAttributedDetail(for: term, against: terms)
            }
            await MainActor.run {
                guard let self else { return }
                for (id, attr) in built where self.detailCache[id] == nil {
                    self.detailCache[id] = attr
                }
            }
        }
    }

    func search(_ query: String) -> [Term] {
        let q = query.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        guard !q.isEmpty else { return [] }
        return allTerms.filter {
            $0.term.lowercased().contains(q)
                || $0.full.lowercased().contains(q)
                || $0.snappy.lowercased().contains(q)
                || $0.detail.lowercased().contains(q)
        }
    }

    func filtered(by filter: FilterState) -> [Term] {
        allTerms
            .filter { term in
                let indMatch = filter.indications.isEmpty
                    || !filter.indications.isDisjoint(with: Set(term.indications))
                let catMatch = filter.categories.isEmpty
                    || filter.categories.contains(term.category)
                return indMatch && catMatch
            }
            .sorted { $0.term.localizedCaseInsensitiveCompare($1.term) == .orderedAscending }
    }

    var allIndications: [String] {
        let counts = allTerms.reduce(into: [String: Int]()) { acc, term in
            for ind in term.indications { acc[ind, default: 0] += 1 }
        }
        return counts.keys.sorted { (counts[$0] ?? 0) > (counts[$1] ?? 0) }
    }

    var allCategories: [String] {
        let counts = allTerms.reduce(into: [String: Int]()) { acc, term in
            acc[term.category, default: 0] += 1
        }
        return counts.keys.sorted { (counts[$0] ?? 0) > (counts[$1] ?? 0) }
    }

    func indicationCount(_ name: String) -> Int {
        allTerms.reduce(0) { $0 + ($1.indications.contains(name) ? 1 : 0) }
    }

    func categoryCount(_ name: String) -> Int {
        allTerms.reduce(0) { $0 + ($1.category == name ? 1 : 0) }
    }
}
