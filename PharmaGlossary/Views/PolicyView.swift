import SwiftUI

struct PolicyView: View {
    @EnvironmentObject var store: GlossaryStore

    private var terms: [Term] { store.policyTerms }

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
        .navigationTitle("Policy")
        .navigationBarTitleDisplayMode(.inline)
    }
}
