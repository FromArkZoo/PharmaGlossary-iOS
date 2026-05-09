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

    var detailCache: [String: AttributedString] = [:]

    static let policyCategories: Set<String> = ["Regulatory", "Commercial / Market Access"]
    static let policyExcludedTerms: Set<String> = [
        "MSL", "Loss of Exclusivity", "Patent Cliff", "NCI", "HEOR", "Gross-to-Net", "Phase 4"
    ]

    var alphabetLetters: [String] {
        letters.filter { $0.range(of: "^[A-Z]$", options: .regularExpression) != nil }
    }

    var policyTerms: [Term] {
        allTerms
            .filter { Self.policyCategories.contains($0.category) && !Self.policyExcludedTerms.contains($0.term) }
            .sorted { $0.term.localizedCaseInsensitiveCompare($1.term) == .orderedAscending }
    }

    init() {
        load()
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
