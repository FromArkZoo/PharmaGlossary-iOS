import SwiftUI

struct FavoritesView: View {
    @EnvironmentObject var store: GlossaryStore
    @State private var selectMode: Bool = false
    @State private var selected: Set<String> = []
    @State private var lastRemoved: Term?
    @State private var undoTask: Task<Void, Never>?

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
            } else if lastRemoved != nil {
                undoBanner
            }
        }
        .onDisappear {
            undoTask?.cancel()
            lastRemoved = nil
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
                    .swipeActions(edge: .trailing, allowsFullSwipe: true) {
                        if !selectMode {
                            Button(role: .destructive) {
                                remove(term)
                            } label: {
                                Label("Remove", systemImage: "star.slash.fill")
                            }
                        }
                    }
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
            Image(systemName: "star")
                .font(.system(size: 40, weight: .light))
                .foregroundStyle(PGColors.inkFaint)
            Text("No favorites yet")
                .font(PGFont.termRowTitle)
                .foregroundStyle(PGColors.ink)
            Text("Tap the star on any term to save it here.")
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

    private var undoBanner: some View {
        HStack(spacing: 12) {
            Image(systemName: "star.slash.fill")
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(PGColors.inkLight)
            Text("Removed \(lastRemoved?.term ?? "")")
                .font(PGFont.metaItalic)
                .foregroundStyle(PGColors.ink)
                .lineLimit(1)
            Spacer()
            Button {
                undo()
            } label: {
                Text("Undo")
                    .font(PGFont.toolbarStrong)
                    .foregroundStyle(PGColors.accent)
            }
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 14)
        .background(.ultraThinMaterial)
        .transition(.move(edge: .bottom).combined(with: .opacity))
        .animation(.easeOut(duration: 0.25), value: lastRemoved?.id)
    }

    private var bulkShareText: String {
        let chosen = store.favoriteTerms.filter { selected.contains($0.term) }
        return chosen.map { $0.shareText }.joined(separator: "\n\n---\n\n")
    }

    private func remove(_ term: Term) {
        guard store.isFavorited(term) else { return }
        store.toggleFavorite(term)
        lastRemoved = term
        undoTask?.cancel()
        undoTask = Task {
            try? await Task.sleep(for: .seconds(4))
            guard !Task.isCancelled else { return }
            await MainActor.run { lastRemoved = nil }
        }
    }

    private func undo() {
        guard let term = lastRemoved else { return }
        if !store.isFavorited(term) {
            store.toggleFavorite(term)
        }
        undoTask?.cancel()
        lastRemoved = nil
    }
}
