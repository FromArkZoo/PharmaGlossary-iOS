import SwiftUI

/// Root view of JB Glossary. Lists every shipped industry as a tile;
/// tapping one mounts that industry's `RootView` via `IndustryShell`.
///
/// Tile lock state + paywall behavior land in Phase 3 (StoreKit). For now
/// every industry opens directly when tapped; the "$2.99" labels are
/// placeholder until purchase gating is wired up.
struct IndustryPickerView: View {
    let onSelectIndustry: (IndustryID) -> Void

    private let columns = [
        GridItem(.flexible(), spacing: 14),
        GridItem(.flexible(), spacing: 14),
    ]

    var body: some View {
        ZStack {
            PGColors.bg.ignoresSafeArea()
            ScrollView {
                VStack(spacing: 0) {
                    header
                        .padding(.horizontal, 20)
                        .padding(.top, 24)
                        .padding(.bottom, 24)

                    LazyVGrid(columns: columns, spacing: 14) {
                        ForEach(IndustryConfig.all) { config in
                            Button {
                                onSelectIndustry(config.id)
                            } label: {
                                IndustryTile(config: config)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.horizontal, 20)
                    .padding(.bottom, 32)
                }
            }
            .scrollIndicators(.hidden)
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack(alignment: .firstTextBaseline, spacing: 6) {
                Text("JB")
                    .font(PGFont.displayBold)
                    .foregroundStyle(PGColors.ink)
                Text("Glossary")
                    .font(PGFont.displayItalic)
                    .foregroundStyle(PGColors.ink)
            }

            Text("Pick an industry")
                .font(PGFont.metaItalic)
                .foregroundStyle(PGColors.inkLight)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

private struct IndustryTile: View {
    let config: IndustryConfig

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(config.brand.titleBody)
                .font(.system(size: 28, weight: .regular, design: .serif).italic())
                .foregroundStyle(config.brand.primaryColor)
                .lineLimit(1)
                .minimumScaleFactor(0.7)

            Text(priceLabel)
                .font(PGFont.eyebrow)
                .tracking(0.8)
                .foregroundStyle(config.isAlwaysFree ? config.brand.primaryColor : PGColors.inkLight)

            Text(config.brand.subtitle)
                .font(PGFont.metaItalic)
                .foregroundStyle(PGColors.inkLight)
                .lineLimit(2)
                .fixedSize(horizontal: false, vertical: true)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(16)
        .background(
            RoundedRectangle(cornerRadius: 12, style: .continuous)
                .fill(PGColors.card)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 12, style: .continuous)
                .stroke(PGColors.cardBorder, lineWidth: 1)
        )
    }

    private var priceLabel: String {
        config.isAlwaysFree ? "FREE" : "$2.99"
    }
}

#Preview {
    IndustryPickerView { _ in }
}
