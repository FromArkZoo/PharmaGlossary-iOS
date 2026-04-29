import Foundation

struct Term: Codable, Identifiable, Hashable {
    let letter: String
    let term: String
    let full: String
    let definition: String

    var id: String { "\(letter)::\(term)" }

    var hasFull: Bool { !full.isEmpty }
}

@MainActor
final class GlossaryStore: ObservableObject {
    @Published private(set) var allTerms: [Term] = []
    @Published private(set) var byLetter: [String: [Term]] = [:]
    @Published private(set) var letters: [String] = []

    init() {
        load()
    }

    private func load() {
        guard let url = Bundle.main.url(forResource: "glossary", withExtension: "json") else {
            assertionFailure("glossary.json missing from bundle")
            return
        }
        do {
            let data = try Data(contentsOf: url)
            let terms = try JSONDecoder().decode([Term].self, from: data)
            self.allTerms = terms
            self.byLetter = Dictionary(grouping: terms, by: { $0.letter })
            self.letters = byLetter.keys.sorted()
        } catch {
            assertionFailure("Failed to decode glossary.json: \(error)")
        }
    }

    func search(_ query: String) -> [Term] {
        let q = query.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        guard !q.isEmpty else { return [] }
        return allTerms.filter {
            $0.term.lowercased().contains(q)
                || $0.full.lowercased().contains(q)
                || $0.definition.lowercased().contains(q)
        }
    }
}
