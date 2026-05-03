#!/usr/bin/env python3
"""
PubMed Literature Fetcher for tosresources.com

Queries PubMed E-utilities API for TOS-related research articles,
deduplicates across search terms, and outputs a sorted JSON file.

Usage:
    python scripts/pubmed_fetch.py

Output:
    pubmed_articles.json (in repo root)
"""

import json
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# --- Configuration ---

EMAIL = "contact.tosresources@gmail.com"
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OUTPUT_FILE = "pubmed_articles.json"
REQUEST_DELAY = 0.4  # seconds between API calls (PubMed asks for ≤3/sec without key)

SEARCH_TERMS = [
    "thoracic outlet syndrome",
    "neurogenic thoracic outlet syndrome",
    "brachial plexus compression",
    "first rib resection",
    "pectoralis minor syndrome",
    "venous thoracic outlet syndrome",
    "arterial thoracic outlet syndrome",
]


def esearch(term, retmax=200):
    """Search PubMed and return a list of PMIDs for the given term."""
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": term,
        "retmax": retmax,
        "retmode": "json",
        "email": EMAIL,
        "sort": "date",
    })
    url = f"{BASE_URL}/esearch.fcgi?{params}"
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode())
    return data.get("esearchresult", {}).get("idlist", [])


def efetch(pmids):
    """Fetch full article details for a list of PMIDs. Returns XML ElementTree root."""
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
        "email": EMAIL,
    })
    url = f"{BASE_URL}/efetch.fcgi?{params}"
    with urllib.request.urlopen(url) as resp:
        return ET.fromstring(resp.read())


def classify_article_type(pub_types):
    """Map PubMed publication types to a single display label."""
    types_lower = [t.lower() for t in pub_types]
    # Check in priority order (most specific first)
    if "meta-analysis" in types_lower:
        return "Meta-Analysis"
    if "systematic review" in types_lower:
        return "Systematic Review"
    if "review" in types_lower:
        return "Review"
    if "case reports" in types_lower:
        return "Case Report"
    if "clinical trial" in types_lower or "randomized controlled trial" in types_lower:
        return "Clinical Trial"
    if "editorial" in types_lower:
        return "Editorial"
    if "letter" in types_lower or "comment" in types_lower:
        return "Letter"
    if "comparative study" in types_lower:
        return "Comparative Study"
    # Default: if it has "journal article", call it Research
    if "journal article" in types_lower:
        return "Research"
    return "Other"


def parse_article(article_elem):
    """Parse a single PubmedArticle XML element into a dict."""
    medline = article_elem.find("MedlineCitation")
    if medline is None:
        return None

    pmid_elem = medline.find("PMID")
    pmid = pmid_elem.text if pmid_elem is not None else ""

    article = medline.find("Article")
    if article is None:
        return None

    # Title
    title_elem = article.find("ArticleTitle")
    title = "".join(title_elem.itertext()).strip() if title_elem is not None else "Untitled"

    # Authors
    authors = []
    author_list = article.find("AuthorList")
    if author_list is not None:
        for author in author_list.findall("Author"):
            last = author.find("LastName")
            fore = author.find("ForeName")
            if last is not None and fore is not None:
                authors.append(f"{fore.text} {last.text}")
            elif last is not None:
                authors.append(last.text)
            else:
                collective = author.find("CollectiveName")
                if collective is not None:
                    authors.append(collective.text)

    # Journal
    journal_elem = article.find("Journal/Title")
    journal = journal_elem.text if journal_elem is not None else ""

    # Publication date — try multiple locations
    pub_date_str = ""
    pub_date_sort = ""

    # First try ArticleDate (electronic publication)
    article_date = article.find("ArticleDate")
    # Then try Journal PubDate
    journal_date = article.find("Journal/JournalIssue/PubDate")

    for date_elem in [article_date, journal_date]:
        if date_elem is not None:
            year = date_elem.find("Year")
            month = date_elem.find("Month")
            day = date_elem.find("Day")
            if year is not None:
                y = year.text
                m = month.text if month is not None else "01"
                d = day.text if day is not None else "01"
                # Convert month name to number if needed
                try:
                    m_num = int(m)
                except ValueError:
                    try:
                        m_num = datetime.strptime(m[:3], "%b").month
                    except ValueError:
                        m_num = 1
                pub_date_str = f"{y} {datetime(2000, m_num, 1).strftime('%b')}"
                if d != "01" or day is not None:
                    pub_date_str += f" {int(d)}"
                pub_date_sort = f"{y}-{m_num:02d}-{int(d):02d}"
                break

    # Abstract
    abstract_elem = article.find("Abstract")
    abstract = ""
    if abstract_elem is not None:
        parts = []
        for text in abstract_elem.findall("AbstractText"):
            label = text.get("Label", "")
            content = "".join(text.itertext()).strip()
            if label:
                parts.append(f"{label}: {content}")
            else:
                parts.append(content)
        abstract = " ".join(parts)

    # Publication types
    pub_types = []
    pub_type_list = article.find("PublicationTypeList")
    if pub_type_list is not None:
        for pt in pub_type_list.findall("PublicationType"):
            if pt.text:
                pub_types.append(pt.text)

    # Classify into a single display label
    article_type = classify_article_type(pub_types)

    # DOI
    doi = ""
    for eloc in article.findall("ELocationID"):
        if eloc.get("EIdType") == "doi" and eloc.text:
            doi = eloc.text
            break
    # Fallback: check ArticleIdList in PubmedData
    if not doi:
        pubmed_data = article_elem.find("PubmedData")
        if pubmed_data is not None:
            for aid in pubmed_data.findall("ArticleIdList/ArticleId"):
                if aid.get("IdType") == "doi" and aid.text:
                    doi = aid.text
                    break

    result = {
        "pmid": pmid,
        "title": title,
        "authors": authors,
        "journal": journal,
        "date": pub_date_str,
        "date_sort": pub_date_sort,
        "abstract": abstract,
        "article_type": article_type,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    }
    if doi:
        result["doi"] = f"https://doi.org/{doi}"

    return result


def main():
    # Collect all unique PMIDs across search terms
    all_pmids = set()
    print(f"Searching PubMed for {len(SEARCH_TERMS)} terms...")

    for term in SEARCH_TERMS:
        print(f"  Searching: \"{term}\"", end="")
        pmids = esearch(term)
        new_count = len(pmids) - len(all_pmids & set(pmids))
        all_pmids.update(pmids)
        print(f" — {len(pmids)} results ({new_count} new)")
        time.sleep(REQUEST_DELAY)

    print(f"\nTotal unique articles: {len(all_pmids)}")

    if not all_pmids:
        print("No articles found. Writing empty JSON.")
        output = {"last_updated": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"), "articles": []}
        with open(OUTPUT_FILE, "w") as f:
            json.dump(output, f, indent=2)
        return

    # Fetch article details in batches of 200
    pmid_list = list(all_pmids)
    articles = []
    batch_size = 200

    for i in range(0, len(pmid_list), batch_size):
        batch = pmid_list[i:i + batch_size]
        print(f"Fetching details for articles {i + 1}–{i + len(batch)}...")
        root = efetch(batch)

        for article_elem in root.findall("PubmedArticle"):
            parsed = parse_article(article_elem)
            if parsed:
                articles.append(parsed)

        time.sleep(REQUEST_DELAY)

    # Sort by date (newest first)
    articles.sort(key=lambda a: a["date_sort"], reverse=True)

    # Build output
    output = {
        "last_updated": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
        "total_articles": len(articles),
        "search_terms": SEARCH_TERMS,
        "articles": articles,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Wrote {len(articles)} articles to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
