import SwiftUI

let financeBrand = Brand(
    appStoreName: "JB Finance",
    displayName: "JB Finance",
    navigationTitle: "JB Finance",
    titlePrefix: "JB",
    titleBody: "Finance",
    subtitle: "decoding market jargon",
    tagline: nil,
    entryNoun: "entries",
    dataResource: "glossary",
    primaryColor: Color(red: 0.333, green: 0.231, blue: 0.494),       // #553B7E royal purple
    primaryDarkColor: Color(red: 0.239, green: 0.165, blue: 0.361),   // #3D2A5C deeper purple
    bgColor: PGColors.bg,
    urlScheme: "finance",
    aboutParagraphs: [
        "JB Finance is a generalist's reference for the language of markets — rates, FX, equities, credit, commodities, and the derivatives and plumbing underneath. The jargon you encounter on earnings calls, in Fed minutes, in broker research, and any time a markets professional starts talking.",
        "Entries summarise publicly available material from central banks, regulators, exchanges, clearers, and industry standards bodies. They are written for orientation in plain English, not as investment advice."
    ],
    aboutDisclaimer: "Educational reference. Not investment advice. Markets change; definitions evolve.",
    aboutSources: [
        BrandSource(
            heading: "Central banks & global bodies",
            items: ["Federal Reserve", "Bank of England", "ECB", "BIS", "IMF", "World Bank", "Federal Reserve FRED"]
        ),
        BrandSource(
            heading: "Regulators",
            items: ["SEC", "CFTC", "FINRA", "FCA", "ESMA", "IOSCO", "OCC"]
        ),
        BrandSource(
            heading: "Exchanges, clearers, index providers",
            items: ["CME Group", "ICE", "LSEG", "NYSE", "Nasdaq", "DTCC", "LCH", "Eurex", "MSCI", "S&P Dow Jones Indices", "FTSE Russell"]
        ),
        BrandSource(
            heading: "Industry standards & reference works",
            items: ["ISDA", "ICMA", "SIFMA", "CFA Institute", "Investopedia"]
        )
    ],
    lenses: [
        LensConfig(
            id: "basics",
            glyph: "B",
            title: "Basics",
            subtitle: "Foundational markets vocabulary",
            kind: .allowlist([
                "Asset", "Liability", "Equity", "Debt", "Bond", "Stock", "Share",
                "Dividend", "Coupon", "Yield", "Yield Curve", "Interest Rate",
                "Inflation", "Deflation", "GDP", "Recession", "Bull Market", "Bear Market",
                "Volatility", "Liquidity", "Spread", "Bid", "Ask", "Bid-Ask Spread",
                "Basis Point", "Hedge", "Arbitrage", "Leverage", "Margin",
                "Short Selling", "Long Position", "Short Position",
                "Derivative", "Option", "Call Option", "Put Option", "Strike Price",
                "Expiration", "Future", "Forward", "Swap", "Repo",
                "Credit Rating", "Default", "Credit Default Swap",
                "Junk Bond", "Investment Grade", "High Yield",
                "Treasury", "T-Bill", "T-Note", "T-Bond",
                "Mortgage-Backed Security", "ETF", "Mutual Fund", "Hedge Fund",
                "Private Equity", "IPO", "Secondary Offering", "Buyback", "Stock Split",
                "Market Cap", "P/E Ratio", "Book Value",
                "Index", "Benchmark", "S&P 500", "Nasdaq Composite", "Dow Jones",
                "VIX", "Implied Volatility", "Historical Volatility",
                "FX", "Exchange Rate", "Currency Pair", "Spot Rate", "Forward Rate", "Carry Trade",
                "Federal Reserve", "Fed Funds Rate", "Quantitative Easing",
                "Central Bank", "Monetary Policy", "Fiscal Policy",
                "Commodities", "Gold", "Oil", "WTI", "Brent",
                "Contango", "Backwardation", "Futures Contract",
                "Settlement", "Settlement Date", "T+1", "Clearing",
                "Counterparty", "Counterparty Risk", "Market Maker",
                "Order Book", "Dark Pool", "Algorithmic Trading",
                "Smart Order Routing", "Block Trade", "OTC",
                "Exchange", "NYSE", "London Stock Exchange", "Nasdaq",
                "Beta", "Alpha", "Sharpe Ratio", "Correlation", "Diversification",
                "Portfolio", "Asset Allocation", "Rebalancing",
                "Duration", "Convexity", "DV01", "PV01",
                "Capital Adequacy", "Tier 1 Capital",
                "SEC", "CFTC", "FCA", "ISDA"
            ])
        ),
        LensConfig(
            id: "markets",
            glyph: "M",
            title: "Markets",
            subtitle: "Instruments, pricing, risk, execution",
            kind: .categoryFilter(
                categories: ["Instruments", "Pricing & Valuation", "Risk", "Trading & Execution", "Market Structure"],
                excludedTerms: []
            )
        )
    ],
    accentTint: nil,
    sourceURLs: [
        // Central banks & global bodies
        "Federal Reserve":            URL(string: "https://www.federalreserve.gov")!,
        "Federal Reserve FRED":       URL(string: "https://fred.stlouisfed.org")!,
        "Bank of England":            URL(string: "https://www.bankofengland.co.uk")!,
        "ECB":                        URL(string: "https://www.ecb.europa.eu")!,
        "BIS":                        URL(string: "https://www.bis.org")!,
        "IMF":                        URL(string: "https://www.imf.org")!,
        "World Bank":                 URL(string: "https://www.worldbank.org")!,
        // Regulators
        "SEC":                        URL(string: "https://www.sec.gov")!,
        "CFTC":                       URL(string: "https://www.cftc.gov")!,
        "FINRA":                      URL(string: "https://www.finra.org")!,
        "FCA":                        URL(string: "https://www.fca.org.uk")!,
        "ESMA":                       URL(string: "https://www.esma.europa.eu")!,
        "IOSCO":                      URL(string: "https://www.iosco.org")!,
        "OCC":                        URL(string: "https://www.occ.gov")!,
        // Exchanges, clearers, index providers
        "CME Group":                  URL(string: "https://www.cmegroup.com")!,
        "ICE":                        URL(string: "https://www.ice.com")!,
        "LSEG":                       URL(string: "https://www.lseg.com")!,
        "NYSE":                       URL(string: "https://www.nyse.com")!,
        "Nasdaq":                     URL(string: "https://www.nasdaq.com")!,
        "DTCC":                       URL(string: "https://www.dtcc.com")!,
        "LCH":                        URL(string: "https://www.lch.com")!,
        "Eurex":                      URL(string: "https://www.eurex.com")!,
        "MSCI":                       URL(string: "https://www.msci.com")!,
        "S&P Dow Jones Indices":      URL(string: "https://www.spglobal.com/spdji/en/")!,
        "FTSE Russell":               URL(string: "https://www.lseg.com/en/ftse-russell")!,
        // Industry standards & reference works
        "ISDA":                       URL(string: "https://www.isda.org")!,
        "ICMA":                       URL(string: "https://www.icmagroup.org")!,
        "SIFMA":                      URL(string: "https://www.sifma.org")!,
        "CFA Institute":              URL(string: "https://www.cfainstitute.org")!,
        "Investopedia":               URL(string: "https://www.investopedia.com")!
    ]
)

extension Brand {
    static let current: Brand = financeBrand
}
