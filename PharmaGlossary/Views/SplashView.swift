import SwiftUI

struct SplashView: View {
    @State private var pulse = false

    var body: some View {
        ZStack {
            PGBackground()

            VStack(spacing: 28) {
                HStack(alignment: .firstTextBaseline, spacing: 6) {
                    Text(Brand.current.titlePrefix)
                        .font(PGFont.displayBold)
                        .foregroundStyle(PGColors.ink)
                    Text(Brand.current.titleBody)
                        .font(PGFont.displayItalic)
                        .foregroundStyle(Brand.current.primaryColor)
                }

                pulsingDots
            }
        }
        .onAppear { pulse = true }
    }

    private var pulsingDots: some View {
        HStack(spacing: 8) {
            ForEach(0..<3, id: \.self) { i in
                Circle()
                    .fill(Brand.current.primaryColor)
                    .frame(width: 6, height: 6)
                    .opacity(pulse ? 1.0 : 0.25)
                    .animation(
                        .easeInOut(duration: 0.65)
                        .repeatForever(autoreverses: true)
                        .delay(Double(i) * 0.18),
                        value: pulse
                    )
            }
        }
    }
}

#Preview {
    SplashView()
}
