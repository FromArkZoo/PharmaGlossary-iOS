import SwiftUI

struct LetterView: View {
    let letter: String
    @EnvironmentObject var store: GlossaryStore

    private var terms: [Term] {
        store.byLetter[letter] ?? []
    }

    var body: some View {
        ZStack {
            PGColors.bg.ignoresSafeArea()
            List(terms) { term in
                NavigationLink(value: Route.term(term)) {
                    TermRow(term: term)
                }
                .listRowBackground(PGColors.card)
            }
            .listStyle(.plain)
            .scrollContentBackground(.hidden)
        }
        .navigationTitle("\(letter) · \(terms.count) terms")
        .navigationBarTitleDisplayMode(.inline)
    }
}
