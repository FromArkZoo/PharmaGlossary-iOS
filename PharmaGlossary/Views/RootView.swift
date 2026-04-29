import SwiftUI

struct RootView: View {
    @EnvironmentObject var store: GlossaryStore
    @State private var query: String = ""

    private let columns = Array(repeating: GridItem(.flexible(), spacing: 10), count: 4)

    var body: some View {
        NavigationStack {
            ZStack {
                PGColors.bg.ignoresSafeArea()
                content
            }
            .navigationTitle("Pharma Glossary")
            .navigationBarTitleDisplayMode(.large)
            .searchable(text: $query, placement: .navigationBarDrawer(displayMode: .always),
                        prompt: "Search terms, abbreviations, definitions")
            .autocorrectionDisabled()
            .textInputAutocapitalization(.never)
        }
    }

    @ViewBuilder
    private var content: some View {
        if query.trimmingCharacters(in: .whitespaces).isEmpty {
            alphabetGrid
        } else {
            searchResults
        }
    }

    private var alphabetGrid: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("\(store.allTerms.count) terms across cancer types, mutations, and drug terminology")
                    .font(PGFont.subtitle)
                    .foregroundStyle(PGColors.textLight)
                    .padding(.horizontal, 16)
                    .padding(.top, 8)

                LazyVGrid(columns: columns, spacing: 10) {
                    ForEach(store.letters, id: \.self) { letter in
                        NavigationLink(value: Route.letter(letter)) {
                            LetterTile(letter: letter,
                                       count: store.byLetter[letter]?.count ?? 0)
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, 16)
                .padding(.bottom, 24)
            }
        }
        .navigationDestination(for: Route.self) { route in
            switch route {
            case .letter(let letter):
                LetterView(letter: letter)
            case .term(let term):
                TermDetailView(term: term)
            }
        }
    }

    private var searchResults: some View {
        let results = store.search(query)
        return Group {
            if results.isEmpty {
                ContentUnavailableView.search(text: query)
            } else {
                List(results) { term in
                    NavigationLink(value: Route.term(term)) {
                        TermRow(term: term)
                    }
                    .listRowBackground(PGColors.card)
                }
                .listStyle(.plain)
                .scrollContentBackground(.hidden)
            }
        }
        .navigationDestination(for: Route.self) { route in
            switch route {
            case .letter(let letter):
                LetterView(letter: letter)
            case .term(let term):
                TermDetailView(term: term)
            }
        }
    }
}

enum Route: Hashable {
    case letter(String)
    case term(Term)
}

private struct LetterTile: View {
    let letter: String
    let count: Int

    var body: some View {
        VStack(spacing: 2) {
            Text(letter)
                .font(PGFont.letterTile)
                .foregroundStyle(.white)
            Text("\(count)")
                .font(.system(size: 11, weight: .medium))
                .foregroundStyle(.white.opacity(0.85))
        }
        .frame(maxWidth: .infinity)
        .frame(height: 64)
        .background(
            LinearGradient(colors: [PGColors.primary, PGColors.primaryDark],
                           startPoint: .topLeading, endPoint: .bottomTrailing)
        )
        .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
        .shadow(color: PGColors.primary.opacity(0.25), radius: 6, x: 0, y: 3)
    }
}

struct TermRow: View {
    let term: Term

    var body: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(term.term)
                .font(PGFont.term)
                .foregroundStyle(PGColors.text)
            if term.hasFull {
                Text(term.full)
                    .font(PGFont.full)
                    .foregroundStyle(PGColors.textLight)
            }
        }
        .padding(.vertical, 4)
    }
}
