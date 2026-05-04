# JB Pharma — Calibration Entries

**Status:** v1.0, 2026-05-04. Locked corpus.

**Purpose:** Eight hand-authored entries that ground the voice, length, structure, and tagging conventions for every other entry in the glossary. These are the canonical examples the LLM batch-rewrite prompt is given (alongside `CONTENT_STYLE_GUIDE.md`) so the model can pattern-match against on-spec output.

**Coverage:** One entry per category (per §7 of the style guide), with a deliberate mix of italic-line hooks (metaphor, analogy, transactional, direct definition) so the LLM has variety to ground against rather than over-fitting to a single hook style.

| # | Term | Category | Italic-line hook | Letter |
|---|---|---|---|---|
| 1 | ADC | Mechanism | Metaphor | A |
| 2 | Adjuvant | Clinical | Direct definition | A |
| 3 | PDUFA | Regulatory | Transactional | P |
| 4 | Biomarker | Mechanism (general) | Analogy | B |
| 5 | Formulary | Commercial / Market Access | Transactional | F |
| 6 | Black Box Warning | Pharmacovigilance | Metaphor | B |
| 7 | CDx | Diagnostics | Direct definition | C |
| 8 | DTx | Digital Health | Analogy | D |

When updating these entries, treat them as a canonical reference. Voice changes here propagate to every batch-authored entry, so changes need careful thought — bump the version at the top.

---

## 1. ADC

```json
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

---

## 2. Adjuvant

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

---

## 3. PDUFA

```json
{
  "letter": "P",
  "term": "PDUFA",
  "full": "Prescription Drug User Fee Act",
  "snappy": "The deal where drug companies pay the FDA to review their applications on a clock — and Congress renews it every five years.",
  "detail": "PDUFA sets the FDA's review timeline — typically 10 months for standard drugs, 6 months for priority ones — and is funded by industry fees rather than taxpayers. Investors and journalists watch the \"PDUFA date\" the way they watch earnings: it's the day the FDA must rule on whether a drug gets approved.",
  "indications": ["General"],
  "category": "Regulatory",
  "sources": ["FDA"]
}
```

---

## 4. Biomarker

```json
{
  "letter": "B",
  "term": "Biomarker",
  "full": "",
  "snappy": "A measurable biological signal — like a fingerprint your body leaves behind — that tells doctors what's happening inside you.",
  "detail": "Biomarkers can be molecules in your blood (such as PSA for prostate cancer), genetic mutations (such as HER2 in breast cancer), or imaging signals. Pharma uses them to diagnose disease, predict which patients will respond to a drug, and track whether a treatment is working — they're the foundation of \"precision medicine.\"",
  "indications": ["General", "Oncology"],
  "category": "Mechanism",
  "sources": ["NCI Dictionary of Cancer Terms"]
}
```

---

## 5. Formulary

```json
{
  "letter": "F",
  "term": "Formulary",
  "full": "",
  "snappy": "The list of drugs your insurance will pay for — and the rules that decide what it costs you when you fill a prescription.",
  "detail": "Insurers and pharmacy benefit managers (PBMs) build formularies to control costs, negotiating rebates with drugmakers in exchange for preferred placement. A drug's tier on the formulary determines patient copays, prior-authorization requirements, and ultimately how easily it gets prescribed. Pharma launch teams obsess over formulary access — at JPMorgan and on earnings calls you'll hear it called \"access\" or \"reimbursement,\" and it's often the difference between a drug's commercial success and failure.",
  "indications": ["General"],
  "category": "Commercial / Market Access",
  "sources": ["CMS Glossary"]
}
```

---

## 6. Black Box Warning

```json
{
  "letter": "B",
  "term": "Black Box Warning",
  "full": "",
  "snappy": "The FDA's strongest safety alert — a warning printed in a literal black-bordered box on a drug's label when the risks are serious enough to demand prescriber attention.",
  "detail": "Black Box Warnings are added when post-market surveillance or clinical trials reveal a risk of serious harm — well-known examples include certain antidepressants flagged for suicide risk in young patients, and some immunotherapies for severe autoimmune side effects. The warning doesn't pull a drug from the market; it requires prescribers to weigh the risk explicitly. You'll see the term in FDA press releases, legal proceedings, and any commercial discussion of a drug's market trajectory after the warning lands.",
  "indications": ["General"],
  "category": "Pharmacovigilance",
  "sources": ["FDA"]
}
```

---

## 7. CDx

```json
{
  "letter": "C",
  "term": "CDx",
  "full": "Companion Diagnostic",
  "snappy": "A diagnostic test paired with a specific drug — used to find the patients whose biology makes the drug likely to actually work for them.",
  "detail": "The FDA approves many targeted therapies — especially in oncology — only alongside an approved diagnostic test that confirms the patient has the specific mutation or protein the drug targets. Herceptin (trastuzumab) for HER2-positive breast cancer is the textbook example. You'll hear CDx in approval announcements and commercial discussions, where access to testing often matters as much as access to the drug itself.",
  "indications": ["General", "Oncology"],
  "category": "Diagnostics",
  "sources": ["FDA"]
}
```

---

## 8. DTx

```json
{
  "letter": "D",
  "term": "DTx",
  "full": "Digital Therapeutic",
  "snappy": "A software-based treatment — usually an app — designed to prevent or manage a medical condition, sometimes prescribed by a doctor like a pill.",
  "detail": "Digital therapeutics deliver evidence-based interventions through software, ranging from cognitive behavioral therapy apps for insomnia to attention-training games for ADHD. Some are FDA-cleared and prescription-only — known as \"PDTs\" (Prescription Digital Therapeutics) — while others are over-the-counter. You'll hear DTx in pharma earnings calls when companies pitch software as the next growth frontier, and at health-tech conferences where pilots are being run with insurers.",
  "indications": ["General"],
  "category": "Digital Health",
  "sources": ["FDA"]
}
```

---

## How to use this file

When designing the LLM batch-rewrite prompt:
- Pass `CONTENT_STYLE_GUIDE.md` as system instructions.
- Pass these eight entries as in-context examples.
- For each term being authored, pass the relevant Tier-1 source text (per §15.1) as the grounding for facts.
- Ask the model to produce the same JSON shape.
- Run Pass 2 fact-check (§15.2) in fresh context.

When updating these entries: bump the version, document what changed, and re-run a sample of recently-authored entries through the prompt to verify the new calibration produces consistent output.
