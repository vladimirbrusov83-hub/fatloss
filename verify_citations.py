#!/usr/bin/env python3
"""Resolve every citation in citations.json against PubMed and write citations_verified.json.

Any reference that does not return a real record, or whose publication type is
weaker than the page claims, must not be given "meta-analysis says" framing.
"""
import json, time, unicodedata, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).parent
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def fetch(pmids):
    url = f"{EUTILS}/efetch.fcgi?db=pubmed&retmode=xml&id={','.join(pmids)}"
    root = ET.fromstring(urllib.request.urlopen(url, timeout=40).read())
    out = {}
    for art in root.iter("PubmedArticle"):
        pmid = art.findtext(".//PMID")
        types = [t.text for t in art.iter("PublicationType")]
        authors = art.findall(".//Author")
        first = "?"
        if authors:
            first = f"{authors[0].findtext('LastName') or ''} {authors[0].findtext('Initials') or ''}".strip()
        out[pmid] = {
            "pmid": pmid,
            "title": art.findtext(".//ArticleTitle") or "",
            "journal": art.findtext(".//Journal/ISOAbbreviation") or "",
            "year": art.findtext(".//JournalIssue/PubDate/Year") or art.findtext(".//PubDate/MedlineDate") or "",
            "first_author": first,
            "publication_types": [t for t in types if t not in ("Journal Article",)],
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        }
    return out


def main():
    cites = json.loads((HERE / "citations.json").read_text())
    pmids = sorted({c["pmid"] for refs in cites.values() for c in refs})
    meta = fetch(pmids)

    verified, problems = {}, []
    for page, refs in cites.items():
        rows = []
        if not refs:
            problems.append(f"{page}: NO citations listed — must be written as a 'thin evidence' page")
        for c in refs:
            m = meta.get(c["pmid"])
            if not m:
                problems.append(f"{page}: PMID {c['pmid']} ({c['label']}) did not resolve — DO NOT CITE")
                continue
            pt = "; ".join(m["publication_types"]) or "(none listed)"
            tags = " ".join(m["publication_types"]) + " " + m["title"]
            is_ma = ("meta-analysis" in tags.lower() or "systematic review" in tags.lower())
            fold = lambda t: "".join(ch for ch in unicodedata.normalize("NFKD", t.lower()) if not unicodedata.combining(ch))
            surname = fold(c["label"].split()[0]).rstrip(",")
            if surname and surname not in fold(m["first_author"]):
                problems.append(f"{page}: PMID {c['pmid']} labelled '{c['label']}' but first author is {m['first_author']} — WRONG PAPER")
            if "meta-analysis" in c["expect"].lower() and not is_ma:
                problems.append(f"{page}: PMID {c['pmid']} expected meta-analysis, PubMed says [{pt}]")
            rows.append({**m, "label": c["label"], "expected": c["expect"], "is_sr_or_ma": is_ma})
        verified[page] = rows

    (HERE / "citations_verified.json").write_text(json.dumps(verified, indent=2))

    for page, rows in verified.items():
        print(f"\n{page}")
        for r in rows:
            flag = "MA/SR" if r["is_sr_or_ma"] else "     "
            print(f"  [{flag}] {r['pmid']} | {r['first_author']} {r['year']} | {r['journal']} | {r['title'][:70]}")
    print("\n" + "=" * 70)
    print("PROBLEMS:" if problems else "No problems.")
    for p in problems:
        print("  ! " + p)


if __name__ == "__main__":
    main()
