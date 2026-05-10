import SwiftUI

struct FilterSheet: View {
    @EnvironmentObject var store: GlossaryStore
    @Binding var filter: FilterState
    var onSelectPolicy: () -> Void
    var onSelectBasics: () -> Void
    var onSelectAbout: () -> Void
    @Environment(\.dismiss) private var dismiss

    private var matchCount: Int {
        store.filtered(by: filter).count
    }

    var body: some View {
        NavigationStack {
            ZStack {
                PGColors.bg.ignoresSafeArea()
                ScrollView {
                    VStack(alignment: .leading, spacing: 0) {
                        lensesSection

                        section(
                            title: "Indications",
                            options: sortedByLengthDescending(store.allIndications),
                            selected: filter.indications,
                            count: { store.indicationCount($0) },
                            toggle: { name in
                                if filter.indications.contains(name) {
                                    filter.indications.remove(name)
                                } else {
                                    filter.indications.insert(name)
                                }
                            }
                        )

                        section(
                            title: "Categories",
                            options: sortedByLengthDescending(store.allCategories),
                            selected: filter.categories,
                            count: { store.categoryCount($0) },
                            toggle: { name in
                                if filter.categories.contains(name) {
                                    filter.categories.remove(name)
                                } else {
                                    filter.categories.insert(name)
                                }
                            }
                        )

                        aboutLink
                    }
                    .padding(.horizontal, 16)
                    .padding(.top, 8)
                    .padding(.bottom, 110)
                }

                VStack {
                    Spacer()
                    applyBar
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .principal) {
                    Text("Filter")
                        .font(PGFont.filterTitleItalic)
                        .foregroundStyle(PGColors.ink)
                }
                ToolbarItem(placement: .topBarLeading) {
                    Button("Clear") { filter = FilterState() }
                        .font(PGFont.toolbarPlain)
                        .foregroundStyle(filter.isActive ? PGColors.inkLight : PGColors.inkFaint)
                        .disabled(!filter.isActive)
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { dismiss() }
                        .font(PGFont.toolbarStrong)
                        .foregroundStyle(PGColors.accent)
                }
            }
        }
    }

    private func sortedByLengthDescending(_ items: [String]) -> [String] {
        items.sorted { $0.count > $1.count }
    }

    private var lensesSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            sectionLabel("Lenses")
            lensCard(
                glyph: "P",
                title: "Policy",
                subtitle: "Regulation, pricing, access · \(store.policyTerms.count) terms",
                action: onSelectPolicy
            )
            lensCard(
                glyph: "B",
                title: "Basics",
                subtitle: "Foundational biology & chemistry · \(store.basicsTerms.count) terms",
                action: onSelectBasics
            )
        }
        .padding(.bottom, 4)
    }

    private func lensCard(glyph: String, title: String, subtitle: String, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            HStack(spacing: 12) {
                Text(glyph)
                    .font(PGFont.policyIcon)
                    .foregroundStyle(PGColors.bg)
                    .frame(width: 34, height: 34)
                    .background(PGColors.ink, in: RoundedRectangle(cornerRadius: 8, style: .continuous))
                VStack(alignment: .leading, spacing: 2) {
                    Text(title)
                        .font(PGFont.policyTitle)
                        .foregroundStyle(PGColors.ink)
                    Text(subtitle)
                        .font(PGFont.policySub)
                        .foregroundStyle(PGColors.inkLight)
                }
                Spacer()
                Image(systemName: "chevron.right")
                    .font(.system(size: 13, weight: .semibold))
                    .foregroundStyle(PGColors.inkFaint)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 10)
            .background(PGColors.card, in: RoundedRectangle(cornerRadius: 10, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .stroke(PGColors.cardBorder, lineWidth: 1)
            )
        }
        .buttonStyle(.plain)
    }

    @ViewBuilder
    private func section(title: String,
                         options: [String],
                         selected: Set<String>,
                         count: @escaping (String) -> Int,
                         toggle: @escaping (String) -> Void) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            sectionLabel(title)
            FlowLayout(spacing: 6) {
                ForEach(options, id: \.self) { name in
                    Chip(label: name,
                         count: count(name),
                         isSelected: selected.contains(name),
                         action: { toggle(name) })
                }
            }
        }
        .padding(.top, 14)
    }

    private var aboutLink: some View {
        HStack {
            Spacer()
            Button(action: onSelectAbout) {
                HStack(spacing: 6) {
                    Image(systemName: "info.circle")
                        .font(.system(size: 13, weight: .semibold))
                    Text("About JB Pharma")
                        .font(PGFont.policySub)
                }
                .foregroundStyle(PGColors.inkLight)
            }
            .buttonStyle(.plain)
            Spacer()
        }
        .padding(.top, 28)
    }

    private func sectionLabel(_ text: String) -> some View {
        Text(text.uppercased())
            .font(PGFont.eyebrow)
            .tracking(1.8)
            .foregroundStyle(PGColors.accent)
    }

    private var applyBar: some View {
        HStack {
            Text(filter.isActive ? "\(matchCount) terms match" : "All \(store.allTerms.count) terms")
                .font(PGFont.metaItalic)
                .foregroundStyle(PGColors.inkLight)
            Spacer()
            Button {
                dismiss()
            } label: {
                Text("APPLY")
                    .font(PGFont.applyLabel)
                    .tracking(1.4)
                    .foregroundStyle(PGColors.bg)
                    .padding(.horizontal, 22)
                    .padding(.vertical, 9)
                    .background(PGColors.accent, in: Capsule())
            }
            .disabled(filter.isActive && matchCount == 0)
            .opacity(filter.isActive && matchCount == 0 ? 0.4 : 1.0)
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
        .background(.ultraThinMaterial)
        .overlay(alignment: .top) {
            Rectangle()
                .fill(PGColors.inkRule)
                .frame(height: 1)
        }
    }
}

private struct Chip: View {
    let label: String
    let count: Int
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 5) {
                Text(label)
                    .font(PGFont.chip)
                Text("\(count)")
                    .font(PGFont.chipCountItalic)
                    .foregroundStyle(isSelected ? PGColors.accentTint : PGColors.inkFaint)
            }
            .foregroundStyle(isSelected ? PGColors.bg : PGColors.ink)
            .padding(.horizontal, 10)
            .padding(.vertical, 5)
            .background {
                if isSelected {
                    Capsule().fill(PGColors.ink)
                } else {
                    Capsule().fill(PGColors.card)
                }
            }
            .overlay(
                Capsule()
                    .stroke(isSelected ? Color.clear : PGColors.cardBorder, lineWidth: 1)
            )
        }
        .buttonStyle(.plain)
    }
}

struct FlowLayout: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let maxWidth = proposal.width ?? .infinity
        var x: CGFloat = 0
        var y: CGFloat = 0
        var rowHeight: CGFloat = 0
        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > maxWidth && x > 0 {
                x = 0
                y += rowHeight + spacing
                rowHeight = 0
            }
            x += size.width + spacing
            rowHeight = max(rowHeight, size.height)
        }
        return CGSize(width: maxWidth, height: y + rowHeight)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        var x = bounds.minX
        var y = bounds.minY
        var rowHeight: CGFloat = 0
        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > bounds.maxX && x > bounds.minX {
                x = bounds.minX
                y += rowHeight + spacing
                rowHeight = 0
            }
            subview.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(size))
            x += size.width + spacing
            rowHeight = max(rowHeight, size.height)
        }
    }
}
