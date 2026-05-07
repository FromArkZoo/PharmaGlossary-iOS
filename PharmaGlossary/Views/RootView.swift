import SwiftUI

struct RootView: View {
    @EnvironmentObject var store: GlossaryStore
    @State private var query: String = ""
    @State private var filter = FilterState()
    @State private var showingFilter = false
    @State private var path: [Route] = []

    private let columns = Array(repeating: GridItem(.flexible(), spacing: 10), count: 4)

    var body: some View {
        NavigationStack(path: $path) {
            ZStack {
                PGColors.bg.ignoresSafeArea()
                content
            }
            .navigationTitle(Brand.current.navigationTitle)
            .navigationBarTitleDisplayMode(.large)
            .searchable(text: $query, placement: .navigationBarDrawer(displayMode: .always),
                        prompt: "Search terms, abbreviations, definitions")
            .autocorrectionDisabled()
            .textInputAutocapitalization(.never)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        showingFilter = true
                    } label: {
                        Image(systemName: filter.isActive
                              ? "line.3.horizontal.decrease.circle.fill"
                              : "line.3.horizontal.decrease.circle")
                            .font(.system(size: 20, weight: .semibold))
                            .foregroundStyle(PGColors.primary)
                    }
                    .accessibilityLabel("Filter")
                }
            }
            .sheet(isPresented: $showingFilter) {
                FilterSheet(filter: $filter, onSelectPolicy: {
                    showingFilter = false
                    path.append(.policy)
                })
                .presentationDetents([.large])
            }
        }
    }

    @ViewBuilder
    private var content: some View {
        if !query.trimmingCharacters(in: .whitespaces).isEmpty {
            searchResults
        } else if filter.isActive {
            filteredResults
        } else {
            alphabetGrid
        }
    }

    private var alphabetGrid: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("\(store.allTerms.count) terms · \(Brand.current.subtitle)")
                    .font(PGFont.subtitle)
                    .foregroundStyle(PGColors.textLight)
                    .padding(.horizontal, 16)
                    .padding(.top, 8)

                LazyVGrid(columns: columns, spacing: 10) {
                    ForEach(store.alphabetLetters, id: \.self) { letter in
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
            case .policy:
                PolicyView()
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
            case .policy:
                PolicyView()
            }
        }
    }

    private var filteredResults: some View {
        let results = store.filtered(by: filter)
        return VStack(spacing: 0) {
            FilterPill(filter: filter, count: results.count) {
                filter = FilterState()
            }
            .padding(.horizontal, 16)
            .padding(.top, 8)
            .padding(.bottom, 4)

            if results.isEmpty {
                Spacer()
                VStack(spacing: 12) {
                    Image(systemName: "magnifyingglass")
                        .font(.system(size: 36))
                        .foregroundStyle(PGColors.textLight)
                    Text("No terms match these filters")
                        .font(PGFont.term)
                        .foregroundStyle(PGColors.text)
                    Button("Clear filters") { filter = FilterState() }
                        .font(.system(size: 14, weight: .semibold))
                        .foregroundStyle(PGColors.primary)
                }
                Spacer()
                Spacer()
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
            case .policy:
                PolicyView()
            }
        }
    }
}

private struct FilterPill: View {
    let filter: FilterState
    let count: Int
    let onClear: () -> Void

    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: "line.3.horizontal.decrease.circle.fill")
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(.white)
            Text(filter.summary)
                .font(.system(size: 14, weight: .medium))
                .foregroundStyle(.white)
                .lineLimit(1)
            Text("· \(count)")
                .font(.system(size: 13, weight: .medium))
                .foregroundStyle(.white.opacity(0.85))
            Spacer()
            Button(action: onClear) {
                Image(systemName: "xmark.circle.fill")
                    .font(.system(size: 16))
                    .foregroundStyle(.white.opacity(0.85))
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Clear filters")
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .background(
            LinearGradient(colors: [PGColors.primary, PGColors.primaryDark],
                           startPoint: .leading, endPoint: .trailing),
            in: Capsule()
        )
    }
}

enum Route: Hashable {
    case letter(String)
    case term(Term)
    case policy
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
