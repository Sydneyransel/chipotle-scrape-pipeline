import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pathlib import Path
import tempfile
import datetime
from scrape_pipeline import url_to_slug, save_results

def test_url_to_slug_basic():
    assert url_to_slug("https://ir.chipotle.com/news-releases") == "ir_chipotle_com_news-releases"

def test_url_to_slug_trailing_slash():
    assert url_to_slug("https://ir.chipotle.com/") == "ir_chipotle_com"

def test_url_to_slug_deep_path():
    assert url_to_slug("https://newsroom.chipotle.com/press-releases") == "newsroom_chipotle_com_press-releases"

def test_url_to_slug_no_path():
    assert url_to_slug("https://ir.chipotle.com") == "ir_chipotle_com"

def test_url_to_slug_query_string():
    assert url_to_slug("https://ir.chipotle.com/page?q=results&sort=date") == "ir_chipotle_com_page"


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
