# Pass 2 — Fresh-Context Fact-Check Prompt

**Status:** v1.0, 2026-05-04.

**Purpose:** Audit a Pass 1-produced glossary entry for unsupported factual claims. Run in **fresh context** (a new conversation, no Pass 1 history) so the model is not anchored to claims it just generated.

**Companion docs:**
- `PASS_1_REWRITE.md` — the rewrite step that produced the entry under review
- `CONTENT_STYLE_GUIDE.md` — full spec
- `RUNBOOK.md` — per-batch workflow

---

## How to use

For every Pass 1 output, before committing it to `glossary.json`:

1. Open a **new** Claude.ai conversation (or fresh API call) — do not use the same session as Pass 1.
2. Paste the system prompt below.
3. Paste the entry under review as the user message.
4. Read the flags. For each flag, check the cited Tier-1 source:
   - If the claim is supported, ignore the flag (the model was being conservative).
   - If the claim is unsupported, fix it (rewrite, soften, or omit) and re-run Pass 2.
5. Repeat until verdict is "clean" or remaining flags are confirmed false-positives.

Pass 2 is conservative by design — it catches false positives sometimes, which is the right tradeoff for medical content. Better to verify five clean claims than miss one drift.

---

## System prompt (copy verbatim)

```
You are an auditor reviewing a single glossary entry for JB Pharma Glossary, a pharma/healthcare reference iOS app shipping to the App Store.

Your job is to flag any factual claim that may not be supported by an authoritative US-government / public-domain source (FDA, NCI Dictionary of Cancer Terms, NIH MedlinePlus, NLM, CMS Glossary), or by EMA's reuse-policy content as a secondary check.

Examine the entry closely. Pay particular attention to:
- Drug name + indication mappings ("Herceptin for HER2-positive breast cancer", "Keytruda for melanoma")
- Approval years, approval pathways, regulatory status, label-expansion claims
- Mechanism descriptions (does the protein/pathway/biology actually work as described?)
- Trial-phase, line-of-therapy, or patient-population claims
- Regulatory facts (PDUFA dates, REMS programs, accelerated-approval pathway, etc.)
- Numerical claims (timelines, percentages, dose ranges if any slipped through, market sizes)
- Brand-name/generic-name pairings ("Kadcyla (trastuzumab emtansine)") — pairing must be correct
- "Examples include" lists — every drug listed must actually fit the description

For each claim you cannot confidently verify against a Tier-1 source, output a flag with:
- "sentence": the exact sentence containing the claim
- "concern": the specific worry (e.g., "Approval year not in source", "Drug X may not actually be a Y", "Mechanism described incorrectly")
- "suggestion": one of: "rewrite to soften / omit / verify against [source name] / replace example with [alternative]"

Do NOT flag stylistic issues — only factual concerns. Voice, length, tone, banned vocab are someone else's job.

Do NOT flag claims you can confidently verify yourself. The signal is reserved for genuine concerns.

Do NOT flag basic definitional content that is general knowledge in the field (e.g., "Phase 3 trials are large and pivotal").

OUTPUT FORMAT (strict — output one of these two shapes only):

If you find concerns, output a JSON array:
[
  { "sentence": "...", "concern": "...", "suggestion": "..." },
  ...
]

If the entry is fully grounded, output exactly:
VERDICT: clean

Do not output prose around the JSON. Do not use markdown code fences.
```

---

## Per-entry user message template

```
ENTRY UNDER REVIEW:

[paste the full JSON entry from Pass 1, or paste it as readable prose]
```

---

## Examples of what Pass 2 should catch vs. ignore

**Should flag:**
- "Herceptin (trastuzumab) was first approved in 1995 for HER2-positive breast cancer." — actual approval year is 1998. Flag with suggestion: "verify approval year against FDA Drugs@FDA."
- "Keytruda (pembrolizumab) is the leading checkpoint inhibitor." — comparative claim, also "leading" is banned. Flag for both content and style — but Pass 2 only owns the content side: "Comparative efficacy claim ('leading'); rewrite to remove ranking."
- "ADCs work by binding to a tumor antigen and releasing payload extracellularly." — actually most ADCs are internalized before payload release. Flag mechanism.

**Should ignore:**
- "Phase 3 trials are large, pivotal studies." — general field knowledge, fine.
- "PDUFA review clocks are typically 10 months for standard drugs." — this is in PDUFA documentation; well-supported.
- Stylistic issues: "snappy line is 33 words" or "italic line uses jargon" — Pass 2's not the place.
- "Kadcyla (trastuzumab emtansine)" — correct brand/generic pairing, no flag.

---

## How to act on flags

For each flag, do one of:

1. **Verify and dismiss:** open the cited source. If the claim IS supported, the flag was a false positive. Move on.
2. **Soften:** if the claim is partially supported, rephrase to match what the source actually says ("approved in the late 1990s" instead of a specific year you can't verify).
3. **Omit:** if you can't verify and the entry doesn't need the claim, delete the sentence.
4. **Replace:** if a drug example seems wrong, swap for one explicitly named in the source.
5. **Rewrite from scratch:** if multiple flags hit, the underlying source-grounded prompt may have failed. Re-run Pass 1 with a better source text.

After any fix, re-run Pass 2 in fresh context. Iterate until "VERDICT: clean" or remaining flags are confirmed false-positives.

---

## When Pass 2 disagrees with Pass 1

Pass 2 is the tiebreaker. If Pass 2 flags a claim and you cannot verify the claim against a Tier-1 source, **trust Pass 2** — soften, omit, or replace. The whole point of running them in separate contexts is independent judgment.

The exception: Pass 2 over-flags general field knowledge sometimes. If a claim is genuinely in the "any pharma generalist knows this" bucket and is supported by multiple Tier-1 sources, it's safe to override Pass 2.
