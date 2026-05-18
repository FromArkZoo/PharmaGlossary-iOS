import SwiftUI
import UIKit

@main
struct JBGlossaryApp: App {
    @State private var currentIndustryID: IndustryID? = Self.persistedIndustry()
    @StateObject private var purchases = PurchaseManager()

    init() {
        Self.configureNavigationBarAppearance()
    }

    var body: some Scene {
        WindowGroup {
            Group {
                // Gate on isUnlocked so a user whose entitlement got revoked
                // (refund, family-sharing change) falls back to the picker
                // instead of opening locked content.
                if let id = currentIndustryID, purchases.isUnlocked(id) {
                    IndustryShell(industryID: id, onSwitchIndustry: {
                        currentIndustryID = nil
                    })
                    .id(id) // remount the shell when the industry changes
                } else {
                    IndustryPickerView { id in
                        UserDefaults.standard.set(id.rawValue, forKey: Self.lastIndustryKey)
                        currentIndustryID = id
                    }
                }
            }
            .environmentObject(purchases)
            .tint(PGColors.accent)
        }
    }

    private static let lastIndustryKey = "jbglossary.lastIndustry"

    private static func persistedIndustry() -> IndustryID? {
        guard let raw = UserDefaults.standard.string(forKey: lastIndustryKey),
              let id = IndustryID(rawValue: raw) else { return nil }
        return id
    }

    /// Inline navigation titles (back-page headers) get a serif font and ink color
    /// so they sit on the cream paper without clashing with the editorial body.
    /// Large titles are intentionally NOT customized here — RootView uses a custom
    /// in-content header instead so we can do "JB <Brand>" with an italic accent
    /// "<Brand>" that the system title style can't express.
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

/// Owns the per-industry `GlossaryStore` and hands the "go back to picker"
/// callback down to `RootView`. Re-mounted (via `.id(industryID)`) every time
/// the user switches industry, so every store starts fresh — no state leak
/// between industries.
struct IndustryShell: View {
    let industryID: IndustryID
    let onSwitchIndustry: () -> Void
    @StateObject private var store: GlossaryStore

    init(industryID: IndustryID, onSwitchIndustry: @escaping () -> Void) {
        self.industryID = industryID
        self.onSwitchIndustry = onSwitchIndustry
        _store = StateObject(wrappedValue: GlossaryStore(industryID: industryID))
    }

    var body: some View {
        ContentRouter(onSwitchIndustry: onSwitchIndustry)
            .environmentObject(store)
    }
}
