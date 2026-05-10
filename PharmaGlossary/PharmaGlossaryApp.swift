import SwiftUI
import UIKit

@main
struct PharmaGlossaryApp: App {
    @StateObject private var store = GlossaryStore()

    init() {
        Self.configureNavigationBarAppearance()
    }

    var body: some Scene {
        WindowGroup {
            ContentRouter()
                .environmentObject(store)
                .tint(PGColors.accent)
        }
    }

    /// Inline navigation titles (back-page headers) get a serif font and ink color
    /// so they sit on the cream paper without clashing with the editorial body.
    /// Large titles are intentionally NOT customized here — RootView uses a custom
    /// in-content header instead so we can do "JB Pharma" with an italic oxblood
    /// "Pharma" that the system title style can't express.
    private static func configureNavigationBarAppearance() {
        let appearance = UINavigationBarAppearance()
        appearance.configureWithOpaqueBackground()
        appearance.backgroundColor = UIColor(PGColors.bg)
        appearance.shadowColor = .clear

        let inlineDescriptor = UIFontDescriptor
            .preferredFontDescriptor(withTextStyle: .headline)
            .withDesign(.serif) ??
            UIFontDescriptor.preferredFontDescriptor(withTextStyle: .headline)
        let inlineFont = UIFont(descriptor: inlineDescriptor, size: 0)

        appearance.titleTextAttributes = [
            .font: inlineFont,
            .foregroundColor: UIColor(PGColors.ink)
        ]

        UINavigationBar.appearance().standardAppearance = appearance
        UINavigationBar.appearance().scrollEdgeAppearance = appearance
        UINavigationBar.appearance().compactAppearance = appearance
    }
}
