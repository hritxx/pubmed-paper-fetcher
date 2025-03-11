import argparse
import pandas as pd
from pubmed_paper_fetcher_cli import fetch_pubmed_ids, fetch_paper_details, save_to_csv

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