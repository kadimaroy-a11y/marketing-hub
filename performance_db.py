# =============================================================
# 📊 PERFORMANCE DB — Structured performance tracking
# =============================================================
# Records performance ratings in a dedicated queryable table
# (separate from the JSONB content_library.data column).
# Enables analytics, trend detection, and AI learning.
# =============================================================

from datetime import datetime, timedelta
from supabase_client import get_supabase


# =============================================================
# RECORD & UPDATE
# =============================================================

def record_rating(
    content_id: str,
    brand_key: str,
    platform: str,
    content_type: str,
    rating: str,
    rating_note: str = "",
    brief_summary: str = "",
):
    """
    Record a structured performance rating.
    Upserts by content_id so re-rating updates the existing record.
    """
    sb = get_supabase()

    # Check if rating already exists for this content
    existing = (
        sb.table("performance_metrics")
        .select("id")
        .eq("content_id", content_id)
        .execute()
    )

    row = {
        "content_id": content_id,
        "brand_key": brand_key,
        "platform": platform,
        "content_type": content_type,
        "rating": rating,
        "rating_note": rating_note,
        "brief_summary": brief_summary,
        "rated_at": datetime.now().isoformat(),
    }

    if existing.data:
        # Update existing
        sb.table("performance_metrics").update(row).eq("content_id", content_id).execute()
    else:
        # Insert new
        sb.table("performance_metrics").insert(row).execute()


def update_real_metrics(
    content_id: str,
    likes: int = None,
    comments: int = None,
    shares: int = None,
    reach: int = None,
    impressions: int = None,
    saves: int = None,
    engagement_rate: float = None,
):
    """Update real engagement metrics (for Phase 2 API integration)."""
    sb = get_supabase()
    updates = {}
    if likes is not None:       updates["likes"] = likes
    if comments is not None:    updates["comments"] = comments
    if shares is not None:      updates["shares"] = shares
    if reach is not None:       updates["reach"] = reach
    if impressions is not None:  updates["impressions"] = impressions
    if saves is not None:       updates["saves"] = saves
    if engagement_rate is not None: updates["engagement_rate"] = engagement_rate

    if updates:
        sb.table("performance_metrics").update(updates).eq("content_id", content_id).execute()


# =============================================================
# QUERIES — Brand Analytics
# =============================================================

def get_brand_performance_summary(brand_key: str) -> dict:
    """
    Aggregate stats for a brand:
    - Rating distribution
    - Best content type
    - Best platform
    - Total rated items
    """
    sb = get_supabase()
    response = (
        sb.table("performance_metrics")
        .select("rating, platform, content_type")
        .eq("brand_key", brand_key)
        .execute()
    )
    items = response.data
    if not items:
        return {"total": 0, "ratings": {}, "best_content_type": None, "best_platform": None}

    # Rating distribution
    ratings = {}
    for item in items:
        r = item["rating"]
        ratings[r] = ratings.get(r, 0) + 1

    # Best content type (most "amazing" + "good" ratings)
    ct_scores = {}
    plat_scores = {}
    for item in items:
        score = {"amazing": 3, "good": 2, "ok": 1, "poor": 0}.get(item["rating"], 0)
        ct = item.get("content_type", "")
        pl = item.get("platform", "")
        if ct:
            ct_scores[ct] = ct_scores.get(ct, 0) + score
        if pl:
            plat_scores[pl] = plat_scores.get(pl, 0) + score

    best_ct = max(ct_scores, key=ct_scores.get) if ct_scores else None
    best_plat = max(plat_scores, key=plat_scores.get) if plat_scores else None

    return {
        "total": len(items),
        "ratings": ratings,
        "best_content_type": best_ct,
        "best_platform": best_plat,
        "content_type_scores": ct_scores,
        "platform_scores": plat_scores,
    }


def get_performance_trends(brand_key: str, days: int = 30) -> list:
    """
    Get performance data over time for trend charts.
    Returns list of {rated_at, rating, content_type, platform}.
    """
    sb = get_supabase()
    since = (datetime.now() - timedelta(days=days)).isoformat()
    response = (
        sb.table("performance_metrics")
        .select("rated_at, rating, content_type, platform, rating_note, brief_summary")
        .eq("brand_key", brand_key)
        .gte("rated_at", since)
        .order("rated_at", desc=False)
        .execute()
    )
    return response.data


def get_all_brand_ratings(brand_key: str) -> list:
    """Get all ratings for a brand (for AI analysis)."""
    sb = get_supabase()
    response = (
        sb.table("performance_metrics")
        .select("*")
        .eq("brand_key", brand_key)
        .order("rated_at", desc=True)
        .execute()
    )
    return response.data


def get_rating_counts() -> dict:
    """Get total rating counts across all brands (for dashboard header)."""
    sb = get_supabase()
    response = sb.table("performance_metrics").select("brand_key, rating").execute()
    total = len(response.data)
    brands = set(r["brand_key"] for r in response.data) if response.data else set()
    amazing = sum(1 for r in response.data if r["rating"] == "amazing")
    return {"total": total, "brands": len(brands), "amazing": amazing}
