#!/usr/bin/env node
// Node.js client for the themineworks/sec-edgar-filings actor on Apify: runs it and saves results.json.
// Flags map 1:1 to the actor's input. Free API token: https://console.apify.com/sign-up
// Docs and pricing: https://themineworks.com/actors/sec-edgar-filings/
import { ApifyClient } from 'apify-client';
import { writeFileSync } from 'node:fs';

const ACTOR = 'themineworks/sec-edgar-filings';

function parseArgs(argv) {
    const out = {};
    for (let i = 0; i < argv.length; i++) {
        if (!argv[i].startsWith('--')) continue;
        const key = argv[i].slice(2);
        out[key] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    }
    return out;
}

const args = parseArgs(process.argv.slice(2));
const token = args.token || process.env.APIFY_TOKEN;
if (!token) {
    console.error('Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up');
    process.exit(1);
}

const runInput = {};
if (args['tickers'] !== undefined) runInput.tickers = String(args['tickers']).split(',').map((s) => s.trim());
if (args['ciks'] !== undefined) runInput.ciks = String(args['ciks']).split(',').map((s) => s.trim());
if (args['form-types'] !== undefined) runInput.formTypes = String(args['form-types']).split(',').map((s) => s.trim());
if (args['max-filings-per-company'] !== undefined) runInput.maxFilingsPerCompany = parseInt(args['max-filings-per-company'], 10);
if (args['date-from'] !== undefined) runInput.dateFrom = String(args['date-from']);
if (args['date-to'] !== undefined) runInput.dateTo = String(args['date-to']);
if (args['include-financials'] !== undefined) runInput.includeFinancials = args['include-financials'] === true || args['include-financials'] === 'true';
if (args['include-document-text'] !== undefined) runInput.includeDocumentText = args['include-document-text'] === true || args['include-document-text'] === 'true';
if (args['contact-email'] !== undefined) runInput.contactEmail = String(args['contact-email']);

const client = new ApifyClient({ token });
console.log(`Running ${ACTOR} ...`);
const run = await client.actor(ACTOR).call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
writeFileSync('results.json', JSON.stringify(items, null, 2));
console.log(`Saved ${items.length} results to results.json`);
