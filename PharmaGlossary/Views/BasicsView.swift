import SwiftUI

struct BasicsView: View {
    @EnvironmentObject var store: GlossaryStore

    private var terms: [Term] { store.basicsTerms }

    var body: some View {
        ZStack {
            PGBackground()
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
        .navigationTitle("Basics")
        .navigationBarTitleDisplayMode(.inline)
    }
}
