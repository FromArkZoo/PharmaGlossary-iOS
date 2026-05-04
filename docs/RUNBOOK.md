# Content Rewrite Runbook

**Status:** v1.0, 2026-05-04.

**Purpose:** Day-to-day workflow for batch-rewriting `glossary.json` from old shape to layered shape. Operationalizes the prompts in `PASS_1_REWRITE.md` and `PASS_2_FACTCHECK.md`.

**Companion docs:**
- `CONTENT_STYLE_GUIDE.md` — voice/format/IP spec
- `CALIBRATION_ENTRIES.md` — 8 in-context examples
- `PASS_1_REWRITE.md` — rewrite prompt
- `PASS_2_FACTCHECK.md` — fact-check prompt

---

## Pre-flight checklist (one-time)

Before starting any batch:

- [ ] Read `CONTENT_STYLE_GUIDE.md` end to end.
- [ ] Skim `CALIBRATION_ENTRIES.md` to internalize the voice.
- [ ] Open the Pass 1 prompt and verify the 8 calibration examples are intact.
- [ ] Have at least three Tier-1 sources bookmarked: NCI Dictionary, FDA glossaries, NIH MedlinePlus, CMS Glossary.
- [ ] Have a fresh Claude.ai session ready for Pass 1, and a separate one for Pass 2.

---

## Per-batch workflow (recommended batch size: 30-50 terms)

### Step 1 — Pick the batch

Open `glossary.json`. Pick a contiguous block of terms (e.g., letters A-C, or all "Mechanism" category, or first 30 entries). Smaller batches are easier to review.

Don't shuffle randomly; alphabetical or category-based picking lets you spot voice drift more easily.

### Step 2 — Source the Tier-1 text

For each term in the batch:

1. Identify which Tier-1 source covers it (per `CONTENT_STYLE_GUIDE.md` §8.2):
   - **Oncology terms** → NCI Dictionary of Cancer Terms (search by term).
   - **Regulatory terms** (PDUFA, REMS, BLA, etc.) → FDA glossaries and guidance pages.
   - **Commercial / market access terms** (formulary, copay, etc.) → CMS Glossary.
   - **General disease/drug terms** → NIH MedlinePlus.
   - **Pharmacology / mechanism** → NCI for cancer-related; FDA / NIH otherwise.
2. Locate the term in that source.
3. Copy the source text verbatim into a per-term note (a markdown file or a scratchpad).
4. If no Tier-1 source covers the term cleanly, mark for **hand-author** — do not attempt LLM rewrite without a source.

Time budget: 2-3 minutes per term. For a batch of 30, sourcing takes 1-1.5 hours.

### Step 3 — Run Pass 1

In a Claude.ai session (or via SDK):

1. Paste the system prompt from `PASS_1_REWRITE.md`.
2. For each term, paste the user-message template with all slots filled.
3. Capture the JSON output.
4. If the model returns `_error: insufficient_source`, route to hand-authoring.

Time budget: ~30 seconds per term plus reading time. For a batch of 30, ~30-45 minutes.

**When to reset context:** every 30-50 terms, or sooner if you spot voice drift. Stale context can cause length creep, vocab drift, and example-recycling.

### Step 4 — Run Pass 2 (fact-check)

For each Pass 1 output, in a **fresh** Claude.ai session:

1. Paste the system prompt from `PASS_2_FACTCHECK.md`.
2. Paste the entry under review.
3. Read flags. For each flag:
   - Verify against the Tier-1 source.
   - If supported → false positive, dismiss.
   - If unsupported → fix per `PASS_2_FACTCHECK.md` action list. Re-run Pass 2.
4. Continue until "VERDICT: clean".

Time budget: 1-3 minutes per entry. Most return clean on first pass; a few need 1-2 iterations. For a batch of 30, ~45-90 minutes.

### Step 5 — Quality gate check

For each verified entry, run the 7-question §12 checklist from `CONTENT_STYLE_GUIDE.md`:

1. Outsider test (italic lands?)
2. Generalist test (detail repeatable?)
3. "Where you'd hear it" beat present?
4. Banned vocab in italic line: zero?
5. No-advice scan: zero?
6. Tagging: ≥1 indication, exactly 1 category?
7. Source: ≥1 Tier-1?

If any check fails, fix or cut. Do not commit failing entries.

### Step 6 — Update `glossary.json`

Open `PharmaGlossary/Resources/glossary.json` and replace the corresponding old entries with the new ones. Preserve the alphabetical order.

### Step 7 — Verify the build

```bash
cd ~/PharmaGlossary-iOS
xcodebuild -project PharmaGlossary.xcodeproj -scheme PharmaGlossary \
  -destination 'platform=iOS Simulator,id=[your-sim-id]' \
  -configuration Debug build 2>&1 | tail -5
```

Expect `** BUILD SUCCEEDED **`. If decode fails (the JSON is malformed or violates the schema), fix and re-verify.

### Step 8 — Visual spot-check

Boot the simulator, open the app, navigate to 3-5 of the rewritten entries. Verify:
- Snappy line displays in italic, reads well.
- Detail paragraph displays, reads naturally.
- Source footer appears at the bottom.
- No truncation, no overflow, no broken layout.

If any entry looks visually off (length too long causing scroll issues, weird character escaping, etc.), note it and fix.

### Step 9 — Commit the batch

```bash
git add PharmaGlossary/Resources/glossary.json
git commit -m "Rewrite [N] entries: [brief description, e.g. letters A-C, or all Mechanism category]"
```

Push at end of session.

---

## Mid-content-rewrite cross-checks

After every ~150 entries authored, run these cross-batch checks:

### Cross-model diff (10% sample)

Pick 15 random entries from the recent ~150. Run them through Pass 1 again using a different LLM family (e.g., GPT instead of Claude, or vice versa). Diff the outputs. Material disagreements (different drug examples, different mechanism descriptions) → human review against source.

### Voice-consistency read-through

Open the recent ~150 entries in alphabetical order. Read 30 random ones. Look for:
- Snappy lines drifting toward the same hook style (e.g., 8 metaphors in a row).
- Length creep (italic >30 words, detail >80 words).
- "Where you'd hear it" beat dropped on later entries.
- Repeated phrasing across entries ("evidence-based interventions" appearing in 5 entries).

If drift is detected, refresh the prompt context with calibration entries and re-run the affected entries.

### Spot-check sample

Pick 25 random entries from the entire authored corpus. Manually verify each against its cited Tier-1 source. If error rate >5% in the sample, halt rewrite work and tighten the prompt before continuing.

---

## When to hand-author instead of LLM-batch

Some terms shouldn't go through the LLM workflow:

- **No clean Tier-1 source.** If a term isn't in FDA / NCI / MedlinePlus / CMS, the LLM will hallucinate. Hand-author from primary research.
- **Highly contested or evolving definitions.** If sources disagree (e.g., "biosimilar" definitions vary slightly between FDA and EMA), pick the framing yourself and write the entry to be deliberately diplomatic.
- **Cross-cutting concept terms** (e.g., "precision medicine", "personalized medicine"). LLMs default to marketing-speak on these. Hand-author with conscious anti-hype framing.

Estimate: ~10-15% of entries (~50-70 of ~470) will go this route. Plan for it.

---

## Failure modes and fallbacks

**The LLM consistently produces overlong snappy lines** → tighten the system prompt: change "18-30 words" to "≤25 words" and re-run.

**The LLM keeps inventing drug examples** → the source text is too thin. Find a richer Tier-1 source with explicit examples, or omit examples in the rewrite.

**Pass 2 flags everything** → the system prompt is too aggressive. Re-read `PASS_2_FACTCHECK.md` and re-issue with the "do not flag general field knowledge" emphasis. Or reduce conservatism slightly.

**You spot a banned word in 3+ recent entries** → the in-context examples in Pass 1 may be polluted (e.g., a recent rewrite snuck through with banned vocab and got fed back into context). Reset context and continue.

**The build fails after committing a batch** → usually a JSON syntax error (a stray quote, missing comma). Re-validate the JSON: `python3 -c "import json; json.load(open('PharmaGlossary/Resources/glossary.json'))"` will pinpoint the error line.

---

## Tracking progress

Maintain a running tally somewhere (markdown file, spreadsheet, or a TODO list):

```
A: 27 done / 27 total
B: 16 done / 19 total
C: 0 done / 16 total
...
```

Update at the end of each batch. This is also useful for App Store messaging ("v1.0 ships with 470 entries across 14 categories").

---

## Pace and cadence

For a focused content sprint (per the 10-week v1.0 plan):
- Day 1: 30 entries (warm-up, calibrating against existing glossary).
- Days 2-5: 50-70 entries per day.
- Daily commit and push at end of session.
- One cross-batch check (cross-model diff or voice read-through) every 2-3 days.

Don't try to rush past 70/day. Voice drift accelerates when you skim.
