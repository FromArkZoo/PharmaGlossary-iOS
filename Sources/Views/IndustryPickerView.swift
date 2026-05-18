import SwiftUI
import StoreKit

/// Root view of JB Glossary. Lists every shipped industry as a tile;
/// tapping an unlocked tile opens that industry's `RootView`, tapping a
/// locked tile presents `PaywallSheet`. Pharma is always unlocked (free
/// anchor industry); the rest are gated by `PurchaseManager`.
struct IndustryPickerView: View {
    @EnvironmentObject var purchases: PurchaseManager
    let onSelectIndustry: (IndustryID) -> Void

    @State private var paywallIndustry: IndustryID?

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
                                handleTap(config.id)
                            } label: {
                                IndustryTile(
                                    config: config,
                                    product: purchases.product(for: config.id),
                                    isUnlocked: purchases.isUnlocked(config.id)
                                )
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
        .sheet(item: $paywallIndustry) { id in
            PaywallSheet(targetIndustry: id)
                .environmentObject(purchases)
                .presentationDetents([.large])
        }
    }

    private func handleTap(_ id: IndustryID) {
        if purchases.isUnlocked(id) {
            onSelectIndustry(id)
        } else {
            paywallIndustry = id
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
    let product: Product?
    let isUnlocked: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .top) {
                Text(config.brand.titleBody)
                    .font(.system(size: 28, weight: .regular, design: .serif).italic())
                    .foregroundStyle(config.brand.primaryColor)
                    .lineLimit(1)
                    .minimumScaleFactor(0.7)
                Spacer(minLength: 4)
                if !isUnlocked {
                    Image(systemName: "lock.fill")
                        .font(.system(size: 11, weight: .semibold))
                        .foregroundStyle(PGColors.inkFaint)
                }
            }

            Text(priceLabel)
                .font(PGFont.eyebrow)
                .tracking(0.8)
                .foregroundStyle(priceColor)

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
        if config.isAlwaysFree { return "FREE" }
        if isUnlocked { return "UNLOCKED" }
        return product?.displayPrice ?? "$2.99"
    }

    private var priceColor: Color {
        if config.isAlwaysFree || isUnlocked {
            return config.brand.primaryColor
        }
        return PGColors.inkLight
    }
}
