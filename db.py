# =============================================================
# DATABASE ENGINE — Supabase-backed brand storage
# =============================================================
# All brand data lives in a Supabase "brands" table (JSONB).
# This module is imported by both app.py and the Brand Manager.
# =============================================================

import copy
from supabase_client import get_supabase

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
    # Phase 3 — Scheduled Events: monthly events injected into generated content
    # { "1": [{"text": str, "active": bool}, ...], ..., "12": [...] }
    "scheduled_events": {},
}


# =============================================================
# CORE CRUD
# =============================================================

def load_brands() -> dict:
    """Load all brands from Supabase."""
    try:
        sb = get_supabase()
        response = sb.table("brands").select("key, data").execute()
        return {row["key"]: row["data"] for row in response.data}
    except Exception:
        return {}


def save_brands(brands: dict):
    """Upsert all brands (bulk save)."""
    sb = get_supabase()
    rows = [{"key": k, "data": v} for k, v in brands.items()]
    if rows:
        sb.table("brands").upsert(rows).execute()


def save_brand(brand_key: str, brand_data: dict):
    """Save or update a single brand."""
    sb = get_supabase()
    sb.table("brands").upsert({"key": brand_key, "data": brand_data}).execute()


def delete_brand(brand_key: str):
    """Delete a brand by key."""
    sb = get_supabase()
    sb.table("brands").delete().eq("key", brand_key).execute()


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
