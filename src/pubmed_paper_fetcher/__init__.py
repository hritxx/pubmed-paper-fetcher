import requests
import pandas as pd
import argparse
import xml.etree.ElementTree as ET
from typing import List, Dict

# PubMed API base URL
PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Keywords to detect pharmaceutical or biotech companies
NON_ACADEMIC_KEYWORDS = ["Pharma", "Biotech", "Therapeutics", "Genomics", "Biosciences", "Corporation"]

def fetch_pubmed_ids(query: str) -> List[str]:
    """Fetch PubMed IDs for a given query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Limit to 10 papers for now
    }
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch detailed information for a list of PubMed IDs."""
    if not pubmed_ids:
        return []
    
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    
    papers = []
    for article in root.findall(".//PubmedArticle"): 
        pmid = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
        pub_date = article.find(".//PubDate/Year")
        pub_date = pub_date.text if pub_date is not None else "Unknown"
        
        authors = article.findall(".//Author")
        non_academic_authors = []
        company_affiliations = []
        
        for author in authors:
            affiliation = author.find(".//Affiliation")
            if affiliation is not None:
                affiliation_text = affiliation.text
                if any(keyword in affiliation_text for keyword in NON_ACADEMIC_KEYWORDS):
                    non_academic_authors.append(author.find(".//LastName").text)
                    company_affiliations.append(affiliation_text)
        
        corresponding_email = "N/A"  # Could extract if present
        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors),
            "Company Affiliation(s)": ", ".join(company_affiliations),
            "Corresponding Author Email": corresponding_email
        })
    
    return papers

def save_to_csv(papers: List[Dict], filename: str):
    """Save paper details to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed with industry affiliations.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Filename to save the results", default=None)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()
    
    if args.debug:
        print(f"Fetching papers for query: {args.query}")
    
    pubmed_ids = fetch_pubmed_ids(args.query)
    if args.debug:
        print(f"Found {len(pubmed_ids)} papers.")
    
    papers = fetch_paper_details(pubmed_ids)
    
    if args.file:
        save_to_csv(papers, args.file)
    else:
        print(pd.DataFrame(papers))

if __name__ == "__main__":
    main()