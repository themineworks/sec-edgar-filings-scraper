#!/usr/bin/env python3
"""Structured SEC filings ready for AI and RAG pipelines. Python, Node.js and cURL clients for the SEC EDGAR Filings Scraper on Apify, pay per result.

Command-line client for the themineworks/sec-edgar-filings actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/sec-edgar-filings/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/sec-edgar-filings"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--tickers", help="Comma-separated. Stock ticker symbols to pull filings for (for example AAPL, MSFT, NVDA)")
    ap.add_argument("--ciks", help="Comma-separated. Direct SEC Central Index Key numbers, if you already have them (for example 320193 or…")
    ap.add_argument("--form-types", help="Comma-separated. Which SEC form types to return (for example 10-K, 10-Q, 8-K, S-1, 4, DEF 14A)")
    ap.add_argument("--max-filings-per-company", type=int, help="Maximum number of filings to return per company, newest first")
    ap.add_argument("--date-from", help="Only return filings filed on or after this date")
    ap.add_argument("--date-to", help="Only return filings filed on or before this date")
    ap.add_argument("--include-financials", action=argparse.BooleanOptionalAction, help="Attach a summary of key XBRL financial facts (revenue, net income, assets, etc.) for each…")
    ap.add_argument("--include-document-text", action=argparse.BooleanOptionalAction, help="Fetch the primary filing document and attach cleaned plain text, ready for LLM/RAG…")
    ap.add_argument("--contact-email", help="SEC requires a contact email in the User-Agent for fair-access")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.tickers: run_input["tickers"] = [s.strip() for s in a.tickers.split(",") if s.strip()]
    if a.ciks: run_input["ciks"] = [s.strip() for s in a.ciks.split(",") if s.strip()]
    if a.form_types: run_input["formTypes"] = [s.strip() for s in a.form_types.split(",") if s.strip()]
    if a.max_filings_per_company is not None: run_input["maxFilingsPerCompany"] = a.max_filings_per_company
    if a.date_from is not None: run_input["dateFrom"] = a.date_from
    if a.date_to is not None: run_input["dateTo"] = a.date_to
    if a.include_financials is not None: run_input["includeFinancials"] = a.include_financials
    if a.include_document_text is not None: run_input["includeDocumentText"] = a.include_document_text
    if a.contact_email is not None: run_input["contactEmail"] = a.contact_email

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
