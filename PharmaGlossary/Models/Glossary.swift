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

@MainActor
final class GlossaryStore: ObservableObject {
    @Published private(set) var allTerms: [Term] = []
    @Published private(set) var byLetter: [String: [Term]] = [:]
    @Published private(set) var letters: [String] = []

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
        } catch {
            assertionFailure("Failed to decode \(Brand.current.dataResource).json: \(error)")
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
}
