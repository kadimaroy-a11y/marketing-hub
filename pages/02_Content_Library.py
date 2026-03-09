# =============================================================
# 📚 CONTENT LIBRARY — Browse, copy and reuse saved content
# =============================================================
import sys
import os
import json
import html as html_lib
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import streamlit.components.v1 as components
from content_db import load_library, delete_from_library, update_notes, get_library_stats
from db import load_brands

st.set_page_config(
    page_title="📚 Content Library",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================
# STYLING
# =============================================================
st.markdown("""
<style>
    label,
    .stCaption p,
    [data-testid="stMarkdownContainer"] p {
        direction: rtl !important;
        text-align: right !important;
    }
    [data-testid="stMainBlockContainer"] h1,
    [data-testid="stMainBlockContainer"] h2,
    [data-testid="stMainBlockContainer"] h3 {
        direction: rtl; text-align: right;
    }
    [data-testid="stAlert"] { direction: rtl; text-align: right; }

    .content-card {
        background: #fafbff;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        border-right: 4px solid #6c63ff;
        direction: rtl;
        text-align: right;
    }
    .card-meta {
        font-size: 12px;
        color: #999;
        direction: rtl;
        text-align: right;
        margin-bottom: 8px;
    }
    .card-brief {
        font-size: 14px;
        color: #555;
        background: #f0f2ff;
        padding: 8px 12px;
        border-radius: 8px;
        direction: rtl;
        text-align: right;
        margin-bottom: 10px;
        font-style: italic;
    }
    .section-box {
        direction: rtl;
        text-align: right;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 14px;
        line-height: 1.85;
        background: #f4f4fb;
        padding: 12px 16px;
        border-radius: 8px;
        border-right: 3px solid #6c63ff;
        color: #1a1a2e;
        white-space: pre-wrap;
        margin-bottom: 6px;
    }
    .section-box-img {
        direction: ltr;
        text-align: left;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        line-height: 1.7;
        background: #f0fff4;
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 3px solid #38a169;
        color: #1a3a2a;
        white-space: pre-wrap;
        margin-bottom: 6px;
    }
    .section-label {
        font-size: 13px;
        font-weight: 700;
        color: #4a4a8a;
        direction: rtl;
        text-align: right;
        margin: 10px 0 4px 0;
    }
    .empty-state {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
        border-radius: 12px;
        padding: 60px 30px;
        text-align: center;
        border: 2px dashed #d0d5ff;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# =============================================================
# HELPERS
# =============================================================
SECTION_CONFIG = [
    ("caption",      "📝", "כיתוב ראשי"),
    ("hashtags",     "#️⃣", "האשטגים"),
    ("visual",       "🎬", "כיוון ויזואלי"),
    ("story",        "📱", "גרסת סטורי"),
    ("image_prompt", "🖼️", "פרומפט לתמונה (AI)"),
]

MARKER_EMOJIS = {
    "caption":      ["📝"],
    "hashtags":     ["#️⃣", "️⃣", "#⃣"],
    "visual":       ["🎬"],
    "story":        ["📱"],
    "image_prompt": ["🖼️"],
}


def parse_sections(content: str) -> dict:
    sections  = {}
    positions = []
    for key, emojis in MARKER_EMOJIS.items():
        for emoji in emojis:
            idx = content.find(emoji)
            if idx != -1:
                positions.append((idx, key))
                break
    positions.sort(key=lambda x: x[0])
    for i, (idx, key) in enumerate(positions):
        line_end = content.find("\n", idx)
        if line_end == -1:
            sections[key] = content[idx:].strip()
            continue
        start = line_end + 1
        end   = positions[i + 1][0] if i + 1 < len(positions) else len(content)
        sections[key] = content[start:end].strip().rstrip("-").strip()
    return sections


def copy_btn(text: str, uid: str):
    safe = json.dumps(text)
    bid  = f"cbtn_{uid}"
    components.html(f"""
    <button id="{bid}"
        onclick="
            var t={safe};
            var b=document.getElementById('{bid}');
            if(navigator.clipboard&&navigator.clipboard.writeText){{
                navigator.clipboard.writeText(t).then(function(){{
                    b.innerHTML='✅ הועתק!';b.style.background='#4CAF50';
                    setTimeout(function(){{b.innerHTML='📋 העתק';b.style.background='#6c63ff';}},2000);
                }});
            }}else{{
                var e=document.createElement('textarea');e.value=t;
                e.style.position='fixed';e.style.opacity='0';
                document.body.appendChild(e);e.select();
                document.execCommand('copy');document.body.removeChild(e);
                b.innerHTML='✅ הועתק!';
                setTimeout(function(){{b.innerHTML='📋 העתק';}},2000);
            }}
        "
        style="background:#6c63ff;color:white;border:none;padding:4px 12px;
               border-radius:6px;cursor:pointer;font-size:12px;font-family:Arial;"
    >📋 העתק</button>
    """, height=32, scrolling=False)


def format_date(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return iso_str


# =============================================================
# PAGE HEADER
# =============================================================
st.markdown("# 📚 ספריית תוכן")
st.markdown("כל התכנים שאושרו ונשמרו — מוכנים לשימוש חוזר בכל עת.")
st.divider()

# =============================================================
# LOAD DATA
# =============================================================
all_items = load_library()
brands    = load_brands()

# =============================================================
# FILTER BAR
# =============================================================
stats = get_library_stats()
col_stat1, col_stat2, col_stat3 = st.columns(3)
col_stat1.metric("סה״כ פריטים שמורים", stats["total"])
col_stat2.metric("מותגים עם תוכן",     stats["brands"])
col_stat3.metric("זמינים לשימוש",      stats["total"])

st.markdown("")

f1, f2, f3, f4 = st.columns([3, 2, 2, 2])

with f1:
    search_term = st.text_input(
        "🔍 חיפוש",
        placeholder="חפש לפי בריף, מותג, תוכן...",
        label_visibility="collapsed",
    )

# Brand filter
brand_options = {"all": "📋 כל המותגים"}
for k, v in brands.items():
    brand_options[k] = f"{v.get('emoji','🏢')} {v.get('name', k)}"

with f2:
    filter_brand = st.selectbox(
        "מותג", options=list(brand_options.keys()),
        format_func=lambda x: brand_options[x],
        label_visibility="collapsed",
    )

# Platform filter
platform_options = {
    "all":       "📡 כל הפלטפורמות",
    "Instagram": "📸 Instagram",
    "TikTok":    "🎵 TikTok",
    "Facebook":  "👥 Facebook",
}
with f3:
    filter_platform = st.selectbox(
        "פלטפורמה", options=list(platform_options.keys()),
        format_func=lambda x: platform_options[x],
        label_visibility="collapsed",
    )

# Sort
with f4:
    sort_order = st.selectbox(
        "מיון", options=["newest", "oldest"],
        format_func=lambda x: "🆕 החדש ביותר" if x == "newest" else "🕰️ הישן ביותר",
        label_visibility="collapsed",
    )

st.divider()

# =============================================================
# FILTER & SORT ITEMS
# =============================================================
filtered = all_items[:]

if filter_brand != "all":
    filtered = [i for i in filtered if i.get("brand_key") == filter_brand]

if filter_platform != "all":
    filtered = [
        i for i in filtered
        if filter_platform.lower() in i.get("platform", "").lower()
    ]

if search_term.strip():
    q = search_term.strip().lower()
    filtered = [
        i for i in filtered
        if q in i.get("brief", "").lower()
        or q in i.get("content", "").lower()
        or q in i.get("brand_name", "").lower()
        or q in i.get("content_type", "").lower()
    ]

if sort_order == "oldest":
    filtered = list(reversed(filtered))

# =============================================================
# EMPTY STATE
# =============================================================
if not filtered:
    if not all_items:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:60px;margin-bottom:16px;">📚</div>
            <div style="font-size:20px;color:#888;font-weight:600;">הספרייה ריקה</div>
            <div style="font-size:14px;color:#bbb;margin-top:10px;direction:rtl;">
                צור תוכן בדף הראשי → אשר אותו → לחץ "שמור לספריית התוכן"
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("לא נמצאו פריטים התואמים לסינון הנוכחי.")
    st.stop()

# =============================================================
# CONTENT CARDS
# =============================================================
st.markdown(f"**{len(filtered)} פריטים**")

for item in filtered:
    item_id = item.get("id", "")
    emoji   = item.get("brand_emoji", "🏢")
    bname   = item.get("brand_name", "")
    plat    = item.get("platform", "")
    ctype   = item.get("content_type", "")
    brief   = item.get("brief", "")
    content = item.get("content", "")
    saved   = format_date(item.get("saved_at", ""))
    notes   = item.get("notes", "")

    card_label = f"{emoji} {bname} · {plat} · {ctype}"

    with st.expander(f"{card_label}  —  {saved}", expanded=False):

        # Meta row
        st.markdown(
            f'<div class="card-meta">📅 נשמר: {saved} &nbsp;|&nbsp; '
            f'📡 {plat} &nbsp;|&nbsp; 📄 {ctype}</div>',
            unsafe_allow_html=True,
        )

        # Brief
        if brief:
            safe_brief = html_lib.escape(brief)
            st.markdown(
                f'<div class="card-brief">💡 {safe_brief}</div>',
                unsafe_allow_html=True,
            )

        # Parsed sections
        sections = parse_sections(content)

        if sections:
            for key, sec_emoji, title in SECTION_CONFIG:
                text = sections.get(key, "")
                if not text:
                    continue

                col_t, col_b = st.columns([7, 2])
                with col_t:
                    st.markdown(
                        f'<div class="section-label">{sec_emoji} {title}</div>',
                        unsafe_allow_html=True,
                    )
                with col_b:
                    copy_btn(text, uid=f"{item_id}_{key}")

                css = "section-box-img" if key == "image_prompt" else "section-box"
                safe_text = html_lib.escape(text)
                st.markdown(
                    f'<div class="{css}">{safe_text}</div>',
                    unsafe_allow_html=True,
                )
        else:
            # Fallback: show raw content
            safe_content = html_lib.escape(content)
            st.markdown(
                f'<div class="section-box">{safe_content}</div>',
                unsafe_allow_html=True,
            )

        # Copy all button
        st.markdown("")
        copy_btn(content, uid=f"{item_id}_all")
        st.caption("^ העתק תוכן מלא")

        # Notes
        st.markdown("")
        new_notes = st.text_area(
            "📝 הערות אישיות",
            value=notes,
            placeholder="לדוגמה: השתמשנו בזה ב-03/03, קיבל 200 לייקים...",
            height=70,
            key=f"notes_{item_id}",
            label_visibility="visible",
        )
        nc1, nc2 = st.columns([2, 1])
        with nc1:
            if st.button("💾 שמור הערה", key=f"save_notes_{item_id}"):
                update_notes(item_id, new_notes)
                st.success("✅ הערה נשמרה!")
        with nc2:
            if st.button("🗑️ מחק פריט", key=f"del_{item_id}"):
                delete_from_library(item_id)
                st.rerun()

# =============================================================
# FOOTER
# =============================================================
st.divider()
st.caption(f"📚 ספריית תוכן · {len(all_items)} פריטים שמורים · Marketing Hub")
