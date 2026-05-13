import SwiftUI

enum PGColors {
    static let bg          = Color(red: 0.961, green: 0.937, blue: 0.902) // #F5EFE6 warm paper
    static let card        = Color.white
    static let cardBorder  = Color(red: 0.863, green: 0.824, blue: 0.761) // #DCD2C2

    static let ink         = Color(red: 0.106, green: 0.094, blue: 0.078) // #1B1814 ink black
    static let inkLight    = Color(red: 0.361, green: 0.329, blue: 0.314) // #5C5450 warm gray
    static let inkFaint    = Color(red: 0.557, green: 0.518, blue: 0.482) // #8E847B fade
    static let inkRule     = Color(red: 0.106, green: 0.094, blue: 0.078).opacity(0.18)

    // Brand-driven accents. Each industry only needs to set primaryColor
    // (+ optional primaryDarkColor / accentTint overrides) in its Brand.
    static var accent: Color     { Brand.current.primaryColor }
    static var accentDark: Color { Brand.current.primaryDarkColor }
    static var accentTint: Color { Brand.current.accentTint ?? Brand.current.primaryColor.lightened(by: 0.40) }

    static var primary: Color     { accent }
    static var primaryDark: Color { accentDark }
    static let text      = ink
    static let textLight = inkLight
}

extension Color {
    /// HSB-space lightening: reduces saturation and raises brightness by `amount`
    /// (0...1). Used as a default tint when a Brand doesn't override accentTint.
    func lightened(by amount: CGFloat) -> Color {
        var h: CGFloat = 0, s: CGFloat = 0, b: CGFloat = 0, a: CGFloat = 0
        UIColor(self).getHue(&h, saturation: &s, brightness: &b, alpha: &a)
        return Color(hue: Double(h),
                     saturation: Double(max(0, s * (1 - amount))),
                     brightness: Double(min(1, b + amount * (1 - b))),
                     opacity: Double(a))
    }

    /// HSB-space darkening: scales brightness down by `amount` (0...1).
    func darkened(by amount: CGFloat) -> Color {
        var h: CGFloat = 0, s: CGFloat = 0, b: CGFloat = 0, a: CGFloat = 0
        UIColor(self).getHue(&h, saturation: &s, brightness: &b, alpha: &a)
        return Color(hue: Double(h),
                     saturation: Double(s),
                     brightness: Double(max(0, b * (1 - amount))),
                     opacity: Double(a))
    }
}
