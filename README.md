# SEC EDGAR Filings Scraper: 10-K, 10-Q, 8-K to JSON for AI

Pull SEC EDGAR filings, including 10-K, 10-Q, 8-K, and more, as clean structured JSON ready for AI and RAG pipelines. Financial facts, filing text, entity data. Empty results are never charged.

**Run it on Apify:** [apify.com/themineworks/sec-edgar-filings](https://apify.com/themineworks/sec-edgar-filings)
**Docs, FAQ and pricing:** [themineworks.com/actors/sec-edgar-filings](https://themineworks.com/actors/sec-edgar-filings/)

**Price:** From $0.60 per 1,000 filings on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* 10-K, 10-Q, 8-K and 20+ form types
* Structured financial facts extracted
* Full filing text for RAG ingestion
* CIK and ticker lookup supported
* Empty results are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/sec-edgar-filings").call(run_input={
    "tickers": [
        "AAPL"
    ],
    "ciks": [
        "0000320193"
    ],
    "formTypes": [
        "10-K",
        "10-Q"
    ],
    "maxFilingsPerCompany": 5
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/sec-edgar-filings').call({
    "tickers": [
        "AAPL"
    ],
    "ciks": [
        "0000320193"
    ],
    "formTypes": [
        "10-K",
        "10-Q"
    ],
    "maxFilingsPerCompany": 5
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~sec-edgar-filings/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["AAPL"], "ciks": ["0000320193"], "formTypes": ["10-K", "10-Q"], "maxFilingsPerCompany": 5}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 sec_edgar_filings_scraper.py --token YOUR_APIFY_TOKEN --tickers "AAPL" --ciks "0000320193" --form-types "10-K,10-Q" --max-filings-per-company "5"
node sec_edgar_filings_scraper.mjs --token YOUR_APIFY_TOKEN --tickers "AAPL" --ciks "0000320193" --form-types "10-K,10-Q" --max-filings-per-company "5"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `tickers` | array |  | Stock ticker symbols to pull filings for (for example AAPL, MSFT, NVDA) |
| `ciks` | array |  | Direct SEC Central Index Key numbers, if you already have them (for example 320193 or 0000320193) |
| `formTypes` | array |  | Which SEC form types to return (for example 10-K, 10-Q, 8-K, S-1, 4, DEF 14A) |
| `maxFilingsPerCompany` | integer | `10` | Maximum number of filings to return per company, newest first |
| `dateFrom` | string |  | Only return filings filed on or after this date |
| `dateTo` | string |  | Only return filings filed on or before this date |
| `includeFinancials` | boolean | `false` | Attach a summary of key XBRL financial facts (revenue, net income, assets, etc.) for each company |
| `includeDocumentText` | boolean | `false` | Fetch the primary filing document and attach cleaned plain text, ready for LLM/RAG ingestion |
| `contactEmail` | string | `"contact@example.com"` | SEC requires a contact email in the User-Agent for fair-access |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `ticker` | string | Stock ticker symbol |
| `cik` | string | SEC Central Index Key (10-digit zero-padded) |
| `company_name` | string | Company name as registered with the SEC |
| `sic` | string | Standard Industrial Classification description |
| `form` | string | SEC form type (for example 10-K, 10-Q, 8-K) |
| `filing_date` | string | Date the filing was submitted (YYYY-MM-DD) |
| `report_date` | string | Period of report end date (YYYY-MM-DD) |
| `accession_number` | string | Unique SEC accession number for the filing |
| `primary_document` | string | Filename of the primary filing document |
| `primary_doc_description` | string | Description of the primary document |
| `items` | string | 8-K item codes reported (if applicable) |
| `is_xbrl` | boolean | Whether the filing includes XBRL data |
| `size_bytes` | number | Total size of the filing in bytes |
| `filing_url` | string | Direct URL to the primary filing document |
| `index_url` | string | URL to the filing index page |
| `scraped_at` | string | ISO timestamp when this record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/sec-edgar-filings
```

## FAQ

### What SEC filing types can I pull?

10-K (annual reports), 10-Q (quarterly reports), 8-K (current reports), 20-F, DEF 14A, S-1, and 20 more form types. Search by ticker, CIK, or company name.

### Is the SEC EDGAR data free?

Yes, EDGAR is a public database. The official API is free but rate-limited and returns raw XBRL or HTML. This scraper handles rate limiting and returns clean structured JSON.

### Can I use this for RAG pipelines over financial documents?

Yes. Each filing is returned with full document text pre-extracted and ready for chunking. Pair it with RAG Crawler for large multi-document ingestion pipelines.

### How far back do the filings go?

EDGAR has filings going back to 1993. Use date range filters to pull historical filings for any public company.

### What data is extracted from each filing?

Accession number, form type, filing date, company name, CIK, document URLs, and full text of the primary document. Financial fact tables are included where available in XBRL format.

### How much does the SEC EDGAR Filings Scraper cost?

From $0.60 per 1,000 filings on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [GST Taxpayer Lookup](https://themineworks.com/actors/gst-taxpayer-lookup/): Verify any Indian GSTIN against the official GST portal
* [World Bank Trade Scraper](https://themineworks.com/actors/global-trade-data/): Imports and exports by country and product, from World Bank WITS
* [Company KYB Lookup](https://themineworks.com/actors/company-identity-resolver/): Resolve company names to their LEI and SEC CIK in one run

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
