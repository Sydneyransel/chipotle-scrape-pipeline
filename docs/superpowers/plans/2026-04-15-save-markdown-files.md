# Save Markdown Files Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `save_results()` function to `scrape_pipeline.py` that writes each Firecrawl search result as a dated markdown file in `knowledge/raw/`.

**Architecture:** A `url_to_slug()` helper sanitizes a URL into a safe filename component; `save_results()` iterates the results list, skips entries with no `markdown` field, builds a `YYYY-MM-DD_slug.md` filename, and writes to `knowledge/raw/`. Both functions live in `scrape_pipeline.py`. The directory is created automatically if absent.

**Tech Stack:** Python 3, `pathlib`, `datetime`, `re` (all stdlib — no new dependencies)

---

## File Structure

- **Modify:** `scrape_pipeline.py` — add `url_to_slug()` and `save_results()`
- **Create:** `tests/test_scrape_pipeline.py` — unit tests for both functions

---

### Task 1: Test and implement `url_to_slug()`

**Files:**
- Create: `tests/test_scrape_pipeline.py`
- Modify: `scrape_pipeline.py`

- [ ] **Step 1: Create the test file**

```python
# tests/test_scrape_pipeline.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scrape_pipeline import url_to_slug

def test_url_to_slug_basic():
    assert url_to_slug("https://ir.chipotle.com/news-releases") == "ir_chipotle_com_news-releases"

def test_url_to_slug_trailing_slash():
    assert url_to_slug("https://ir.chipotle.com/") == "ir_chipotle_com"

def test_url_to_slug_deep_path():
    assert url_to_slug("https://newsroom.chipotle.com/press-releases") == "newsroom_chipotle_com_press-releases"

def test_url_to_slug_no_path():
    assert url_to_slug("https://ir.chipotle.com") == "ir_chipotle_com"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
venv/Scripts/python -m pytest tests/test_scrape_pipeline.py -v
```

Expected: `ImportError` or `AttributeError` — `url_to_slug` not defined yet.

- [ ] **Step 3: Add `url_to_slug()` to `scrape_pipeline.py`**

Add this import at the top of `scrape_pipeline.py` (after existing imports):

```python
import re
from pathlib import Path
import datetime
```

Add this function before the API call block:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
venv/Scripts/python -m pytest tests/test_scrape_pipeline.py -v
```

Expected: 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scrape_pipeline.py tests/test_scrape_pipeline.py
git commit -m "feat: add url_to_slug helper with tests"
```

---

### Task 2: Test and implement `save_results()`

**Files:**
- Modify: `tests/test_scrape_pipeline.py`
- Modify: `scrape_pipeline.py`

- [ ] **Step 1: Add tests for `save_results()`**

Append to `tests/test_scrape_pipeline.py`:

```python
import tempfile
from scrape_pipeline import save_results

def test_save_results_writes_files():
    results = [
        {"url": "https://ir.chipotle.com/news-releases", "markdown": "# News\nContent here."},
        {"url": "https://newsroom.chipotle.com/press-releases", "markdown": "# Press\nMore content."},
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        count = save_results(results, tmpdir)
        files = list(Path(tmpdir).glob("*.md"))
        assert count == 2
        assert len(files) == 2

def test_save_results_skips_missing_markdown():
    results = [
        {"url": "https://ir.chipotle.com/news-releases", "markdown": "# News"},
        {"url": "https://ir.chipotle.com/sec-filings"},  # no markdown key
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        count = save_results(results, tmpdir)
        files = list(Path(tmpdir).glob("*.md"))
        assert count == 1
        assert len(files) == 1

def test_save_results_file_content():
    results = [
        {"url": "https://ir.chipotle.com/news-releases", "markdown": "# News\nContent here."},
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        save_results(results, tmpdir)
        files = list(Path(tmpdir).glob("*.md"))
        assert files[0].read_text(encoding="utf-8") == "# News\nContent here."

def test_save_results_creates_directory():
    results = [
        {"url": "https://ir.chipotle.com/news-releases", "markdown": "# News"},
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = os.path.join(tmpdir, "knowledge", "raw")
        save_results(results, out_dir)
        assert Path(out_dir).exists()

def test_save_results_filename_format():
    results = [
        {"url": "https://ir.chipotle.com/news-releases", "markdown": "# News"},
    ]
    today = datetime.date.today().isoformat()
    with tempfile.TemporaryDirectory() as tmpdir:
        save_results(results, tmpdir)
        files = list(Path(tmpdir).glob("*.md"))
        assert files[0].name == f"{today}_ir_chipotle_com_news-releases.md"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
venv/Scripts/python -m pytest tests/test_scrape_pipeline.py -v
```

Expected: `ImportError` — `save_results` not defined yet.

- [ ] **Step 3: Add `save_results()` to `scrape_pipeline.py`**

Add after `url_to_slug()`:

```python
def save_results(results, out_dir):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    saved = 0
    for result in results:
        markdown = result.get("markdown")
        if not markdown:
            continue
        slug = url_to_slug(result["url"])
        filename = f"{today}_{slug}.md"
        (out_path / filename).write_text(markdown, encoding="utf-8")
        saved += 1
    return saved
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
venv/Scripts/python -m pytest tests/test_scrape_pipeline.py -v
```

Expected: all 9 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scrape_pipeline.py tests/test_scrape_pipeline.py
git commit -m "feat: add save_results with tests"
```

---

### Task 3: Wire `save_results()` into the pipeline

**Files:**
- Modify: `scrape_pipeline.py`

- [ ] **Step 1: Call `save_results()` after the existing print block**

At the bottom of `scrape_pipeline.py`, after the existing summary print, add:

```python
results = response.json().get("data", {}).get("web", [])
count = save_results(results, "knowledge/raw")
print(f"Saved {count} files to knowledge/raw/")
```

> Note: check what variable name is used for the results list in the existing print block — reuse it rather than calling `.json()` again.

- [ ] **Step 2: Run the full pipeline**

```bash
venv/Scripts/python scrape_pipeline.py
```

Expected output ends with: `Saved 5 files to knowledge/raw/`

- [ ] **Step 3: Verify files were written**

```bash
ls knowledge/raw/
```

Expected: 5 `.md` files with today's date prefix, e.g.:
```
2026-04-15_ir_chipotle_com_news-releases.md
2026-04-15_newsroom_chipotle_com_press-releases.md
...
```

- [ ] **Step 4: Commit**

```bash
git add scrape_pipeline.py
git commit -m "feat: wire save_results into pipeline"
```
