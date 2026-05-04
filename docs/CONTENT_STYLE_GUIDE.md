# JB Pharma — Content Style Guide

**Status:** v0.4 draft, 2026-05-04. Living doc — expect revisions as we batch-rewrite the 324 oncology entries and discover edge cases.

**v0.4 changes:** Added CMS to Tier-1 sources in §8.2 (canonical for formulary, coverage, and reimbursement terminology; US federal, public domain).
**v0.3 changes:** Added §15 LLM-assisted authoring workflow (source-grounded prompting, two-pass verification, cross-model diff, in-app feedback loop, spot-check sampling).
**v0.2 changes:** §8 expanded with copyright/license analysis per source, "facts vs. expression" rule, and trademark guidance for drug brand names.

**Purpose:** This is the spec for every glossary entry. It is the source of truth when rewriting existing entries, authoring new ones, or running LLM-assisted drafts. If an entry doesn't satisfy this guide, it isn't done.

**Use it as:** the reviewer's checklist, the author's brief, and the LLM prompt's grounding.

---

## 1. Who we're writing for

Two readers. Both must be served by every entry.

- **The curious outsider** — no industry context. A journalist, a friend at a dinner party, a junior person who just walked into pharma. Served by the **italic snappy line.**
- **The industry-adjacent generalist** — has *some* context (works at a biotech in marketing, covers the sector as an analyst, sits on the regulatory side and is reading a commercial deck). Served by the **detail paragraph.**

Voice in one phrase: **a smart friend who works in pharma explaining at coffee** — not Wikipedia, not a textbook, not WebMD, not a marketing deck.

> **Rule of thumb:** if removing the italic line would lose the outsider, the italic line is failing. If the detail paragraph reads like Wikipedia's first sentence, the detail paragraph is failing.

---

## 2. Entry anatomy

```
{
  "letter": "A",
  "term": "ADC",
  "full": "Antibody-Drug Conjugate",
  "snappy": "Think of it as a guided missile for cancer: an antibody that hunts down tumor cells, fused to a chemo drug that destroys them on contact.",
  "detail": "ADCs deliver toxic chemotherapy directly to cancer cells while sparing healthy ones, which means stronger results with fewer side effects than traditional chemo. They're a fast-growing class across breast, bladder, and lung cancers — well-known examples include Kadcyla (trastuzumab emtansine) and Enhertu.",
  "indications": ["Oncology"],
  "category": "Mechanism",
  "sources": ["NCI Dictionary of Cancer Terms"]
}
```

Every entry has:
- `term` — the headline (acronym or full term, written as you'd see it in print).
- `full` — the expanded form if `term` is an acronym; empty string if not.
- `snappy` — italic one-liner. See §3.
- `detail` — plain-English paragraph. See §4.
- `indications[]` — multi-tag from the controlled list (§7). Use `["General"]` for terms that aren't disease-specific.
- `category` — single tag from the controlled list (§7).
- `sources[]` — primary sources for the definition. See §8.

---

## 3. The italic snappy line

**Length target:** 18–30 words. Hard cap: 35.

**Job:** decode the term in one breath, no jargon, for someone who has never heard it before. If they read only this, they get the core idea.

**Allowed hooks** (pick one — different terms call for different hooks):

- **Metaphor:** *"Think of it as a guided missile for cancer..."* (ADC)
- **Analogy:** *"A measurable biological signal — like a fingerprint your body leaves behind..."* (Biomarker)
- **Transactional plain-English:** *"The deal where drug companies pay the FDA to review their applications on a clock..."* (PDUFA)
- **Direct definition:** *"A drug that activates a receptor in your body, like turning on a switch."* (Agonist)

**Forbidden in the italic line:**
- Industry jargon. If a word would make a journalist pause, it doesn't belong here.
- Hedge words: "may", "can", "is sometimes", "potentially", "in some cases".
- Marketing language: "groundbreaking", "revolutionary", "cutting-edge".
- Acronyms not already explained inside this line.
- Passive voice ("is administered", "is given by") — use active.

**Banned vocabulary in italic lines** (always rewrite around):
modality, MoA, indication, patient population, pivotal, label, endpoint, IND, NDA, BLA, CMC, GMP, GLP, REMS, label expansion, unmet need, mechanism of action, pharmacokinetics, pharmacodynamics, bioavailability, sponsor, regulatory, biomarker (unless this entry IS biomarker).

These can appear in the **detail** paragraph, with brief context.

**Tense and person:**
- Present tense.
- Second person ("you") OK when natural and inclusive ("a fingerprint *your body* leaves behind").
- Avoid first-person plural ("we use these to..." — no "we").

---

## 4. The detail paragraph

**Length target:** 40–80 words. Hard cap: 100.

**Job:** add context, real-world examples, and the "why it matters / where you'd hear it" beat. Written for someone who got the gist from the italic line and now wants the version they could repeat at the conference.

**Required structure** (loose — don't make it formulaic):

1. **Add precision** — what the italic line glossed over (mechanism, scope, specifics).
2. **Anchor with examples** — real drug names (with generics), diseases, companies, contexts.
3. **The "where you'd hear it" beat** — at least one phrase that tells the generalist *why this term shows up in their world*. Examples:
   - *"Investors and journalists watch the PDUFA date the way they watch earnings."*
   - *"You'll hear this constantly in oncology trial press releases."*
   - *"It's the question every analyst asks on the earnings call."*
   - *"Reps lean on this when explaining a label expansion to physicians."*

This beat is what differentiates JB Pharma from a textbook. **Don't drop it.**

**Allowed industry terms in detail paragraph:** FDA, EMA, clinical trial, approval, drug, treatment, biotech, oncologist, chemo, immunotherapy, radiation, surgery, antibody, gene, mutation, receptor, dose, side effect, label. Any other industry term must be explained in the same sentence or in an obviously bracketed example.

**Forbidden in detail paragraph:**
- Bullet lists (this is mobile prose, not a slide).
- Bold or italic emphasis (italic is reserved for the snappy line).
- Links (cross-refs in v1 are plain prose; v1.1 makes them tappable).
- Dosing recommendations or numbers ("Patients should take 50mg daily" — never).
- Specific clinical recommendations ("This is the preferred treatment for X" — never).
- Pricing claims ("Costs $100k a year" — even if true, drifts and ages badly).
- Hedge ladders: "It is generally believed that this may sometimes be the case in some patients."

---

## 5. Voice and tone

- **American English** spelling and idiom. App's primary market is US App Store. (e.g., "tumor" not "tumour", "fiber" not "fibre".)
- **Active voice** by default.
- **Conversational but precise.** Imagine you're explaining to a smart friend who genuinely wants to understand, not impress.
- **No hype.** No "groundbreaking", "revolutionary", "transformative". State what the thing is and why it matters; let the reader form their own view.
- **No editorializing.** Avoid "unfortunately", "tragically", "remarkably". The terms are doing enough work.
- **No first-person from the app.** Never "we recommend", "in our view". The glossary doesn't have opinions; it explains.

---

## 6. Drug names, examples, and references

**Drug name format on first mention in a detail paragraph:**

> Brand name (generic name)

Example: *Keytruda (pembrolizumab)*, *Enhertu (trastuzumab deruxtecan)*.

After the first mention in the same entry, you can use either form alone.

> See §8.5 for trademark rules: descriptive use inside entries is fine; brand names must stay out of the app's name, icon, screenshots, and marketing.

**Picking examples:**
- Prefer well-known examples over technically perfect ones. *Keytruda* lands; *Tislelizumab* doesn't.
- Use 1–2 examples max in a detail paragraph. More is clutter.
- For non-oncology entries (when we expand), pick examples from the relevant therapeutic area, not always oncology — e.g., for "REMS", use *Accutane (isotretinoin)* not a cancer drug.
- Don't recommend, rank, or claim superiority. *"Examples include..."* is fine; *"The leading example is..."* is not.

**What to never include:**
- Dosing, frequency, route of administration in clinical-instruction form.
- Specific pricing.
- "Best in class" / "first in class" / "blockbuster" / "billion-dollar drug" framing.
- Anything that could be read as medical advice.

---

## 7. Indication and category tagging

**Indication (multi-tag, controlled list):**
Oncology · Cardiovascular · Neurology · Rare Disease · Immunology · Metabolic · Infectious Disease · Respiratory · Gastroenterology · Dermatology · Ophthalmology · Women's Health · Mental Health · General

`General` is the right answer for terms that aren't disease-specific (PDUFA, GMP, biosimilar, GTN, REMS, MedDRA, formulary). When in doubt, prefer `General` over forcing a specific indication.

A term can have multiple indications when genuinely cross-cutting (e.g., "Biomarker" → `["General", "Oncology"]` because it's universal but most often discussed in onco).

**Category (single tag, controlled list):**
Clinical · Regulatory · Commercial / Market Access · Mechanism · Manufacturing · Pharmacovigilance · Diagnostics · Digital Health

Pick the **primary** category. If a term spans two, pick the one a generalist would most likely encounter it under.

**Quality check:** every term must have at least one indication tag and exactly one category. No exceptions.

---

## 8. Sources, citation, and IP

**Why we cite:** App Store reviewers treat medical content strictly. A visible sources list signals credibility, supports the medical disclaimer, and makes the app defensible.

### 8.1 The core principle: citation ≠ license

Citing a source does **not** grant a license to copy from it. Citation is editorial etiquette and a credibility signal — it is not legal cover. You can cite sources you are not allowed to copy.

What protects us legally is one of three things:
1. The source is **public domain**, or
2. The source's **license** permits commercial App Store redistribution, or
3. We use only the **facts** (which aren't copyrightable) and write in our **own original expression**.

**Operating rule for JB Pharma:** sources inform the facts; every entry is written from scratch in our own voice. No copy-paste from any source, ever — even from public domain ones, even for "just one sentence." This rule keeps us legally clean and editorially differentiated. The snappy/detail format already enforces original expression; this rule makes it explicit.

### 8.2 Approved primary sources (in preference order)

**Tier 1 — US federal government, public domain (17 U.S.C. § 105). Lead with these.**
1. **FDA** — glossaries, guidance documents, drug labels (Drugs@FDA, FDA Approved Drug Products).
2. **NCI Dictionary of Cancer Terms** — explicitly free to use, plain-language oncology gold standard.
3. **NIH MedlinePlus** — plain-language disease and drug descriptions. Note: some embedded third-party content is not public domain; stick to NIH-authored portions.
4. **NLM** drug information resources.
5. **CMS Glossary** — Centers for Medicare & Medicaid Services. Canonical source for formulary, coverage, reimbursement, and Medicare/Medicaid terminology. Public domain.

**Tier 2 — research-only references. Use to verify facts, do not copy text.**
5. **EMA glossary and guidance** — not US public domain. EMA permits reuse with attribution under their reuse policy, but it is not unrestricted; treat as research-only.
6. **WHO** content — typically licensed CC BY-NC-SA 3.0 IGO. **The "NC" (non-commercial) clause is incompatible with a paid App Store app or one with IAP/subscription.** Use as a fact reference; do not copy WHO text into the app. Citing WHO as a research source is fine.
7. **NCCN** patient and physician resources — strictly copyrighted. Use to verify clinical facts only; never copy any text. Substantial reuse requires permission.
8. **Established peer-reviewed reviews** (NEJM, Lancet, Nature Reviews Drug Discovery) — fully copyrighted. Use to learn facts; rewrite entirely.

**Do not use as sources at all:**
- **Wikipedia** — research only. Don't cite, don't copy. Their CC BY-SA license would propagate to derivative works.
- **Drug manufacturer websites** — perceived as biased, often copyrighted, often promotional.
- **Press releases, investor decks, news articles.**

### 8.3 How to cite

- One Tier-1 source per entry preferred. Two when a term genuinely spans (e.g., regulatory + clinical).
- Sources appear in the entry's `sources[]` array.
- An aggregated **Sources & Methodology** section appears in the About screen.
- Sources do **not** appear inline in the prose — keeps the detail paragraph clean.
- Cite honestly: list the source(s) that informed the facts in the entry. Do not list a source we did not actually use.

### 8.4 Compilation/database considerations

Copyright covers not just text but also the **selection and arrangement** of a list. Mirroring NCCN's term list in NCCN's order — even with rewritten definitions — could face a compilation copyright claim.

Mitigation: source terms from a wide range of references (FDA + NCI + MedlinePlus + EMA + our own editorial judgment about what generalists hit at conferences and in news). Don't mirror any single source's term list or order.

### 8.5 Trademark: drug brand names

This is a separate IP regime from copyright.

- **Generic drug names** (pembrolizumab, trastuzumab, atorvastatin) are International Nonproprietary Names designated by WHO. Free to use as ordinary words.
- **Brand names** (Keytruda, Enhertu, Lipitor, Ozempic) are registered trademarks of the manufacturer. Using them descriptively to identify the actual drug — *"Keytruda (pembrolizumab)"* — is **nominative fair use** in US law and is fine inside glossary entries.

**What we cannot do with brand names:**
- Use them in the app's **name, icon, screenshots, or marketing copy**.
- Imply **affiliation, endorsement, or sponsorship** by the manufacturer.
- Use them in any way that could **confuse a consumer** about who makes the app.

Apple's App Store Review specifically rejects apps that misuse third-party trademarks. Inside the glossary content, descriptive use is fine and useful for the reader. Outside (icon, App Store name/subtitle, promotional graphics) — keep it clean.

### 8.6 Quick checklist for any entry

- Did we use only public-domain sources for the facts, or write originally based on research?
- Did we copy zero text from any source? (Original expression in both snappy and detail.)
- Are the cited sources real, used, and from the approved list?
- If brand names appear, are they used descriptively (with generic name on first mention) and not in any promotional way?

---

## 9. Medical disclaimer & safety

This is the bright line.

**The glossary explains terms; it does not advise.** Never:
- Recommend a specific treatment.
- Suggest a dose, frequency, or route.
- Claim a treatment is "safe", "unsafe", "preferred", "best".
- Tell a reader what they should do for themselves or anyone else.
- Compare treatments by efficacy or side-effect profile in a way that reads as a clinical recommendation.

**Factual descriptions of risks are fine** when written as descriptions, not advice:
- ✓ *"Black Box Warning is the FDA's strongest safety alert — placed on a drug's label when it carries a risk of serious or life-threatening side effects."*
- ✗ *"You should be cautious about drugs with a Black Box Warning."*

The in-app medical disclaimer (separate copy task) reinforces all of this; the content style guide enforces it inside individual entries.

---

## 10. Cross-references

In v1, cross-references are plain prose — readers see related terms by name and search for them.

- **Mention related terms naturally** when they help understanding: *"...used in patients with HER2-positive breast cancer..."*
- **Don't shoehorn.** If a sentence reads better without the cross-ref, drop it.
- **Don't include a "See also:" section.** That's Wikipedia voice.
- **v1.1** will make these tappable; the content already supports it because we're using consistent term casing.

---

## 11. Length, format, mechanics

- **No bullet lists in detail.** Prose only.
- **No emphasis** (bold/italic) inside detail. Italic is reserved for the snappy line.
- **No links** in v1.
- **Numbers:** spell out under 10 in prose ("five years"); numerals for percentages, years, dose ranges-as-context, and trial phases ("Phase 3", "PDUFA date in Q3 2026").
- **Em dashes:** OK and encouraged for natural pauses — but don't overuse. Two per paragraph max.
- **Quotation marks:** use straight quotes in JSON (the editor will handle this).
- **No emoji.**
- **No exclamation points.**
- **End the snappy line and detail paragraph with a period.**

---

## 12. Quality checklist (run on every entry)

Before marking an entry done, answer all seven:

1. **Outsider test** — could a journalist who has never heard the term read just the italic line and get the core idea?
2. **Generalist test** — does the detail paragraph give an industry-adjacent reader something they could repeat in a meeting?
3. **"Where you'd hear it" beat** — is there at least one phrase telling the reader *why this term shows up in their world*?
4. **Banned-vocab scan** — zero forbidden jargon in the italic line.
5. **No-advice scan** — zero clinical recommendations, dosing, or "you should" phrasing.
6. **Tagging** — at least one indication, exactly one category, both from the controlled lists.
7. **Source** — at least one primary source from the allowed list.

If all seven are yes, the entry is done.

---

## 13. Worked example: rewriting an existing entry

**Current entry (v0):**
```json
{
  "letter": "A",
  "term": "Adjuvant",
  "full": "",
  "definition": "Treatment given after primary therapy (like surgery) to prevent cancer from coming back."
}
```

Issues: defines the term but no hook, no examples, no "where you'd hear it" beat, no tags, no source.

**Rewritten (v1):**
```json
{
  "letter": "A",
  "term": "Adjuvant",
  "full": "",
  "snappy": "The follow-up treatment after surgery or radiation, designed to mop up cancer cells you can't see and stop the disease coming back.",
  "detail": "Adjuvant therapy — usually chemo, hormone therapy, or immunotherapy — is what oncologists use to lower the chance of recurrence after the visible tumor has been removed. You'll hear it constantly in breast, colon, and lung cancer trial readouts, often framed around the question \"did adjuvant treatment improve survival?\"",
  "indications": ["Oncology"],
  "category": "Clinical",
  "sources": ["NCI Dictionary of Cancer Terms"]
}
```

Snappy = 22 words, no jargon, "mop up cancer cells you can't see" gives the outsider an instant mental picture. Detail = 49 words, includes example modalities, the "you'll hear it" beat ties it to trial readouts.

---

## 14. Open questions / future revisions

- Cross-reference linking format for v1.1 — `{Term}` markup or auto-detection?
- Multi-language: when does Spanish/French become worth the cost?
- Layered detail (TL;DR + expanded) for terms where 80 words isn't enough — defer until we hit a real case.
- Versioning of the glossary: each App Store update bumps a `glossaryVersion` so users can see what's new.

---

**This guide is meant to be edited.** When something here turns out to be wrong, fix it and bump the version at the top.

---

## 15. LLM-assisted authoring workflow

We use LLM assistance to scale content writing across ~470 entries without a pharma-domain expert reviewer. The workflow below mitigates the dominant risk (hallucinated medical facts) and is documented here so anyone can re-run it consistently.

### 15.1 Pass 1 — Source-grounded rewrite

For each entry being rewritten or authored, the prompt includes:

1. The **style guide** (this document) as system instructions.
2. The **8 calibration entries** as in-context examples (ADC, Adjuvant, PDUFA, Biomarker, Formulary, Black Box Warning, CDx, DTx).
3. The **actual source text** from a Tier-1 source (FDA glossary entry, NCI Dictionary of Cancer Terms entry, NIH MedlinePlus entry) — pasted verbatim into the prompt.
4. The **term being authored** with any existing v0 definition.
5. Instruction: rewrite this term in our format, paraphrasing the supplied source. Do not introduce facts not present in the source. If a fact in the source seems uncertain, omit it.

Why this matters: pasting the source converts the task from "recall facts from training" to "paraphrase a known-good text." Hallucination rate drops materially because the model isn't relying on memorized facts.

If no Tier-1 source covers the term cleanly, hand-author the entry. Don't ask the LLM to write it from training alone.

### 15.2 Pass 2 — Fresh-context fact-check

Every entry from Pass 1 goes through a second pass with **fresh context** (a new conversation, not the rewrite session):

> "Read this glossary entry. Identify any factual claim that cannot be supported by an FDA / NCI / MedlinePlus / EMA source. Flag drug examples, approval years, mechanism specifics, and indication scope. Quote the questionable sentence and explain the concern. If the entry is fully grounded, say so."

The fresh context prevents the model from rationalizing claims it just wrote. Flags from Pass 2 → human review against the source.

### 15.3 Cross-model diff (10% sample)

Pick a random 10% of authored entries (~45 entries). Have a different model family (different vendor, ideally) author them independently from the same source-grounded prompt. Diff the two outputs for the same term.

Material disagreements (different drug examples, different mechanism descriptions, different approval pathways) → human review against the source. Stylistic differences are ignored.

### 15.4 Spot-check sampling

Before TestFlight build, manually verify 25-30 random entries (~6%) by:
- Reading the entry.
- Looking up the term in the cited Tier-1 source.
- Checking that every factual claim in the entry is supported by the source.

If error rate >5% in the sample, halt; the workflow needs adjustment before submission.

### 15.5 Voice-consistency pass

After all entries are authored, do a single human read-through (or LLM-assisted read-through with the §12 checklist) of the full file in alphabetical order, looking for:
- Italic-line voice drift (does the snappy line still sound consistent?).
- Length outliers (italic line >30 words, detail >80 words — tighten).
- "Where you'd hear it" beat dropped.
- Banned vocab in italic lines (run the §3 banned-vocab list as a regex).

### 15.6 In-app feedback loop (post-launch)

The About screen and every term detail screen include a "Report an error" mailto link to a triage inbox. Errors flagged by users are:
- Triaged within 1 week.
- Verified against Tier-1 sources.
- Fixed in the next monthly app update.
- Logged in `CONTENT_CHANGELOG.md` (future file) so changes are auditable.

This loop is the long-tail safety net. We don't rely on it for v1.0 quality, but it's how the corpus stays accurate over time.

### 15.7 What this workflow does NOT cover

- **Subjective quality** — "is this entry actually useful for the generalist?" is a judgment call that needs a human read.
- **Strategic gaps** — what terms are missing that a generalist would expect to find. Driven by editorial judgment, not LLM.
- **Non-medical IP risks** — trademark, copyright (covered in §8).

These are author/editor responsibilities, not LLM tasks.
