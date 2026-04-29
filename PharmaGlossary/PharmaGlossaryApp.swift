import SwiftUI

@main
struct PharmaGlossaryApp: App {
    @StateObject private var store = GlossaryStore()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(store)
                .tint(PGColors.primary)
        }
    }
}
