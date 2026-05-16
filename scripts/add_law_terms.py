"""Idempotently merge US-law terms into Targets/Law/Resources/glossary.json.

Mirrors scripts/add_ai_terms.py — append-only, case-insensitive dedup against
existing terms, sort by (letter asc, term asc) on write. Each batch is a
Python list built via the entry() helper which enforces category +
indication enums so we don't drift away from the lenses in LawBrand.swift.

Voice: plain English for a generalist (citizen, journalist, business
owner). Snappy line ~12 words, must make sense WITHOUT prior legal
knowledge. Detail 50–75 words with a concrete anchor (famous case, common
clause, news headline, statute citation).

Usage:
    python scripts/add_law_terms.py
    python scripts/add_law_terms.py --batches 1,2     # run specific batches
    python scripts/add_law_terms.py --dry-run         # preview without writing
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

GLOSSARY = Path(__file__).parent.parent / "Targets" / "Law" / "Resources" / "glossary.json"

# Keep in sync with Targets/Law/LawBrand.swift `lenses[].kind` category lists.
VALID_CATEGORIES = {
    # Practice lens
    "Contract", "IP", "Property", "Tort", "Procedure",
    # Public-law lens
    "Criminal", "Constitutional", "Regulatory",
}

VALID_INDICATIONS = {
    "General", "Personal", "Business",
    "Litigation", "Transactional",
    "Federal", "State", "International",
}


def entry(term, full, snappy, detail, sources, indications=None, category="Contract"):
    assert category in VALID_CATEGORIES, f"Unknown category '{category}' for term '{term}'"
    indications = indications or ["General"]
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
# BATCH 1 — Civil Procedure basics (16 terms)
# ============================================================================

BATCH_PROCEDURE = [
    entry(
        "Burden of proof", "",
        "Which side has to prove its case, and how convincingly.",
        "In US civil cases the plaintiff usually has to prove its case by a 'preponderance of the evidence' — more likely than not. Criminal prosecutions are much harder: 'beyond a reasonable doubt'. Some civil claims (fraud, deportation, parental-rights termination) sit in between at 'clear and convincing'. Who carries the burden, and at what level, often decides the case before any facts are weighed.",
        ["Cornell LII", "US Courts"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Complaint", "",
        "The opening document of a lawsuit — what the plaintiff says happened and what they want.",
        "Filed in court, served on the defendant. It names the parties, lays out the facts, identifies the causes of action (negligence, breach of contract, etc.), and asks for specific relief (money, an injunction, declaratory judgment). Sloppy complaints can be dismissed under Federal Rule 12(b)(6) for failure to state a claim — Bell Atlantic v. Twombly (2007) raised the bar.",
        ["Cornell LII", "Federal Rules of Civil Procedure"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Answer", "",
        "The defendant's first written response to a complaint — admit, deny, or 'lack knowledge'.",
        "Due roughly 21 days after service in federal court. The answer responds paragraph-by-paragraph to the complaint and raises affirmative defences (statute of limitations, contributory negligence, release). Failure to deny an allegation is treated as admission. The answer may also include counterclaims against the plaintiff.",
        ["Federal Rules of Civil Procedure", "Cornell LII"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Motion", "",
        "A formal written request asking the judge to do something — dismiss the case, suppress evidence, grant summary judgment.",
        "Motions drive most of pretrial litigation. The motion to dismiss tests whether the complaint, even if true, states a legal claim. The motion for summary judgment asks the judge to decide without a trial because no factual dispute matters. Motions in limine handle evidence rulings before trial begins. Each is briefed by both sides, often with oral argument.",
        ["Cornell LII", "Federal Rules of Civil Procedure"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Discovery", "",
        "The pretrial phase where each side exchanges evidence — documents, depositions, interrogatories.",
        "Discovery is how parties learn what the other side knows before trial. It's expensive and often the most contentious phase: document productions can run into the millions in big commercial cases. Modern e-discovery covers email, Slack, text messages, and cloud storage. Rules limit scope to information 'relevant to any party's claim or defense' and proportional to the case.",
        ["Federal Rules of Civil Procedure", "Cornell LII"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Deposition", "",
        "Pretrial questioning of a witness under oath, transcribed by a court reporter.",
        "Lawyers from both sides attend; the witness answers questions live, usually for a single day capped at seven hours under the federal rules. The transcript can be used at trial to impeach inconsistent testimony or, if the witness is unavailable, as substantive evidence. Video depositions are now standard, especially after the pandemic normalised remote testimony.",
        ["Federal Rules of Civil Procedure"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Subpoena", "",
        "A court-backed order to appear, testify, or produce documents — ignore it and you can be held in contempt.",
        "Two flavours: subpoena ad testificandum (testify) and subpoena duces tecum (bring documents). Issued by parties to a lawsuit, by grand juries, and by congressional committees. Targets can move to quash for overbreadth, undue burden, or privilege. High-profile recent examples: the January 6th committee subpoenas; SEC subpoenas in crypto enforcement actions.",
        ["Cornell LII", "Federal Rules of Civil Procedure"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Affidavit", "",
        "A written statement of facts sworn under oath — used as evidence when live testimony isn't available.",
        "Routinely attached to motions to back up factual assertions. The signer (the 'affiant') swears under penalty of perjury that the statements are true. Many courts now accept the substitute 'declaration under penalty of perjury' which doesn't require a notary. False statements in either are prosecutable as perjury.",
        ["Cornell LII", "Federal Rules of Civil Procedure"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Summons", "",
        "The official notice telling a defendant they've been sued and must respond.",
        "Served along with the complaint by a process server or sheriff. Improper service can get a case dismissed. The summons states which court, the deadline to answer (typically 21 days in federal court), and the consequences of not appearing — a default judgment that can be enforced like any other.",
        ["Federal Rules of Civil Procedure"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Jurisdiction", "",
        "Whether a court has the legal power to hear a particular case.",
        "Two questions: subject-matter jurisdiction (does this court handle this type of case — federal vs state, civil vs criminal) and personal jurisdiction (does the court have authority over this specific defendant). Personal jurisdiction over out-of-state defendants is the modern battleground, especially for online conduct and product liability. International Shoe v. Washington (1945) is the founding case.",
        ["Cornell LII"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Venue", "",
        "The geographic court where a case should be heard, even if multiple courts have jurisdiction.",
        "Federal venue rules generally permit suit where the defendant resides or where a substantial part of the events occurred. Venue can be transferred 'for the convenience of parties and witnesses' under 28 USC § 1404. Forum-selection clauses in contracts pre-pick the venue and are usually enforced absent strong policy reasons not to.",
        ["Cornell LII"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Standing", "",
        "Whether a plaintiff has suffered a real, concrete injury that lets them sue at all.",
        "Article III standing requires injury-in-fact, traceability to the defendant's conduct, and redressability by a court. The Supreme Court has narrowed standing in privacy and statutory-damages cases (Spokeo, TransUnion v. Ramirez 2021) — a bare statutory violation isn't enough. State courts often have looser standing rules than federal courts.",
        ["Cornell LII"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Settlement", "",
        "The parties agree to resolve the dispute themselves before the court decides.",
        "Roughly 95% of US civil cases settle. Settlement usually involves a payment plus a release of claims — sometimes confidential, often with a non-disparagement clause. Class-action settlements require court approval to protect absent class members. After Epic Systems v. Lewis (2018), pre-dispute arbitration agreements steer many disputes out of court before any settlement is needed.",
        ["Cornell LII", "ABA Public Education"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Verdict", "",
        "The jury's or judge's formal decision at the end of a trial.",
        "In jury trials the verdict is the jury's answer to the questions put to it. Most civil verdicts in federal court require unanimity; some states allow non-unanimous civil verdicts. Bench trials produce 'findings of fact and conclusions of law' rather than a jury verdict. Either way, the verdict becomes a judgment when the court enters it on the docket, starting the appeal clock.",
        ["Cornell LII", "Federal Rules of Civil Procedure"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Appeal", "",
        "Asking a higher court to review and possibly overturn the trial court's decision.",
        "Appellate courts don't retry the facts; they review for legal error and abuse of discretion. The federal system has 13 circuit courts of appeals and the Supreme Court at the top. Most appeals affirm. A successful appeal can mean reversal, remand for a new trial, or modification of the judgment. Strict deadlines apply — usually 30 days from judgment in federal civil cases.",
        ["US Courts", "Cornell LII"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    entry(
        "Class action", "",
        "A lawsuit where one plaintiff sues on behalf of a large group with similar claims.",
        "Governed by Federal Rule 23: commonality, typicality, adequacy of representation, and either predominance (for damages classes) or cohesion (for injunctive classes). Common in consumer fraud, antitrust, and securities cases. The Supreme Court's Wal-Mart v. Dukes (2011) and Comcast v. Behrend (2013) tightened certification. After AT&T v. Concepcion (2011), arbitration clauses with class waivers have shrunk the class-action footprint in consumer disputes.",
        ["Cornell LII", "Federal Rules of Civil Procedure"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
]


# ============================================================================
# BATCH 2 — Contract basics (16 terms — 'Contract' itself is in the stub)
# ============================================================================

BATCH_CONTRACT_BASICS = [
    entry(
        "Offer", "",
        "A clear proposal that, if accepted, creates a contract.",
        "An offer must be definite enough that a reasonable person would understand they could close the deal by accepting. Advertisements are usually not offers — they're invitations to deal. The Lefkowitz fur-coat case (1957) is the classic counterexample: a clear quantity and price plus 'first come, first served' made the ad itself an offer. An offer can be revoked any time before acceptance, with narrow exceptions.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["General", "Transactional"],
        category="Contract",
    ),
    entry(
        "Acceptance", "",
        "Agreement to the exact terms of the offer — that's what forms the contract.",
        "Under the 'mirror image rule', acceptance has to match the offer; a counter-offer kills the original. The UCC relaxes this for sales of goods (§ 2-207, the 'battle of the forms'). Acceptance can be by signing, by performance, or sometimes by silence if the parties have a course of dealing. The 'mailbox rule' makes acceptance effective when sent, not when received — important when offers are revoked in the gap.",
        ["Restatement of Contracts", "UCC"],
        indications=["General", "Transactional"],
        category="Contract",
    ),
    entry(
        "Consideration", "",
        "Something of value each side gives up — what makes a promise legally binding rather than just a gift.",
        "Could be money, goods, services, forbearance from a legal right, or a return promise. Courts won't second-guess whether the exchange is fair (no 'adequacy of consideration' inquiry) — $1 for a house is enforceable as long as both sides meant it. Past consideration doesn't count; nor does a 'pre-existing duty'. Without consideration, you're looking at gift, not contract — see promissory estoppel for the workaround.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["General", "Transactional"],
        category="Contract",
    ),
    entry(
        "Breach", "",
        "Failing to perform a contractual obligation when performance was due.",
        "Material breach excuses the other side from continuing performance and triggers damages. Minor breach (substantial performance) still entitles the non-breacher to damages but not to walk away. Anticipatory breach — making clear you won't perform before the time arrives — lets the other side sue immediately. The choice between repudiation and waiting matters: act too early and you're the breaching party.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["General", "Litigation", "Transactional"],
        category="Contract",
    ),
    entry(
        "Damages", "",
        "Money awarded to make the non-breaching party whole.",
        "Expectation damages are the default — put the plaintiff in the position they'd have been in had the contract been performed. Reliance damages refund what they spent. Restitution returns what was paid. Consequential damages cover foreseeable losses beyond the contract itself (Hadley v. Baxendale, 1854). Liquidated damages clauses pre-set the number; courts strike them as 'penalties' if they aren't a reasonable forecast.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["General", "Litigation"],
        category="Contract",
    ),
    entry(
        "Specific performance", "",
        "Court order forcing the breaching party to actually do what they promised, not just pay.",
        "An equitable remedy granted when money damages are inadequate — typically real-estate sales (every parcel of land is treated as unique), rare goods, and some custom services. Courts won't order specific performance of personal-service contracts (no involuntary servitude) or where supervision would be impractical. Specific performance is the default remedy in many civil-law countries; in the US it remains the exception.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["General", "Litigation"],
        category="Contract",
    ),
    entry(
        "Warranty", "",
        "A guarantee about a fact or future performance — break it and you're liable.",
        "Express warranties are stated outright ('this car has 50,000 miles'). Implied warranties arise automatically: merchantability (the product works for its ordinary purpose) and fitness for a particular purpose (the seller knew the buyer's use case). The UCC governs goods; service contracts use 'workmanlike' standards. Disclaimers must be conspicuous (the famous 'AS IS' in all caps) to be effective.",
        ["UCC", "Cornell LII"],
        indications=["General", "Transactional"],
        category="Contract",
    ),
    entry(
        "NDA", "Non-disclosure agreement",
        "A contract to keep specified information confidential.",
        "Unilateral (one side discloses) or mutual (both do). Key terms: scope of confidential information, exclusions (already public, independently developed), duration of obligation, permitted uses, return-or-destroy at termination. Overbroad NDAs run into trade-secret defences and, in some states, anti-NDA statutes for sexual harassment. Federal Defend Trade Secrets Act notice should be included to preserve whistleblower-immunity protections.",
        ["Cornell LII", "USPTO"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Indemnity", "",
        "One party agrees to cover the other's losses from defined risks.",
        "Common in commercial contracts: vendor indemnifies customer for IP-infringement claims arising from the vendor's product. Indemnity clauses fight over scope (which claims), procedure (control of defence, consent to settle), and caps (liability ceilings). Insurance is the financial backing; many indemnity obligations are uninsurable if not crafted carefully. Mutual indemnity is common between commercial peers.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Liquidated damages", "",
        "A pre-set dollar amount the breaching party must pay — written into the contract.",
        "Enforceable if (a) actual damages would be hard to quantify at signing, and (b) the amount is a reasonable forecast of likely harm. Courts strike them as 'penalty clauses' if they look punitive — e.g., a $1,000-per-day fee bearing no relation to actual delay costs. Common in construction (delay damages), software (SLA credits), and real-estate purchase agreements (forfeiture of earnest money).",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Force majeure", "",
        "A clause excusing performance when 'acts of God' or named disruptive events occur.",
        "From the French 'superior force'. Triggers vary by clause: wars, strikes, pandemics, government action, supply-chain failure. COVID-19 spawned a wave of force-majeure disputes; results turned on whether the clause specifically listed pandemics or just 'unforeseeable events'. Best-practice modern clauses list named events and add a catch-all, with notice obligations and a duty to mitigate.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Statute of frauds", "",
        "Rule that certain contracts must be in writing to be enforceable.",
        "Originating in a 1677 English statute. The classic six: sales of land, contracts that can't be performed within a year, sales of goods over $500 (UCC § 2-201), promises to pay another's debt (suretyship), marriage-consideration agreements, and contracts in consideration of marriage. A 'writing' just needs to identify the parties, subject matter, and essential terms — and be signed by the party to be charged. Email and DocuSign qualify under the federal E-SIGN Act.",
        ["Cornell LII", "UCC"],
        indications=["General", "Transactional"],
        category="Contract",
    ),
    entry(
        "Voidable", "",
        "A contract one party can choose to cancel — distinct from a 'void' contract (no contract at all).",
        "Common voidable scenarios: a minor's contract (the minor can disaffirm), contracts induced by fraud or duress, contracts entered while intoxicated or mentally incapacitated. The non-injured party can ratify (confirm) or rescind. Void contracts — illegal subject matter, missing essential elements — were never enforceable in the first place. The distinction matters for who can do what about the deal.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["General", "Litigation"],
        category="Contract",
    ),
    entry(
        "Unconscionable", "",
        "So unfair that no reasonable person would agree and no fair person would impose it.",
        "Two prongs: procedural unconscionability (unfair surprise, hidden terms, take-it-or-leave-it) and substantive unconscionability (terms grossly favouring one side). Courts can refuse to enforce the contract or reform the offending clause. Arbitration clauses with class waivers and one-sided fee provisions are the modern battlefield. Carnival Cruise v. Shute (1991) and AT&T v. Concepcion (2011) sharply limited the doctrine's reach.",
        ["Cornell LII", "UCC"],
        indications=["General", "Litigation"],
        category="Contract",
    ),
    entry(
        "Capacity", "",
        "Whether a party is legally able to enter a contract at all.",
        "Minors (under 18 in most states) generally can disaffirm contracts; they're still liable for necessaries (food, shelter, basic medical). Mental incapacity — inability to understand the nature and consequences — also makes a contract voidable. Intoxication only voids if the other party knew. Corporations have capacity to contract within their charter; ultra-vires doctrines are now largely vestigial.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["General", "Personal"],
        category="Contract",
    ),
    entry(
        "Mutual assent", "",
        "Both sides have to mean the same thing — the 'meeting of the minds'.",
        "Assessed objectively: what would a reasonable person have understood from the words and conduct, not what the parties privately thought. Mistakes about identity, subject matter, or terms can negate assent. Raffles v. Wichelhaus (1864) — the famous 'Peerless' ship case — held no contract when two ships of the same name caused genuine confusion. Modern courts rarely rescue parties from their own carelessness.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["General", "Transactional"],
        category="Contract",
    ),
]


# ============================================================================
# BATCH 3 — IP basics (15 terms)
# ============================================================================

BATCH_IP = [
    entry(
        "Patent", "",
        "Government-granted monopoly on a new invention for ~20 years.",
        "Issued by the USPTO after examination for novelty, non-obviousness, and utility. Three types: utility (new functional inventions), design (ornamental designs), and plant (new plant varieties). The patent owner can exclude others from making, using, or selling — but doesn't necessarily have the right to practise their own invention if it infringes someone else's patent. Big pharma, biotech, and chip-design industries are patent-thick; software patents face hostile case law since Alice v. CLS Bank (2014).",
        ["USPTO", "Cornell LII"],
        indications=["Business", "Federal"],
        category="IP",
    ),
    entry(
        "Trademark", "",
        "A word, logo, or design that identifies the source of goods or services.",
        "Rights come from use in commerce; federal registration (USPTO) provides stronger protection and constructive nationwide notice. Trademark owners can stop others from using confusingly similar marks. Famous marks (Apple, Coca-Cola) get extra anti-dilution protection. Generic terms can't be trademarked, and once-strong marks can become generic ('escalator', 'aspirin'). Trademark trials happen at the TTAB or in federal court.",
        ["USPTO", "Cornell LII"],
        indications=["Business", "Federal"],
        category="IP",
    ),
    entry(
        "Copyright", "",
        "Automatic protection for original creative works fixed in tangible form.",
        "Covers books, music, code, photographs, paintings, films, choreography, architectural works. Protection arises automatically on creation; registration (with the US Copyright Office) is required before suing for infringement and unlocks statutory damages and attorneys' fees. Term: life of the author plus 70 years (works for hire: 95/120 years). Fair use is the main defence; the four factors come from § 107 of the Copyright Act.",
        ["Copyright Office", "Cornell LII"],
        indications=["Personal", "Business"],
        category="IP",
    ),
    entry(
        "Trade secret", "",
        "Confidential business information that derives value from being secret.",
        "Coca-Cola's formula, Google's search algorithm, KFC's spice blend. Federally protected since the Defend Trade Secrets Act (2016); also state law (Uniform Trade Secrets Act, adopted by most states). Owner must take reasonable steps to maintain secrecy — NDAs, access controls, exit interviews. Loses protection if it becomes public, even through wrongful disclosure. Reverse engineering from a lawfully obtained product is not misappropriation.",
        ["USPTO", "Cornell LII"],
        indications=["Business"],
        category="IP",
    ),
    entry(
        "Fair use", "",
        "Limited use of copyrighted material without permission — for criticism, news, teaching, parody.",
        "Four-factor test: purpose of use (commercial vs nonprofit, transformative?), nature of the original, amount used, and effect on the market. Transformative use is the heavyweight factor since Campbell v. Acuff-Rose (1994). The Andy Warhol Foundation v. Goldsmith (2023) clarified that purpose matters as a separate matter from artistic transformation. Generative AI training data cases (NYT v. OpenAI) are the next major fair-use frontier.",
        ["Cornell LII", "Copyright Office"],
        indications=["Personal", "Business", "Federal"],
        category="IP",
    ),
    entry(
        "Public domain", "",
        "Works free for anyone to use — no copyright owner, no permission needed.",
        "Works enter the public domain when copyright expires, when no rights ever attached (US government works), or when the author dedicates them. As of 2024, US works published before 1929 are public-domain; Sonny Bono Term Extension Act (1998) froze the clock for two decades. Steamboat Willie's Mickey Mouse joined the public domain January 1, 2024.",
        ["Copyright Office", "Cornell LII"],
        indications=["Personal", "Business"],
        category="IP",
    ),
    entry(
        "License", "",
        "Permission to use IP that the owner still controls.",
        "Software, music, patents, trademarks all licensed daily. Exclusive licenses transfer the practical right to exclude (the licensee can sue infringers). Non-exclusive licenses allow multiple licensees. Terms cover scope (territory, field of use, duration), royalties, sublicensing rights, and termination. Open-source licenses (MIT, GPL, Apache) are still licenses — the copyright holder is just generous about the terms.",
        ["Cornell LII", "USPTO"],
        indications=["Business", "Transactional"],
        category="IP",
    ),
    entry(
        "Royalty", "",
        "A payment to the IP owner for each use, sale, or unit licensed.",
        "Music royalties split into mechanical (per copy), performance (per public play), and synchronisation (per use in film/TV). Patent royalties tied to per-unit sales or revenue. Drug patents drive billions in pharma royalties — Humira's loss of exclusivity in 2023 was a $20B/year inflection. Music streaming pays fractions of a cent per stream; ASCAP, BMI, and SESAC are the major US PROs collecting on songwriters' behalf.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="IP",
    ),
    entry(
        "Infringement", "",
        "Unauthorised use of someone else's IP — making, selling, or copying without permission.",
        "Patent infringement is judged element-by-element against the claims. Trademark infringement asks whether consumers are likely to be confused about source. Copyright infringement requires copying (often inferred from access plus substantial similarity). Remedies: injunctions, monetary damages, sometimes treble damages for willful conduct. Defences include licensure, fair use (copyright), and non-infringement on the merits.",
        ["USPTO", "Copyright Office"],
        indications=["Business", "Litigation"],
        category="IP",
    ),
    entry(
        "Prior art", "",
        "Everything publicly known before a patent's filing date — used to attack novelty.",
        "Includes earlier patents, journal articles, conference papers, product launches, and even oral disclosures. A patent must be novel over the prior art and non-obvious to a person of ordinary skill. Patent prosecution is largely a fight over what counts as prior art and what it teaches. Inter partes review (IPR) at the USPTO has become a popular forum for accused infringers to challenge patents on prior-art grounds.",
        ["USPTO"],
        indications=["Business", "Federal"],
        category="IP",
    ),
    entry(
        "DMCA", "Digital Millennium Copyright Act",
        "1998 law providing copyright safe harbours for online services that promptly take down infringing content.",
        "Notice-and-takedown is the core operational mechanism: the rights holder sends a takedown notice, the platform removes the content, the user can counter-notice. § 512 grants service providers (YouTube, Reddit, GitHub) immunity if they comply. § 1201 separately bars circumvention of digital rights management. Heavily criticised on both sides: rights holders say takedowns are too slow; users say they're abused for censorship.",
        ["Copyright Office", "Cornell LII"],
        indications=["Personal", "Business", "Federal"],
        category="IP",
    ),
    entry(
        "Trademark dilution", "",
        "Weakening of a famous mark even without consumer confusion.",
        "Federal Trademark Dilution Act (1995, amended 2006) protects 'famous' marks against blurring (third-party use weakening distinctiveness) and tarnishment (associations harmful to reputation). Standard is higher than ordinary infringement — only nationally recognised marks qualify (Apple, Nike, Tiffany). Free-speech parody and noncommercial use are safe harbours; Louis Vuitton v. Haute Diggity Dog (2007) upheld a 'Chewy Vuiton' dog toy.",
        ["USPTO", "Cornell LII"],
        indications=["Business", "Federal"],
        category="IP",
    ),
    entry(
        "Work for hire", "",
        "Work whose copyright belongs to the employer or commissioner, not the actual creator.",
        "Two paths under the Copyright Act: (1) work prepared by an employee within the scope of employment, or (2) certain commissioned works (contributions to collective works, movies, translations, etc.) where the parties expressly agree in writing. Without a work-for-hire arrangement or written assignment, the freelancer retains copyright even if you paid for the work. Critical concept for any commissioned content, software, or design.",
        ["Copyright Office", "Cornell LII"],
        indications=["Business", "Transactional"],
        category="IP",
    ),
    entry(
        "Statutory damages", "",
        "Pre-set damages for copyright infringement — claimable without proving actual loss.",
        "Available only if registration occurred before the infringement (or within three months of publication). Range $750–$30,000 per work, up to $150,000 for willful infringement. Makes copyright litigation viable when actual damages are hard to prove — typical in music, photography, and software. Anchored a generation of file-sharing lawsuits in the 2000s. Different from punitive damages, which are tort-side.",
        ["Copyright Office", "Cornell LII"],
        indications=["Business", "Litigation"],
        category="IP",
    ),
    entry(
        "Patentable subject matter", "",
        "What you can patent at all — limits set by 35 USC § 101.",
        "Statutory categories: processes, machines, manufactures, compositions of matter. Excluded: laws of nature, natural phenomena, abstract ideas. The Supreme Court trilogy of Mayo (2012), Myriad (2013), and Alice (2014) significantly narrowed software and biotech patent eligibility, especially around diagnostic methods and isolated DNA. Software patents now face a two-step Alice/Mayo analysis; many issued patents fall on motion practice.",
        ["USPTO", "Cornell LII"],
        indications=["Business", "Federal"],
        category="IP",
    ),
]


# ============================================================================
# BATCH 4 — Property basics (15 terms)
# ============================================================================

BATCH_PROPERTY = [
    entry(
        "Deed", "",
        "The written document transferring ownership of real estate.",
        "Three main flavours: warranty deed (seller guarantees clear title — strongest), special warranty deed (seller guarantees only against their own actions), quitclaim deed (seller conveys whatever interest they have, no guarantees — used between family members or to clear clouds on title). Must be in writing, signed, and typically recorded in the county registry. The deed conveys title; the closing happens when it's delivered and accepted.",
        ["Cornell LII"],
        indications=["Personal", "Transactional"],
        category="Property",
    ),
    entry(
        "Title", "",
        "Legal ownership of property — and the documentary trail proving it.",
        "Real-estate buyers get title insurance to protect against undiscovered defects: forged deeds, missing heirs, unpaid liens. Title companies search county records before closing. Clear title means no clouds; a 'cloud on title' is a third-party claim that needs to be resolved or insured around. Marketable title is the standard contracts typically require — title clean enough that a reasonable buyer would accept.",
        ["Cornell LII"],
        indications=["Personal", "Transactional"],
        category="Property",
    ),
    entry(
        "Easement", "",
        "A right to use someone else's land for a specific purpose.",
        "Utility easements let power companies run lines across private property; access easements let landlocked neighbours reach the road; conservation easements restrict development for environmental reasons. Easements can be appurtenant (tied to a neighbouring parcel) or in gross (held by a person or company). They run with the land — they don't disappear when the property is sold. Search for them before buying.",
        ["Cornell LII"],
        indications=["Personal", "Transactional"],
        category="Property",
    ),
    entry(
        "Lien", "",
        "A legal claim against property securing a debt.",
        "Mortgages are voluntary liens. Mechanic's liens (unpaid contractors), tax liens (unpaid taxes), and judgment liens (court judgments) are involuntary. A lien must be discharged before clean title can transfer — the proceeds of sale typically pay off recorded liens at closing. Priority follows recording order in most states (first to record, first paid), with tax liens and some statutory liens taking priority regardless.",
        ["Cornell LII"],
        indications=["Personal", "Business"],
        category="Property",
    ),
    entry(
        "Mortgage", "",
        "A loan secured by real estate — if you don't pay, the lender can take the property.",
        "Two-part instrument: the promissory note (the IOU) and the mortgage itself (the security interest). Standard 30-year fixed-rate mortgages dominate the US market thanks to the secondary market run by Fannie Mae and Freddie Mac. After the 2008 crisis, the Dodd-Frank ability-to-repay rules tightened underwriting. The lender records the mortgage in county land records to perfect its priority against later claims.",
        ["Cornell LII"],
        indications=["Personal", "Transactional"],
        category="Property",
    ),
    entry(
        "Foreclosure", "",
        "The legal process letting a mortgage lender force the sale of property after default.",
        "Two regimes: judicial foreclosure (court-supervised, the rule in about half of US states) and non-judicial foreclosure (out-of-court, faster, the rest). Borrowers have rights to notice, cure (catch up on payments), and sometimes redemption (buy back after sale). Federal CARES Act (2020) and CFPB rules added moratoriums during COVID. Foreclosure can leave the borrower with a deficiency judgment if proceeds don't cover the debt — depends on the state.",
        ["CFPB", "Cornell LII"],
        indications=["Personal"],
        category="Property",
    ),
    entry(
        "Eminent domain", "",
        "Government's power to take private property for public use, paying just compensation.",
        "Fifth Amendment grants the power; the just-compensation clause limits it. Public use was broadly defined in Kelo v. New London (2005) to include economic development — sparking a backlash and state-law reforms restricting takings for private redevelopment. Just compensation is usually fair market value at the time of taking, established through appraisal and (if contested) jury trial.",
        ["Cornell LII"],
        indications=["Personal", "Federal"],
        category="Property",
    ),
    entry(
        "Landlord", "",
        "The owner of property leased to a tenant.",
        "Owes duties of habitability (implied in most states for residential rentals — heat, water, structural safety), quiet enjoyment, and disclosure of known hazards (lead paint, radon, prior deaths in some states). Cannot retaliate against tenants who report code violations. Eviction must follow statutory process. Commercial landlords get more contractual freedom than residential ones, where consumer-protection rules dominate.",
        ["HUD", "Cornell LII"],
        indications=["Personal", "Business"],
        category="Property",
    ),
    entry(
        "Tenant", "",
        "A person or entity renting property under a lease.",
        "Owes rent and lease compliance; entitled to habitability (residential) and quiet enjoyment. May withhold rent or repair-and-deduct for landlord violations, depending on state. Can be evicted only after notice and judicial process. Holdover tenants (staying past lease end) become month-to-month tenants in most states unless lease language says otherwise. Subletting and assignment usually require landlord consent.",
        ["HUD", "Cornell LII"],
        indications=["Personal", "Business"],
        category="Property",
    ),
    entry(
        "Lease", "",
        "A contract granting a tenant possession of property for a specified time and rent.",
        "Residential leases face heavy regulation: implied warranty of habitability, security-deposit caps, anti-discrimination rules (federal Fair Housing Act, state protected classes). Commercial leases are far more negotiable — gross vs net rent, common-area maintenance, exclusivity clauses, percentage rent for retail. Length matters: most jurisdictions require leases over a year to be in writing under the statute of frauds.",
        ["HUD", "Cornell LII"],
        indications=["Personal", "Business", "Transactional"],
        category="Property",
    ),
    entry(
        "Escrow", "",
        "Money or documents held by a neutral third party until conditions are met.",
        "In real-estate closings, the escrow agent holds buyer's funds and seller's signed deed, releasing both when closing conditions clear (title, financing, inspection contingencies). Outside real estate, escrow is used in M&A deals (purchase-price holdbacks for indemnity claims), payment platforms, and online marketplaces. Escrow.com handles small-scale online transactions; major banks and title companies handle real-estate closings.",
        ["Cornell LII"],
        indications=["Personal", "Business", "Transactional"],
        category="Property",
    ),
    entry(
        "Fixture", "",
        "Personal property attached to real estate so firmly it becomes part of the land.",
        "Built-in dishwashers, fireplaces, light fixtures, plumbing — these transfer with a house sale. Free-standing appliances, area rugs, and personal furniture don't. The legal test: physical attachment, adaptation to the property, and intent. Disputes are common at closing — buyers expect chandeliers; sellers think they're keeping them. Best practice: specify in the contract what stays and what goes.",
        ["Cornell LII"],
        indications=["Personal", "Transactional"],
        category="Property",
    ),
    entry(
        "Joint tenancy", "",
        "Co-ownership where if one owner dies, the others inherit automatically — no probate.",
        "Requires the 'four unities': time, title, interest, possession (all owners get the same interest at the same time via the same deed, sharing the whole). Right of survivorship is the key feature, used by spouses and family co-owners to avoid probate. Compare 'tenancy in common', the default for unrelated co-owners — each has a transferable share that passes by will or intestate succession. Many states have an intermediate 'tenancy by the entirety' for married couples.",
        ["Cornell LII"],
        indications=["Personal", "Transactional"],
        category="Property",
    ),
    entry(
        "Real estate", "",
        "Land and anything permanently attached — buildings, fixtures, trees, mineral rights.",
        "Distinguished from personal property ('chattels'), which is movable. Real estate includes airspace (subject to FAA limits) and subsurface rights (mineral, water). Property law historically split into estates: fee simple (full ownership, the default for buyers), life estate (ownership for someone's lifetime), and remainder (whoever takes after). Modern conveyances usually deal in fee simple unless an estate plan does otherwise.",
        ["Cornell LII"],
        indications=["Personal", "Business"],
        category="Property",
    ),
    entry(
        "Adverse possession", "",
        "Acquiring legal title to land by openly using it long enough.",
        "Elements: actual possession, open and notorious, hostile (without permission), continuous, and exclusive — for the statutory period (often 10–21 years depending on the state). Originated to keep land productive when boundaries were unclear. Modern uses: boundary disputes between neighbours, abandoned-lot squatters, fence-line encroachments. Some states require the adverse possessor to pay property taxes for the full period.",
        ["Cornell LII"],
        indications=["Personal"],
        category="Property",
    ),
]


# ============================================================================
# BATCH 5 — Tort basics (13 terms — 'Tort' itself is in the stub)
# ============================================================================

BATCH_TORT = [
    entry(
        "Negligence", "",
        "Failing to use the care a reasonable person would — the workhorse tort.",
        "Four elements: duty of care, breach, causation (factual + proximate), and damages. The reasonable-person standard is objective: what would a reasonable person have done? Comparative negligence in most states reduces damages by the plaintiff's share of fault. Famous duty case: Palsgraf v. Long Island Railroad (1928) — Justice Cardozo limiting duty to the foreseeable plaintiff. The vast majority of personal-injury cases are negligence claims.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Personal", "Litigation"],
        category="Tort",
    ),
    entry(
        "Defamation", "",
        "Publishing a false statement of fact that damages someone's reputation.",
        "Libel (written, more durable) and slander (spoken). Public figures must prove 'actual malice' — knowledge of falsity or reckless disregard — under New York Times v. Sullivan (1964). Private figures only need to prove negligence in most states. Truth is an absolute defence; opinion is generally protected. Damages: actual harm to reputation, sometimes presumed for libel per se (accusations of crime, professional incompetence, disease, sexual misconduct).",
        ["Cornell LII"],
        indications=["Personal", "Business", "Litigation"],
        category="Tort",
    ),
    entry(
        "Libel", "",
        "Written or printed defamation — distinct from spoken (slander).",
        "Includes social media posts, emails, blog comments, photographs, and broadcast media (which counts as libel even though spoken because it reaches a fixed audience). Libel per se categories — accusations of crime, professional incompetence, loathsome disease, sexual misconduct — let plaintiffs collect without proving specific economic loss. Online libel raises tricky jurisdictional questions: where you can sue depends on where the statement was 'aimed'.",
        ["Cornell LII"],
        indications=["Personal", "Business", "Litigation"],
        category="Tort",
    ),
    entry(
        "Slander", "",
        "Spoken defamation — generally requires proof of actual damage.",
        "The exception is slander per se: accusations of crime, professional misconduct, sexual impurity (historically), and loathsome disease — actionable without proof of specific loss. Most defamation cases now travel under libel because so much communication is written. The legal frameworks are largely converging across the two with modern statutes treating them similarly.",
        ["Cornell LII"],
        indications=["Personal", "Litigation"],
        category="Tort",
    ),
    entry(
        "Trespass", "",
        "Intentionally entering someone else's land without permission.",
        "Includes physical entry by a person, throwing objects onto the land, or even causing chemicals or smoke to cross the boundary. Trespass to chattels covers interference with personal property — the basis of early computer-network-intrusion cases (eBay v. Bidder's Edge, 2000). Nominal damages are recoverable even without proof of harm. Continuing trespass (e.g., a structure built on a neighbour's land) creates ongoing claims until removed.",
        ["Cornell LII"],
        indications=["Personal", "Business"],
        category="Tort",
    ),
    entry(
        "Strict liability", "",
        "Liability without fault — you pay even if you weren't careless.",
        "Applies to abnormally dangerous activities (blasting, keeping wild animals), defective products (the foundation of products-liability law), and in some states to dog bites by particular breeds. Justification: the actor benefits from the activity and is in the best position to insure against losses. Products-liability strict liability is the modern engine of class-action tort law — Bridgestone tires, Vioxx, talc, opioids.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Personal", "Business", "Litigation"],
        category="Tort",
    ),
    entry(
        "Vicarious liability", "",
        "Liability for someone else's wrongdoing — most often, an employer for an employee.",
        "Respondeat superior makes employers liable for employees' negligence committed within the scope of employment. Independent contractors generally don't trigger vicarious liability — but the line between contractor and employee is contested (especially in gig-economy litigation: California's AB5, Uber/Lyft Prop 22). Parents are vicariously liable for children's torts only in narrow circumstances set by state statutes.",
        ["Cornell LII"],
        indications=["Business", "Litigation"],
        category="Tort",
    ),
    entry(
        "Punitive damages", "",
        "Money awarded to punish defendants and deter future misconduct, on top of actual losses.",
        "Available only for conduct beyond ordinary negligence — typically intentional wrongs, fraud, or recklessness. The Supreme Court limits punitives constitutionally: usually no more than 9× compensatory damages (BMW v. Gore, State Farm v. Campbell). Some states cap them by statute. Famously high awards (the McDonald's coffee case, 1994) are often reduced on appeal — the McDonald's punitives were cut from $2.7M to $480K.",
        ["Cornell LII"],
        indications=["Personal", "Litigation"],
        category="Tort",
    ),
    entry(
        "Battery", "",
        "Intentionally making harmful or offensive physical contact without consent.",
        "Distinct from criminal battery; a tort battery doesn't require injury, just unwanted contact. A doctor operating without informed consent commits battery. So does the pickpocket who never threatens harm. The contact can be indirect — spitting, throwing a punch that lands. Doctrinal cousin: assault (creating apprehension of imminent contact, even without contact). Often pled together as 'assault and battery'.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Personal"],
        category="Tort",
    ),
    entry(
        "Assault", "",
        "Intentionally causing apprehension of imminent harmful contact — no touching required.",
        "Tort assault is about the threat, not the impact (the impact is battery). A raised fist and a credible 'I'm going to hit you' qualifies; words alone usually don't unless paired with threatening gesture. Conditional threats ('Apologise or I'll punch you') can still be assault. Commonly pled together with battery: 'assault and battery'. Criminal assault statutes use the term more loosely, sometimes including actual contact.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Personal"],
        category="Tort",
    ),
    entry(
        "False imprisonment", "",
        "Unlawfully restraining someone's freedom of movement.",
        "Requires intentional confinement to a bounded area, awareness or harm to the plaintiff, and no privilege or consent. Shop owners face the 'shopkeeper's privilege' — limited authority to detain suspected shoplifters with reasonable cause and reasonable duration. Schools, hospitals, and police have specific authority that can override otherwise actionable confinement. Often paired with claims for negligent infliction of emotional distress.",
        ["Cornell LII"],
        indications=["Personal"],
        category="Tort",
    ),
    entry(
        "Conversion", "",
        "Treating someone else's property as your own — civil cousin of theft.",
        "Plaintiff recovers the full value of the converted property, plus consequential damages. Differs from trespass to chattels (interference without taking) and theft (criminal). Examples: a contractor using salvaged materials from a job site for personal projects; an employer keeping a former employee's tools. Online conversion theories have been pressed for stolen domain names, NFTs, and cryptocurrency — courts are still working out the doctrinal fit.",
        ["Cornell LII"],
        indications=["Personal", "Business"],
        category="Tort",
    ),
    entry(
        "Proximate cause", "",
        "Whether the harm was a foreseeable consequence of the defendant's act — limits liability to nearby effects.",
        "Distinct from cause-in-fact (the 'but-for' test): defendant's act actually caused harm. Proximate cause asks the next question: is it fair to hold defendant responsible for this particular result? Wagon Mound (1961) made foreseeability the dominant test. Bridge cases like Palsgraf (1928) and the Polemis line wrestle with how unforeseeable a consequence has to be before liability cuts off.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Personal", "Litigation"],
        category="Tort",
    ),
]


# ============================================================================
# BATCH 6 — Criminal basics (15 terms)
# ============================================================================

BATCH_CRIMINAL = [
    entry(
        "Mens rea", "Guilty mind (Latin)",
        "The mental state required for a crime — knowing, intentional, reckless, or negligent.",
        "Most serious crimes require some level of culpable mental state. The Model Penal Code defines four: purposeful (acting with conscious goal), knowing (aware act will cause result), reckless (conscious disregard of risk), negligent (should have known of risk). Strict-liability crimes (statutory rape in some states, most traffic infractions) require no mens rea at all — controversial because they punish without moral fault.",
        ["Cornell LII", "Justia"],
        indications=["Personal", "Litigation"],
        category="Criminal",
    ),
    entry(
        "Actus reus", "Guilty act (Latin)",
        "The physical act or omission that constitutes a crime — the conduct element.",
        "Paired with mens rea (the mental element) to form criminal liability. Voluntary acts only; reflexes, sleepwalking, and convulsions generally don't qualify. Omissions count only when there's a legal duty to act — parents for children, contractual obligation, statute requiring action. Mere thoughts are never punishable; the criminal law requires conduct.",
        ["Cornell LII"],
        indications=["Personal"],
        category="Criminal",
    ),
    entry(
        "Felony", "",
        "A serious crime — generally punishable by more than a year in prison.",
        "Includes murder, manslaughter, rape, robbery, burglary, fraud above certain thresholds, drug-trafficking offences. Felony convictions trigger collateral consequences: loss of voting rights (varies by state), firearms restrictions, immigration consequences, professional licensing barriers, housing eligibility. Recent reform movement has narrowed mandatory-minimums (First Step Act, 2018) and broadened expungement.",
        ["Cornell LII", "DOJ"],
        indications=["Personal", "Federal", "State"],
        category="Criminal",
    ),
    entry(
        "Misdemeanor", "",
        "A less serious crime — generally punishable by a year or less in jail, or a fine.",
        "Examples: petty theft, simple assault, public intoxication, disorderly conduct, first-offence DUI in some states. Despite the lesser sentence, misdemeanour convictions can still affect employment, immigration, and housing. The 'misdemeanour-felony' line varies by state — same conduct (theft, drug possession) can be either depending on amount and prior record. Most criminal cases in US courts are misdemeanours.",
        ["Cornell LII", "DOJ"],
        indications=["Personal", "State"],
        category="Criminal",
    ),
    entry(
        "Bail", "",
        "Money or conditions allowing an arrested person to be released pending trial.",
        "Set at the bail hearing based on flight risk and danger to the community. Cash bail releases on payment; bond uses a bail-bondsman (typically 10% non-refundable fee). Recognizance release means no money required — your promise to appear. Bail reform efforts (NY, NJ, CA) have largely eliminated cash bail for most misdemeanours, citing wealth-based detention concerns. Federal system uses a presumption-of-detention model for serious charges.",
        ["Cornell LII", "ABA Public Education"],
        indications=["Personal", "Litigation"],
        category="Criminal",
    ),
    entry(
        "Plea bargain", "",
        "An agreement where the defendant pleads guilty in exchange for reduced charges or sentence.",
        "Resolves 90%+ of criminal cases in the US — only a small fraction go to trial. Variants: charge bargaining (plead to a lesser offence), sentence bargaining (plead in exchange for a sentence recommendation), fact bargaining (stipulate to specific facts). Critics argue plea bargaining coerces guilty pleas from innocent defendants facing severe trial penalties; defenders cite efficiency and finality.",
        ["Cornell LII", "DOJ"],
        indications=["Personal", "Litigation"],
        category="Criminal",
    ),
    entry(
        "Indictment", "",
        "Formal felony charge issued by a grand jury after reviewing prosecution evidence.",
        "Required in federal felony cases by the Fifth Amendment; some states use indictment, others use prosecutor's 'information'. Grand juries operate in secret, hear only the prosecution's side, and indict on probable cause — a low standard, hence Sol Wachtler's famous quip that a grand jury would 'indict a ham sandwich'. The federal grand jury also issues subpoenas, making it a powerful investigative tool.",
        ["Cornell LII", "Federal Rules of Civil Procedure"],
        indications=["Personal", "Federal"],
        category="Criminal",
    ),
    entry(
        "Arraignment", "",
        "First court appearance after charging — defendant hears the charges and enters a plea.",
        "Defendant is advised of rights (right to counsel, right to remain silent), formally told the charges, and asked to plead guilty, not guilty, or no contest (nolo contendere). Bail is typically addressed at or near arraignment. Federal Rule of Criminal Procedure 5 governs initial federal appearances. State practice varies but the basic structure — advice, charges, plea — is universal.",
        ["Federal Rules of Civil Procedure", "Cornell LII"],
        indications=["Personal", "Litigation"],
        category="Criminal",
    ),
    entry(
        "Probable cause", "",
        "Reasonable belief based on facts that a crime occurred or that specific evidence will be found.",
        "Lower standard than 'beyond a reasonable doubt' but more than mere suspicion. Required for arrests, search warrants, and indictments. Probable-cause hearings (preliminary hearings) screen out weak cases between charging and trial in some jurisdictions. Police can also act on 'reasonable suspicion' for brief Terry stops — even lower threshold than probable cause.",
        ["Cornell LII"],
        indications=["Personal"],
        category="Criminal",
    ),
    entry(
        "Search warrant", "",
        "Court order authorising police to search a specific place for specific evidence.",
        "Fourth Amendment requires probable cause and particularity (where to search, what to seize). Warrantless searches are presumptively unreasonable, with major exceptions: consent, plain view, exigent circumstances, search incident to arrest, automobile, border. Evidence obtained without a warrant or applicable exception is subject to the exclusionary rule (Mapp v. Ohio, 1961). Carpenter v. United States (2018) extended warrant protection to cell-site location data.",
        ["Cornell LII"],
        indications=["Personal", "Federal"],
        category="Criminal",
    ),
    entry(
        "Miranda warning", "",
        "The 'You have the right to remain silent…' warning given before custodial interrogation.",
        "From Miranda v. Arizona (1966). Required before police can question a suspect 'in custody'. Statements obtained in violation are inadmissible in the prosecution's case-in-chief (though can sometimes be used for impeachment). Police can ask 'routine booking questions' without Miranda. The warnings vary somewhat by jurisdiction; the core four: right to remain silent, anything said can be used, right to attorney, attorney provided if can't afford.",
        ["Cornell LII", "Supreme Court of the United States"],
        indications=["Personal"],
        category="Criminal",
    ),
    entry(
        "Habeas corpus", "Have the body (Latin)",
        "Court order requiring the government to justify someone's detention.",
        "Constitutionally protected (Article I, Section 9 — Congress may suspend only during invasion or rebellion). Federal habeas under 28 USC § 2254 is the main vehicle for state prisoners to challenge their convictions in federal court after exhausting state remedies. AEDPA (1996) sharply restricted the scope. Guantanamo detainees won habeas rights in Boumediene v. Bush (2008). One of the oldest legal protections in common law.",
        ["Cornell LII", "Supreme Court of the United States"],
        indications=["Personal", "Federal"],
        category="Criminal",
    ),
    entry(
        "Double jeopardy", "",
        "Fifth Amendment ban on being tried twice for the same offence after acquittal.",
        "Attaches once a jury is sworn (or first witness called in bench trial). Doesn't bar retrial after a mistrial declared with the defendant's consent or for manifest necessity. Doesn't apply across separate sovereigns: federal and state can both prosecute the same conduct (Gamble v. United States, 2019, reaffirmed this). Doesn't bar civil suits after criminal acquittal — O.J. Simpson civil case is the famous example.",
        ["Cornell LII"],
        indications=["Personal", "Federal", "State"],
        category="Criminal",
    ),
    entry(
        "Statute of limitations", "",
        "The deadline by which a case must be filed — after that, it's barred.",
        "Criminal limitations vary by offence: typically 3–6 years for felonies, none for murder in most states. Civil limitations vary widely: 2–6 years for personal injury, 4 for fraud, often longer for breach of written contract. Federal Title VII discrimination claims must reach the EEOC within 180–300 days. The clock generally starts when the cause of action accrues — sometimes when discovered ('discovery rule').",
        ["Cornell LII"],
        indications=["General", "Litigation"],
        category="Criminal",
    ),
    entry(
        "Probation", "",
        "Court-imposed supervision in the community instead of jail or prison.",
        "Conditions typically include reporting to a probation officer, maintaining employment, no contact with co-defendants/victims, no new offences, drug testing. Violation can result in revocation and incarceration. Distinct from parole, which is supervised release after serving prison time. Roughly 3.5 million Americans are on probation at any given moment — outnumbering those in prison.",
        ["DOJ", "Cornell LII"],
        indications=["Personal"],
        category="Criminal",
    ),
]


# ============================================================================
# BATCH 7 — Constitutional basics (10 terms — 'Statute' is in stub)
# ============================================================================

BATCH_CONSTITUTIONAL = [
    entry(
        "Due process", "",
        "Fair procedure before government deprives anyone of life, liberty, or property.",
        "Fifth Amendment (federal) and Fourteenth Amendment (state) both contain due-process clauses. Procedural due process requires notice, an opportunity to be heard, and a neutral decision-maker. Substantive due process protects certain fundamental rights (privacy, marriage, parental autonomy) from arbitrary government interference. Roe v. Wade (1973) was decided on substantive-due-process grounds; Dobbs (2022) overruled it.",
        ["Cornell LII", "Supreme Court of the United States"],
        indications=["Personal", "Federal"],
        category="Constitutional",
    ),
    entry(
        "Equal protection", "",
        "Constitutional guarantee against arbitrary discrimination by government.",
        "Fourteenth Amendment. Three levels of scrutiny: strict (race, national origin, fundamental rights — government must show compelling interest, narrowly tailored), intermediate (sex, illegitimacy — important interest, substantially related), and rational basis (everything else — legitimate interest, rationally related). Modern equal-protection cases: Bostock (2020, sex discrimination includes sexual orientation), Students for Fair Admissions (2023, affirmative action).",
        ["Cornell LII", "Supreme Court of the United States"],
        indications=["Personal", "Federal"],
        category="Constitutional",
    ),
    entry(
        "First Amendment", "",
        "Free speech, free press, religion, assembly, and petition.",
        "Content-based restrictions face strict scrutiny; content-neutral restrictions get intermediate scrutiny. Categories outside protection: incitement to imminent lawless action (Brandenburg, 1969), true threats, defamation, obscenity, fighting words, child sexual abuse material. Free Exercise vs Establishment Clause tension drives religion cases. Recent battlegrounds: social-media regulation (NetChoice 2024), school speech (Mahanoy, 2021).",
        ["Cornell LII", "Supreme Court of the United States"],
        indications=["Personal", "Federal"],
        category="Constitutional",
    ),
    entry(
        "Fourth Amendment", "",
        "Protection from unreasonable searches and seizures.",
        "Warrant generally required for searches; exceptions include consent, plain view, exigent circumstances, automobile, search incident to arrest, border. Modern frontiers: cell-site data (Carpenter, 2018), GPS tracking (Jones, 2012), aerial surveillance, third-party doctrine (information shared with banks/phone companies traditionally outside Fourth Amendment protection). Exclusionary rule (Mapp, 1961) is the main remedy: suppress evidence illegally obtained.",
        ["Cornell LII", "Supreme Court of the United States"],
        indications=["Personal", "Federal"],
        category="Constitutional",
    ),
    entry(
        "Fifth Amendment", "",
        "Self-incrimination, grand jury, double jeopardy, due process, takings.",
        "'I plead the Fifth' invokes the privilege against self-incrimination — applies in any proceeding where testimony could expose to criminal liability. Includes due-process protections, double-jeopardy bar, requirement of grand-jury indictment for federal felonies, and the just-compensation requirement for eminent domain. Often paired with Miranda warnings during interrogation.",
        ["Cornell LII", "Supreme Court of the United States"],
        indications=["Personal", "Federal"],
        category="Constitutional",
    ),
    entry(
        "Sixth Amendment", "",
        "Speedy trial, jury trial, confrontation of witnesses, right to counsel.",
        "Counsel must be provided to indigent defendants in felony cases (Gideon v. Wainwright, 1963) and misdemeanour cases that result in jail (Argersinger, 1972). Public-defender systems exist in every state, often underfunded. Speedy-trial right is enforced through the federal Speedy Trial Act (70-day limit) and state analogues. Confrontation clause (Crawford, 2004) bars hearsay testimonial statements unless witness is available.",
        ["Cornell LII"],
        indications=["Personal", "Federal"],
        category="Constitutional",
    ),
    entry(
        "Bill of Rights", "",
        "The first ten amendments to the Constitution, ratified 1791.",
        "Originally limited federal government only (Barron v. Baltimore, 1833). After the Fourteenth Amendment (1868), the Supreme Court 'incorporated' most provisions against the states one by one — process effectively complete by the late 20th century, with Bruen (2022) incorporating the Second Amendment against state gun regulations. Some provisions remain unincorporated (grand-jury requirement, civil-jury right above $20).",
        ["Cornell LII", "Library of Congress"],
        indications=["General", "Federal"],
        category="Constitutional",
    ),
    entry(
        "Federalism", "",
        "Division of power between federal and state governments.",
        "Federal government has enumerated powers (Constitution Article I); states have everything else (Tenth Amendment). Supremacy Clause means federal law overrides conflicting state law. Modern federalism fights: cannabis (illegal federally, legal in many states), abortion post-Dobbs, immigration enforcement, ERISA preemption of state benefits regulation. Commerce Clause cases (Lopez 1995, Sebelius 2012) test the outer limits of federal power.",
        ["Cornell LII"],
        indications=["General", "Federal", "State"],
        category="Constitutional",
    ),
    entry(
        "Separation of powers", "",
        "Division of federal power among legislative, executive, and judicial branches.",
        "Article I (Congress makes law), Article II (President executes law), Article III (courts interpret law). Checks: presidential veto, congressional override, impeachment, judicial review, advice and consent for appointments. Modern separation-of-powers fights: administrative-agency authority (Chevron doctrine, overruled in Loper Bright 2024), recess appointments (Noel Canning 2014), executive privilege.",
        ["Cornell LII", "Supreme Court of the United States"],
        indications=["General", "Federal"],
        category="Constitutional",
    ),
    entry(
        "Judicial review", "",
        "Court power to strike down laws and executive actions that violate the Constitution.",
        "Established in Marbury v. Madison (1803), Chief Justice Marshall: 'It is emphatically the province and duty of the judicial department to say what the law is.' Not explicit in the Constitution. The Supreme Court is final on federal law. State courts can also review state laws under state constitutions, often providing broader protections than federal counterparts. Major exercises: Brown v. Board (1954), Citizens United (2010), Dobbs (2022).",
        ["Supreme Court of the United States", "Cornell LII"],
        indications=["General", "Federal"],
        category="Constitutional",
    ),
]


# ============================================================================
# BATCH 8 — Regulatory basics (10 terms)
# ============================================================================

BATCH_REGULATORY = [
    entry(
        "Regulation", "",
        "Rules issued by executive-branch agencies to implement statutes.",
        "Distinct from statutes (passed by legislature) and case law (issued by courts). Federal regulations are codified in the Code of Federal Regulations (CFR); proposed and finalised through notice-and-comment in the Federal Register. State-level regulatory bodies operate similarly under state administrative-procedure acts. After Loper Bright (2024), courts no longer defer to agencies' interpretations of ambiguous statutes — major shift in administrative law.",
        ["Cornell LII", "FCC"],
        indications=["Business", "Federal"],
        category="Regulatory",
    ),
    entry(
        "Compliance", "",
        "Internal processes ensuring an organisation follows applicable laws and regulations.",
        "Modern compliance departments cover privacy (GDPR, CCPA, HIPAA), financial reporting (Sarbanes-Oxley), anti-corruption (FCPA, UK Bribery Act), sanctions (OFAC), securities (Reg FD, Reg S-K), and industry-specific rules. Heavy regulated industries (banks, pharma, healthcare) have the deepest functions. Companies that violate can face fines, consent decrees, deferred-prosecution agreements, and individual prosecution of officers.",
        ["SEC", "DOJ"],
        indications=["Business"],
        category="Regulatory",
    ),
    entry(
        "Administrative law", "",
        "Rules governing how agencies operate — procedures, rulemaking, adjudication.",
        "Federal Administrative Procedure Act (1946) sets the framework: notice-and-comment rulemaking, formal hearings, judicial review under 'arbitrary and capricious' standard. Major Supreme Court doctrines shape agency power: Chevron deference (1984, overruled 2024), Auer/Kisor deference, major-questions doctrine (West Virginia v. EPA, 2022). Agencies wield extraordinary authority — the modern 'fourth branch' of government.",
        ["Cornell LII"],
        indications=["General", "Federal"],
        category="Regulatory",
    ),
    entry(
        "Notice-and-comment", "",
        "Required rulemaking process — agency proposes a rule, takes public comments, then finalises.",
        "Under § 553 of the APA. Agency publishes notice of proposed rulemaking in the Federal Register, sets a comment period (usually 60+ days), reviews comments, and publishes final rule with explanation of major changes. Skipping the process — without a valid exception — gets the rule struck down. Courts review whether the agency adequately responded to substantial comments. Major rules can attract hundreds of thousands of comments.",
        ["Cornell LII", "FCC"],
        indications=["Business", "Federal"],
        category="Regulatory",
    ),
    entry(
        "Agency", "",
        "Executive-branch body with delegated authority to regulate a field.",
        "Examples: FDA (food/drugs), FCC (telecoms), FTC (consumer protection), SEC (securities), EPA (environment), FAA (aviation), NHTSA (vehicles). Agencies issue rules, investigate, bring enforcement actions, and adjudicate. Some are independent (FTC, SEC) — heads serve fixed terms, can't be removed at will; others are 'executive' (FDA, FAA) — directly under presidential control. Independent-agency structure is constitutionally contested (Seila Law, 2020).",
        ["Cornell LII"],
        indications=["Business", "Federal"],
        category="Regulatory",
    ),
    entry(
        "Enforcement action", "",
        "A formal proceeding by an agency or prosecutor to enforce the law against a specific actor.",
        "SEC files civil enforcement actions in federal court or its own administrative forum. DOJ brings criminal cases. State AGs bring state actions. Targets respond with motions to dismiss, settlement offers, or full litigation. Most actions settle — typical settlement includes fines, injunctive relief, and required compliance improvements. High-profile recent: FTC v. Microsoft (Activision deal), FTC v. Meta (Instagram/WhatsApp divestiture).",
        ["SEC", "FTC", "DOJ"],
        indications=["Business", "Federal"],
        category="Regulatory",
    ),
    entry(
        "Cease and desist", "",
        "An order or letter demanding immediate stop to specified conduct.",
        "Often the first step in trademark, copyright, or false-advertising disputes — cheaper than litigation and sometimes resolves the matter. Agency cease-and-desist orders carry legal force; private ones are leverage but require a lawsuit to enforce. Recipients should respond thoughtfully — silence is often interpreted as defiance, while admissions can boomerang in later litigation.",
        ["FTC", "Cornell LII"],
        indications=["Business"],
        category="Regulatory",
    ),
    entry(
        "Consent decree", "",
        "A court-approved settlement requiring specific conduct, enforceable by contempt.",
        "Combines features of contract (negotiated) and judicial order (court enforces). Common in DOJ antitrust enforcement (the Microsoft consent decree, 2001), FTC consumer-protection actions, civil-rights cases (police-department reforms after DOJ pattern-or-practice investigations), and environmental cleanup. Lasts for years or decades; modifying requires court approval. Plays a major role in keeping regulated entities in line after one-off violations.",
        ["DOJ", "FTC"],
        indications=["Business", "Federal"],
        category="Regulatory",
    ),
    entry(
        "GDPR", "General Data Protection Regulation",
        "EU privacy law with global reach over companies handling EU residents' data.",
        "Effective 2018. Requires lawful basis for processing personal data, gives users rights (access, deletion, portability), and mandates breach notification within 72 hours. Fines up to 4% of global annual revenue or €20M. Has driven privacy programs at global companies and inspired similar laws — California CCPA, Brazil LGPD, India DPDPA. US companies serving EU customers must comply or face enforcement by EU data-protection authorities.",
        ["FTC"],
        indications=["Business", "International"],
        category="Regulatory",
    ),
    entry(
        "HIPAA", "Health Insurance Portability and Accountability Act",
        "Federal law protecting US patient health information.",
        "Privacy Rule limits disclosure of protected health information (PHI). Security Rule requires technical and administrative safeguards. Breach Notification Rule requires notice within 60 days. Covered entities: healthcare providers, health plans, healthcare clearinghouses. Business associates (cloud vendors, EHR systems) must sign HIPAA business-associate agreements (BAAs). Enforced by HHS Office for Civil Rights with penalties up to $1.9M per violation category per year.",
        ["DOJ", "FTC"],
        indications=["Business", "Federal"],
        category="Regulatory",
    ),
]


# ============================================================================
# BATCH 9 — Contracts deep-dive (50 terms — extends Contract coverage)
# ============================================================================

BATCH_CONTRACT_DEPTH = [
    # --- Formation refinements ---
    entry(
        "Counter-offer", "",
        "A response that changes the terms of the original offer — it rejects the offer and proposes a new one.",
        "Under the common-law 'mirror image rule', any deviation in acceptance creates a counter-offer rather than acceptance. The original offer dies and the original offeror becomes the new offeree, free to accept or reject. The UCC § 2-207 ('battle of the forms') relaxes this for goods, letting acceptance form a contract despite differing terms — the differing terms then drop out or get handled by gap-fillers.",
        ["Cornell LII", "UCC"],
        indications=["General", "Transactional"],
        category="Contract",
    ),
    entry(
        "Mirror image rule", "",
        "Acceptance must match the offer exactly — any deviation is a counter-offer.",
        "Strict common-law doctrine still applied to service contracts and other non-goods deals. Modern commercial reality (purchase orders crossing acknowledgments) led the UCC drafters to soften it for goods via § 2-207. Lawyers exchanging redlines in heavy negotiations effectively make a series of counter-offers until both sides sign the same document.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["General", "Transactional"],
        category="Contract",
    ),
    entry(
        "Mailbox rule", "",
        "Acceptance is effective when sent — not when received.",
        "Default common-law rule: a properly addressed, properly posted acceptance binds the offeror the moment it leaves the offeree's hands. Matters when an offer is revoked in the gap between sending and receipt. The rule doesn't apply to option contracts (where acceptance is effective on receipt) or to email/text — most courts treat instant messaging as received when sent anyway.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["General", "Transactional"],
        category="Contract",
    ),
    entry(
        "Option contract", "",
        "A separate, paid-for promise to keep an offer open — can't be revoked during the option period.",
        "Real-estate option agreements (buyer pays $5,000 for the right to purchase within 90 days) are classic examples. Stock options use the same structure. Option contracts require their own consideration; the underlying offer is supported by the option payment. The Restatement § 87 and the UCC's 'firm offer' rule (§ 2-205) create exceptions where some offers can't be revoked even without consideration.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Promissory estoppel", "",
        "A promise can be enforced even without consideration, if the other side reasonably relied on it.",
        "Restatement § 90: a promise the promisor should reasonably expect to induce reliance, that does induce reliance, is binding if injustice can be avoided only by enforcement. Famous case: Hoffman v. Red Owl Stores (1965) — a grocery franchisor strung a prospective franchisee along, who sold his bakery and moved towns. No final contract existed, but the franchisor's preliminary promises were enforced. Reliance damages, not expectation, are the usual remedy.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["General", "Business"],
        category="Contract",
    ),
    entry(
        "Quasi-contract", "",
        "Not a real contract — an equitable remedy preventing unjust enrichment.",
        "Also called 'contract implied in law'. Imposed by courts when one party benefits at another's expense and it'd be unjust to let them keep the benefit. The classic example: doctor renders emergency care to unconscious patient — no contract, but the patient is liable for reasonable medical costs. Damages are 'restitution' — the value of the benefit conferred, not expectation damages.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["General", "Litigation"],
        category="Contract",
    ),
    entry(
        "Course of dealing", "",
        "Past business practices between the same parties — used to fill gaps in a current contract.",
        "UCC § 1-303. If parties have repeatedly handled defective shipments by quick replacement in past deals, that pattern shapes interpretation of the current contract even if silent. Course of dealing precedes the current contract; 'course of performance' is the analogous concept for repeated conduct within the same contract; 'usage of trade' draws on industry-wide practice.",
        ["UCC", "Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    # --- Performance and breach ---
    entry(
        "Substantial performance", "",
        "Performance that's close enough to the contract — entitles the performer to the price, minus damages for the shortfall.",
        "Common-law doctrine softening the harsh 'perfect tender' rule. Jacob & Youngs v. Kent (1921, Cardozo): a contractor used Cohoes-brand pipe instead of the specified Reading-brand. Substantially identical. The owner had to pay the contract price minus the trivial difference in value. Doctrine doesn't apply to UCC sales of goods, which keep something closer to perfect-tender.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Material breach", "",
        "A breach serious enough to excuse the other side from continuing to perform.",
        "Restatement § 241 factors: extent of benefit deprived, adequacy of damages, forfeiture by breaching party, likelihood of cure, good faith. Material breach lets the non-breacher walk away and sue for total damages. Minor breach (substantial performance) entitles only damages, not termination. Hard line to draw; turns on facts, often litigated.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Anticipatory breach", "",
        "Repudiating the contract before performance is due — the other side can sue immediately.",
        "Once one party clearly indicates they won't perform (statement or unequivocal act), the other can treat the contract as breached without waiting. Hochster v. De La Tour (1853) established the rule. Risky for the repudiator: misjudging the other side's response leads to liability. Retracting before the other side relies typically nullifies the repudiation.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Repudiation", "",
        "A clear statement or act showing one party won't perform.",
        "Must be unequivocal — saying 'I might not perform' isn't enough. Courts have grown more permissive with electronic communications: a clear email refusing performance counts. The non-repudiating party may treat the contract as breached, sue immediately, suspend their own performance, or wait for the actual due date. Each path has different risk profiles.",
        ["UCC", "Restatement of Contracts"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Cover", "",
        "A buyer's right under the UCC to substitute goods elsewhere when the seller breaches.",
        "UCC § 2-712: buyer purchases substitute goods in good faith and without unreasonable delay, then recovers the difference between cover price and contract price, plus incidental damages. The duty of good faith means the buyer can't run up the price by picking the most expensive substitute available. Common-law contracts don't have a formal 'cover' doctrine but mitigation operates similarly.",
        ["UCC", "Cornell LII"],
        indications=["Business", "Litigation", "Transactional"],
        category="Contract",
    ),
    entry(
        "Mitigation of damages", "",
        "Duty of the non-breaching party to take reasonable steps to limit their losses.",
        "A fired employee must look for comparable work; a wronged landlord must try to re-let. Failure to mitigate doesn't bar recovery, but it reduces damages by the amount that reasonable effort would have saved. Standard is reasonableness — the plaintiff doesn't have to take heroic measures or accept inferior substitutes. Sometimes called 'the doctrine of avoidable consequences'.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    # --- Remedies (deep) ---
    entry(
        "Expectation damages", "",
        "The default remedy — money that would put the plaintiff in the position of full performance.",
        "Captures the 'benefit of the bargain' — profit plus reliance, minus what's been saved by not performing. Includes consequential damages if foreseeable (Hadley v. Baxendale). Hard to prove with precision in new-business cases ('lost profits' are speculative). Courts award them when the plaintiff can establish damages with 'reasonable certainty'.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Reliance damages", "",
        "Money compensating for expenses incurred in reliance on the contract — put plaintiff back where they started.",
        "Alternative when expectation damages are too speculative. Available in promissory estoppel cases and as a fallback when expectation is unprovable. Hoffman v. Red Owl (1965) is the classic application. Capped at the contract price in some jurisdictions — plaintiff can't end up better off than performance would have left them.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Restitution", "",
        "Returning to plaintiff the value of any benefit conferred on defendant.",
        "Restitution recovery aims to disgorge unjust enrichment, not to compensate plaintiff's loss. Used as a contract remedy when the plaintiff doesn't want to enforce the deal (e.g., breaching party seeks return of partial payment). Also stand-alone via quasi-contract. Measured by the value of the benefit, which can exceed contract price in some scenarios.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Rescission", "",
        "Cancellation of the contract — both parties return to their pre-contract positions.",
        "Equitable remedy available for fraud, mutual mistake, misrepresentation, duress, undue influence, or material breach. Must be sought promptly; delay can waive the right. Restitution often accompanies rescission — each side returns what they received. Famously available in real-estate fraud, art-fraud, and securities cases.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Reformation", "",
        "Court rewriting the contract to reflect what the parties actually agreed.",
        "Equitable remedy for scrivener's errors, mutual mistake about a term, or fraud as to the writing. The court fixes the writing to match the original intent. Parol evidence rule is suspended for reformation actions — extrinsic evidence is essential to prove what the parties actually meant. Rare in commercial disputes but common in real-estate deeds with boundary errors.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["Transactional", "Litigation"],
        category="Contract",
    ),
    entry(
        "Quantum meruit", "Latin: 'as much as he deserved'",
        "Recovery of the reasonable value of services rendered when no enforceable contract exists.",
        "Available in quasi-contract claims and as fallback when a contract is unenforceable (e.g., violates statute of frauds, lacks mutual assent on price). Plaintiff proves services were rendered, the defendant was unjustly enriched, and recovery is based on market value — not the parties' (failed) agreed price. Common in construction disputes where work proceeded without a final signed contract.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    # --- Doctrines / defences ---
    entry(
        "Parol evidence rule", "",
        "Bars evidence of prior agreements that contradict a final written contract.",
        "Protects integrated writings: if the parties intended their writing to be the complete deal, earlier negotiations and verbal side-deals can't vary the terms. Exceptions allow parol evidence to show fraud, ambiguity, or collateral agreements on separate subjects. Merger clauses ('this is the entire agreement') strengthen the presumption of integration. Misnamed — applies to oral and written prior agreements alike.",
        ["UCC", "Cornell LII"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Accord and satisfaction", "",
        "A new agreement that replaces and discharges an old contractual obligation.",
        "Accord is the new agreement; satisfaction is its performance. Common when parties dispute the amount owed: debtor sends a check marked 'payment in full' for less than claimed; creditor cashing it accepts the accord. Some states require the disputed-claim element; others let any new agreement substitute. Different from novation (which substitutes a new party as well).",
        ["UCC", "Cornell LII"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Novation", "",
        "Substituting a new party or new obligation for an old one — with all parties' consent.",
        "Releases the original obligor from the original obligation. Used in M&A (target's contracts assigned to acquirer), corporate restructurings, and assignment situations where the assignee actually takes over the duty (not just the right). Distinct from assignment (which transfers rights but typically keeps the assignor on the hook) and accord-and-satisfaction (which replaces the obligation but not the parties).",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Condition precedent", "",
        "An event that must happen before a duty to perform arises.",
        "Common examples: 'subject to financing' in real-estate contracts; 'subject to board approval' in corporate deals; 'on receipt of regulatory approval' in mergers. Failure of the condition discharges the duty. Distinguished from a promise (which would be breached if it didn't happen). Often blurred at the boundary — courts interpret to avoid forfeiture where possible.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Condition subsequent", "",
        "An event that, if it happens, terminates an existing duty to perform.",
        "Rarer than conditions precedent in modern drafting. Insurance contracts use them — coverage exists until a triggering event (claim denial after fraud finding). The party arguing for termination has the burden of proving the condition occurred. Modern courts often re-characterise apparent conditions subsequent as conditions precedent to maintain consistent allocation of burdens.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Frustration of purpose", "",
        "Discharge of a contract because the reason for entering it has been destroyed.",
        "Both parties can still perform, but the underlying purpose has vanished. Krell v. Henry (1903) — a flat rented to view King Edward VII's coronation; the king got sick, the parade cancelled. The flat was still available, but the purpose was gone. US courts apply it narrowly. COVID-era restaurant-lease cases have refined the doctrine: lockdowns frustrating the purpose vs merely making performance harder.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Impossibility", "",
        "Discharge of a contract because performance has become physically or legally impossible.",
        "Traditional examples: subject matter destroyed (Taylor v. Caldwell, 1863 — music hall burned down); death of the personal-services obligor; subsequent illegality. Courts apply impossibility strictly — mere difficulty or expense isn't enough. The modern, more flexible doctrine is 'commercial impracticability' (UCC § 2-615), which extends the relief to unforeseen events that make performance unreasonably burdensome.",
        ["UCC", "Restatement of Contracts"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    entry(
        "Commercial impracticability", "",
        "UCC's relaxed version of impossibility — performance excused if a basic assumption fails.",
        "UCC § 2-615: a seller can be excused if performance has become impracticable by occurrence of a contingency the non-occurrence of which was a basic assumption. Bare price increases aren't enough; the change has to be extreme and unforeseeable. The pandemic revived the doctrine; supply-chain shortages and force-majeure clauses overlapped extensively. Common-law contracts use the parallel Restatement § 261 standard.",
        ["UCC", "Restatement of Contracts"],
        indications=["Business", "Litigation"],
        category="Contract",
    ),
    # --- Drafting / boilerplate ---
    entry(
        "Integration clause", "",
        "Statement in a contract that it represents the entire agreement between the parties.",
        "Also called a 'merger clause' or 'entire agreement clause'. Strengthens parol evidence-rule protection — outside agreements, oral promises, and prior drafts can't be used to vary the terms. Courts give significant weight but not automatic deference; a contract still has to be free of fraud, ambiguity, or mistake. Standard in nearly every commercial agreement.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Severability", "",
        "Provision saying that if any part of the contract is unenforceable, the rest still binds.",
        "Also called 'savings clause'. Without it, a single invalid clause can void the whole agreement under the 'blue pencil' rule. Common in non-compete and restrictive-covenant contexts: overbroad geographic or temporal scope can be narrowed to enforceable bounds, with the rest standing. Severability isn't bulletproof — courts can still refuse to enforce if the unenforceable part is essential.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Governing law", "",
        "Clause specifying which state's or country's law applies to interpret the contract.",
        "Standard in any contract between parties from different jurisdictions. Courts generally enforce the chosen law if it has a 'reasonable relationship' to the parties or transaction. Some areas (consumer protection, employment) limit choice-of-law freedom. New York and Delaware law are popular for commercial deals because their case law is deep, sophisticated, and businesses-friendly.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Forum selection clause", "",
        "Clause picking the court or arbitration forum where disputes must be filed.",
        "Carnival Cruise v. Shute (1991) upheld a forum clause in a passenger ticket — even one printed on the back. Courts generally enforce them unless 'unreasonable and unjust' or product of fraud. Different from choice-of-law clauses (which pick the substantive law, not the courthouse). Most boilerplate pairs both: 'governed by Delaware law, courts of Delaware'.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Assignment", "",
        "Transfer of contractual rights from one party to another.",
        "Generally permitted unless prohibited by contract or by the nature of the right (personal-services contracts can't be assigned). Anti-assignment clauses limit transfers but vary in strictness — some require consent, others bar absolutely. The assignor remains liable unless released. Common in M&A, financing (lenders assigning loan portfolios), and intellectual-property transactions.",
        ["Cornell LII", "Restatement of Contracts"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Delegation", "",
        "Transfer of contractual duties — distinct from assignment of rights.",
        "Generally permitted unless the duty is personal (paint my portrait — not delegable) or prohibited by contract. The delegator stays liable; the delegatee becomes secondarily liable. Often confused with assignment but conceptually distinct: assignment moves rights, delegation moves duties. Together they make a complete transfer of the contractual relationship.",
        ["Restatement of Contracts", "Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Survival clause", "",
        "Provision listing which obligations continue after the contract ends.",
        "Typical survivors: confidentiality, indemnity, IP ownership, payment for performance before termination, dispute-resolution clauses, governing law, limits on liability. Without a survival clause, courts may infer some — but explicit listing avoids fights. Standard in SaaS agreements, employment contracts, joint ventures, and any contract with information-confidentiality stakes.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    # --- Specific contracts ---
    entry(
        "Master services agreement", "MSA",
        "Umbrella contract setting overall terms — specific deals layered on as separate 'statements of work'.",
        "Standard in consulting, IT services, marketing agencies, and outsourcing. The MSA covers stable terms (payment terms, IP ownership, confidentiality, liability caps, governing law, indemnification), while each SOW handles deliverables, schedule, and price for a specific engagement. Lets sophisticated customers negotiate the legal terms once and run dozens of projects against them.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Statement of work", "SOW",
        "Project-specific addendum to an MSA — what's getting delivered, by when, for how much.",
        "Standard SOW content: scope, deliverables, milestones, acceptance criteria, schedule, price (fixed-fee, time-and-materials, or hybrid), assigned personnel, and any project-specific terms. The MSA's legal terms govern unless the SOW says otherwise. Conflict between MSA and SOW often goes to the MSA, but well-drafted MSAs let SOWs override on commercial terms while not on legal ones.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Letter of intent", "LOI",
        "Preliminary document outlining a contemplated deal — usually non-binding except on specified terms.",
        "Common in M&A, real-estate, and major commercial negotiations. Lays out the basic deal (price, structure, key conditions) before the parties spend money on diligence and definitive documents. Most LOIs are non-binding overall but contain binding provisions for exclusivity (no-shop), confidentiality, expense allocation, and break-up fees. Bad drafting can create unintended binding obligations — Texaco v. Pennzoil (1987) being the cautionary example.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Term sheet", "",
        "Concise summary of proposed deal terms — usually non-binding, used as a negotiating tool.",
        "Standard in venture-capital financings, M&A, and major contracts. Lists key economic terms (valuation, share class, liquidation preference, vesting, board composition) without the legal mechanics. Once signed, definitive documents are drafted to mirror the term sheet's economics. Most are explicitly non-binding except for exclusivity and confidentiality. The Y Combinator SAFE term sheet is a standardised version for early-stage rounds.",
        ["SEC", "Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Employment agreement", "",
        "Contract setting out terms of employment beyond at-will defaults.",
        "Common content: title, duties, compensation, benefits, vacation, IP assignment (for inventions and work product), confidentiality, restrictive covenants, termination conditions, severance. Without an agreement, most US employment is 'at-will' (either side can terminate any time, for any non-discriminatory reason). Executive agreements add change-of-control protections, golden parachutes, and good-reason termination rights.",
        ["DOL", "Cornell LII"],
        indications=["Business", "Personal", "Transactional"],
        category="Contract",
    ),
    entry(
        "Non-compete", "",
        "Clause barring an employee from working for competitors after leaving — within limits.",
        "Enforceability varies dramatically by state. California has banned them since 1872; FTC's 2024 federal ban was blocked by a Texas federal court before taking effect, currently on appeal. Where enforceable (most states), restrictions must be 'reasonable' in scope, geography, and duration — typically capped at 1–2 years. Heavy enforcement against high-paid executives and salespeople; broad use against low-wage workers is the policy battleground.",
        ["FTC", "DOL"],
        indications=["Business", "Personal"],
        category="Contract",
    ),
    entry(
        "Non-solicitation", "",
        "Bar on a departing employee from poaching customers or colleagues for a specified period.",
        "More widely enforceable than non-competes — even California enforces customer non-solicits in some employment contexts. Two flavours: customer non-solicits (don't approach the company's customers) and employee non-solicits (don't recruit former colleagues). Modern challenges focus on what counts as 'solicitation' on social media — LinkedIn-era case law is still developing.",
        ["Cornell LII"],
        indications=["Business", "Personal"],
        category="Contract",
    ),
    entry(
        "Severance agreement", "",
        "Contract paying a departing employee in exchange for releases and other obligations.",
        "Employer pays severance; employee waives claims (typically discrimination, wage-and-hour, common-law tort), agrees to confidentiality, sometimes non-disparagement, and post-employment restrictions. Older Workers Benefit Protection Act requires 21-day consideration period plus 7-day revocation period for releases of age-discrimination claims. SEC scrutiny of clauses chilling whistleblower reports has reshaped recent drafting.",
        ["DOL", "SEC", "EEOC"],
        indications=["Business", "Personal", "Transactional"],
        category="Contract",
    ),
    entry(
        "Joint venture agreement", "JV agreement",
        "Contract setting up a shared business between two or more companies for a limited purpose.",
        "Distinct from a merger — each party keeps its separate existence and contributes specific assets, capital, or expertise. Governs ownership splits, capital contributions, governance, profit allocation, and exit mechanics. International JVs are heavily used in jurisdictions requiring local partners (China historically, Saudi Arabia, India). Common in pharma R&D, oil-and-gas exploration, infrastructure projects, and large defence contracts.",
        ["Cornell LII"],
        indications=["Business", "International", "Transactional"],
        category="Contract",
    ),
    entry(
        "Partnership agreement", "",
        "Contract setting up the terms of a partnership.",
        "Default rules under the Uniform Partnership Act (or state variants) cover gap-fillers, but a written agreement is standard for any serious business. Key terms: capital contributions, profit/loss allocation, management rights, withdrawal mechanics, dispute resolution. General partnerships make each partner jointly and severally liable; limited partnerships and LLPs limit liability for non-managing partners. Many family businesses operate without one and pay the price in succession.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "Operating agreement", "",
        "The internal governance contract for an LLC.",
        "Sets management structure (member-managed or manager-managed), capital contributions, distributions, voting, transfers of interests, and dissolution. Delaware LLC law is famously permissive — operating agreements can override most defaults. Multi-member LLCs without one fall back on default state rules, which often don't match what the members actually wanted. Single-member LLCs increasingly still draft them for piercing-the-veil protection.",
        ["Cornell LII"],
        indications=["Business", "Transactional"],
        category="Contract",
    ),
    entry(
        "EULA", "End User License Agreement",
        "The contract you agree to when installing software.",
        "Grants limited license to use the software, reserving title with the publisher. Typical terms: scope of use (number of devices, commercial/personal), restrictions (no reverse engineering, no redistribution), disclaimer of warranties, limitation of liability, termination on breach. Enforceability depends on adequate notice and opportunity to read; click-through EULAs generally pass; browse-wrap is more contested.",
        ["Cornell LII"],
        indications=["Personal", "Business"],
        category="Contract",
    ),
    entry(
        "Terms of service", "ToS",
        "Contract governing use of a website or online service.",
        "Often used interchangeably with 'terms of use' or 'user agreement'. Standard contents: account rules, acceptable use, IP ownership and license-back of user content, disclaimers, limitation of liability, dispute resolution (often arbitration with class waiver), and the right to modify terms. Modification clauses are heavily litigated — Douglas v. Talk America (2007) bars unilateral changes without notice and assent.",
        ["FTC", "Cornell LII"],
        indications=["Personal", "Business"],
        category="Contract",
    ),
    entry(
        "Click-through agreement", "Clickwrap",
        "Online contract requiring affirmative click ('I agree') to accept terms.",
        "The gold standard for online contract formation. Courts almost uniformly enforce clickwrap when the terms are reasonably available and the user must take an affirmative action signalling assent. Specht v. Netscape (2002) is the foundational case distinguishing clickwrap from browse-wrap. Modern best practice: 'unmissable' button, terms visible or linked clearly, button text clearly indicating assent.",
        ["Cornell LII"],
        indications=["Personal", "Business"],
        category="Contract",
    ),
    entry(
        "Browse-wrap agreement", "Browsewrap",
        "Online terms purportedly accepted just by using a site — no affirmative click required.",
        "Weakest form of online contract. Courts require evidence that the user had actual or constructive knowledge of the terms — typically a clear and conspicuous notice. Many browse-wraps fail enforcement because the link to terms is buried in the footer. Nguyen v. Barnes & Noble (2014) refused to enforce a browse-wrap arbitration clause for this reason. Modern litigation heavy: SCOTUS denied cert on several browse-wrap cases through 2024.",
        ["Cornell LII"],
        indications=["Personal", "Business"],
        category="Contract",
    ),
    entry(
        "Shrink-wrap agreement", "Shrinkwrap",
        "Terms inside or on packaging of physical software — agreed to by opening the box.",
        "Older mechanism dating to floppy-disk and CD-ROM era. ProCD v. Zeidenberg (1996) enforced a shrink-wrap restriction. Courts split on cases where the buyer can't see terms before purchase. Largely overtaken by clickwrap as software downloads displaced physical media, but still occasionally relevant for boxed enterprise products and consumer goods with embedded software.",
        ["Cornell LII"],
        indications=["Personal", "Business"],
        category="Contract",
    ),
]


# ============================================================================
# BATCH 10 — Letter-fill (K, Y, Z) so the alphabet grid isn't gappy
# ============================================================================

BATCH_FILL_LETTERS = [
    # --- K ---
    entry(
        "Kickback", "",
        "A secret payment in exchange for steering business — usually illegal.",
        "Federal Anti-Kickback Statute makes paying or receiving anything of value for referrals in federally funded healthcare (Medicare, Medicaid) a felony — up to $100,000 per violation plus exclusion. Banking, defence procurement, and construction industries have their own anti-kickback regimes. Civil False Claims Act allows whistleblowers ('qui tam') to share in recoveries — driving billions in pharma settlements over the past decade.",
        ["DOJ", "Cornell LII"],
        indications=["Business", "Federal"],
        category="Criminal",
    ),
    entry(
        "Kelo v. New London", "",
        "2005 Supreme Court case allowing eminent domain for private economic development.",
        "5–4 decision permitting New London, Connecticut, to seize private homes (including Susette Kelo's iconic pink house) to make way for a Pfizer-anchored redevelopment plan. The Court read 'public use' to include 'public purpose' — and economic development counted. Massive popular backlash followed; over 40 states passed laws restricting takings for private benefit. The redevelopment itself never happened — the site sat empty for years.",
        ["Supreme Court of the United States", "Cornell LII"],
        indications=["Personal", "Federal"],
        category="Property",
    ),
    entry(
        "Knock-and-announce rule", "",
        "Fourth Amendment requirement that police identify themselves before forcing entry.",
        "Officers serving a warrant must knock, announce ('Police! Search warrant!'), and wait a reasonable time before breaking in. Exceptions: risk to officers, destruction of evidence, futility. Hudson v. Michigan (2006) controversially held that violations don't trigger the exclusionary rule — evidence still admissible. State courts can provide stricter protection under state constitutions. Botched no-knock raids (Breonna Taylor, 2020) drove reform efforts in several jurisdictions.",
        ["Cornell LII", "Supreme Court of the United States"],
        indications=["Personal"],
        category="Criminal",
    ),
    # --- Y ---
    entry(
        "Year-and-a-day rule", "",
        "Old common-law rule: if the victim survives more than a year and a day, the death isn't murder.",
        "Originated when medieval medicine couldn't reliably trace cause of death over long periods. Modern medicine and life-support technology made the rule absurd: a victim kept alive for over a year by ventilator couldn't yield a murder conviction. Most US jurisdictions have abolished it by statute or judicial decision. Rogers v. Tennessee (2001) upheld retroactive abolition against an ex post facto challenge.",
        ["Cornell LII", "Justia"],
        indications=["Personal", "State"],
        category="Criminal",
    ),
    entry(
        "Yellow-dog contract", "",
        "Employment contract requiring the worker to promise not to join a union.",
        "Common in the late 19th and early 20th centuries; effectively eliminated by the Norris-LaGuardia Act (1932) which made yellow-dog contracts unenforceable in federal court. The National Labor Relations Act (1935) formalised the right to organise. Modern non-compete and non-solicit agreements occupy adjacent ground; class-action waivers in employment arbitration (Epic Systems, 2018) revived analogous concerns about workers contracting away collective rights.",
        ["DOL", "Cornell LII"],
        indications=["Business", "Personal"],
        category="Contract",
    ),
    # --- Z ---
    entry(
        "Zoning", "",
        "Local government regulation dividing land into use categories — residential, commercial, industrial.",
        "Upheld by the Supreme Court in Village of Euclid v. Ambler Realty (1926). Modern zoning addresses density, setbacks, height limits, parking minimums, and use restrictions. Hotly contested in housing-policy debates: NIMBY-driven single-family-only zones have been blamed for the US housing shortage. State preemption laws (California SB 9, Oregon HB 2001) have started overriding local zoning to allow more density. Variances and conditional-use permits handle case-by-case relief.",
        ["Cornell LII", "HUD"],
        indications=["Personal", "Business", "State"],
        category="Property",
    ),
    entry(
        "Zealous representation", "",
        "Lawyer's duty to represent a client vigorously within the bounds of law.",
        "Drawn from the ABA Model Rules of Professional Conduct. Often phrased as 'zealous advocacy' — the rules now require 'diligent representation' (Rule 1.3) plus an obligation of candour to the tribunal (Rule 3.3). Zealous representation has limits: lawyers can't suborn perjury, mislead the court, or pursue frivolous claims. The competing duties (zealous to client vs honest to court) generate much of legal ethics.",
        ["ABA Public Education", "Cornell LII"],
        indications=["General", "Litigation"],
        category="Procedure",
    ),
    # --- X ---
    entry(
        "X-mark", "Mark in lieu of signature",
        "An X used as a signature by someone unable to write — still legally valid.",
        "The UCC defines 'signed' as 'any symbol executed or adopted with present intention to adopt or accept a writing' (§ 1-201(b)(37)) — an X qualifies. State statutes typically require witnesses to attest that the marker intended the X as their signature. Common historically on wills, contracts, and deeds executed by illiterate parties. Modern equivalents include digital signatures under the federal E-SIGN Act and state UETA statutes.",
        ["UCC", "Cornell LII"],
        indications=["General", "Transactional"],
        category="Contract",
    ),
]


BATCHES = {
    1: BATCH_PROCEDURE,
    2: BATCH_CONTRACT_BASICS,
    3: BATCH_IP,
    4: BATCH_PROPERTY,
    5: BATCH_TORT,
    6: BATCH_CRIMINAL,
    7: BATCH_CONSTITUTIONAL,
    8: BATCH_REGULATORY,
    9: BATCH_CONTRACT_DEPTH,
    10: BATCH_FILL_LETTERS,
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
