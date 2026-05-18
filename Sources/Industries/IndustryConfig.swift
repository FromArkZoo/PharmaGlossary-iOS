import Foundation

/// Canonical identifier for each industry shipped inside JB Glossary.
///
/// Adding industry #5+: append a case here, create a `Sources/Industries/<Industry>Brand.swift`,
/// register it in `IndustryConfig.all`, and add a `glossary_<industry>.json` to the bundle.
enum IndustryID: String, CaseIterable, Identifiable, Codable {
    case pharma
    case ai
    case law
    case finance

    var id: String { rawValue }

    /// The always-free anchor industry. Every install gets this unlocked.
    static let freeAnchor: IndustryID = .pharma
}

/// Pairs an industry's brand identity with its StoreKit product (if any).
struct IndustryConfig: Identifiable {
    let id: IndustryID
    let brand: Brand
    /// `nil` means the industry is always free (Pharma). Otherwise this is the
    /// StoreKit product identifier the user purchases to unlock the industry.
    let iapProductID: String?

    var isAlwaysFree: Bool { iapProductID == nil }
}

extension IndustryConfig {
    /// Registry — order here is the canonical display order in the picker.
    static let all: [IndustryConfig] = [
        .init(id: .pharma,  brand: pharmaBrand,  iapProductID: nil),
        .init(id: .ai,      brand: aiBrand,      iapProductID: "com.jamesbrowne.JBGlossary.ai"),
        .init(id: .law,     brand: lawBrand,     iapProductID: "com.jamesbrowne.JBGlossary.law"),
        .init(id: .finance, brand: financeBrand, iapProductID: "com.jamesbrowne.JBGlossary.finance"),
    ]

    /// Look up an industry by ID. Safe to force-unwrap because `IndustryID`
    /// cases are 1:1 with `all` entries; a missing case is a programmer error.
    static func config(for id: IndustryID) -> IndustryConfig {
        all.first { $0.id == id }!
    }

    /// Set the global `Brand.current` so all existing call sites (PGColors,
    /// AboutView, FilterSheet, SplashView, Hyperlinks, GlossaryStore, etc.)
    /// see the right industry's brand. Call before mounting an industry's
    /// view tree.
    static func activate(_ id: IndustryID) {
        Brand.current = config(for: id).brand
    }
}

/// StoreKit product identifier for the master "All Industries" unlock.
/// Owners get every current and future paid industry as a free entitlement.
let masterUnlockProductID = "com.jamesbrowne.JBGlossary.all"
