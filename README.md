# Fat Loss (formerly Nutrition Checked)

Twenty-three of the most-asked fat-loss questions, each answered from the
strongest available research, with the PubMed citation and the population that
was actually studied. Renamed and expanded on 2026-10-17: 8 new dieting pages
(calories, best diet, hunger, stalls, diet breaks, set point, regain/maintenance,
stubborn fat). Written in Vladimir's own coaching voice: no text taken from
other sites, coaching calls labelled as such.

**Status:** all 23 pages written and locally complete. No GitHub repo, no Vercel
project, no subdomain yet. Live: https://fatloss.brusovcoach.org (Vercel project `fatloss`, auto-deploys on push to GitHub `vladimirbrusov83-hub/fatloss`).

## Run it locally

```bash
cd ~/Documents/NutritionHub
python3 -m http.server 8890
# → http://localhost:8890
```

## Files

| File | What it is |
|---|---|
| `index.html` | Hub landing page: 23 question cards, search, category filters |
| `how-much-protein.html` | The template article page (built first, signed off, then replicated) |
| 22 more `*.html` | One page per question, generated from the template so the CSS and chrome stay identical |
| `citations.json` | Every reference, per page, with expected study design |
| `verify_citations.py` | Resolves each PMID against PubMed; flags wrong papers and weak designs |
| `citations_verified.json` | Generated output: real title, journal, year, publication type |
| `robots.txt` | Allow-all. The `Sitemap:` line was removed; it still pointed at HypertrophyHub |

## The citation rule

No page gets "a meta-analysis says" framing unless `verify_citations.py` returns
`MA/SR` for that reference. Run it before writing or editing any prose:

```bash
python3 verify_citations.py
```

It catches three failure modes: a PMID that doesn't resolve, a PMID that resolves
to a *different paper* than the label claims, and a reference cited as a
meta-analysis that PubMed classifies as something weaker.

Two references from the source inventory were **rejected** by this process:
a "Morton 2025 protein-timing meta-analysis" (no PubMed record, do not cite) and
Barakat 2020 on body recomposition (not indexed, and a narrative review, not a
meta-analysis). Three PubMed searches found no SR or meta-analysis on body
recomposition at all, so that page is written as a "here is what we don't know"
page rather than an evidence-backed verdict.

## Design

Same system as the Hypertrophy Hub: cream `#f5f0e8` ground, `#d4500a` accent,
Barlow Condensed + DM Sans, so the hubs read as one family. Two components are
new here: the **verdict badge** (True / Mostly true / Overstated / False /
Depends) and the **citation block** (study design, sample size, PubMed link).

Every article also carries a **"Who was studied"** box. Most nutrition content
quotes research done on untrained, older, or clinically obese people as if it
were a finding about lifters; naming that gap is the point of the site.

## Three claims the research didn't support

While writing the pages, three index-card blurbs turned out to overstate their
citation and were rewritten to match:

- **Fasted cardio.** Aird 2018 measured performance and acute metabolism, not
  body fat. "Over 24 hours it evens out" isn't in the paper.
- **Intermittent fasting.** Ashtary-Larky 2021 found IF *beat* the controls on
  fat loss. Those controls weren't calorie-matched, which is the actual story.
- **Plant vs animal protein.** Reid-McCann 2025 found a small animal advantage
  for muscle mass. Soy matched milk; the gap was against rice, oat, chia, potato.

## Still to do (all of it needs the domain first)

- `sitemap.xml`
- Fill in `<link rel="canonical">` on every page (each has a TODO comment in place)
- Restore a `Sitemap:` line in `robots.txt`
- Wire into the main site: sixth Training Hub card, sitemap, `llms.txt`,
  cross-links from the Hypertrophy and Health hubs
