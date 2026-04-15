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
