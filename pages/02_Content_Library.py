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
from translations import get_t, get_section_config

st.set_page_config(
    page_title="📚 Content Library",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================
# LANGUAGE SETUP
# =============================================================
if "lang" not in st.session_state:
    st.session_state.lang = "he"

lang = st.session_state.lang
t    = get_t(lang)
D    = t["dir"]
A    = t["align"]

SECTION_CONFIG = get_section_config(lang)

# =============================================================
# LANGUAGE TOGGLE — sidebar
# =============================================================
with st.sidebar:
    st.markdown("---")
    lc = st.radio(
        t["lang_toggle_label"],
        options=["עב", "EN"],
        index=0 if lang == "he" else 1,
        horizontal=True,
        key="cl_lang_radio",
        label_visibility="visible",
    )
    new_lang = "he" if lc == "עב" else "en"
    if new_lang != lang:
        st.session_state.lang = new_lang
        st.rerun()

# =============================================================
# STYLING
# UI chrome follows language direction; content boxes always RTL
# =============================================================
st.markdown(f"""
<style>
    label,
    .stCaption p,
    [data-testid="stMarkdownContainer"] p {{
        direction: {D} !important;
        text-align: {A} !important;
    }}
    [data-testid="stMainBlockContainer"] h1,
    [data-testid="stMainBlockContainer"] h2,
    [data-testid="stMainBlockContainer"] h3 {{
        direction: {D}; text-align: {A};
    }}
    [data-testid="stAlert"] {{ direction: {D}; text-align: {A}; }}

    .content-card {{
        background: #fafbff;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 14px;
        border-right: 4px solid #6c63ff;
        direction: {D};
        text-align: {A};
    }}
    .card-meta {{
        font-size: 12px;
        color: #999;
        direction: {D};
        text-align: {A};
        margin-bottom: 8px;
    }}
    .card-brief {{
        font-size: 14px;
        color: #555;
        background: #f0f2ff;
        padding: 8px 12px;
        border-radius: 8px;
        direction: {D};
        text-align: {A};
        margin-bottom: 10px;
        font-style: italic;
    }}
    .section-label {{
        font-size: 13px;
        font-weight: 700;
        color: #4a4a8a;
        direction: {D};
        text-align: {A};
        margin: 10px 0 4px 0;
    }}
    /* Generated content ALWAYS RTL — content is Hebrew */
    .section-box {{
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
    }}
    /* Image prompts always LTR (English) */
    .section-box-img {{
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
    }}
    .empty-state {{
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
    }}
    footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# =============================================================
# HELPERS
# =============================================================
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


def copy_btn(text: str, uid: str, copy_label: str = "📋 העתק", copied_label: str = "✅ הועתק!"):
    safe = json.dumps(text)
    cl   = json.dumps(copy_label)
    cpl  = json.dumps(copied_label)
    bid  = f"cbtn_{uid}"
    components.html(f"""
    <button id="{bid}"
        onclick="
            var t={safe};
            var cl={cl};
            var cpl={cpl};
            var b=document.getElementById('{bid}');
            if(navigator.clipboard&&navigator.clipboard.writeText){{
                navigator.clipboard.writeText(t).then(function(){{
                    b.innerHTML=cpl;b.style.background='#4CAF50';
                    setTimeout(function(){{b.innerHTML=cl;b.style.background='#6c63ff';}},2000);
                }});
            }}else{{
                var e=document.createElement('textarea');e.value=t;
                e.style.position='fixed';e.style.opacity='0';
                document.body.appendChild(e);e.select();
                document.execCommand('copy');document.body.removeChild(e);
                b.innerHTML=cpl;
                setTimeout(function(){{b.innerHTML=cl;}},2000);
            }}
        "
        style="background:#6c63ff;color:white;border:none;padding:4px 12px;
               border-radius:6px;cursor:pointer;font-size:12px;font-family:Arial;"
    >{copy_label}</button>
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
st.markdown(f"# {t['cl_title']}")
st.markdown(t["cl_subtitle"])
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
col_stat1.metric(t["cl_total_metric"],     stats["total"])
col_stat2.metric(t["cl_brands_metric"],    stats["brands"])
col_stat3.metric(t["cl_available_metric"], stats["total"])

st.markdown("")

f1, f2, f3, f4 = st.columns([3, 2, 2, 2])

with f1:
    search_term = st.text_input(
        "🔍",
        placeholder=t["cl_search_placeholder"],
        label_visibility="collapsed",
    )

# Brand filter
brand_options = {"all": t["cl_all_brands"]}
for k, v in brands.items():
    brand_options[k] = f"{v.get('emoji','🏢')} {v.get('name', k)}"

with f2:
    filter_brand = st.selectbox(
        "brand", options=list(brand_options.keys()),
        format_func=lambda x: brand_options[x],
        label_visibility="collapsed",
    )

# Platform filter
platform_options = {
    "all":       t["cl_all_platforms"],
    "Instagram": "📸 Instagram",
    "TikTok":    "🎵 TikTok",
    "Facebook":  "👥 Facebook",
}
with f3:
    filter_platform = st.selectbox(
        "platform", options=list(platform_options.keys()),
        format_func=lambda x: platform_options[x],
        label_visibility="collapsed",
    )

# Sort
with f4:
    sort_order = st.selectbox(
        "sort", options=["newest", "oldest"],
        format_func=lambda x: t["cl_newest"] if x == "newest" else t["cl_oldest"],
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
        st.markdown(f"""
        <div class="empty-state">
            <div style="font-size:60px;margin-bottom:16px;">📚</div>
            <div style="font-size:20px;color:#888;font-weight:600;">{t['cl_empty_title']}</div>
            <div style="font-size:14px;color:#bbb;margin-top:10px;direction:{D};">
                {t['cl_empty_sub']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(t["cl_no_filter_match"])
    st.stop()

# =============================================================
# CONTENT CARDS
# =============================================================
st.markdown(f"**{t['cl_items_count'].format(n=len(filtered))}**")

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
            f'<div class="card-meta">{t["cl_saved_label"]} {saved} &nbsp;|&nbsp; '
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
                    copy_btn(
                        text,
                        uid=f"{item_id}_{key}",
                        copy_label=t["cl_copy_btn"],
                        copied_label=t["cl_copied_btn"],
                    )

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
        copy_btn(
            content,
            uid=f"{item_id}_all",
            copy_label=t["cl_copy_btn"],
            copied_label=t["cl_copied_btn"],
        )
        st.caption(t["cl_copy_full_caption"])

        # Notes
        st.markdown("")
        new_notes = st.text_area(
            t["cl_notes_label"],
            value=notes,
            placeholder=t["cl_notes_placeholder"],
            height=70,
            key=f"notes_{item_id}",
            label_visibility="visible",
        )
        nc1, nc2 = st.columns([2, 1])
        with nc1:
            if st.button(t["cl_save_notes_btn"], key=f"save_notes_{item_id}"):
                update_notes(item_id, new_notes)
                st.success(t["cl_notes_saved"])
        with nc2:
            if st.button(t["cl_delete_btn"], key=f"del_{item_id}"):
                delete_from_library(item_id)
                st.rerun()

# =============================================================
# FOOTER
# =============================================================
st.divider()
st.caption(t["cl_footer"].format(n=len(all_items)))
