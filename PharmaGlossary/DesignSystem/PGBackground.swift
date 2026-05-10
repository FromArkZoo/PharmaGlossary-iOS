import SwiftUI

/// Page background: warm paper base with a subtle oxblood radial wash anchored bottom-right.
struct PGBackground: View {
    var body: some View {
        ZStack {
            PGColors.bg
            RadialGradient(
                colors: [
                    PGColors.accent.opacity(0.10),
                    PGColors.accent.opacity(0.0)
                ],
                center: .bottomTrailing,
                startRadius: 0,
                endRadius: 620
            )
        }
        .ignoresSafeArea()
        .allowsHitTesting(false)
    }
}

#Preview {
    PGBackground()
}
