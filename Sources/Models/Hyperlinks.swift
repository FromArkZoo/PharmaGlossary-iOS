import Foundation
import SwiftUI

extension GlossaryStore {
    /// Builds an AttributedString for a term's detail body, with every reference to
    /// another known term wrapped as a tappable `<brand-scheme>://term/<name>` link
    /// styled in the brand accent color with a thin underline. Result is cached
    /// per-term — the regex pass is the dominant cost of pushing a TermDetailView,
    /// so caching makes repeat navigations effectively free.
    func attributedDetail(for term: Term) -> AttributedString {
        if let cached = detailCache[term.id] { return cached }
        let built = Self.computeAttributedDetail(for: term, against: allTerms, urlScheme: Brand.current.urlScheme)
        detailCache[term.id] = built
        return built
    }

    nonisolated static func computeAttributedDetail(for term: Term, against allTerms: [Term], urlScheme: String) -> AttributedString {
        var attributed = AttributedString(term.detail)
        guard !term.detail.isEmpty else { return attributed }

        // Sort longest-first so "monoclonal antibody" wins over "antibody" when both match.
        // Skip self-references and single-char tokens that risk false positives (e.g. "I", "K").
        let candidates = allTerms
            .filter { $0.id != term.id && $0.term.count >= 2 }
            .sorted { $0.term.count > $1.term.count }

        let body = term.detail
        let nsBody = body as NSString
        let fullRange = NSRange(location: 0, length: nsBody.length)

        // Track NSRanges already linked so shorter matches don't overlap longer ones.
        var linked: [NSRange] = []

        for candidate in candidates {
            let escaped = NSRegularExpression.escapedPattern(for: candidate.term)
            // Reject matches where either neighbor is a word character OR a hyphen.
            // Plain \b would let "cell" match inside "B-cell" / "non-small-cell" because
            // \b treats hyphens as boundaries — we don't want a substring of a hyphenated
            // medical compound to win. The lookarounds skip those cases while still
            // matching standalone occurrences ("cell." / "cell," / "the cell ").
            let pattern = "(?<![\\w-])\(escaped)(?![\\w-])"
            // Acronym terms (no lowercase letters, e.g. "ALL", "NET", "PD-1") match case-
            // sensitively so common English words like "all" or "net" don't get linked.
            // Mixed/lowercase terms ("Antibody", "Cmax") match case-insensitively so a
            // sentence-start "Antibody" still resolves to its lowercase canonical entry.
            let hasLowercase = candidate.term.contains { $0.isLowercase }
            let options: NSRegularExpression.Options = hasLowercase ? [.caseInsensitive] : []
            guard let regex = try? NSRegularExpression(pattern: pattern, options: options) else { continue }

            let matches = regex.matches(in: body, options: [], range: fullRange)
            for match in matches {
                let r = match.range
                if linked.contains(where: { NSIntersectionRange($0, r).length > 0 }) { continue }

                guard
                    let stringRange = Range(r, in: body),
                    let attrRange = Range(stringRange, in: attributed),
                    let url = Self.termURL(for: candidate, urlScheme: urlScheme)
                else { continue }

                attributed[attrRange].link = url
                attributed[attrRange].foregroundColor = PGColors.accent
                attributed[attrRange].underlineStyle = .single

                linked.append(r)
            }
        }

        return attributed
    }

    /// Resolve a `<brand-scheme>://term/<encoded-name>` URL back to a Term in the store.
    func term(matchingURL url: URL) -> Term? {
        guard url.scheme == Brand.current.urlScheme, url.host == "term" else { return nil }
        let raw = url.path.hasPrefix("/") ? String(url.path.dropFirst()) : url.path
        guard let decoded = raw.removingPercentEncoding else { return nil }
        return allTerms.first { $0.term.compare(decoded, options: .caseInsensitive) == .orderedSame }
    }

    nonisolated static func termURL(for term: Term, urlScheme: String) -> URL? {
        let allowed = CharacterSet.urlPathAllowed
        let encoded = term.term.addingPercentEncoding(withAllowedCharacters: allowed) ?? term.term
        return URL(string: "\(urlScheme)://term/\(encoded)")
    }
}
