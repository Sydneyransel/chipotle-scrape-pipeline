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
    # Strip trailing slash
    slug = slug.rstrip('/')
    # Replace dots and slashes with underscores
    slug = slug.replace('.', '_').replace('/', '_')
    # Collapse repeated underscores
    slug = re.sub(r'_+', '_', slug)
    return slug.strip('_')


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
