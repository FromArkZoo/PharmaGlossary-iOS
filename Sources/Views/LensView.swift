import SwiftUI

/// Generic lens view — replaces the per-lens BasicsView/PolicyView pattern.
/// Each industry's Brand.lenses array drives both the filter-sheet cards
/// and the destination here; this view just dispatches to GlossaryStore
/// using the LensConfig.
struct LensView: View {
    let lens: LensConfig
    @EnvironmentObject var store: GlossaryStore
    @EnvironmentObject var purchases: PurchaseManager
    @State private var showingPaywall = false

    private var terms: [Term] { store.terms(forLens: lens) }

    var body: some View {
        ZStack {
            PGBackground()
            List(terms) { term in
                lockableRow(term: term)
                    .listRowBackground(PGColors.card)
                    .listRowSeparatorTint(PGColors.inkRule)
            }
            .listStyle(.plain)
            .scrollContentBackground(.hidden)
        }
        .navigationTitle(lens.title)
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $showingPaywall) {
            PaywallSheet(targetIndustry: store.industryID)
                .environmentObject(purchases)
                .presentationDetents([.large])
        }
    }

    @ViewBuilder
    private func lockableRow(term: Term) -> some View {
        let isLocked = purchases.isLocked(term, in: store.industryID)
        if isLocked {
            Button {
                showingPaywall = true
            } label: {
                TermRow(term: term).lockedAffordance(true)
            }
            .buttonStyle(.plain)
        } else {
            NavigationLink(value: Route.term(term)) {
                TermRow(term: term)
            }
        }
    }
}
