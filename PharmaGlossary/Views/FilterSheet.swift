import SwiftUI

struct FilterSheet: View {
    @EnvironmentObject var store: GlossaryStore
    @Binding var filter: FilterState
    var onSelectPolicy: () -> Void
    @Environment(\.dismiss) private var dismiss

    private var matchCount: Int {
        store.filtered(by: filter).count
    }

    var body: some View {
        NavigationStack {
            ZStack {
                PGColors.bg.ignoresSafeArea()
                ScrollView {
                    VStack(alignment: .leading, spacing: 24) {
                        lensesSection
                        section(
                            title: "Indications",
                            options: store.allIndications,
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
                            options: store.allCategories,
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
                    }
                    .padding(.horizontal, 16)
                    .padding(.top, 12)
                    .padding(.bottom, 96)
                }

                VStack {
                    Spacer()
                    applyBar
                }
            }
            .navigationTitle("Filter")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Clear") { filter = FilterState() }
                        .disabled(!filter.isActive)
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { dismiss() }
                        .fontWeight(.semibold)
                }
            }
        }
    }

    private var lensesSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Lenses")
                .font(.system(size: 13, weight: .semibold))
                .foregroundStyle(PGColors.textLight)
                .textCase(.uppercase)
                .tracking(0.5)
            Button(action: onSelectPolicy) {
                HStack(spacing: 12) {
                    Image(systemName: "building.columns.fill")
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundStyle(.white)
                        .frame(width: 36, height: 36)
                        .background(
                            LinearGradient(colors: [PGColors.primary, PGColors.primaryDark],
                                           startPoint: .topLeading, endPoint: .bottomTrailing),
                            in: RoundedRectangle(cornerRadius: 10, style: .continuous)
                        )
                    VStack(alignment: .leading, spacing: 2) {
                        Text("Policy")
                            .font(.system(size: 15, weight: .semibold))
                            .foregroundStyle(PGColors.text)
                        Text("Regulation, pricing, access · \(store.policyTerms.count) terms")
                            .font(.system(size: 13))
                            .foregroundStyle(PGColors.textLight)
                    }
                    Spacer()
                    Image(systemName: "chevron.right")
                        .font(.system(size: 13, weight: .semibold))
                        .foregroundStyle(PGColors.textLight)
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 10)
                .background(PGColors.card, in: RoundedRectangle(cornerRadius: 12, style: .continuous))
                .overlay(
                    RoundedRectangle(cornerRadius: 12, style: .continuous)
                        .stroke(PGColors.textLight.opacity(0.15), lineWidth: 1)
                )
            }
            .buttonStyle(.plain)
        }
    }

    @ViewBuilder
    private func section(title: String,
                         options: [String],
                         selected: Set<String>,
                         count: @escaping (String) -> Int,
                         toggle: @escaping (String) -> Void) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title)
                .font(.system(size: 13, weight: .semibold))
                .foregroundStyle(PGColors.textLight)
                .textCase(.uppercase)
                .tracking(0.5)
            FlowLayout(spacing: 8) {
                ForEach(options, id: \.self) { name in
                    Chip(label: name,
                         count: count(name),
                         isSelected: selected.contains(name),
                         action: { toggle(name) })
                }
            }
        }
    }

    private var applyBar: some View {
        HStack {
            Text(filter.isActive ? "\(matchCount) terms match" : "All \(store.allTerms.count) terms")
                .font(.system(size: 14, weight: .medium))
                .foregroundStyle(PGColors.textLight)
            Spacer()
            Button {
                dismiss()
            } label: {
                Text("Apply")
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundStyle(.white)
                    .padding(.horizontal, 24)
                    .padding(.vertical, 12)
                    .background(
                        LinearGradient(colors: [PGColors.primary, PGColors.primaryDark],
                                       startPoint: .topLeading, endPoint: .bottomTrailing),
                        in: Capsule()
                    )
            }
            .disabled(filter.isActive && matchCount == 0)
            .opacity(filter.isActive && matchCount == 0 ? 0.4 : 1.0)
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
        .background(.ultraThinMaterial)
    }
}

private struct Chip: View {
    let label: String
    let count: Int
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 6) {
                Text(label)
                    .font(.system(size: 14, weight: .medium))
                Text("\(count)")
                    .font(.system(size: 12, weight: .medium))
                    .foregroundStyle(isSelected ? .white.opacity(0.8) : PGColors.textLight)
            }
            .foregroundStyle(isSelected ? Color.white : PGColors.text)
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background {
                if isSelected {
                    Capsule().fill(
                        LinearGradient(colors: [PGColors.primary, PGColors.primaryDark],
                                       startPoint: .topLeading, endPoint: .bottomTrailing)
                    )
                } else {
                    Capsule().fill(PGColors.card)
                }
            }
            .overlay(
                Capsule()
                    .stroke(isSelected ? Color.clear : PGColors.textLight.opacity(0.25), lineWidth: 1)
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
