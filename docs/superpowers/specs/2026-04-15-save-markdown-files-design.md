# Design: Save Firecrawl Results as Markdown Files

**Date:** 2026-04-15

## Goal

Extend `scrape_pipeline.py` so each Firecrawl search result is saved as a markdown file in `knowledge/raw/`.

## Architecture

Add a single `save_results(results, out_dir)` function to `scrape_pipeline.py`. Called after the existing search/print block. `knowledge/raw/` is created automatically if it does not exist. No other files change.

## Filename Convention

Each filename is composed of today's date and a slug derived from the result URL:

- Strip scheme (`https://`)
- Replace `/` and `.` with `_`
- Collapse repeated underscores

Example: `https://ir.chipotle.com/news-releases` → `2026-04-15_ir_chipotle_com_news-releases.md`

Date is sourced from `datetime.date.today()`.

## File Content

Raw markdown from `result["markdown"]`. No frontmatter. Each run always writes files (date in filename provides natural versioning across runs).

## Data Flow

```
response.json()
  └─ data.web[]
       └─ for each result:
            ├─ result["url"]      → filename slug
            ├─ result["markdown"] → file content
            └─ write to knowledge/raw/<filename>.md

Print: "Saved N files to knowledge/raw/"
```

## Error Handling

- If a result has no `markdown` field, skip it silently and reduce the saved count.
- If the API call fails, `response.json()` raises naturally — no additional handling needed.
