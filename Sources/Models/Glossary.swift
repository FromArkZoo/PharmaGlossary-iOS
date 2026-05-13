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

    /// "Source: [FDA](https://www.fda.gov), [NIH](https://www.nih.gov)".
    /// Each source name becomes a markdown link if `Brand.sourceURLs` has
    /// a matching key; otherwise it renders as plain text.
    var sourcesMarkdown: String {
        let urls = Brand.current.sourceURLs
        let parts = sources.map { name -> String in
            if let url = urls[name] {
                return "[\(name)](\(url.absoluteString))"
            }
            return name
        }
        return "Source: " + parts.joined(separator: ", ")
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

    var alphabetLetters: [String] {
        letters.filter { $0.range(of: "^[A-Z]$", options: .regularExpression) != nil }
    }

    var policyTerms: [Term] {
        let cfg = Brand.current.policyConfig
        return allTerms
            .filter { cfg.categories.contains($0.category) && !cfg.excludedTerms.contains($0.term) }
            .sorted { $0.term.localizedCaseInsensitiveCompare($1.term) == .orderedAscending }
    }

    var basicsTerms: [Term] {
        let allow = Brand.current.basicsAllowlist
        return allTerms
            .filter { allow.contains($0.term) }
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
        let urlScheme = Brand.current.urlScheme
        Task.detached(priority: .utility) { [weak self] in
            var built: [String: AttributedString] = [:]
            built.reserveCapacity(terms.count)
            for term in terms {
                built[term.id] = Self.computeAttributedDetail(for: term, against: terms, urlScheme: urlScheme)
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
