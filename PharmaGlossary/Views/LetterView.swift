import SwiftUI

struct LetterView: View {
    let letter: String
    @EnvironmentObject var store: GlossaryStore

    private var terms: [Term] {
        (store.byLetter[letter] ?? [])
            .sorted { $0.term.localizedCaseInsensitiveCompare($1.term) == .orderedAscending }
    }

    var body: some View {
        ZStack {
            PGColors.bg.ignoresSafeArea()
            List(terms) { term in
                NavigationLink(value: Route.term(term)) {
                    TermRow(term: term)
                }
                .listRowBackground(PGColors.card)
                .listRowSeparatorTint(PGColors.inkRule)
            }
            .listStyle(.plain)
            .scrollContentBackground(.hidden)
        }
        .navigationTitle(letter)
        .navigationBarTitleDisplayMode(.inline)
    }
}
