import SwiftUI

struct FavoritesView: View {
    @EnvironmentObject var store: GlossaryStore
    @State private var selectMode: Bool = false
    @State private var selected: Set<String> = []

    var body: some View {
        ZStack {
            PGBackground()
            content
        }
        .navigationTitle("Favorites")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                if !store.favoriteTerms.isEmpty {
                    Button(selectMode ? "Done" : "Select") {
                        if selectMode {
                            selected.removeAll()
                        }
                        selectMode.toggle()
                    }
                    .font(PGFont.toolbarStrong)
                    .foregroundStyle(PGColors.accent)
                }
            }
        }
        .safeAreaInset(edge: .bottom) {
            if selectMode {
                selectionToolbar
            }
        }
    }

    @ViewBuilder
    private var content: some View {
        let terms = store.favoriteTerms
        if terms.isEmpty {
            emptyState
        } else {
            List(terms) { term in
                row(for: term)
                    .listRowBackground(PGColors.card)
                    .listRowSeparatorTint(PGColors.inkRule)
            }
            .listStyle(.plain)
            .scrollContentBackground(.hidden)
        }
    }

    @ViewBuilder
    private func row(for term: Term) -> some View {
        if selectMode {
            Button {
                if selected.contains(term.term) {
                    selected.remove(term.term)
                } else {
                    selected.insert(term.term)
                }
            } label: {
                HStack(spacing: 12) {
                    Image(systemName: selected.contains(term.term) ? "checkmark.circle.fill" : "circle")
                        .font(.system(size: 20, weight: .regular))
                        .foregroundStyle(selected.contains(term.term) ? PGColors.accent : PGColors.inkFaint)
                    TermRow(term: term)
                }
            }
            .buttonStyle(.plain)
        } else {
            NavigationLink(value: Route.term(term)) {
                TermRow(term: term)
            }
        }
    }

    private var emptyState: some View {
        VStack(spacing: 14) {
            Image(systemName: "heart")
                .font(.system(size: 40, weight: .light))
                .foregroundStyle(PGColors.inkFaint)
            Text("No favorites yet")
                .font(PGFont.termRowTitle)
                .foregroundStyle(PGColors.ink)
            Text("Tap the heart on any term to save it here.")
                .font(PGFont.metaItalic)
                .foregroundStyle(PGColors.inkLight)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 40)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private var selectionToolbar: some View {
        HStack(spacing: 16) {
            Button {
                let all = store.favoriteTerms.map { $0.term }
                if selected.count == all.count {
                    selected.removeAll()
                } else {
                    selected = Set(all)
                }
            } label: {
                Text(selected.count == store.favoriteTerms.count ? "Clear" : "Select all")
                    .font(PGFont.toolbarStrong)
                    .foregroundStyle(PGColors.accent)
            }

            Spacer()

            Text("\(selected.count) selected")
                .font(PGFont.metaItalic)
                .foregroundStyle(PGColors.inkLight)

            Spacer()

            ShareLink(item: bulkShareText) {
                Label("Share", systemImage: "square.and.arrow.up")
                    .font(PGFont.toolbarStrong)
            }
            .disabled(selected.isEmpty)
            .foregroundStyle(selected.isEmpty ? PGColors.inkFaint : PGColors.accent)
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 14)
        .background(.ultraThinMaterial)
    }

    private var bulkShareText: String {
        let chosen = store.favoriteTerms.filter { selected.contains($0.term) }
        return chosen.map { $0.shareText }.joined(separator: "\n\n---\n\n")
    }
}
