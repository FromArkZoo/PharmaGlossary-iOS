# App Store Connect — In-App Purchase setup for JB Glossary v2

Create these **4 non-consumable** in-app purchases against the
`com.jamesbrowne.PharmaGlossary` app record in App Store Connect. The
product identifiers below MUST match exactly — they are hardcoded in
`Sources/Industries/IndustryConfig.swift` (3 industry IDs) and
`masterUnlockProductID` (1 master).

| Product ID | Reference Name | Display Name | Price (US) | Family Sharing |
|---|---|---|---|---|
| `com.jamesbrowne.JBGlossary.ai` | AI | Unlock AI | $2.99 (Tier 3) | On |
| `com.jamesbrowne.JBGlossary.law` | Law | Unlock Law | $2.99 (Tier 3) | On |
| `com.jamesbrowne.JBGlossary.finance` | Finance | Unlock Finance | $2.99 (Tier 3) | On |
| `com.jamesbrowne.JBGlossary.all` | All Industries | Unlock All Industries | $14.99 (Tier 15) | On |

## Descriptions (used on the App Store IAP listing)

**AI** — Unlock the JB Glossary AI industry: 785 terms covering models,
training, hardware, and silicon. One-time purchase, no subscription.

**Law** — Unlock the JB Glossary Law industry: 836 US-law terms across
contracts, criminal, constitutional, employment, IP, family, and more.
One-time purchase, no subscription.

**Finance** — Unlock the JB Glossary Finance industry: 626 markets terms
across rates, FX, equities, credit, commodities, and derivatives. One-time
purchase, no subscription.

**All Industries** — Unlock every paid industry in JB Glossary (AI, Law,
Finance, and all future industries we ship). One purchase covers your
current and future devices via Apple ID. Best value once you'd buy more
than 4 individual industries.

## Review notes (for App Review)

> JB Glossary ships with Pharma as a free anchor industry. Three additional
> industries (AI, Law, Finance) are gated behind one-time non-consumable
> IAPs at $2.99 each. The "Unlock All Industries" $14.99 IAP grants
> entitlement to every current and future paid industry. There are no
> subscriptions; everything is one-time. "Restore Purchases" is available
> from every paywall sheet, satisfying 3.1.1.

## Local sandbox testing (already wired)

The project ships with `Configuration.storekit` and the scheme is
configured to use it (`scheme.storeKitConfiguration` in `project.yml`).
Running on the simulator from Xcode resolves the four products against
the local config, so the paywall sheet shows real prices ($2.99 / $14.99)
and `Product.purchase()` simulates a transaction.

Sandbox testing on a real device requires an App Store Connect Sandbox
Tester account and the actual products created above. Add the tester in
ASC → Users and Access → Sandbox Testers, then sign into the device's
App Store with that account before launching.

## Grandfathering legacy Pharma users

`PurchaseManager.checkGrandfathering()` reads
`AppTransaction.originalAppVersion` on first v2 launch. If the original
version starts with `1.` (i.e., the user installed any pre-v2 Pharma
build — whether they paid or downloaded free), the master "All
Industries" entitlement is granted locally and persisted under
`jbglossary.grandfathered.masterUnlock` in `UserDefaults`. This costs
nothing if Pharma was launched free and creates a strong "thanks for
being early" moment if any Pharma users were paid.

The check is idempotent and retried on every launch until it succeeds
(simulator builds without a receipt can fail the AppTransaction call).
