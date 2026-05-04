# JB Glossary — Content Style Guide

**Status:** v1.0, 2026-05-04. The brief that travels across every glossary in the suite (JB Pharma, JB Med Devices, JB Finance, etc.). Voice rules are the same; vocabulary changes per industry.

## Who we're writing for

The **generalist** — someone who hits a term at a conference, in a meeting, or in news and needs to understand it instantly. Not a specialist's encyclopedia, not a layperson's primer. Industry-adjacent: investors, journalists, junior consultants, marketing/comms, sales, regulatory, plus the curious outsider.

Two readers, both served:
- **Curious outsider** — no industry context. Served by the italic snappy line.
- **Industry-adjacent generalist** — has some context. Served by the detail paragraph.

Voice in one phrase: **a smart friend who works in the industry, explaining at coffee.**

## Entry shape

```json
{
  "letter": "A",
  "term": "ADC",
  "full": "Antibody-Drug Conjugate",
  "snappy": "italic line, 18-30 words",
  "detail": "paragraph, 40-80 words, with a 'where you'd hear it' beat",
  "indications": ["Oncology"],
  "category": "Mechanism",
  "sources": ["NCI Dictionary of Cancer Terms"]
}
```

## The italic snappy line

- 18-30 words. Hard cap 35.
- Plain English. Use one of four hooks: metaphor, analogy, transactional plain-English, or direct definition.
- **No jargon.** Banned in the italic line: modality, MoA, indication, patient population, pivotal, label, endpoint, IND, NDA, BLA, REMS, mechanism of action, pharmacokinetics, pharmacodynamics, sponsor, regulatory, biomarker (unless the entry IS biomarker).
- No hedge words (may, can, sometimes, potentially), no marketing language (groundbreaking, revolutionary), no passive voice, no acronyms unexplained inside the line.
- Active voice. Present tense. Second person OK ("you'll hear...").

## The detail paragraph

- 40-80 words. Hard cap 100.
- Plain language. Light industry vocabulary OK because the outsider already got the gist from the italic line.
- **Must include a "where you'd hear it" beat** — at least one phrase tying the term to the generalist's world: earnings calls, conference floors, FDA press releases, trial readouts, JPMorgan, ASCO, investor decks. This is the differentiator vs. a textbook glossary.
- Anchor with examples — real drug names, diseases, contexts. Drug names on first mention: brand (generic), e.g., Keytruda (pembrolizumab).
- No bullet lists, no bold/italic emphasis, no links. Prose only.
- **Never:** dosing recommendations, clinical advice ("you should"), comparative efficacy claims, pricing claims.

## Tagging

- **Indications** (multi-tag, controlled list): Oncology, Cardiovascular, Neurology, Rare Disease, Immunology, Metabolic, Infectious Disease, Respiratory, Gastroenterology, Dermatology, Ophthalmology, Women's Health, Mental Health, General. Use **General** for terms that aren't disease-specific (PDUFA, GMP, formulary, biosimilar). Multi-tag when genuinely cross-cutting.
- **Category** (single, controlled list): Clinical, Regulatory, Commercial / Market Access, Mechanism, Manufacturing, Pharmacovigilance, Diagnostics, Digital Health.

## Sources and IP

- Definitions are paraphrased from US public-domain references (FDA, NCI Dictionary of Cancer Terms, NIH MedlinePlus, NLM, CMS Glossary) and standard pharma references. Cite the primary source in the `sources[]` array.
- **Never copy text verbatim** from any source — write originally, even from public-domain sources. The format already enforces this.
- **Drug brand names** are trademarks. Descriptive use inside entries (e.g., "Keytruda (pembrolizumab)") is nominative fair use. **Never use brand names in the app's name, icon, screenshots, or marketing.**

## Quality checklist (every entry)

1. Outsider test — italic line lands?
2. Generalist test — detail repeatable in a meeting?
3. "Where you'd hear it" beat present?
4. Banned vocab in italic line: zero?
5. No-advice scan: zero clinical recommendations or dosing?
6. Tagging: ≥1 indication, exactly 1 category?
7. Source: ≥1 primary source cited?

If any check fails, fix or cut.
