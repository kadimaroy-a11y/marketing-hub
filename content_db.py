# =============================================================
# 📚 CONTENT LIBRARY — Supabase-backed content storage
# =============================================================
# All saved content lives in a Supabase "content_library" table.
# Each item stores: brand, platform, content type, brief, full
# content, date saved, optional notes, and performance rating.
# =============================================================

import copy
from datetime import datetime
from supabase_client import get_supabase


# =============================================================
# CORE CRUD
# =============================================================

def load_library() -> list:
    """Load all saved content items (newest first)."""
    try:
        sb = get_supabase()
        response = (
            sb.table("content_library")
            .select("data")
            .order("saved_at", desc=True)
            .execute()
        )
        return [row["data"] for row in response.data]
    except Exception:
        return []


def save_library(items: list):
    """Overwrite the entire content library (used by legacy callers)."""
    sb = get_supabase()
    # Clear and re-insert
    sb.table("content_library").delete().neq("id", "").execute()
    if items:
        rows = [
            {
                "id":        i["id"],
                "brand_key": i.get("brand_key", ""),
                "data":      i,
                "saved_at":  i.get("saved_at", datetime.now().isoformat()),
            }
            for i in items
        ]
        sb.table("content_library").upsert(rows).execute()


def add_to_library(item: dict) -> str:
    """
    Add a content item to the library.
    Auto-generates an ID and timestamp.
    Returns the item ID.
    """
    sb = get_supabase()
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    brand   = item.get("brand_key", "unknown")
    item_id = f"{ts}_{brand}"

    item_copy = copy.deepcopy(item)
    item_copy["id"]       = item_id
    item_copy["saved_at"] = datetime.now().isoformat()

    sb.table("content_library").insert({
        "id":        item_id,
        "brand_key": brand,
        "data":      item_copy,
        "saved_at":  item_copy["saved_at"],
    }).execute()
    return item_id


def delete_from_library(item_id: str):
    """Remove an item by ID."""
    sb = get_supabase()
    sb.table("content_library").delete().eq("id", item_id).execute()


def update_notes(item_id: str, notes: str):
    """Update the notes field of a saved item."""
    sb = get_supabase()
    response = sb.table("content_library").select("data").eq("id", item_id).execute()
    if response.data:
        data = response.data[0]["data"]
        data["notes"] = notes
        sb.table("content_library").update({"data": data}).eq("id", item_id).execute()


def update_performance(item_id: str, rating: str, note: str = ""):
    """Update the performance rating and note of a saved item."""
    sb = get_supabase()
    response = sb.table("content_library").select("data").eq("id", item_id).execute()
    if response.data:
        data = response.data[0]["data"]
        data["performance_rating"] = rating
        data["performance_note"]   = note
        sb.table("content_library").update({"data": data}).eq("id", item_id).execute()


# =============================================================
# QUERIES
# =============================================================

def get_brand_library(brand_key: str) -> list:
    """Return all items for a specific brand (newest first)."""
    sb = get_supabase()
    response = (
        sb.table("content_library")
        .select("data")
        .eq("brand_key", brand_key)
        .order("saved_at", desc=True)
        .execute()
    )
    return [row["data"] for row in response.data]


def get_top_performing(brand_key: str, limit: int = 5) -> list:
    """Return top-rated content items for a brand (for AI prompt injection)."""
    items = get_brand_library(brand_key)
    top = [i for i in items if i.get("performance_rating") in ("amazing", "good")]
    return top[:limit]


def get_library_stats() -> dict:
    """Return summary stats for the footer."""
    sb = get_supabase()
    response = sb.table("content_library").select("brand_key").execute()
    brands = set(row["brand_key"] for row in response.data)
    return {
        "total":  len(response.data),
        "brands": len(brands),
    }
