import SwiftUI

/// Visual affordance for locked content: dims the view and adds a `lock.fill`
/// icon at the requested edge. Pair with a `Button` (rather than `NavigationLink`)
/// that presents `PaywallSheet` for the actual tap behavior.
///
/// Use `.trailing` for row layouts (search/filter/lens/favorites lists where
/// each row is a horizontal `TermRow`). Use `.topTrailing` for square tile
/// layouts (the alphabet grid in `RootView`).
extension View {
    func lockedAffordance(_ isLocked: Bool, iconAlignment: Alignment = .trailing) -> some View {
        modifier(LockedAffordanceModifier(isLocked: isLocked, alignment: iconAlignment))
    }
}

private struct LockedAffordanceModifier: ViewModifier {
    let isLocked: Bool
    let alignment: Alignment

    func body(content: Content) -> some View {
        content
            .opacity(isLocked ? 0.55 : 1.0)
            .overlay(alignment: alignment) {
                if isLocked {
                    Image(systemName: "lock.fill")
                        .font(.system(size: alignment == .topTrailing ? 10 : 13, weight: .semibold))
                        .foregroundStyle(PGColors.inkFaint)
                        .padding(.top, alignment == .topTrailing ? 4 : 0)
                        .padding(.trailing, alignment == .topTrailing ? 4 : 6)
                }
            }
    }
}
