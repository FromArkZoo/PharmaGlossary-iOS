# Adding a new industry to JB Glossary

This is the manual recipe — the framework is deliberately minimum-viable
for N=2 industries. Once you've done this twice and it's still
annoying, write `scripts/scaffold_industry.py`. Not before.

## 1. Pick a slug, brand name, accent color

Decide three things up front:

- **Slug**: lowercase one-word identifier. Used for URL scheme, target
  name in Xcode, and bundle ID suffix. Examples: `pharma`, `ai`,
  `finance`, `legal`.
- **Display name**: shown in App Store and on home screen. Pattern:
  `JB <Industry>` (e.g. `JB Finance`).
- **Accent color**: one hex value. PGColors derives `accentDark` and
  `accentTint` automatically. Pick something visually distinct from
  the other industries' accents — siblings should be recognisably
  different on the home screen.

## 2. Copy the Pharma target as your starting point

```bash
cp -r Targets/Pharma Targets/<Industry>
mv Targets/<Industry>/PharmaBrand.swift Targets/<Industry>/<Industry>Brand.swift
```

The per-target Brand file MUST have a unique filename — Xcode
forbids same-named source files within a target. `PharmaBrand.swift`,
`AIBrand.swift`, `FinanceBrand.swift`, etc.

## 3. Edit the Brand instance

Open `Targets/<Industry>/<Industry>Brand.swift`. Rename the global
instance from `pharmaBrand` to `<industry>Brand`, and edit every field:

- `appStoreName`, `displayName`, `navigationTitle`, `titlePrefix`,
  `titleBody`, `subtitle`, `tagline`, `entryNoun`
- `dataResource`: usually stay `"glossary"` since each target has its
  own `Resources/glossary.json`
- `primaryColor`: the hex from Step 1 as `Color(red: r, green: g, blue: b)`
- `primaryDarkColor`: a hand-darkened version (or use `.darkened(by: 0.15)`)
- `bgColor`: keep `PGColors.bg` unless this industry deserves its own
  paper background
- `urlScheme`: the slug
- `aboutParagraphs`, `aboutDisclaimer`, `aboutSources`: industry-
  appropriate About content. Sources should be authoritative bodies
  for the field (regulators, standards orgs, vendors, labs).
- `basicsAllowlist`: term names (must match `term` field in
  glossary.json exactly) — defines what's in the Basics lens
- `basicsSubtitle`: e.g. "Foundational biology & chemistry",
  "Foundational ML & hardware"
- `policyConfig`: rename `displayName` if your second lens isn't
  called Policy (Pharma="Policy", AI="Frontier", Finance could be
  "Compliance"). Set `categories` to the `category` values in
  glossary.json that should appear in this lens. `excludedTerms`
  drops specific terms even if their category matches.
- `accentTint`: leave `nil` to derive from primaryColor, or pass a
  hand-picked editorial complement (Pharma overrides with a warm
  beige; AI lets it derive)

At the bottom of the file, keep the extension that declares
`Brand.current`:

```swift
extension Brand {
    static let current: Brand = <industry>Brand
}
```

Each target supplies exactly one such extension — that's how
`Brand.current` resolves correctly per target with no duplicate.

## 4. Edit the resources

Inside `Targets/<Industry>/Resources/`:

- **`Assets.xcassets/AccentColor.colorset/Contents.json`** — update RGB
  components to the slug's accent (alpha 1.000, sRGB). Note: this asset
  is the Xcode "global accent" — the app actually drives accents via
  Brand.current, so this is mainly for system controls.
- **`Assets.xcassets/AppIcon.appiconset/icon-1024.png`** — replace with
  a 1024×1024 PNG for this industry. The Pharma icon will copy through
  unless you replace it; do so before App Store submission.
- **`Assets.xcassets/LaunchBackground.colorset/Contents.json`** — keep
  cream (`#F5EFE6`) unless this industry deserves a different launch
  background.
- **`Info.plist`** — change `CFBundleDisplayName` to your display name.
- **`glossary.json`** — replace with your industry content. Schema:
  `{letter, term, full, snappy, detail, indications[], category, sources[]}`.
  Start with a small stub (3-10 terms) just to verify wiring; batch
  the real content in via a follow-up `scripts/add_<industry>_terms.py`
  mirroring `scripts/add_basics.py`.
- **`PrivacyInfo.xcprivacy`** — leave as-is unless this industry has
  different data-collection behavior.

## 5. Add the target to `project.yml`

Copy the Pharma target block and adapt:

```yaml
  <Industry>:
    type: application
    platform: iOS
    deploymentTarget: "17.0"
    sources:
      - path: Sources
      - path: Targets/<Industry>
        excludes:
          - "Resources/Info.plist"
    resources:
      - Targets/<Industry>/Resources/Assets.xcassets
      - Targets/<Industry>/Resources/glossary.json
      - Targets/<Industry>/Resources/PrivacyInfo.xcprivacy
    info:
      path: Targets/<Industry>/Resources/Info.plist
      properties:
        CFBundleDisplayName: JB <Industry>
        # ... (mirror Pharma's block exactly)
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.jamesbrowne.<Industry>Glossary
        # ... (mirror Pharma's block exactly)
```

Then regenerate the Xcode project:

```bash
xcodegen generate
```

## 6. Build and visually verify

```bash
xcodebuild -scheme <Industry> -destination 'platform=iOS Simulator,name=iPhone 17 Pro Max' build
```

Then in Xcode, switch scheme to `<Industry>`, Run on the sim, and
eyeball:

- The home header shows "JB <Industry>" with the italic accent applied
  to the `titleBody`
- Splash dots and Favorites star are the new accent color
- The radial-wash on PGBackground (bottom-right) uses the new accent
- Tap Filter → check the Basics + Policy/Frontier lens cards show
  the right title and subtitle
- Tap About → confirm `aboutParagraphs`, `aboutDisclaimer`, and
  `aboutSources` render with industry-specific copy
- Tap a term → confirm hyperlinks resolve `<slug>://term/...` not
  `pharma://...`

Take a screenshot:

```bash
xcrun simctl io booted screenshot /tmp/<industry>.png
```

## 7. Capture screenshots and create ASC record

When ready to ship:

- Capture the standard set of App Store screenshots. Re-use the
  composite trick documented for Pharma (`composite_ipad13.py`-style
  pattern) for iPad sizes.
- Create a new App Store Connect app record at
  `com.jamesbrowne.<Industry>Glossary`. Pricing usually £2.99,
  manual release.
- Upload build via Xcode → Organizer.

## 8. Don't shave the yak yet

Resist the urge to:

- Write a Python scaffolder until you've done this manual recipe at
  least twice and it still hurts.
- Templatize `docs/<industry>/` until the third industry is shipping.
- Localize until you have evidence non-English speakers want this.
- Build a content-curation DSL — glossary content is content work,
  separate from the framework.

The whole point of this layout is that adding industry #2, #3, #4 is
finite manual effort, not a build system project. When the manual
effort exceeds the scaffolding effort, scaffold then.
