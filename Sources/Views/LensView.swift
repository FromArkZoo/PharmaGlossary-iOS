import SwiftUI

/// Generic lens view — replaces the per-lens BasicsView/PolicyView pattern.
/// Each industry's Brand.lenses array drives both the filter-sheet cards
/// and the destination here; this view just dispatches to GlossaryStore
/// using the LensConfig.
struct LensView: View {
    let lens: LensConfig
    @EnvironmentObject var store: GlossaryStore

    private var terms: [Term] { store.terms(forLens: lens) }

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
        .navigationTitle(lens.title)
        .navigationBarTitleDisplayMode(.inline)
    }
}
