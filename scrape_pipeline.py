import os
import re
from pathlib import Path
import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("FIRECRAWL_API_KEY")


def url_to_slug(url):
    # Strip scheme
    slug = re.sub(r'^https?://', '', url)
    slug = re.sub(r'[?#].*', '', slug)  # strip query string and fragment
    # Strip trailing slash
    slug = slug.rstrip('/')
    # Replace dots and slashes with underscores
    slug = slug.replace('.', '_').replace('/', '_')
    # Collapse repeated underscores
    slug = re.sub(r'_+', '_', slug)
    return slug.strip('_')


def save_results(results, out_dir):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    saved = 0
    for result in results:
        markdown = result.get("markdown")
        if not markdown:
            continue
        url = result.get("url")
        if not url:
            continue
        slug = url_to_slug(url)
        filename = f"{today}_{slug}.md"
        (out_path / filename).write_text(markdown, encoding="utf-8")
        saved += 1
    return saved


if __name__ == "__main__":
    # --- Step 01: Search + scrape with Firecrawl ---

    api_url = "https://api.firecrawl.dev/v2/search"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "query": "Chipotle investor relations press releases",
        "limit": 5,
        "scrapeOptions": {"formats": ["markdown"]}
    }

    response = requests.post(api_url, headers=headers, json=payload)

    data = response.json()
    results = data["data"]["web"]
    print(f"Firecrawl returned {len(results)} results")

    for r in results:
        print(f"  - {r['title']}")
        print(f"    {r['url']}")
        print(f"    markdown length: {len(r.get('markdown') or '')} chars")

    count = save_results(results, "knowledge/raw")
    print(f"Saved {count} files to knowledge/raw/")
