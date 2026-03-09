# =============================================================
# 🏢 BRAND MANAGER — Add, edit and grow brand knowledge
# =============================================================
# This page lets you manage all brand DNA profiles without
# touching any code. All data saved to brands_db.json
# =============================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from db import (
    load_brands, save_brand, delete_brand,
    brand_key_from_name, get_brand_with_defaults, EMPTY_BRAND
)

st.set_page_config(
    page_title="🏢 Brand Manager",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================
# STYLING
# =============================================================
st.markdown("""
<style>
    textarea, input[type="text"] {
        direction: rtl !important;
        text-align: right !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }
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
    [data-testid="stExpander"] summary { direction: rtl; text-align: right; }

    .brand-card {
        background: #f4f4fb;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-right: 4px solid #6c63ff;
        direction: rtl;
        text-align: right;
    }
    .kb-section {
        background: #f0fff4;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-right: 4px solid #4CAF50;
    }
    .danger-zone {
        background: #fff5f5;
        border-radius: 10px;
        padding: 14px 18px;
        border: 1px solid #ffcccc;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =============================================================
# SESSION STATE
# =============================================================
if "bm_selected_key"   not in st.session_state: st.session_state.bm_selected_key   = None
if "bm_creating_new"   not in st.session_state: st.session_state.bm_creating_new   = False
if "bm_delete_confirm" not in st.session_state: st.session_state.bm_delete_confirm = False
if "bm_save_ok"        not in st.session_state: st.session_state.bm_save_ok        = False


# =============================================================
# HELPERS
# =============================================================
def list_to_text(lst: list) -> str:
    """Convert a list to newline-separated string for text areas."""
    return "\n".join(lst) if lst else ""


def text_to_list(text: str) -> list:
    """Convert newline-separated text area back to a list."""
    return [x.strip() for x in text.split("\n") if x.strip()]


def sv(key, fallback=""):
    """Read a string widget value from session_state."""
    return st.session_state.get(key, fallback)


def sl(key, fallback=None):
    """Read a list widget value from session_state (textarea → list)."""
    val = st.session_state.get(key, None)
    if val is None:
        return fallback or []
    return text_to_list(val)


def collect_brand_from_form(sk: str, current: dict) -> dict:
    """
    sk = widget key prefix (brand key).
    Reads all form fields from session_state and builds the brand dict.
    Falls back to current brand data for any field not yet in session_state.
    """
    c = current  # shorthand
    ca = c.get("audience", {})
    cv = c.get("voice", {})
    cp = c.get("platforms", {})
    ck = c.get("knowledge_base", {})

    def plat(p):
        return cp.get(p, {})

    return {
        # ── Basic ──────────────────────────────────────────────
        "name":              sv(f"{sk}_name",    c.get("name", "")),
        "hebrew_name":       sv(f"{sk}_hname",   c.get("hebrew_name", "")),
        "emoji":             sv(f"{sk}_emoji",   c.get("emoji", "🏢")),
        "type":              sv(f"{sk}_type",    c.get("type", "")),
        "parent_company":    sv(f"{sk}_parent",  c.get("parent_company", "")),
        "website":           sv(f"{sk}_website", c.get("website", "")),
        "language":          sv(f"{sk}_lang",    c.get("language", "עברית")),
        "posting_frequency": sv(f"{sk}_freq",    c.get("posting_frequency", "")),

        # ── Products ───────────────────────────────────────────
        "products":          sl(f"{sk}_products", c.get("products", [])),
        "usp":               sl(f"{sk}_usp",      c.get("usp", [])),
        "content_that_works":sl(f"{sk}_ctw",      c.get("content_that_works", [])),
        "content_to_avoid":  sl(f"{sk}_cta",      c.get("content_to_avoid", [])),

        # ── Audience ───────────────────────────────────────────
        "audience": {
            "age":           sv(f"{sk}_aud_age",    ca.get("age", "")),
            "gender":        sv(f"{sk}_aud_gender",  ca.get("gender", "")),
            "interests":     sl(f"{sk}_aud_int",     ca.get("interests", [])),
            "psychographic": sv(f"{sk}_aud_psycho",  ca.get("psychographic", "")),
            "motivation":    sv(f"{sk}_aud_motiv",   ca.get("motivation", "")),
        },

        # ── Voice ──────────────────────────────────────────────
        "voice": {
            "tone":           sv(f"{sk}_v_tone",  cv.get("tone", "")),
            "style":          sv(f"{sk}_v_style", cv.get("style", "")),
            "language_notes": sv(f"{sk}_v_lang",  cv.get("language_notes", "")),
            "do":             sl(f"{sk}_v_do",    cv.get("do", [])),
            "dont":           sl(f"{sk}_v_dont",  cv.get("dont", [])),
        },

        # ── Platforms ──────────────────────────────────────────
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

        # ── Knowledge Base ─────────────────────────────────────
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
st.markdown("# 🏢 ניהול מותגים")
st.markdown("הוסף מותגים חדשים, ערוך פרופילים קיימים, ובנה את **בסיס הידע** שמחכים לו הסוכן.")
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
        # Keep selected key valid
        if st.session_state.bm_selected_key not in brands:
            st.session_state.bm_selected_key = list(brands.keys())[0]

        chosen_key = st.selectbox(
            "בחר מותג לעריכה:",
            options=list(brand_options.keys()),
            format_func=lambda x: brand_options[x],
            index=list(brand_options.keys()).index(st.session_state.bm_selected_key),
            label_visibility="collapsed",
        )
        if chosen_key != st.session_state.bm_selected_key:
            # Clear web-sources state for the old brand so new brand loads fresh
            old_src_key = f"{st.session_state.bm_selected_key}_src_list"
            st.session_state.pop(old_src_key, None)
            st.session_state.bm_selected_key   = chosen_key
            st.session_state.bm_delete_confirm = False
            st.session_state.bm_save_ok        = False
            st.rerun()
    else:
        st.info("אין מותגים עדיין. לחץ על '➕ מותג חדש' להתחיל.")
        st.session_state.bm_selected_key = None

with col_new:
    if st.button("➕ מותג חדש", use_container_width=True, type="primary"):
        st.session_state.bm_creating_new   = True
        st.session_state.bm_delete_confirm = False
        st.session_state.bm_save_ok        = False
        st.rerun()

# =============================================================
# NEW BRAND CREATION FORM
# =============================================================
if st.session_state.bm_creating_new:
    st.markdown("---")
    st.markdown("### ✨ מותג חדש")
    with st.container(border=True):
        nc1, nc2, nc3 = st.columns([4, 3, 1])
        with nc1:
            new_name = st.text_input("שם המותג (באנגלית)", placeholder="My Brand", key="new_brand_name")
        with nc2:
            new_hname = st.text_input("שם בעברית", placeholder="המותג שלי", key="new_brand_hname")
        with nc3:
            new_emoji = st.text_input("אמוג'י", value="🏢", key="new_brand_emoji", max_chars=4)

        new_type = st.text_input("סוג / קטגוריה", placeholder="לדוגמה: חנות קמעונאית / מותג ייבוא", key="new_brand_type")

        cb1, cb2 = st.columns(2)
        with cb1:
            if st.button("✅ צור מותג", type="primary", use_container_width=True):
                if new_name.strip():
                    new_key = brand_key_from_name(new_name.strip())
                    if new_key in brands:
                        st.error(f"מותג עם מזהה '{new_key}' כבר קיים.")
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
                    st.warning("נא להזין שם מותג.")
        with cb2:
            if st.button("ביטול", use_container_width=True):
                st.session_state.bm_creating_new = False
                st.rerun()
    st.markdown("---")

# =============================================================
# BRAND EDITOR
# =============================================================
if st.session_state.bm_selected_key and not st.session_state.bm_creating_new:
    brands = load_brands()   # reload after any new-brand creation
    sk = st.session_state.bm_selected_key

    if sk not in brands:
        st.error("המותג לא נמצא. אולי נמחק?")
        st.stop()

    brand = get_brand_with_defaults(brands[sk])

    # ── Shortcut refs ────────────────────────────────────────
    aud  = brand["audience"]
    voc  = brand["voice"]
    plat = brand["platforms"]
    kb   = brand["knowledge_base"]

    st.markdown(f"## {brand['emoji']} {brand['name']}  <span style='font-size:14px; color:#999;'>({sk})</span>", unsafe_allow_html=True)

    if st.session_state.bm_save_ok:
        st.success("✅ המותג נשמר בהצלחה!")
        st.session_state.bm_save_ok = False

    # ── TABS ─────────────────────────────────────────────────
    tabs = st.tabs(["🏷️ בסיס", "📦 מוצרים", "👥 קהל יעד", "🎤 קול המותג", "📱 פלטפורמות", "🧠 בסיס ידע", "🌐 מקורות אינטרנט"])

    # ════════════════════════════════════════════════════════
    # TAB 1: Basic Info
    # ════════════════════════════════════════════════════════
    with tabs[0]:
        st.markdown("#### 🏷️ פרטי בסיס")
        r1c1, r1c2, r1c3 = st.columns([4, 3, 1])
        with r1c1:
            st.text_input("שם המותג", value=brand["name"],        key=f"{sk}_name")
        with r1c2:
            st.text_input("שם בעברית",  value=brand["hebrew_name"],  key=f"{sk}_hname")
        with r1c3:
            st.text_input("אמוג'י",     value=brand["emoji"],        key=f"{sk}_emoji", max_chars=4)

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.text_input("סוג / קטגוריה",  value=brand["type"],           key=f"{sk}_type")
            st.text_input("חברת אם",         value=brand["parent_company"], key=f"{sk}_parent")
        with r2c2:
            st.text_input("אתר אינטרנט",     value=brand["website"],        key=f"{sk}_website")
            st.text_input("תדירות פרסום",    value=brand["posting_frequency"], key=f"{sk}_freq")

        st.text_input("שפת תוכן", value=brand["language"], key=f"{sk}_lang")

    # ════════════════════════════════════════════════════════
    # TAB 2: Products & Positioning
    # ════════════════════════════════════════════════════════
    with tabs[1]:
        st.markdown("#### 📦 מוצרים ומיצוב")
        p1, p2 = st.columns(2)
        with p1:
            st.markdown("**מוצרים** (שורה לכל מוצר)")
            st.text_area("", value=list_to_text(brand["products"]),
                         height=180, label_visibility="collapsed", key=f"{sk}_products")

            st.markdown("**מה עובד בתוכן** (שורה לכל סוג)")
            st.text_area("", value=list_to_text(brand["content_that_works"]),
                         height=130, label_visibility="collapsed", key=f"{sk}_ctw")
        with p2:
            st.markdown("**יתרונות ייחודיים — USP** (שורה לכל יתרון)")
            st.text_area("", value=list_to_text(brand["usp"]),
                         height=180, label_visibility="collapsed", key=f"{sk}_usp")

            st.markdown("**מה להימנע בתוכן** (שורה לכל סוג)")
            st.text_area("", value=list_to_text(brand["content_to_avoid"]),
                         height=130, label_visibility="collapsed", key=f"{sk}_cta")

    # ════════════════════════════════════════════════════════
    # TAB 3: Audience
    # ════════════════════════════════════════════════════════
    with tabs[2]:
        st.markdown("#### 👥 קהל יעד")
        a1, a2 = st.columns(2)
        with a1:
            st.text_input("גיל",    value=aud["age"],    key=f"{sk}_aud_age")
            st.text_input("מגדר",   value=aud["gender"], key=f"{sk}_aud_gender")
            st.markdown("**תחומי עניין** (שורה לכל עניין)")
            st.text_area("", value=list_to_text(aud["interests"]),
                         height=150, label_visibility="collapsed", key=f"{sk}_aud_int")
        with a2:
            st.markdown("**פסיכוגרפיה** — מי הם באמת?")
            st.text_area("", value=aud["psychographic"],
                         height=150, label_visibility="collapsed", key=f"{sk}_aud_psycho")
            st.markdown("**מה מניע אותם לקנות?**")
            st.text_area("", value=aud["motivation"],
                         height=130, label_visibility="collapsed", key=f"{sk}_aud_motiv")

    # ════════════════════════════════════════════════════════
    # TAB 4: Voice & Tone
    # ════════════════════════════════════════════════════════
    with tabs[3]:
        st.markdown("#### 🎤 קול המותג")
        v1, v2 = st.columns(2)
        with v1:
            st.markdown("**טון**")
            st.text_input("",  value=voc["tone"],           label_visibility="collapsed", key=f"{sk}_v_tone")
            st.markdown("**סגנון**")
            st.text_area("",   value=voc["style"],          height=110, label_visibility="collapsed", key=f"{sk}_v_style")
            st.markdown("**הנחיות שפה**")
            st.text_area("",   value=voc["language_notes"], height=110, label_visibility="collapsed", key=f"{sk}_v_lang")
        with v2:
            st.markdown("**✅ לעשות תמיד** (שורה לכל הנחיה)")
            st.text_area("",   value=list_to_text(voc["do"]),   height=160, label_visibility="collapsed", key=f"{sk}_v_do")
            st.markdown("**❌ לא לעשות לעולם** (שורה לכל הנחיה)")
            st.text_area("",   value=list_to_text(voc["dont"]), height=160, label_visibility="collapsed", key=f"{sk}_v_dont")

    # ════════════════════════════════════════════════════════
    # TAB 5: Platforms
    # ════════════════════════════════════════════════════════
    with tabs[4]:
        st.markdown("#### 📱 פלטפורמות")
        PRIORITY_OPTIONS = ["primary", "secondary", "disabled"]

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
                        "עדיפות",
                        PRIORITY_OPTIONS,
                        index=pri_idx,
                        key=f"{sk}_{plat_key[:2]}_pri",
                        format_func=lambda x: {"primary":"⭐ ראשי","secondary":"📌 משני","disabled":"🚫 כבוי"}[x],
                    )
                    st.text_input("כמות האשטגים", value=pd.get("hashtag_count",""),
                                  key=f"{sk}_{plat_key[:2]}_hash")
                with pp2:
                    st.markdown("**סוגי תוכן** (שורה לכל סוג)")
                    st.text_area("", value=list_to_text(pd.get("content_types",[])),
                                 height=100, label_visibility="collapsed",
                                 key=f"{sk}_{plat_key[:2]}_types")
                with pp3:
                    st.text_input("אורך כיתוב", value=pd.get("caption_length",""),
                                  key=f"{sk}_{plat_key[:2]}_cap")

    # ════════════════════════════════════════════════════════
    # TAB 6: Knowledge Base 🧠
    # ════════════════════════════════════════════════════════
    with tabs[5]:
        st.markdown("#### 🧠 בסיס הידע — המוח שגדל עם הזמן")
        st.caption("כל מה שמכניסים כאן הסוכן ישתמש בו אוטומטית בכל יצירת תוכן למותג זה.")

        st.markdown(
            '<div class="kb-section">',
            unsafe_allow_html=True,
        )

        kb1, kb2 = st.columns(2)

        with kb1:
            st.markdown("**✅ מה עובד** — לפי ניסיון הצוות (שורה לכל פריט)")
            st.text_area(
                "", value=list_to_text(kb["what_works"]), height=110,
                placeholder="לדוגמה: ריילס עם מוזיקה מקבלים 3x יותר reach",
                label_visibility="collapsed", key=f"{sk}_kb_works",
            )

            st.markdown("**🏆 מתחרים** — שמות / אתרים (שורה לכל אחד)")
            st.text_area(
                "", value=list_to_text(kb["competitors"]), height=90,
                placeholder="לדוגמה: kuma-toys.co.il",
                label_visibility="collapsed", key=f"{sk}_kb_comp",
            )

            st.markdown("**🔗 לינקים ללמידה** — מאמרים / מקורות (שורה לכל לינק)")
            st.text_area(
                "", value=list_to_text(kb["learning_links"]), height=90,
                placeholder="לדוגמה: https://www.funko.com/news",
                label_visibility="collapsed", key=f"{sk}_kb_links",
            )

            st.markdown("**#️⃣ האשטגים מאושרים** (שורה לכל האשטג, ללא #)")
            st.text_area(
                "", value=list_to_text(kb["approved_hashtags"]), height=90,
                placeholder="לדוגמה: מיסט\nפופקאלצ'ר\nFunkoPop",
                label_visibility="collapsed", key=f"{sk}_kb_hashtags",
            )

        with kb2:
            st.markdown("**❌ מה לא עובד** — לפי ניסיון הצוות (שורה לכל פריט)")
            st.text_area(
                "", value=list_to_text(kb["what_doesnt"]), height=110,
                placeholder="לדוגמה: פוסטי טקסט בלי תמונה — כמעט אפס engagement",
                label_visibility="collapsed", key=f"{sk}_kb_doesnt",
            )

            st.markdown("**📰 מקורות חדשות** — לעקוב אחריהם (שורה לכל אחד)")
            st.text_area(
                "", value=list_to_text(kb["news_sources"]), height=90,
                placeholder="לדוגמה: ign.com\nkotaku.com\nmarvel.com/news",
                label_visibility="collapsed", key=f"{sk}_kb_news",
            )

            st.markdown("**📝 הערות צוות שיווק** (שורה לכל הערה)")
            st.text_area(
                "", value=list_to_text(kb["team_notes"]), height=170,
                placeholder="לדוגמה: אל תפרסמו ביום שישי אחה\"צ\nהקהל מגיב טוב לסלנג גיימינג",
                label_visibility="collapsed", key=f"{sk}_kb_notes",
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # TAB 7: Web Sources 🌐
    # ════════════════════════════════════════════════════════
    with tabs[6]:
        st.markdown("#### 🌐 מקורות אינטרנט — הסוכן יקרא אלה לפני כל יצירת תוכן")
        st.caption(
            "הוסף כתובות URL שהסוכן יסרוק לפני כל פוסט — אתר המותג, חדשות, דפי מוצר. "
            "בכל מקור ציין **מה לחפש** ומה **להתעלם** ממנו."
        )

        # Initialise source list in session state (once per brand load)
        src_key = f"{sk}_src_list"
        if src_key not in st.session_state:
            import copy
            st.session_state[src_key] = copy.deepcopy(brand.get("web_sources", []))

        sources_list = st.session_state[src_key]

        # ── Existing sources ──────────────────────────────
        if not sources_list:
            st.info("אין מקורות עדיין. לחץ ➕ להוסיף מקור ראשון.")

        for i, src in enumerate(sources_list):
            active_icon = "✅" if src.get("active", True) else "⏸️"
            label       = src.get("name") or src.get("url") or f"מקור {i+1}"
            with st.expander(f"{active_icon} {label}", expanded=not src.get("url")):

                row1c1, row1c2 = st.columns([1, 6])
                with row1c1:
                    new_active = st.checkbox(
                        "פעיל", value=src.get("active", True),
                        key=f"{sk}_src_{i}_active",
                    )
                with row1c2:
                    new_name = st.text_input(
                        "שם המקור", value=src.get("name", ""),
                        placeholder="לדוגמה: אתר מיסט / Razor Facebook Israel",
                        key=f"{sk}_src_{i}_name",
                    )

                new_url = st.text_input(
                    "🔗 URL", value=src.get("url", ""),
                    placeholder="https://myst.co.il",
                    key=f"{sk}_src_{i}_url",
                )

                fc1, fc2 = st.columns(2)
                with fc1:
                    st.text_input(
                        "🔍 מה לחפש",
                        value=src.get("focus", ""),
                        placeholder="מוצרים חדשים, מחירים, מבצעים",
                        key=f"{sk}_src_{i}_focus",
                    )
                with fc2:
                    st.text_input(
                        "🚫 מה להתעלם",
                        value=src.get("ignore", ""),
                        placeholder="מוצרים לא ישראליים, מידע ישן",
                        key=f"{sk}_src_{i}_ignore",
                    )

                if st.button(f"🗑️ מחק מקור זה", key=f"{sk}_src_{i}_del"):
                    sources_list.pop(i)
                    st.rerun()

        # ── Add new source button ─────────────────────────
        st.markdown("")
        if st.button("➕ הוסף מקור חדש", use_container_width=True):
            sources_list.append({
                "active": True, "name": "", "url": "", "focus": "", "ignore": "",
            })
            st.rerun()

        # ── Help tip ──────────────────────────────────────
        with st.expander("💡 טיפים למקורות טובים"):
            st.markdown("""
| סוג | דוגמה לURL | מה לכתוב ב"מה לחפש" |
|-----|-----------|-------------------|
| **אתר המותג** | `myst.co.il` | מוצרים חדשים, מחירים, מבצעים |
| **דף פייסבוק** | `facebook.com/RazorIsrael` | פוסטים חדשים, מוצרים |
| **אתר חדשות** | `ign.com/news` | טרנדים, הודעות חדשות |
| **מתחרה** | `competitor.co.il` | מה הם מפרסמים השבוע |
| **דף מוצר** | `amazon.co.il/product/...` | מחיר, זמינות, ביקורות |
            """)

    # ════════════════════════════════════════════════════════
    # SAVE & DELETE BUTTONS
    # ════════════════════════════════════════════════════════
    st.markdown("---")
    col_save, col_del = st.columns([3, 1])

    with col_save:
        if st.button("💾 שמור מותג", type="primary", use_container_width=True):
            updated = collect_brand_from_form(sk, brand)

            # ── Collect web sources from dynamic list ─────
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
            st.session_state[src_key] = saved_sources   # sync state

            save_brand(sk, updated)
            st.session_state.bm_save_ok        = True
            st.session_state.bm_delete_confirm = False
            st.rerun()

    with col_del:
        if not st.session_state.bm_delete_confirm:
            if st.button("🗑️ מחק מותג", use_container_width=True):
                st.session_state.bm_delete_confirm = True
                st.rerun()
        else:
            st.markdown(
                '<div class="danger-zone">',
                unsafe_allow_html=True,
            )
            st.warning(f"למחוק את **{brand['name']}** לצמיתות?")
            dc1, dc2 = st.columns(2)
            with dc1:
                if st.button("✅ כן, מחק", type="primary", use_container_width=True):
                    delete_brand(sk)
                    st.session_state.bm_selected_key   = None
                    st.session_state.bm_delete_confirm = False
                    st.rerun()
            with dc2:
                if st.button("ביטול", use_container_width=True):
                    st.session_state.bm_delete_confirm = False
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Brand summary card ────────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📊 סיכום מותג")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("מוצרים",           len(brand["products"]))
    s2.metric("פלטפורמות פעילות", sum(1 for p in brand["platforms"].values() if p.get("priority") != "disabled"))
    s3.metric("פריטי ידע",        sum(len(v) for v in brand["knowledge_base"].values() if isinstance(v, list)))
    s4.metric("האשטגים מאושרים", len(brand["knowledge_base"].get("approved_hashtags", [])))

# =============================================================
# EMPTY STATE (no brands at all)
# =============================================================
elif not brands and not st.session_state.bm_creating_new:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
        border-radius: 12px; padding: 60px 30px; text-align: center;
        border: 2px dashed #d0d5ff; min-height: 300px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    ">
        <div style="font-size: 60px; margin-bottom: 16px;">🏢</div>
        <div style="font-size: 20px; color: #888; font-weight: 600;">אין מותגים עדיין</div>
        <div style="font-size: 14px; color: #bbb; margin-top: 10px;">
            לחץ על ➕ מותג חדש כדי להתחיל
        </div>
    </div>
    """, unsafe_allow_html=True)
