import SwiftUI

enum PGColors {
    static let bg          = Color(red: 0.961, green: 0.937, blue: 0.902) // #F5EFE6 warm paper
    static let card        = Color.white
    static let cardBorder  = Color(red: 0.863, green: 0.824, blue: 0.761) // #DCD2C2

    static let ink         = Color(red: 0.106, green: 0.094, blue: 0.078) // #1B1814 ink black
    static let inkLight    = Color(red: 0.361, green: 0.329, blue: 0.314) // #5C5450 warm gray
    static let inkFaint    = Color(red: 0.557, green: 0.518, blue: 0.482) // #8E847B fade
    static let inkRule     = Color(red: 0.106, green: 0.094, blue: 0.078).opacity(0.18)

    static let accent      = Color(red: 0.545, green: 0.180, blue: 0.122) // #8B2E1F oxblood
    static let accentDark  = Color(red: 0.467, green: 0.137, blue: 0.094) // deeper oxblood
    static let accentTint  = Color(red: 0.784, green: 0.714, blue: 0.541) // #C8B68A used for selected count text

    // Aliases preserved for Brand.swift / PharmaGlossaryApp tint
    static let primary     = accent
    static let primaryDark = accentDark
    static let text        = ink
    static let textLight   = inkLight
}
