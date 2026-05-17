"""Idempotently merge markets/finance terms into Targets/Finance/Resources/glossary.json.

Mirrors scripts/add_law_terms.py — append-only, case-insensitive dedup against
existing terms, sort by (letter asc, term asc) on write. Each batch is a
Python list built via the entry() helper which enforces category +
indication enums so we don't drift away from the lenses in FinanceBrand.swift.

Voice: Bloomberg-desk register for a generalist (citizen, journalist, business
owner). Snappy line ~12 words, present tense, must make sense WITHOUT prior
markets knowledge. Detail 50–75 words anchored on a real instrument, a desk
practice, a regulatory citation, or a famous market event. No prices,
no trade ideas, no "you should".

Usage:
    python scripts/add_finance_terms.py
    python scripts/add_finance_terms.py --batches 1,2     # run specific batches
    python scripts/add_finance_terms.py --dry-run         # preview without writing
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

GLOSSARY = Path(__file__).parent.parent / "Targets" / "Finance" / "Resources" / "glossary.json"

# Keep in sync with Targets/Finance/FinanceBrand.swift `lenses[].kind` category lists.
VALID_CATEGORIES = {
    "Instruments", "Pricing & Valuation", "Risk", "Market Structure",
    "Trading & Execution", "Settlement & Operations", "Regulation",
    "Indexes & Benchmarks", "Quantitative", "Corporate Actions",
}

VALID_INDICATIONS = {
    "Rates", "FX", "Equities", "Credit", "Commodities",
    "Derivatives", "Cross-asset", "Macro",
}


def entry(term, full, snappy, detail, sources, indications=None, category="Instruments"):
    assert category in VALID_CATEGORIES, f"Unknown category '{category}' for term '{term}'"
    indications = indications or ["Cross-asset"]
    for ind in indications:
        assert ind in VALID_INDICATIONS, f"Unknown indication '{ind}' for term '{term}'"
    return {
        "letter": term[0].upper(),
        "term": term,
        "full": full,
        "snappy": snappy,
        "detail": detail,
        "indications": indications,
        "category": category,
        "sources": sources,
    }


# ============================================================================
# BATCH 1 — Smoke test (20 terms covering all 8 asset-class tags
# and 8 of 10 categories — first-hour-on-the-desk vocabulary)
# ============================================================================

BATCH_SMOKE_TEST = [
    entry("Bid-Ask Spread", "",
        "Gap between what buyers offer and sellers accept — the dealer's cut.",
        "Quoted as the difference between bid (where a market-maker will buy) and offer (where they'll sell). Tightens with volume and competition; widens around news, illiquid hours, or stress. A penny S&P 500 spread costs retail almost nothing; a fifty-cent emerging-market bond spread is the trader's bread and butter. Regulators (MiFID II in Europe, Rule 605 in the US) require disclosure as a proxy for execution quality.",
        ["SEC", "ESMA"],
        indications=["Cross-asset"], category="Market Structure"),

    entry("Yield", "",
        "Return a bond pays as a percentage of its price.",
        "Several flavours: current yield (coupon over price), yield-to-maturity (the discount rate equating cash flows to price), yield-to-call (assumes the issuer redeems early). Inverse to price — when rates rise, bond prices fall. The Treasury's daily yield curve, posted by the Federal Reserve, is the global benchmark. Equity 'yield' (dividend over price) is a different beast.",
        ["Federal Reserve", "CFA Institute"],
        indications=["Rates"], category="Pricing & Valuation"),

    entry("Duration", "",
        "How much a bond's price moves for a one-percent rate shift, expressed in years.",
        "Macaulay duration is the weighted-average time to cash flows. Modified duration is what traders quote — a seven-year-duration bond loses roughly seven percent if yields rise one percent. Effective duration handles callable bonds and mortgage-backed securities. Portfolio managers target duration to express macro views; index funds match the benchmark duration to track. Long-duration assets got hammered in 2022 as the Fed hiked 525 basis points.",
        ["CFA Institute", "Federal Reserve"],
        indications=["Rates"], category="Risk"),

    entry("Convexity", "",
        "How a bond's duration itself changes as yields move — the second-order kicker.",
        "Duration alone is a first-order approximation. Convexity captures the curvature: positive convexity (most non-callable bonds) means the price gains more on a rate drop than it loses on an equivalent rise — good for the holder. Mortgage-backed securities have negative convexity because prepayment shortens duration in rallies, the dreaded MBS hedge flow that whipsaws Treasury markets.",
        ["CFA Institute"],
        indications=["Rates"], category="Risk"),

    entry("Basis Point", "",
        "Tiny unit traders use for yields and spreads — one one-hundredth of a percent.",
        "One basis point (often 'bp' or 'bip', pronounced 'beep') equals 0.01 percent. A 25 bp Fed hike is a quarter-percent move. Credit spreads, central-bank moves, swap rates, mortgage points — every fixed-income conversation runs in bps because percentage-of-a-percentage is too clumsy. 'Came in twelve wider' means the spread widened by twelve basis points.",
        ["Federal Reserve", "Bank of England"],
        indications=["Rates"], category="Pricing & Valuation"),

    entry("DV01", "Dollar Value of an 01",
        "Dollar P&L hit from a one-basis-point yield move — the rates trader's primary risk metric.",
        "Calculated from duration times price times 0.0001. A position with a hundred-thousand-dollar DV01 makes or loses that amount per basis point. Quoted in millions for big books. Used to size trades to risk limits, to compare positions across instruments, and to hedge: matching DV01s between cash bonds and swaps neutralises first-order rate risk. The 'PV01' variant is essentially the same number from the present-value direction.",
        ["CFA Institute", "ISDA"],
        indications=["Rates"], category="Risk"),

    entry("Repo", "Repurchase agreement",
        "Borrowing cash overnight against collateral — usually Treasuries.",
        "A repo is a sale with an agreement to buy back next day at a slightly higher price; the difference is the repo rate. The plumbing of short-term funding: dealers fund inventories, money funds park cash. Tri-party repo at BNY Mellon clears trillions daily. The September 2019 repo spike — rates briefly hit ten percent — forced the Fed to launch standing facilities. SOFR is calculated from repo activity.",
        ["Federal Reserve", "DTCC", "SIFMA"],
        indications=["Rates"], category="Instruments"),

    entry("FX Swap", "",
        "Exchange currencies now, agree to swap them back at a fixed forward rate.",
        "Two legs: spot exchange today, reverse exchange at maturity. Used by corporates to hedge cross-currency funding, by central banks (the Fed's swap lines with the ECB, Bank of Japan, Bank of England), and by anyone wanting to synthesise foreign-currency exposure without borrowing. The 'cross-currency basis' — the forward points implied minus what covered interest parity says — became a watched stress gauge after 2008 when banks lost access to dollar funding.",
        ["BIS", "Federal Reserve", "ICMA"],
        indications=["FX"], category="Instruments"),

    entry("Forward Points", "",
        "Premium or discount added to spot to get the forward FX rate.",
        "Derived from interest-rate differentials: borrow the high-rate currency, lend the low-rate one, and the forward must price arbitrage out (covered interest parity). Quoted as pips: USD/JPY at spot 150 with three-month forward points of -45 means the three-month forward is 149.55. Forwards above spot mean the base currency is at a premium; below means a discount. Tight in normal times, blow out in funding stress.",
        ["BIS", "Federal Reserve"],
        indications=["FX"], category="Pricing & Valuation"),

    entry("VWAP", "Volume-Weighted Average Price",
        "Average price weighted by traded volume across the day — the execution benchmark.",
        "Resets daily. Traders measure execution quality against VWAP: 'I bought five cents inside.' Brokers offer VWAP algos that slice an order across the day proportional to expected volume, minimising market impact for big trades. Index rebalances and ETF creations often target VWAP. Distinct from arrival-price benchmarks (Implementation Shortfall) which capture timing risk too.",
        ["NYSE", "SEC"],
        indications=["Equities"], category="Trading & Execution"),

    entry("TWAP", "Time-Weighted Average Price",
        "Average price across equal time slices — execution algo's simpler sibling to VWAP.",
        "TWAP algos chop an order into evenly-spaced child orders over a chosen window. Used when volume forecasts are unreliable, for less-liquid names, or when minimising signalling matters more than tracking volume. Easier to model and explain than VWAP. Common in crypto and small-cap equities. Critics note TWAP is gameable by predatory algos that detect the regular slicing pattern.",
        ["SEC", "FINRA"],
        indications=["Equities"], category="Trading & Execution"),

    entry("Implied Volatility", "IV",
        "The volatility the option market is pricing in — derived backwards from the option's premium.",
        "Black-Scholes (and successors) take inputs — spot, strike, time, rate, volatility — and output an option price. Invert the model on a traded option and the only unknown is volatility; that's IV, the market's forward-looking estimate. The VIX is a weighted IV reading off S&P 500 options. IV usually trades above realised volatility — the 'vol risk premium' that volatility sellers harvest.",
        ["CFA Institute", "CME Group"],
        indications=["Derivatives"], category="Pricing & Valuation"),

    entry("Delta", "",
        "How much an option's price moves for a one-point move in the underlying.",
        "A call's delta runs from 0 (deep out-of-the-money) to 1 (deep in-the-money); puts run 0 to -1. At-the-money options sit near plus or minus 0.5. Traders use delta to hedge: short a 0.5-delta call and buy fifty shares of the underlying to neutralise directional risk. Delta-hedging keeps shifting as the underlying moves — the gamma problem — generating the buy-high-sell-low flows that bleed long-volatility books.",
        ["ISDA", "CME Group"],
        indications=["Derivatives"], category="Risk"),

    entry("CDS Spread", "Credit Default Swap Spread",
        "Annual premium paid to insure a bond against default — basis points on notional.",
        "Buyer pays a quarterly premium (the spread), seller pays out if the reference name defaults. A 200 bp CDS on a ten-million notional costs two hundred thousand a year. Spreads widen when default looks more likely. iTraxx (Europe) and CDX (US) indexes track baskets. Blew out during the 2008 Lehman crisis and the 2023 SVB stress. Post-2009 reforms moved most trades to central clearing at LCH and ICE.",
        ["ISDA", "LCH", "ICE"],
        indications=["Credit"], category="Pricing & Valuation"),

    entry("Contango", "",
        "Futures price above spot — usually means storage costs or surplus inventory.",
        "Crude oil in storage-glut periods sits in contango: a one-month forward trades above near-month, the curve sloping upward. Holders of long futures roll into pricier contracts each month, paying the 'roll yield' penalty. The April 2020 negative WTI episode was contango taken to extremes — storage was so full that nearby contracts went negative. ETF investors in commodity products learn about contango the hard way.",
        ["CME Group", "ICE"],
        indications=["Commodities"], category="Pricing & Valuation"),

    entry("Backwardation", "",
        "Futures price below spot — usually means scarcity or strong demand for prompt delivery.",
        "The opposite of contango. Curve slopes downward. Common in commodities with seasonal demand (heating oil in winter), supply disruptions (oil after the 2022 Russia-Ukraine invasion), or storage costs that exceed convenience yield. Long futures holders earn positive roll yield, rolling cheaper. Backwardation is a generally bullish signal for the spot commodity — physical market is tight.",
        ["CME Group", "ICE"],
        indications=["Commodities"], category="Pricing & Valuation"),

    entry("SOFR", "Secured Overnight Financing Rate",
        "Overnight rate based on Treasury repo trades — the LIBOR replacement.",
        "Published daily by the New York Fed using actual transaction volume (roughly 1.5 trillion dollars daily), making it manipulation-resistant. Replaced USD LIBOR after the 2012 manipulation scandals; the formal cessation was June 2023. SOFR is risk-free (collateralised), so spreads to credit-sensitive benchmarks matter for swaps. Term SOFR (CME-published forward-looking rate) is used in business loans, and the Fed's standing repo facility helps pin the floor.",
        ["Federal Reserve", "CME Group", "Federal Reserve FRED"],
        indications=["Rates"], category="Indexes & Benchmarks"),

    entry("Settlement Date", "",
        "When ownership and cash actually change hands — distinct from the trade date.",
        "US equities moved to T+1 (one business day after trade) in May 2024, joining India and Canada. US Treasuries settle T+1. Most government bonds settle T+1 or T+2. FX spot is T+2 for most pairs (T+1 for USD/CAD). Fails to settle attract penalties under SEC Rule 204 and CSDR in Europe. The shorter cycle reduces counterparty risk but compresses post-trade processing time.",
        ["SEC", "DTCC", "ESMA"],
        indications=["Cross-asset"], category="Settlement & Operations"),

    entry("Yield Curve", "",
        "Yields plotted across maturities — the most-watched chart in markets.",
        "Usually upward-sloping: longer bonds yield more because investors demand a term premium. Inverted curve (short rates above long) has preceded every modern US recession with one false positive (1966). The 10-year-minus-2-year and 10-year-minus-3-month spreads are watched gauges. The Federal Reserve controls the short end via policy rates; the long end reflects growth and inflation expectations plus term premia. Bull steepeners, bear flatteners — every shape carries a macro meaning.",
        ["Federal Reserve", "Federal Reserve FRED", "Bank of England"],
        indications=["Rates", "Macro"], category="Pricing & Valuation"),

    entry("Fed Funds Rate", "",
        "The Fed's policy rate — what banks charge each other for overnight reserves.",
        "The Federal Open Market Committee (FOMC) sets a target range eight times a year. Since 2008 the Fed has implemented policy through interest on reserves (IORB) and the overnight reverse repo rate, which bracket the effective rate. Cuts in 2008 (from 5.25 percent to 0), hikes in 2022-23 (0 to 5.50 percent), and the path from here drive global asset prices. Watch the dot plot for the FOMC's own rate projections.",
        ["Federal Reserve", "Federal Reserve FRED"],
        indications=["Rates", "Macro"], category="Indexes & Benchmarks"),
]


BATCHES = {
    1: BATCH_SMOKE_TEST,
}


def merge(batches_to_run, dry_run=False):
    existing = json.loads(GLOSSARY.read_text())
    existing_names = {t["term"].lower() for t in existing}

    new_entries = []
    for n in batches_to_run:
        batch = BATCHES.get(n)
        if batch is None:
            print(f"warning: batch {n} not found, skipping")
            continue
        for e in batch:
            key = e["term"].lower()
            if key in existing_names:
                print(f"skip: {e['term']} already exists")
                continue
            new_entries.append(e)
            existing_names.add(key)

    if dry_run:
        print(f"would merge {len(new_entries)} new entries; total would be {len(existing) + len(new_entries)}")
        return

    combined = existing + new_entries
    combined.sort(key=lambda t: (t["letter"], t["term"].lower()))
    GLOSSARY.write_text(json.dumps(combined, ensure_ascii=False, indent=2) + "\n")
    print(f"merged {len(new_entries)} new entries; total {len(combined)}")


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--batches", default=",".join(str(n) for n in BATCHES),
                   help="comma-separated batch numbers to run (default: all)")
    p.add_argument("--dry-run", action="store_true", help="preview without writing")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    nums = [int(x) for x in args.batches.split(",") if x.strip()]
    merge(nums, dry_run=args.dry_run)
