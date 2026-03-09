# =============================================================
# DATABASE ENGINE — brands_db.json read/write
# =============================================================
# All brand data lives in brands_db.json
# This module is imported by both app.py and the Brand Manager
# =============================================================

import json
import copy
from pathlib import Path

DB_PATH = Path(__file__).parent / "brands_db.json"

# ── Empty brand template (used for new brands + merging defaults) ──
EMPTY_BRAND = {
    "name":              "",
    "hebrew_name":       "",
    "emoji":             "🏢",
    "type":              "",
    "parent_company":    "",
    "website":           "",
    "language":          "עברית",
    "posting_frequency": "",
    "products":          [],
    "usp":               [],
    "audience": {
        "age":           "",
        "gender":        "",
        "interests":     [],
        "psychographic": "",
        "motivation":    "",
    },
    "voice": {
        "tone":           "",
        "style":          "",
        "language_notes": "",
        "do":             [],
        "dont":           [],
    },
    "platforms": {
        "instagram": {"priority": "primary",   "content_types": [], "caption_length": "", "hashtag_count": ""},
        "tiktok":    {"priority": "secondary", "content_types": [], "caption_length": "", "hashtag_count": ""},
        "facebook":  {"priority": "secondary", "content_types": [], "caption_length": "", "hashtag_count": ""},
    },
    "content_that_works": [],
    "content_to_avoid":   [],
    "knowledge_base": {
        "what_works":        [],
        "what_doesnt":       [],
        "competitors":       [],
        "news_sources":      [],
        "learning_links":    [],
        "team_notes":        [],
        "approved_hashtags": [],
    },
    # Phase 2 — Web Awareness: list of curated URLs the agent reads before generating
    # Each entry: { "active": bool, "name": str, "url": str, "focus": str, "ignore": str }
    "web_sources": [],
}


# =============================================================
# CORE CRUD
# =============================================================

def load_brands() -> dict:
    """Load all brands from the JSON database."""
    if not DB_PATH.exists():
        return {}
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_brands(brands: dict):
    """Overwrite the entire brands database."""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(brands, f, ensure_ascii=False, indent=2)


def save_brand(brand_key: str, brand_data: dict):
    """Save or update a single brand (others unchanged)."""
    brands = load_brands()
    brands[brand_key] = brand_data
    save_brands(brands)


def delete_brand(brand_key: str):
    """Delete a brand by key."""
    brands = load_brands()
    if brand_key in brands:
        del brands[brand_key]
        save_brands(brands)


def get_brand_with_defaults(brand_data: dict) -> dict:
    """
    Merge a brand's data with the empty template so every field
    is guaranteed to exist — safe for forms and prompts.
    """
    result = copy.deepcopy(EMPTY_BRAND)
    for key, val in brand_data.items():
        if key in ("audience", "voice", "knowledge_base") and isinstance(val, dict):
            result[key].update(val)
        elif key == "platforms" and isinstance(val, dict):
            for plat, pdata in val.items():
                if plat in result["platforms"]:
                    result["platforms"][plat].update(pdata)
                else:
                    result["platforms"][plat] = pdata
        else:
            result[key] = val
    return result


# =============================================================
# HELPERS
# =============================================================

def brand_key_from_name(name: str) -> str:
    """
    'My Brand Name' → 'my_brand_name'
    Used when creating a new brand.
    """
    return (
        name.lower()
        .strip()
        .replace(" ", "_")
        .replace("'", "")
        .replace('"', "")
        .replace("-", "_")
    )
