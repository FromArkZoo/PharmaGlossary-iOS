import SwiftUI

/// Shows SplashView at launch until the data is loaded AND a minimum
/// display window has elapsed, then crossfades to RootView. The min
/// window guarantees the splash is actually visible even when JSON
/// loads in <100ms — without it the user just sees a flash.
struct ContentRouter: View {
    @EnvironmentObject var store: GlossaryStore
    @State private var minTimeReached = false

    private var isReady: Bool {
        !store.allTerms.isEmpty && minTimeReached
    }

    var body: some View {
        ZStack {
            if isReady {
                RootView()
                    .transition(.opacity)
            } else {
                SplashView()
                    .transition(.opacity)
            }
        }
        .animation(.easeInOut(duration: 0.35), value: isReady)
        .task {
            try? await Task.sleep(for: .milliseconds(1200))
            minTimeReached = true
        }
    }
}
