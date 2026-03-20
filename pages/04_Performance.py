# =============================================================
# 📊 PERFORMANCE DASHBOARD — Analytics & AI Learning
# =============================================================
# Shows performance trends, content analysis, and AI-generated
# insights. Lets the team understand what works and feed
# learnings back into the brand DNA.
# =============================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from db import load_brands, save_brand
from performance_db import (
    get_brand_performance_summary,
    get_performance_trends,
    get_rating_counts,
)
from learning_engine import (
    generate_brand_insights,
    save_insight,
    apply_insight,
    get_brand_insights,
    build_learning_context,
)
import importlib
if "translations" in sys.modules:
    importlib.reload(sys.modules["translations"])
from translations import get_t

load_dotenv()

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="📊 Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Language ────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "he"

lang = st.session_state.lang
t = get_t(lang)
D = t["dir"]
A = t["align"]

BRANDS = load_brands()

# ── UI Strings ──────────────────────────────────────────────
UI = {
    "he": {
        "title": "📊 דשבורד ביצועים",
        "subtitle": "נתח מה עובד, למד דפוסים, ושפר עם AI",
        "select_brand": "בחר מותג",
        "all_brands": "כל המותגים",
        "tab_overview": "📊 סקירה",
        "tab_trends": "📈 מגמות",
        "tab_insights": "💡 תובנות AI",
        "tab_learning": "🧠 מה Claude למד",
        "total_rated": "תכנים מדורגים",
        "total_brands": "מותגים פעילים",
        "total_amazing": "תכנים מעולים 🏆",
        "rating_dist": "התפלגות דירוגים",
        "best_content_type": "סוג תוכן מוצלח",
        "best_platform": "פלטפורמה מוצלחת",
        "content_type_ranking": "דירוג סוגי תוכן",
        "platform_ranking": "דירוג פלטפורמות",
        "no_data": "אין מספיק נתונים. דרג תכנים בספריית התוכן כדי לראות ניתוחים.",
        "trends_title": "מגמות ביצועים (30 ימים)",
        "trends_no_data": "אין נתונים ב-30 הימים האחרונים.",
        "generate_insights": "🧠 צור תובנות AI",
        "generating": "מנתח נתונים...",
        "insight_generated": "תובנות נוצרו בהצלחה!",
        "apply_to_brand": "🎯 החל על DNA המותג",
        "applied": "✅ הוחל!",
        "past_insights": "תובנות קודמות",
        "no_insights": "עדיין אין תובנות. לחץ 'צור תובנות AI' כדי להתחיל.",
        "learning_preview": "תצוגה מקדימה: מה Claude רואה כשהוא יוצר תוכן",
        "learning_empty": "Claude עדיין לא צבר מספיק נתונים. דרג לפחות 3 תכנים.",
        "rating_labels": {
            "amazing": "🔥 מעולה",
            "good": "👍 טוב",
            "ok": "😐 בסדר",
            "poor": "👎 חלש",
        },
        "success_rate": "אחוז הצלחה",
    },
    "en": {
        "title": "📊 Performance Dashboard",
        "subtitle": "Analyze what works, learn patterns, improve with AI",
        "select_brand": "Select Brand",
        "all_brands": "All Brands",
        "tab_overview": "📊 Overview",
        "tab_trends": "📈 Trends",
        "tab_insights": "💡 AI Insights",
        "tab_learning": "🧠 What Claude Learned",
        "total_rated": "Rated Content",
        "total_brands": "Active Brands",
        "total_amazing": "Amazing Content 🏆",
        "rating_dist": "Rating Distribution",
        "best_content_type": "Best Content Type",
        "best_platform": "Best Platform",
        "content_type_ranking": "Content Type Ranking",
        "platform_ranking": "Platform Ranking",
        "no_data": "Not enough data. Rate content in the Content Library to see analytics.",
        "trends_title": "Performance Trends (30 days)",
        "trends_no_data": "No data in the last 30 days.",
        "generate_insights": "🧠 Generate AI Insights",
        "generating": "Analyzing data...",
        "insight_generated": "Insights generated successfully!",
        "apply_to_brand": "🎯 Apply to Brand DNA",
        "applied": "✅ Applied!",
        "past_insights": "Past Insights",
        "no_insights": "No insights yet. Click 'Generate AI Insights' to start.",
        "learning_preview": "Preview: What Claude sees when generating content",
        "learning_empty": "Claude hasn't accumulated enough data yet. Rate at least 3 pieces of content.",
        "rating_labels": {
            "amazing": "🔥 Amazing",
            "good": "👍 Good",
            "ok": "😐 OK",
            "poor": "👎 Poor",
        },
        "success_rate": "Success Rate",
    },
}

ui = UI[lang]

# ── Styling ─────────────────────────────────────────────────
st.markdown(f"""
<style>
    [data-testid="stMainBlockContainer"] h1,
    [data-testid="stMainBlockContainer"] h2,
    [data-testid="stMainBlockContainer"] h3,
    [data-testid="stMainBlockContainer"] p {{
        direction: {D}; text-align: {A};
    }}
    .insight-card {{
        background: #f8f9ff;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        border-right: 4px solid #6c63ff;
        direction: rtl;
        text-align: right;
        line-height: 1.8;
        white-space: pre-wrap;
    }}
    .insight-meta {{
        font-size: 12px;
        color: #999;
        margin-bottom: 8px;
    }}
    .metric-card {{
        background: linear-gradient(135deg, #f4f4fb 0%, #ebe8ff 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }}
    .learning-preview {{
        background: #f0fff4;
        border: 2px dashed #38a169;
        border-radius: 12px;
        padding: 20px;
        direction: rtl;
        text-align: right;
        white-space: pre-wrap;
        font-size: 13px;
        line-height: 1.8;
        max-height: 500px;
        overflow-y: auto;
    }}
    footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ── Language toggle ─────────────────────────────────────────
col_lang_l, col_lang_r = st.columns([8, 2])
with col_lang_r:
    col_he, col_en = st.columns(2)
    with col_he:
        if st.checkbox("עב", value=(lang == "he"), key="perf_he"):
            if lang != "he":
                st.session_state.lang = "he"
                st.rerun()
    with col_en:
        if st.checkbox("EN", value=(lang == "en"), key="perf_en"):
            if lang != "en":
                st.session_state.lang = "en"
                st.rerun()

# ── Title ───────────────────────────────────────────────────
st.markdown(f"# {ui['title']}")
st.markdown(f"*{ui['subtitle']}*")
st.divider()

# ── Brand selector ──────────────────────────────────────────
brand_options = {k: f"{v.get('emoji', '🏢')} {v.get('name', k)}" for k, v in BRANDS.items()}
selected_brand = st.selectbox(
    ui["select_brand"],
    options=list(brand_options.keys()),
    format_func=lambda x: brand_options[x],
)

# ── Global stats ────────────────────────────────────────────
global_stats = get_rating_counts()
c1, c2, c3 = st.columns(3)
c1.metric(ui["total_rated"], global_stats["total"])
c2.metric(ui["total_brands"], global_stats["brands"])
c3.metric(ui["total_amazing"], global_stats["amazing"])

st.markdown("")

# =============================================================
# TABS
# =============================================================
tab_overview, tab_trends, tab_insights, tab_learning = st.tabs([
    ui["tab_overview"], ui["tab_trends"], ui["tab_insights"], ui["tab_learning"]
])


# ── TAB: Overview ───────────────────────────────────────────
with tab_overview:
    summary = get_brand_performance_summary(selected_brand)

    if summary["total"] == 0:
        st.info(ui["no_data"])
    else:
        # Rating distribution chart
        st.markdown(f"### {ui['rating_dist']}")
        ratings = summary.get("ratings", {})
        chart_data = {
            ui["rating_labels"].get(k, k): v
            for k, v in ratings.items()
        }
        st.bar_chart(chart_data)

        # Success rate
        total = summary["total"]
        amazing = ratings.get("amazing", 0)
        good = ratings.get("good", 0)
        success_rate = round((amazing + good) / total * 100) if total else 0

        mc1, mc2, mc3 = st.columns(3)
        mc1.metric(ui["success_rate"], f"{success_rate}%")
        mc2.metric(ui["best_content_type"], summary.get("best_content_type", "—"))
        mc3.metric(ui["best_platform"], summary.get("best_platform", "—"))

        # Content type ranking
        st.markdown(f"### {ui['content_type_ranking']}")
        ct_scores = summary.get("content_type_scores", {})
        if ct_scores:
            st.bar_chart(ct_scores)

        # Platform ranking
        st.markdown(f"### {ui['platform_ranking']}")
        plat_scores = summary.get("platform_scores", {})
        if plat_scores:
            st.bar_chart(plat_scores)


# ── TAB: Trends ─────────────────────────────────────────────
with tab_trends:
    st.markdown(f"### {ui['trends_title']}")
    trends = get_performance_trends(selected_brand, days=30)

    if not trends:
        st.info(ui["trends_no_data"])
    else:
        # Convert ratings to scores for line chart
        score_map = {"amazing": 4, "good": 3, "ok": 2, "poor": 1}
        trend_scores = []
        for item in trends:
            trend_scores.append({
                "date": item["rated_at"][:10],
                "score": score_map.get(item["rating"], 0),
                "type": item.get("content_type", ""),
                "platform": item.get("platform", ""),
            })

        # Line chart of scores over time
        import pandas as pd
        df = pd.DataFrame(trend_scores)
        if not df.empty:
            chart_df = df.groupby("date")["score"].mean()
            st.line_chart(chart_df)

            # Recent ratings list
            st.markdown("---")
            for item in reversed(trends[-10:]):
                rating_emoji = {"amazing": "🔥", "good": "👍", "ok": "😐", "poor": "👎"}.get(item["rating"], "")
                st.markdown(
                    f"{rating_emoji} **{item['rating']}** — {item.get('content_type', '')} "
                    f"({item.get('platform', '')}) — {item.get('brief_summary', '')[:60]}"
                )


# ── TAB: AI Insights ────────────────────────────────────────
with tab_insights:
    brand_info = BRANDS.get(selected_brand, {})
    brand_name = brand_info.get("name", selected_brand)

    # Generate button
    if st.button(ui["generate_insights"], type="primary", use_container_width=True):
        with st.spinner(ui["generating"]):
            insight_text = generate_brand_insights(selected_brand, brand_name)
            save_insight(selected_brand, insight_text)
            st.success(ui["insight_generated"])
            st.rerun()

    # Show past insights
    st.markdown(f"### {ui['past_insights']}")
    insights = get_brand_insights(selected_brand, limit=10)

    if not insights:
        st.info(ui["no_insights"])
    else:
        for insight in insights:
            dt = insight.get("generated_at", "")[:16].replace("T", " ")
            applied = insight.get("applied", False)
            status = "✅" if applied else "⏳"

            st.markdown(
                f'<div class="insight-card">'
                f'<div class="insight-meta">{status} {dt}</div>'
                f'{insight["content"]}'
                f'</div>',
                unsafe_allow_html=True,
            )

            if not applied:
                if st.button(
                    ui["apply_to_brand"],
                    key=f"apply_{insight['id']}",
                ):
                    apply_insight(insight["id"])
                    st.success(ui["applied"])
                    st.rerun()


# ── TAB: What Claude Learned ────────────────────────────────
with tab_learning:
    st.markdown(f"### {ui['learning_preview']}")
    st.caption(
        "זה מה שClaude רואה כחלק מה-System Prompt כשהוא יוצר תוכן חדש למותג הזה."
        if lang == "he" else
        "This is what Claude sees as part of the System Prompt when generating new content for this brand."
    )

    learning_ctx = build_learning_context(selected_brand)

    if learning_ctx.strip():
        st.markdown(
            f'<div class="learning-preview">{learning_ctx}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info(ui["learning_empty"])
