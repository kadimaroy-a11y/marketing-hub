# =============================================================
# 🏢 BRAND MANAGER — Add, edit and grow brand knowledge
# =============================================================
import sys
import os
import copy
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from db import (
    load_brands, save_brand, save_brands, delete_brand,
    brand_key_from_name, get_brand_with_defaults, EMPTY_BRAND
)
import importlib, sys
if "translations" in sys.modules:
    importlib.reload(sys.modules["translations"])
from translations import get_t

st.set_page_config(
    page_title="🏢 Brand Manager",
    page_icon="🏢",
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

# =============================================================
# LANGUAGE TOGGLE — sidebar
# =============================================================
with st.sidebar:
    st.markdown("---")
    lc = st.radio(
        t.get("lang_toggle_label", "🌐"),
        options=["עב", "EN"],
        index=0 if lang == "he" else 1,
        horizontal=True,
        key="bm_lang_radio",
        label_visibility="visible",
    )
    new_lang = "he" if lc == "עב" else "en"
    if new_lang != lang:
        st.session_state.lang = new_lang
        st.rerun()

# =============================================================
# STYLING  (direction follows language; content boxes stay RTL)
# =============================================================
st.markdown(f"""
<style>
    textarea, input[type="text"] {{
        direction: {D} !important;
        text-align: {A} !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }}
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
    [data-testid="stExpander"] summary {{ direction: {D}; text-align: {A}; }}

    .brand-card {{
        background: #f4f4fb;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-right: 4px solid #6c63ff;
        direction: {D};
        text-align: {A};
    }}
    .kb-section {{
        background: #f0fff4;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-right: 4px solid #4CAF50;
    }}
    .danger-zone {{
        background: #fff5f5;
        border-radius: 10px;
        padding: 14px 18px;
        border: 1px solid #ffcccc;
    }}
    footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# =============================================================
# SESSION STATE
# =============================================================
if "bm_selected_key"   not in st.session_state: st.session_state.bm_selected_key   = None
if "bm_creating_new"   not in st.session_state: st.session_state.bm_creating_new   = False
if "bm_delete_confirm" not in st.session_state: st.session_state.bm_delete_confirm = False
if "bm_save_ok"        not in st.session_state: st.session_state.bm_save_ok        = False
if "bm_ev_add_ctr"     not in st.session_state: st.session_state.bm_ev_add_ctr     = 0


# =============================================================
# HELPERS
# =============================================================
def list_to_text(lst: list) -> str:
    return "\n".join(lst) if lst else ""


def text_to_list(text: str) -> list:
    return [x.strip() for x in text.split("\n") if x.strip()]


def sv(key, fallback=""):
    return st.session_state.get(key, fallback)


def sl(key, fallback=None):
    val = st.session_state.get(key, None)
    if val is None:
        return fallback or []
    return text_to_list(val)


def _autosave_events(sk: str, ev_data: dict):
    """Persist ev_data to brands_db.json immediately (no Save button needed)."""
    scheduled_events = {}
    for m_str, m_evs in (ev_data or {}).items():
        saved = [{"text": e["text"].strip(), "active": e.get("active", True)}
                 for e in m_evs if e.get("text", "").strip()]
        if saved:
            scheduled_events[m_str] = saved
    all_brands = load_brands()
    if sk in all_brands:
        all_brands[sk]["scheduled_events"] = scheduled_events
        save_brands(all_brands)


def _on_ev_checkbox_change(sk: str, ev_state_key: str, month_str: str, ev_idx: int, ck: str):
    """Called by st.checkbox on_change — syncs new active value and auto-saves."""
    ev_data = st.session_state.get(ev_state_key) or {}
    new_val = st.session_state.get(ck, True)
    if month_str in ev_data and ev_idx < len(ev_data[month_str]):
        ev_data[month_str][ev_idx]["active"] = new_val
    _autosave_events(sk, ev_data)


def collect_brand_from_form(sk: str, current: dict) -> dict:
    c  = current
    ca = c.get("audience", {})
    cv = c.get("voice", {})
    cp = c.get("platforms", {})
    ck = c.get("knowledge_base", {})

    def plat(p):
        return cp.get(p, {})

    return {
        "name":              sv(f"{sk}_name",    c.get("name", "")),
        "hebrew_name":       sv(f"{sk}_hname",   c.get("hebrew_name", "")),
        "emoji":             sv(f"{sk}_emoji",   c.get("emoji", "🏢")),
        "type":              sv(f"{sk}_type",    c.get("type", "")),
        "parent_company":    sv(f"{sk}_parent",  c.get("parent_company", "")),
        "website":           sv(f"{sk}_website", c.get("website", "")),
        "language":          sv(f"{sk}_lang",    c.get("language", "עברית")),
        "posting_frequency": sv(f"{sk}_freq",    c.get("posting_frequency", "")),
        "products":          sl(f"{sk}_products", c.get("products", [])),
        "usp":               sl(f"{sk}_usp",      c.get("usp", [])),
        "content_that_works":sl(f"{sk}_ctw",      c.get("content_that_works", [])),
        "content_to_avoid":  sl(f"{sk}_cta",      c.get("content_to_avoid", [])),
        "audience": {
            "age":           sv(f"{sk}_aud_age",    ca.get("age", "")),
            "gender":        sv(f"{sk}_aud_gender",  ca.get("gender", "")),
            "interests":     sl(f"{sk}_aud_int",     ca.get("interests", [])),
            "psychographic": sv(f"{sk}_aud_psycho",  ca.get("psychographic", "")),
            "motivation":    sv(f"{sk}_aud_motiv",   ca.get("motivation", "")),
        },
        "voice": {
            "tone":           sv(f"{sk}_v_tone",  cv.get("tone", "")),
            "style":          sv(f"{sk}_v_style", cv.get("style", "")),
            "language_notes": sv(f"{sk}_v_lang",  cv.get("language_notes", "")),
            "do":             sl(f"{sk}_v_do",    cv.get("do", [])),
            "dont":           sl(f"{sk}_v_dont",  cv.get("dont", [])),
        },
        "platforms": {
            "instagram": {
                "priority":      sv(f"{sk}_ig_pri",     plat("instagram").get("priority", "primary")),
                "content_types": sl(f"{sk}_ig_types",   plat("instagram").get("content_types", [])),
                "caption_length":sv(f"{sk}_ig_cap",     plat("instagram").get("caption_length", "")),
                "hashtag_count": sv(f"{sk}_ig_hash",    plat("instagram").get("hashtag_count", "")),
            },
            "tiktok": {
                "priority":      sv(f"{sk}_tt_pri",     plat("tiktok").get("priority", "secondary")),
                "content_types": sl(f"{sk}_tt_types",   plat("tiktok").get("content_types", [])),
                "caption_length":sv(f"{sk}_tt_cap",     plat("tiktok").get("caption_length", "")),
                "hashtag_count": sv(f"{sk}_tt_hash",    plat("tiktok").get("hashtag_count", "")),
            },
            "facebook": {
                "priority":      sv(f"{sk}_fb_pri",     plat("facebook").get("priority", "secondary")),
                "content_types": sl(f"{sk}_fb_types",   plat("facebook").get("content_types", [])),
                "caption_length":sv(f"{sk}_fb_cap",     plat("facebook").get("caption_length", "")),
                "hashtag_count": sv(f"{sk}_fb_hash",    plat("facebook").get("hashtag_count", "")),
            },
        },
        "knowledge_base": {
            "what_works":        sl(f"{sk}_kb_works",    ck.get("what_works", [])),
            "what_doesnt":       sl(f"{sk}_kb_doesnt",   ck.get("what_doesnt", [])),
            "competitors":       sl(f"{sk}_kb_comp",     ck.get("competitors", [])),
            "news_sources":      sl(f"{sk}_kb_news",     ck.get("news_sources", [])),
            "learning_links":    sl(f"{sk}_kb_links",    ck.get("learning_links", [])),
            "team_notes":        sl(f"{sk}_kb_notes",    ck.get("team_notes", [])),
            "approved_hashtags": sl(f"{sk}_kb_hashtags", ck.get("approved_hashtags", [])),
        },
    }


# =============================================================
# PAGE HEADER
# =============================================================
st.markdown(f"# {t['bm_title']}")
st.markdown(t["bm_subtitle"])
st.divider()

# =============================================================
# BRAND SELECTION BAR
# =============================================================
brands = load_brands()

col_sel, col_new = st.columns([7, 2])

with col_sel:
    if brands:
        brand_options = {
            k: f"{v.get('emoji','🏢')} {v.get('name', k)}"
            for k, v in brands.items()
        }
        if st.session_state.bm_selected_key not in brands:
            st.session_state.bm_selected_key = list(brands.keys())[0]

        chosen_key = st.selectbox(
            t["bm_tab_basic"],
            options=list(brand_options.keys()),
            format_func=lambda x: brand_options[x],
            index=list(brand_options.keys()).index(st.session_state.bm_selected_key),
            label_visibility="collapsed",
        )
        if chosen_key != st.session_state.bm_selected_key:
            old_src_key = f"{st.session_state.bm_selected_key}_src_list"
            st.session_state.pop(old_src_key, None)
            st.session_state.bm_selected_key   = chosen_key
            st.session_state.bm_delete_confirm = False
            st.session_state.bm_save_ok        = False
            st.rerun()
    else:
        st.info(t["bm_no_brands_info"])
        st.session_state.bm_selected_key = None

with col_new:
    if st.button(t["bm_new_brand_btn"], use_container_width=True, type="primary"):
        st.session_state.bm_creating_new   = True
        st.session_state.bm_delete_confirm = False
        st.session_state.bm_save_ok        = False
        st.rerun()

# =============================================================
# NEW BRAND CREATION FORM
# =============================================================
if st.session_state.bm_creating_new:
    st.markdown("---")
    st.markdown(f"### {t['bm_new_brand_title']}")
    with st.container(border=True):
        nc1, nc2, nc3 = st.columns([4, 3, 1])
        with nc1:
            new_name = st.text_input(
                t["bm_brand_name_en_label"],
                placeholder="My Brand",
                key="new_brand_name",
            )
        with nc2:
            new_hname = st.text_input(
                t["bm_brand_hname_label"],
                placeholder="המותג שלי",
                key="new_brand_hname",
            )
        with nc3:
            new_emoji = st.text_input(
                t["bm_emoji_label"],
                value="🏢",
                key="new_brand_emoji",
                max_chars=4,
            )

        new_type = st.text_input(
            t["bm_type_cat_label"],
            placeholder=t["bm_type_placeholder"],
            key="new_brand_type",
        )

        cb1, cb2 = st.columns(2)
        with cb1:
            if st.button(t["bm_create_btn"], type="primary", use_container_width=True):
                if new_name.strip():
                    new_key = brand_key_from_name(new_name.strip())
                    if new_key in brands:
                        st.error(t["bm_brand_exists_err"].format(key=new_key))
                    else:
                        import copy
                        fresh = copy.deepcopy(EMPTY_BRAND)
                        fresh["name"]        = new_name.strip()
                        fresh["hebrew_name"] = new_hname.strip()
                        fresh["emoji"]       = new_emoji.strip() or "🏢"
                        fresh["type"]        = new_type.strip()
                        save_brand(new_key, fresh)
                        st.session_state.bm_selected_key = new_key
                        st.session_state.bm_creating_new = False
                        st.rerun()
                else:
                    st.warning(t["bm_brand_name_warning"])
        with cb2:
            if st.button(t["bm_cancel_btn"], use_container_width=True):
                st.session_state.bm_creating_new = False
                st.rerun()
    st.markdown("---")

# =============================================================
# BRAND EDITOR
# =============================================================
if st.session_state.bm_selected_key and not st.session_state.bm_creating_new:
    brands = load_brands()
    sk = st.session_state.bm_selected_key

    if sk not in brands:
        st.error(t["bm_not_found_err"])
        st.stop()

    brand = get_brand_with_defaults(brands[sk])

    aud  = brand["audience"]
    voc  = brand["voice"]
    plat = brand["platforms"]
    kb   = brand["knowledge_base"]

    st.markdown(
        f"## {brand['emoji']} {brand['name']}  "
        f"<span style='font-size:14px; color:#999;'>({sk})</span>",
        unsafe_allow_html=True,
    )

    if st.session_state.bm_save_ok:
        st.success(t["bm_save_ok_msg"])
        st.session_state.bm_save_ok = False

    # ── TABS ─────────────────────────────────────────────────
    tabs = st.tabs([
        t["bm_tab_basic"],
        t["bm_tab_products"],
        t["bm_tab_audience"],
        t["bm_tab_voice"],
        t["bm_tab_platforms"],
        t["bm_tab_kb"],
        t["bm_tab_web"],
        t["bm_tab_events"],
    ])

    # ════════════════════════════════════════════════════════
    # TAB 1: Basic Info
    # ════════════════════════════════════════════════════════
    with tabs[0]:
        st.markdown(t["bm_basic_header"])
        r1c1, r1c2, r1c3 = st.columns([4, 3, 1])
        with r1c1:
            st.text_input(t["bm_name_label"],  value=brand["name"],        key=f"{sk}_name")
        with r1c2:
            st.text_input(t["bm_hname_label"], value=brand["hebrew_name"], key=f"{sk}_hname")
        with r1c3:
            st.text_input(t["bm_emoji_label"], value=brand["emoji"],       key=f"{sk}_emoji", max_chars=4)

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.text_input(t["bm_type_label"],   value=brand["type"],              key=f"{sk}_type")
            st.text_input(t["bm_parent_label"], value=brand["parent_company"],    key=f"{sk}_parent")
        with r2c2:
            st.text_input(t["bm_website_label"],value=brand["website"],           key=f"{sk}_website")
            st.text_input(t["bm_freq_label"],   value=brand["posting_frequency"], key=f"{sk}_freq")

        st.text_input(t["bm_content_lang_label"], value=brand["language"], key=f"{sk}_lang")

    # ════════════════════════════════════════════════════════
    # TAB 2: Products & Positioning
    # ════════════════════════════════════════════════════════
    with tabs[1]:
        st.markdown(t["bm_products_header"])
        p1, p2 = st.columns(2)
        with p1:
            st.markdown(t["bm_products_list_label"])
            st.text_area("", value=list_to_text(brand["products"]),
                         height=180, label_visibility="collapsed", key=f"{sk}_products")

            st.markdown(t["bm_ctw_label"])
            st.text_area("", value=list_to_text(brand["content_that_works"]),
                         height=130, label_visibility="collapsed", key=f"{sk}_ctw")
        with p2:
            st.markdown(t["bm_usp_label"])
            st.text_area("", value=list_to_text(brand["usp"]),
                         height=180, label_visibility="collapsed", key=f"{sk}_usp")

            st.markdown(t["bm_cta_label"])
            st.text_area("", value=list_to_text(brand["content_to_avoid"]),
                         height=130, label_visibility="collapsed", key=f"{sk}_cta")

    # ════════════════════════════════════════════════════════
    # TAB 3: Audience
    # ════════════════════════════════════════════════════════
    with tabs[2]:
        st.markdown(t["bm_audience_header"])
        a1, a2 = st.columns(2)
        with a1:
            st.text_input(t["bm_age_label"],    value=aud["age"],    key=f"{sk}_aud_age")
            st.text_input(t["bm_gender_label"], value=aud["gender"], key=f"{sk}_aud_gender")
            st.markdown(t["bm_interests_label"])
            st.text_area("", value=list_to_text(aud["interests"]),
                         height=150, label_visibility="collapsed", key=f"{sk}_aud_int")
        with a2:
            st.markdown(t["bm_psycho_label"])
            st.text_area("", value=aud["psychographic"],
                         height=150, label_visibility="collapsed", key=f"{sk}_aud_psycho")
            st.markdown(t["bm_motiv_label"])
            st.text_area("", value=aud["motivation"],
                         height=130, label_visibility="collapsed", key=f"{sk}_aud_motiv")

    # ════════════════════════════════════════════════════════
    # TAB 4: Voice & Tone
    # ════════════════════════════════════════════════════════
    with tabs[3]:
        st.markdown(t["bm_voice_header"])
        v1, v2 = st.columns(2)
        with v1:
            st.markdown(t["bm_tone_label"])
            st.text_input("",  value=voc["tone"],           label_visibility="collapsed", key=f"{sk}_v_tone")
            st.markdown(t["bm_style_label"])
            st.text_area("",   value=voc["style"],          height=110, label_visibility="collapsed", key=f"{sk}_v_style")
            st.markdown(t["bm_lang_notes_label"])
            st.text_area("",   value=voc["language_notes"], height=110, label_visibility="collapsed", key=f"{sk}_v_lang")
        with v2:
            st.markdown(t["bm_do_label"])
            st.text_area("",   value=list_to_text(voc["do"]),   height=160, label_visibility="collapsed", key=f"{sk}_v_do")
            st.markdown(t["bm_dont_label"])
            st.text_area("",   value=list_to_text(voc["dont"]), height=160, label_visibility="collapsed", key=f"{sk}_v_dont")

    # ════════════════════════════════════════════════════════
    # TAB 5: Platforms
    # ════════════════════════════════════════════════════════
    with tabs[4]:
        st.markdown(t["bm_platforms_header"])
        PRIORITY_OPTIONS = ["primary", "secondary", "disabled"]
        pri_labels = {
            "primary":   t["bm_pri_primary"],
            "secondary": t["bm_pri_secondary"],
            "disabled":  t["bm_pri_disabled"],
        }

        for plat_key, plat_label, plat_emoji in [
            ("instagram", "Instagram", "📸"),
            ("tiktok",    "TikTok",    "🎵"),
            ("facebook",  "Facebook",  "👥"),
        ]:
            pd = plat.get(plat_key, {})
            with st.expander(f"{plat_emoji} {plat_label}", expanded=(pd.get("priority") == "primary")):
                pp1, pp2, pp3 = st.columns([2, 3, 2])
                with pp1:
                    pri_idx = PRIORITY_OPTIONS.index(pd.get("priority", "secondary")) \
                              if pd.get("priority") in PRIORITY_OPTIONS else 1
                    st.selectbox(
                        t["bm_priority_label"],
                        PRIORITY_OPTIONS,
                        index=pri_idx,
                        key=f"{sk}_{plat_key[:2]}_pri",
                        format_func=lambda x: pri_labels[x],
                    )
                    st.text_input(t["bm_hashtag_count_label"], value=pd.get("hashtag_count", ""),
                                  key=f"{sk}_{plat_key[:2]}_hash")
                with pp2:
                    st.markdown(t["bm_content_types_label"])
                    st.text_area("", value=list_to_text(pd.get("content_types", [])),
                                 height=100, label_visibility="collapsed",
                                 key=f"{sk}_{plat_key[:2]}_types")
                with pp3:
                    st.text_input(t["bm_caption_length_label"], value=pd.get("caption_length", ""),
                                  key=f"{sk}_{plat_key[:2]}_cap")

    # ════════════════════════════════════════════════════════
    # TAB 6: Knowledge Base 🧠
    # ════════════════════════════════════════════════════════
    with tabs[5]:
        st.markdown(t["bm_kb_header"])
        st.caption(t["bm_kb_caption"])

        st.markdown('<div class="kb-section">', unsafe_allow_html=True)

        kb1, kb2 = st.columns(2)

        with kb1:
            st.markdown(t["bm_kb_works_label"])
            st.text_area(
                "", value=list_to_text(kb["what_works"]), height=110,
                placeholder="לדוגמה: ריילס עם מוזיקה מקבלים 3x יותר reach",
                label_visibility="collapsed", key=f"{sk}_kb_works",
            )
            st.markdown(t["bm_kb_comp_label"])
            st.text_area(
                "", value=list_to_text(kb["competitors"]), height=90,
                placeholder="לדוגמה: kuma-toys.co.il",
                label_visibility="collapsed", key=f"{sk}_kb_comp",
            )
            st.markdown(t["bm_kb_links_label"])
            st.text_area(
                "", value=list_to_text(kb["learning_links"]), height=90,
                placeholder="לדוגמה: https://www.funko.com/news",
                label_visibility="collapsed", key=f"{sk}_kb_links",
            )
            st.markdown(t["bm_kb_hashtags_label"])
            st.text_area(
                "", value=list_to_text(kb["approved_hashtags"]), height=90,
                placeholder="לדוגמה: מיסט\nפופקאלצ'ר\nFunkoPop",
                label_visibility="collapsed", key=f"{sk}_kb_hashtags",
            )

        with kb2:
            st.markdown(t["bm_kb_doesnt_label"])
            st.text_area(
                "", value=list_to_text(kb["what_doesnt"]), height=110,
                placeholder="לדוגמה: פוסטי טקסט בלי תמונה — כמעט אפס engagement",
                label_visibility="collapsed", key=f"{sk}_kb_doesnt",
            )
            st.markdown(t["bm_kb_news_label"])
            st.text_area(
                "", value=list_to_text(kb["news_sources"]), height=90,
                placeholder="לדוגמה: ign.com\nkotaku.com\nmarvel.com/news",
                label_visibility="collapsed", key=f"{sk}_kb_news",
            )
            st.markdown(t["bm_kb_notes_label"])
            st.text_area(
                "", value=list_to_text(kb["team_notes"]), height=170,
                placeholder="לדוגמה: אל תפרסמו ביום שישי אחה\"צ",
                label_visibility="collapsed", key=f"{sk}_kb_notes",
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # TAB 7: Web Sources 🌐
    # ════════════════════════════════════════════════════════
    with tabs[6]:
        st.markdown(t["bm_web_header"])
        st.caption(t["bm_web_caption"])

        src_key = f"{sk}_src_list"
        if src_key not in st.session_state:
            import copy
            st.session_state[src_key] = copy.deepcopy(brand.get("web_sources", []))

        sources_list = st.session_state[src_key]

        if not sources_list:
            st.info(t["bm_no_sources"])

        for i, src in enumerate(sources_list):
            active_icon = "✅" if src.get("active", True) else "⏸️"
            src_default = t["bm_src_default"].format(i=i + 1)
            label       = src.get("name") or src.get("url") or src_default
            with st.expander(f"{active_icon} {label}", expanded=not src.get("url")):

                row1c1, row1c2 = st.columns([1, 6])
                with row1c1:
                    st.checkbox(
                        t["bm_src_active_label"], value=src.get("active", True),
                        key=f"{sk}_src_{i}_active",
                    )
                with row1c2:
                    st.text_input(
                        t["bm_src_name_label"], value=src.get("name", ""),
                        placeholder=t["bm_src_name_placeholder"],
                        key=f"{sk}_src_{i}_name",
                    )

                st.text_input(
                    "🔗 URL", value=src.get("url", ""),
                    placeholder="https://myst.co.il",
                    key=f"{sk}_src_{i}_url",
                )

                fc1, fc2 = st.columns(2)
                with fc1:
                    st.text_input(
                        t["bm_src_focus_label"],
                        value=src.get("focus", ""),
                        placeholder=t["bm_src_focus_placeholder"],
                        key=f"{sk}_src_{i}_focus",
                    )
                with fc2:
                    st.text_input(
                        t["bm_src_ignore_label"],
                        value=src.get("ignore", ""),
                        placeholder=t["bm_src_ignore_placeholder"],
                        key=f"{sk}_src_{i}_ignore",
                    )

                if st.button(t["bm_src_delete_btn"], key=f"{sk}_src_{i}_del"):
                    sources_list.pop(i)
                    st.rerun()

        st.markdown("")
        if st.button(t["bm_add_source_btn"], use_container_width=True):
            sources_list.append({
                "active": True, "name": "", "url": "", "focus": "", "ignore": "",
            })
            st.rerun()

        with st.expander(t["bm_tips_sources_expander"]):
            st.markdown(t["bm_tips_sources_table"])

    # ════════════════════════════════════════════════════════
    # TAB 8: Scheduled Events 📅
    # ════════════════════════════════════════════════════════
    with tabs[7]:
        st.markdown(t["bm_events_header"])
        st.caption(t["bm_events_caption"])

        current_month_num = datetime.now().month
        ev_state_key = f"{sk}_ev_data"
        if ev_state_key not in st.session_state:
            # use `or {}` to guard against null/None in the DB
            st.session_state[ev_state_key] = copy.deepcopy(
                brand.get("scheduled_events") or {}
            )
        ev_data = st.session_state[ev_state_key] or {}

        st.caption("✅ אירועים נשמרים אוטומטית — אין צורך ללחוץ שמור.")
        months  = t["bm_months"]   # list of 12 month names

        for row_start in range(0, 12, 3):
            cols = st.columns(3)
            for col_idx in range(3):
                month_num  = row_start + col_idx + 1
                month_str  = str(month_num)
                month_name = months[month_num - 1]
                is_current = (month_num == current_month_num)

                with cols[col_idx]:
                    with st.container(border=True):
                        # Month header
                        if is_current:
                            st.markdown(
                                f"**📅 {month_name}** &nbsp;"
                                f"<span style='color:#4CAF50;font-size:11px;'>"
                                f"{t['bm_events_current_badge']}</span>",
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(f"**📅 {month_name}**")

                        # Existing events
                        month_events = ev_data.get(month_str, [])
                        if not month_events:
                            st.caption(t["bm_events_no_events"])

                        del_triggered = None
                        for ev_idx, event in enumerate(month_events):
                            ev_col, del_col = st.columns([5, 1])
                            ck = f"{sk}_ev_{month_str}_{ev_idx}_active"
                            with ev_col:
                                st.checkbox(
                                    event["text"],
                                    value=event.get("active", True),
                                    key=ck,
                                    on_change=_on_ev_checkbox_change,
                                    args=(sk, ev_state_key, month_str, ev_idx, ck),
                                )
                            with del_col:
                                if st.button(
                                    "🗑️",
                                    key=f"{sk}_del_ev_{month_str}_{ev_idx}",
                                    help="מחק",
                                ):
                                    del_triggered = ev_idx

                        if del_triggered is not None:
                            ev_data.get(month_str, []).pop(del_triggered)
                            _autosave_events(sk, ev_data)
                            st.rerun()

                        # Add new event
                        # Use a counter in the key so rerun creates a fresh empty input
                        ctr = st.session_state.bm_ev_add_ctr
                        new_ev_key = f"{sk}_new_ev_{month_str}_{ctr}"
                        new_ev = st.text_input(
                            "new_event",
                            placeholder=t["bm_events_new_placeholder"],
                            key=new_ev_key,
                            label_visibility="collapsed",
                        )
                        if st.button(
                            t["bm_events_add_btn"],
                            key=f"{sk}_add_ev_{month_str}",
                            use_container_width=True,
                        ):
                            if new_ev.strip():
                                ev_data.setdefault(month_str, []).append(
                                    {"text": new_ev.strip(), "active": True}
                                )
                                _autosave_events(sk, ev_data)
                                st.session_state.bm_ev_add_ctr += 1
                                st.rerun()

    # ════════════════════════════════════════════════════════
    # SAVE & DELETE BUTTONS
    # ════════════════════════════════════════════════════════
    st.markdown("---")
    col_save, col_del = st.columns([3, 1])

    with col_save:
        if st.button(t["bm_save_btn"], type="primary", use_container_width=True):
            updated = collect_brand_from_form(sk, brand)

            src_key      = f"{sk}_src_list"
            raw_sources  = st.session_state.get(src_key, brand.get("web_sources", []))
            saved_sources = []
            for i in range(len(raw_sources)):
                url_val = st.session_state.get(f"{sk}_src_{i}_url",
                          raw_sources[i].get("url", ""))
                if str(url_val).strip():
                    saved_sources.append({
                        "active": bool(st.session_state.get(f"{sk}_src_{i}_active", True)),
                        "name":   str(st.session_state.get(f"{sk}_src_{i}_name",  raw_sources[i].get("name", ""))),
                        "url":    str(url_val).strip(),
                        "focus":  str(st.session_state.get(f"{sk}_src_{i}_focus", raw_sources[i].get("focus", ""))),
                        "ignore": str(st.session_state.get(f"{sk}_src_{i}_ignore",raw_sources[i].get("ignore", ""))),
                    })
            updated["web_sources"] = saved_sources
            st.session_state[src_key] = saved_sources

            # Collect scheduled events
            ev_state_key = f"{sk}_ev_data"
            ev_data = st.session_state.get(ev_state_key) or {}
            scheduled_events = {}
            for month_str, month_events in ev_data.items():
                saved_ev = []
                for ev_idx, ev in enumerate(month_events):
                    ck = f"{sk}_ev_{month_str}_{ev_idx}_active"
                    active = st.session_state.get(ck, ev.get("active", True))
                    if ev.get("text", "").strip():
                        saved_ev.append({
                            "text": ev["text"].strip(),
                            "active": active,
                        })
                if saved_ev:
                    scheduled_events[month_str] = saved_ev
            updated["scheduled_events"] = scheduled_events

            save_brand(sk, updated)
            st.session_state.bm_save_ok        = True
            st.session_state.bm_delete_confirm = False
            st.rerun()

    with col_del:
        if not st.session_state.bm_delete_confirm:
            if st.button(t["bm_delete_btn"], use_container_width=True):
                st.session_state.bm_delete_confirm = True
                st.rerun()
        else:
            st.markdown('<div class="danger-zone">', unsafe_allow_html=True)
            st.warning(t["bm_delete_confirm_msg"].format(name=brand["name"]))
            dc1, dc2 = st.columns(2)
            with dc1:
                if st.button(t["bm_confirm_delete_btn"], type="primary", use_container_width=True):
                    delete_brand(sk)
                    st.session_state.bm_selected_key   = None
                    st.session_state.bm_delete_confirm = False
                    st.rerun()
            with dc2:
                if st.button(t["bm_cancel_btn"], use_container_width=True):
                    st.session_state.bm_delete_confirm = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Brand summary card ────────────────────────────────────
    st.markdown("---")
    st.markdown(t["bm_summary_header"])
    s1, s2, s3, s4 = st.columns(4)
    s1.metric(t["bm_products_metric"],      len(brand["products"]))
    s2.metric(t["bm_active_plat_metric"],   sum(1 for p in brand["platforms"].values() if p.get("priority") != "disabled"))
    s3.metric(t["bm_knowledge_metric"],     sum(len(v) for v in brand["knowledge_base"].values() if isinstance(v, list)))
    s4.metric(t["bm_hashtags_metric"],      len(brand["knowledge_base"].get("approved_hashtags", [])))

# =============================================================
# EMPTY STATE (no brands at all)
# =============================================================
elif not brands and not st.session_state.bm_creating_new:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
        border-radius: 12px; padding: 60px 30px; text-align: center;
        border: 2px dashed #d0d5ff; min-height: 300px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    ">
        <div style="font-size: 60px; margin-bottom: 16px;">🏢</div>
        <div style="font-size: 20px; color: #888; font-weight: 600;">{t['bm_empty_title']}</div>
        <div style="font-size: 14px; color: #bbb; margin-top: 10px;">
            {t['bm_empty_sub']}
        </div>
    </div>
    """, unsafe_allow_html=True)
