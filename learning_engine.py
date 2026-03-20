# =============================================================
# 🧠 LEARNING ENGINE — AI-powered pattern analysis
# =============================================================
# Analyzes accumulated performance data to find patterns,
# generate brand insights, and build enhanced learning context
# for Claude's content generation prompts.
# =============================================================

import os
import anthropic
from datetime import datetime
from dotenv import load_dotenv
from supabase_client import get_supabase
from performance_db import get_all_brand_ratings, get_brand_performance_summary

load_dotenv()


# =============================================================
# LEARNING CONTEXT — Enhanced prompt injection
# =============================================================

def build_learning_context(brand_key: str) -> str:
    """
    Build an enhanced learning context section for the system prompt.
    Combines:
    - Top-performing content examples
    - Pattern analysis summary
    - Latest AI insights (if any)
    Returns a string to inject into the system prompt.
    """
    sections = []

    # 1. Top-performing examples (from content_library)
    try:
        from content_db import get_top_performing
        top_items = get_top_performing(brand_key, limit=5)
        if top_items:
            examples = []
            for i, item in enumerate(top_items, 1):
                rating = item.get("performance_rating", "good")
                note = item.get("performance_note", "")
                brief = item.get("brief", "")[:100]
                ctype = item.get("content_type", "")
                plat = item.get("platform", "")
                content_preview = item.get("content", "")[:300]
                entry = f"דוגמה {i} ({rating}) — {ctype} ל-{plat}:\n  בריף: {brief}"
                if note:
                    entry += f"\n  ביצועים: {note}"
                entry += f"\n  תוכן:\n{content_preview}"
                if len(item.get("content", "")) > 300:
                    entry += "..."
                examples.append(entry)

            sections.append(
                "═══════════════════════════════════════\n"
                " 🏆 דוגמאות מוצלחות מהעבר — למד מהן\n"
                "═══════════════════════════════════════\n\n"
                "התוכן הבא קיבל דירוג גבוה מהצוות. השתמש בו כהשראה לטון, סגנון ומבנה:\n\n"
                + "\n\n---\n\n".join(examples)
            )
    except Exception:
        pass

    # 2. Pattern analysis from structured ratings
    try:
        summary = get_brand_performance_summary(brand_key)
        if summary["total"] >= 3:  # Need at least 3 ratings for patterns
            pattern_lines = []
            pattern_lines.append(f"סה\"כ תכנים מדורגים: {summary['total']}")

            if summary.get("best_content_type"):
                pattern_lines.append(f"סוג תוכן מוצלח ביותר: {summary['best_content_type']}")
            if summary.get("best_platform"):
                pattern_lines.append(f"פלטפורמה מוצלחת ביותר: {summary['best_platform']}")

            ratings = summary.get("ratings", {})
            if ratings:
                amazing = ratings.get("amazing", 0)
                good = ratings.get("good", 0)
                poor = ratings.get("poor", 0)
                total = summary["total"]
                success_rate = round((amazing + good) / total * 100)
                pattern_lines.append(f"אחוז הצלחה (amazing+good): {success_rate}%")

                if poor > 0:
                    pattern_lines.append(f"תכנים חלשים: {poor} — שים לב ללמוד מהטעויות")

            # Content type breakdown
            ct_scores = summary.get("content_type_scores", {})
            if len(ct_scores) > 1:
                sorted_ct = sorted(ct_scores.items(), key=lambda x: x[1], reverse=True)
                ranking = " > ".join(f"{ct}" for ct, _ in sorted_ct[:4])
                pattern_lines.append(f"דירוג סוגי תוכן (מהטוב לפחות): {ranking}")

            sections.append(
                "═══════════════════════════════════════\n"
                " 📊 ניתוח דפוסים — מה עובד לפי נתונים\n"
                "═══════════════════════════════════════\n\n"
                + "\n".join(f"  • {line}" for line in pattern_lines)
            )
    except Exception:
        pass

    # 3. Latest AI insights (if any)
    try:
        sb = get_supabase()
        response = (
            sb.table("learning_snapshots")
            .select("content, generated_at")
            .eq("brand_key", brand_key)
            .eq("applied", True)
            .order("generated_at", desc=True)
            .limit(1)
            .execute()
        )
        if response.data:
            insight = response.data[0]
            sections.append(
                "═══════════════════════════════════════\n"
                " 💡 תובנות AI — מה למדנו\n"
                "═══════════════════════════════════════\n\n"
                + insight["content"]
            )
    except Exception:
        pass

    if not sections:
        return ""

    return "\n\n" + "\n\n".join(sections)


# =============================================================
# AI INSIGHTS GENERATION
# =============================================================

def generate_brand_insights(brand_key: str, brand_name: str = "") -> str:
    """
    Use Claude to analyze all rated content for a brand and produce
    actionable insights about what works, what doesn't, and patterns.
    Returns the insight text.
    """
    ratings = get_all_brand_ratings(brand_key)
    if not ratings:
        return "אין מספיק נתונים. דרג תכנים בספריית התוכן כדי לצבור נתונים."

    # Build data summary for Claude
    data_lines = []
    for r in ratings:
        line = (
            f"- [{r['rating']}] {r['content_type']} ל-{r['platform']}"
        )
        if r.get("brief_summary"):
            line += f" | בריף: {r['brief_summary']}"
        if r.get("rating_note"):
            line += f" | הערה: {r['rating_note']}"
        data_lines.append(line)

    data_text = "\n".join(data_lines)

    summary = get_brand_performance_summary(brand_key)

    prompt = f"""אתה אנליסט שיווק דיגיטלי מומחה. נתח את ביצועי התוכן של {brand_name or brand_key} וספק תובנות מעשיות.

נתוני ביצועים ({summary['total']} תכנים מדורגים):

{data_text}

סיכום:
- סוג תוכן מוצלח: {summary.get('best_content_type', 'לא ידוע')}
- פלטפורמה מוצלחת: {summary.get('best_platform', 'לא ידוע')}
- התפלגות: amazing={summary['ratings'].get('amazing',0)}, good={summary['ratings'].get('good',0)}, ok={summary['ratings'].get('ok',0)}, poor={summary['ratings'].get('poor',0)}

ספק ניתוח מובנה בעברית:

1. 🏆 מה עובד הכי טוב (2-3 תובנות ספציפיות)
2. ⚠️ מה לא עובד (1-2 דברים להימנע)
3. 💡 המלצות לשיפור (2-3 פעולות קונקרטיות)
4. 📊 דפוס מרכזי (תובנה אחת על-ארכית)

היה קצר, מדויק, ומעשי. כל תובנה = משפט אחד עד שניים מקסימום.
"""

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-haiku-4-20250414",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


def save_insight(brand_key: str, insight_text: str, applied: bool = False):
    """Save an AI-generated insight to the learning_snapshots table."""
    sb = get_supabase()
    sb.table("learning_snapshots").insert({
        "brand_key": brand_key,
        "snapshot_type": "ai_insight",
        "content": insight_text,
        "generated_at": datetime.now().isoformat(),
        "applied": applied,
    }).execute()


def apply_insight(snapshot_id: str):
    """Mark an insight as applied (it will be injected into future prompts)."""
    sb = get_supabase()
    sb.table("learning_snapshots").update({"applied": True}).eq("id", snapshot_id).execute()


def get_brand_insights(brand_key: str, limit: int = 5) -> list:
    """Get recent insights for a brand."""
    sb = get_supabase()
    response = (
        sb.table("learning_snapshots")
        .select("*")
        .eq("brand_key", brand_key)
        .order("generated_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data
