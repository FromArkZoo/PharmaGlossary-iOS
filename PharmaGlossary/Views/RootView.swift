import SwiftUI

enum Route: Hashable {
    case letter(String)
    case term(Term)
    case policy
}

struct RootView: View {
    @EnvironmentObject var store: GlossaryStore
    @State private var query: String = ""
    @State private var filter = FilterState()
    @State private var showingFilter = false
    @State private var path: [Route] = []

    private let columns = Array(repeating: GridItem(.flexible(minimum: 50), spacing: 6), count: 4)

    var body: some View {
        NavigationStack(path: $path) {
            ZStack {
                PGColors.bg.ignoresSafeArea()
                VStack(spacing: 0) {
                    if shouldShowEditorialHeader {
                        EditorialHeader(brand: .current, entryCount: store.allTerms.count)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding(.horizontal, 20)
                            .padding(.top, 8)
                            .padding(.bottom, 16)
                    }

                    PGSearchBar(text: $query)
                        .padding(.horizontal, 20)
                        .padding(.bottom, 12)

                    content
                }
            }
            .navigationTitle("")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(PGColors.bg, for: .navigationBar)
            .toolbarBackground(.visible, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        showingFilter = true
                    } label: {
                        Image(systemName: filter.isActive
                              ? "line.3.horizontal.decrease.circle.fill"
                              : "line.3.horizontal.decrease.circle")
                            .font(.system(size: 19, weight: .semibold))
                            .foregroundStyle(PGColors.accent)
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
        .tint(PGColors.accent)
        .environment(\.openURL, OpenURLAction { url in
            if let term = store.term(matchingURL: url) {
                path.append(.term(term))
                return .handled
            }
            return .systemAction
        })
    }

    private var shouldShowEditorialHeader: Bool {
        query.trimmingCharacters(in: .whitespaces).isEmpty && !filter.isActive
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
            LazyVGrid(columns: columns, spacing: 6) {
                ForEach(store.alphabetLetters, id: \.self) { letter in
                    NavigationLink(value: Route.letter(letter)) {
                        LetterTile(letter: letter,
                                   count: store.byLetter[letter]?.count ?? 0)
                    }
                    .buttonStyle(.plain)
                }
            }
            .padding(.horizontal, 20)
            .padding(.top, 4)
            .padding(.bottom, 24)
        }
        .scrollDismissesKeyboard(.immediately)
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
                    .listRowSeparatorTint(PGColors.inkRule)
                }
                .listStyle(.plain)
                .scrollContentBackground(.hidden)
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
                VStack(spacing: 10) {
                    Image(systemName: "magnifyingglass")
                        .font(.system(size: 32))
                        .foregroundStyle(PGColors.inkFaint)
                    Text("No terms match these filters")
                        .font(PGFont.termRowTitle)
                        .foregroundStyle(PGColors.ink)
                    Button("Clear filters") { filter = FilterState() }
                        .font(PGFont.buttonLabel)
                        .foregroundStyle(PGColors.accent)
                }
                Spacer()
                Spacer()
            } else {
                List(results) { term in
                    NavigationLink(value: Route.term(term)) {
                        TermRow(term: term)
                    }
                    .listRowBackground(PGColors.card)
                    .listRowSeparatorTint(PGColors.inkRule)
                }
                .listStyle(.plain)
                .scrollContentBackground(.hidden)
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
                .foregroundStyle(PGColors.bg)
            Text(filter.summary)
                .font(.system(size: 13, weight: .medium))
                .foregroundStyle(PGColors.bg)
                .lineLimit(1)
            Text("· \(count)")
                .font(PGFont.chipCountItalic)
                .foregroundStyle(PGColors.accentTint)
            Spacer()
            Button(action: onClear) {
                Image(systemName: "xmark.circle.fill")
                    .font(.system(size: 16))
                    .foregroundStyle(PGColors.bg.opacity(0.85))
            }
            .buttonStyle(.plain)
            .accessibilityLabel("Clear filters")
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .background(PGColors.ink, in: Capsule())
    }
}

private struct LetterTile: View {
    let letter: String
    let count: Int

    var body: some View {
        VStack(spacing: 2) {
            Text(letter)
                .font(PGFont.letterTileItalic)
                .foregroundStyle(PGColors.ink)
            Text("\(count)")
                .font(PGFont.tileCount)
                .foregroundStyle(PGColors.inkFaint)
        }
        .frame(maxWidth: .infinity, minHeight: 56)
        .padding(.vertical, 4)
        .background(
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .fill(PGColors.card)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .stroke(PGColors.cardBorder, lineWidth: 1)
        )
    }
}

struct TermRow: View {
    let term: Term

    var body: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(term.term)
                .font(PGFont.termRowTitle)
                .foregroundStyle(PGColors.ink)
            if term.hasFull {
                Text(term.full)
                    .font(PGFont.termRowFullItalic)
                    .foregroundStyle(PGColors.inkLight)
            }
        }
        .padding(.vertical, 4)
    }
}
