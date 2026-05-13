import SwiftUI

struct AboutView: View {
    var body: some View {
        ZStack {
            PGBackground()
            ScrollView {
                VStack(alignment: .leading, spacing: 24) {
                    disclaimer
                    sources
                    Spacer(minLength: 24)
                }
                .padding(.horizontal, 20)
                .padding(.top, 12)
            }
        }
        .navigationTitle("About")
        .navigationBarTitleDisplayMode(.inline)
    }

    private var disclaimer: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("ABOUT")
                .font(PGFont.eyebrow)
                .tracking(1.8)
                .foregroundStyle(PGColors.accent)

            ForEach(Brand.current.aboutParagraphs, id: \.self) { paragraph in
                Text(paragraph)
                    .font(PGFont.body)
                    .foregroundStyle(PGColors.ink)
                    .lineSpacing(3)
            }

            if !Brand.current.aboutDisclaimer.isEmpty {
                Text(Brand.current.aboutDisclaimer)
                    .font(PGFont.snappyItalic)
                    .foregroundStyle(PGColors.accent)
                    .padding(.top, 4)
            }
        }
    }

    private var sources: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("SOURCES")
                .font(PGFont.eyebrow)
                .tracking(1.8)
                .foregroundStyle(PGColors.accent)
                .padding(.top, 8)

            ForEach(Brand.current.aboutSources, id: \.heading) { group in
                sourceGroup(heading: group.heading, items: group.items)
            }
        }
    }

    private func sourceGroup(heading: String, items: [String]) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(heading)
                .font(PGFont.policyTitle)
                .foregroundStyle(PGColors.ink)
            ForEach(items, id: \.self) { item in
                Text(LocalizedStringKey(linkifiedSource(item)))
                    .font(PGFont.body)
                    .foregroundStyle(PGColors.inkLight)
                    .tint(PGColors.accent)
                    .lineSpacing(2)
                    .accessibilityHint("Opens \(item) website in browser.")
            }
        }
    }

    /// "FDA — Food and Drug Administration"
    ///   → "[FDA](https://www.fda.gov) — Food and Drug Administration"
    private func linkifiedSource(_ item: String) -> String {
        guard let dashRange = item.range(of: " — ") else { return item }
        let abbrev = String(item[..<dashRange.lowerBound])
        let rest = String(item[dashRange.lowerBound...])
        if let url = Brand.sourceURLs[abbrev] {
            return "[\(abbrev)](\(url.absoluteString))\(rest)"
        }
        return item
    }
}

#Preview {
    NavigationStack { AboutView() }
}
