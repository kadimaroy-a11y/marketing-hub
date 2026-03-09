# =============================================================
# 📚 CONTENT LIBRARY — Save, browse and reuse generated content
# =============================================================
# All saved content lives in content_library.json
# Each item stores: brand, platform, content type, brief, full
# content, date saved, and optional notes.
# =============================================================

import json
import copy
from pathlib import Path
from datetime import datetime

LIBRARY_PATH = Path(__file__).parent / "content_library.json"


# =============================================================
# CORE CRUD
# =============================================================

def load_library() -> list:
    """Load all saved content items."""
    if not LIBRARY_PATH.exists():
        return []
    try:
        with open(LIBRARY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("items", [])
    except (json.JSONDecodeError, IOError):
        return []


def save_library(items: list):
    """Overwrite the entire content library."""
    with open(LIBRARY_PATH, "w", encoding="utf-8") as f:
        json.dump({"items": items}, f, ensure_ascii=False, indent=2)


def add_to_library(item: dict) -> str:
    """
    Add a content item to the library.
    Auto-generates an ID and timestamp.
    Returns the item ID.
    """
    items = load_library()
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    brand   = item.get("brand_key", "unknown")
    item_id = f"{ts}_{brand}"

    item_copy = copy.deepcopy(item)
    item_copy["id"]       = item_id
    item_copy["saved_at"] = datetime.now().isoformat()

    items.insert(0, item_copy)   # newest first
    save_library(items)
    return item_id


def delete_from_library(item_id: str):
    """Remove an item by ID."""
    items = [i for i in load_library() if i.get("id") != item_id]
    save_library(items)


def update_notes(item_id: str, notes: str):
    """Update the notes field of a saved item."""
    items = load_library()
    for item in items:
        if item.get("id") == item_id:
            item["notes"] = notes
            break
    save_library(items)


# =============================================================
# QUERIES
# =============================================================

def get_brand_library(brand_key: str) -> list:
    """Return all items for a specific brand."""
    return [i for i in load_library() if i.get("brand_key") == brand_key]


def get_library_stats() -> dict:
    """Return summary stats for the footer."""
    items = load_library()
    brands = set(i.get("brand_key", "") for i in items)
    return {
        "total":  len(items),
        "brands": len(brands),
    }
