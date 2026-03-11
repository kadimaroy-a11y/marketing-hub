# =============================================================
# 🚀 MARKETING HUB — Main Application v3.0
# =============================================================
# Powered by Claude AI
# Built for: Pupik Group — Myst & Prime51
# v3.0: Full HEB/EN language toggle + all previous features
# =============================================================

import json
import streamlit as st
import streamlit.components.v1 as components
import anthropic
import os
import html as html_lib
from dotenv import load_dotenv
from db import load_brands
from brand_profiles import CONTENT_TYPES, BRAND_PROFILES as _FALLBACK_PROFILES
import importlib, sys
if "web_reader" in sys.modules:
    importlib.reload(sys.modules["web_reader"])
from web_reader import get_brand_awareness, get_product_links
if "translations" in sys.modules:
    importlib.reload(sys.modules["translations"])
from content_db import add_to_library
from translations import get_t, get_section_config

# Load brands from JSON database; fall back to brand_profiles.py if db is empty
BRAND_PROFILES = load_brands() or _FALLBACK_PROFILES

load_dotenv()

st.set_page_config(
    page_title="🚀 Marketing Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================
# SESSION STATE
# =============================================================
def init_session():
    defaults = {
        "api_messages":       [],
        "chat_display":       [],
        "system_prompt":      "",
        "has_content":        False,
        "latest_content":     "",
        "approved":           False,
        "pending_refinement": None,
        "saved_brand":        "",
        "saved_brand_key":    "",
        "saved_brand_emoji":  "",
        "saved_platform":     "",
        "saved_type":         "",
        "saved_brief":        "",
        "input_counter":      0,
        "library_saved":      False,
        "lang":               "he",   # "he" or "en"
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# ── Language + translation shortcuts ─────────────────────────
lang = st.session_state.lang
t    = get_t(lang)
D    = t["dir"]    # "rtl" or "ltr"
A    = t["align"]  # "right" or "left"

# ── Dynamic SECTION_CONFIG for current language ───────────────
SECTION_CONFIG = get_section_config(lang)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# =============================================================
# STYLING — base styles + direction-aware overrides
# =============================================================
st.markdown("""
<style>
    /* ── Page header ── */
    .main-header { text-align: center; padding: 10px 0 20px 0; }

    /* ── Generated content boxes: ALWAYS RTL (Hebrew content) ── */
    .rtl-output {
        direction: rtl;
        text-align: right;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 15px;
        line-height: 1.95;
        background: #fafbff;
        padding: 16px 20px;
        border-radius: 10px;
        border-right: 4px solid #6c63ff;
        color: #1a1a2e;
        white-space: pre-wrap;
        min-height: 50px;
        margin-bottom: 2px;
    }
    .rtl-stream {
        direction: rtl;
        text-align: right;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 15px;
        line-height: 1.95;
        background: #fafbff;
        padding: 20px 24px;
        border-radius: 12px;
        border-right: 4px solid #6c63ff;
        color: #1a1a2e;
        white-space: pre-wrap;
        min-height: 120px;
    }
    .user-bubble {
        direction: rtl;
        text-align: right;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 14px;
        background: #e8f5e9;
        padding: 10px 16px;
        border-radius: 10px;
        border-right: 4px solid #4CAF50;
        color: #1b5e20;
        margin: 10px 0 6px 0;
    }

    /* ── Image prompt box (always LTR / English) ── */
    .ltr-output {
        direction: ltr;
        text-align: left;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        line-height: 1.75;
        background: #f0fff4;
        padding: 16px 20px;
        border-radius: 10px;
        border-left: 4px solid #38a169;
        color: #1a3a2a;
        white-space: pre-wrap;
        min-height: 50px;
        margin-bottom: 2px;
    }

    /* ── Hebrew image prompt (two-column dual-language display) ── */
    .he-image-prompt {
        direction: rtl;
        text-align: right;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 13px;
        line-height: 1.75;
        background: #faf5ff;
        padding: 16px 20px;
        border-radius: 10px;
        border-right: 4px solid #9f7aea;
        color: #2d1b4e;
        white-space: pre-wrap;
        min-height: 50px;
        margin-bottom: 2px;
    }
    .lang-badge {
        font-size: 11px;
        font-weight: 700;
        color: #777;
        padding: 2px 0 5px 0;
        letter-spacing: 0.3px;
    }

    /* ── Version label ── */
    .version-label {
        font-size: 12px;
        color: #999;
        margin-bottom: 2px;
        font-style: italic;
    }
    .version-label.current {
        color: #6c63ff;
        font-weight: 600;
        font-style: normal;
        font-size: 13px;
    }

    /* ── Refinement input area ── */
    .refine-box {
        background: #f0f2ff;
        border-radius: 10px;
        padding: 12px 14px;
        margin: 12px 0 8px 0;
    }

    /* ── Lang toggle pill ── */
    .lang-toggle {
        display: flex;
        gap: 6px;
        justify-content: flex-end;
        padding-top: 8px;
    }

    @keyframes blink { 50% { opacity: 0; } }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Direction-aware CSS (changes with language) ───────────────
st.markdown(f"""
<style>
    textarea {{
        direction: {D} !important;
        text-align: {A} !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }}
    .section-header {{
        direction: {D};
        text-align: {A};
        font-weight: 700;
        font-size: 14px;
        color: #4a4a8a;
        margin: 14px 0 4px 0;
        letter-spacing: 0.3px;
    }}
    label,
    .stCaption p,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stText"] {{
        direction: {D} !important;
        text-align: {A} !important;
    }}
    [data-testid="stMainBlockContainer"] h1,
    [data-testid="stMainBlockContainer"] h2,
    [data-testid="stMainBlockContainer"] h3 {{
        direction: {D}; text-align: {A};
    }}
    [data-testid="stAlert"]    {{ direction: {D}; text-align: {A}; }}
    [data-testid="stExpander"] summary {{ direction: {D}; text-align: {A}; }}
</style>
""", unsafe_allow_html=True)


# =============================================================
# SECTION PARSING — emoji markers (language-independent)
# =============================================================
def parse_content_sections(content: str) -> dict:
    """Split Claude output into named sections using emoji markers."""
    sections = {}
    marker_emojis = {
        "caption":      ["📝"],
        "hashtags":     ["#️⃣", "️⃣", "#⃣"],
        "visual":       ["🎬"],
        "story":        ["📱"],
        "image_prompt": ["🖼️"],
    }
    positions = []
    for key, emojis in marker_emojis.items():
        for emoji in emojis:
            idx = content.find(emoji)
            if idx != -1:
                positions.append((idx, key))
                break
    positions.sort(key=lambda x: x[0])
    for i, (idx, key) in enumerate(positions):
        line_end = content.find('\n', idx)
        if line_end == -1:
            sections[key] = content[idx:].strip()
            continue
        content_start = line_end + 1
        content_end   = positions[i + 1][0] if i + 1 < len(positions) else len(content)
        sections[key] = content[content_start:content_end].strip().rstrip('-').strip()
    return sections


# =============================================================
# COPY BUTTON — language-aware labels
# =============================================================
def copy_button(text: str, uid: str):
    """Render a copy-to-clipboard button, labels follow UI language."""
    # Sanitize uid → valid HTML id and JS identifier
    safe_uid   = "".join(c if c.isalnum() else "_" for c in uid)
    btn_id     = f"b_{safe_uid}"
    # json.dumps with ensure_ascii avoids any non-ASCII in the script;
    # replace </ to prevent </script> breakout inside <script> tags.
    safe_js    = json.dumps(text,             ensure_ascii=True).replace("</", "<\\/")
    copy_lbl   = json.dumps(t["copy_btn"],    ensure_ascii=True)
    copied_lbl = json.dumps(t["copied_btn"],  ensure_ascii=True)

    components.html(f"""
    <button id="{btn_id}"
        style="background:#6c63ff;color:white;border:none;padding:5px 14px;
               border-radius:6px;cursor:pointer;font-size:13px;font-family:Arial;
               white-space:nowrap;">
        {t["copy_btn"]}
    </button>
    <script>
    (function() {{
        var text      = {safe_js};
        var copyLbl   = {copy_lbl};
        var copiedLbl = {copied_lbl};
        var btn = document.getElementById('{btn_id}');
        if (!btn) return;

        function onCopied() {{
            btn.textContent = copiedLbl;
            btn.style.background = '#4CAF50';
            setTimeout(function() {{
                btn.textContent = copyLbl;
                btn.style.background = '#6c63ff';
            }}, 2000);
        }}

        function legacyCopy() {{
            var inp = document.createElement('input');
            inp.setAttribute('readonly', '');
            inp.value = text;
            inp.style.cssText = 'position:absolute;left:-9999px;top:0;opacity:0;';
            document.body.appendChild(inp);
            inp.focus();
            inp.select();
            inp.setSelectionRange(0, inp.value.length);
            try {{ document.execCommand('copy'); }} catch(e) {{}}
            document.body.removeChild(inp);
            onCopied();
        }}

        btn.addEventListener('click', function() {{
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(text).then(onCopied).catch(legacyCopy);
            }} else {{
                legacyCopy();
            }}
        }});
    }})();
    </script>
    """, height=40, scrolling=False)


# =============================================================
# SECTION DISPLAY — parsed boxes with copy buttons
# =============================================================
def display_content_sections(content: str, uid_prefix: str = "sec",
                              section_config: list = None):
    """Parse content and render each section as its own box + copy button."""
    cfg      = section_config or SECTION_CONFIG
    sections = parse_content_sections(content)

    if not sections:
        safe = html_lib.escape(content)
        st.markdown(f'<div class="rtl-stream">{safe}</div>', unsafe_allow_html=True)
        return

    for i, (key, emoji, title) in enumerate(cfg):
        text = sections.get(key, "")
        if not text:
            continue

        is_dual = key == "image_prompt" and "---HE---" in text

        if is_dual:
            # ── Dual-language image prompt: EN + HE side by side ──
            col_chk, col_title = st.columns([1, 8])
            with col_chk:
                st.checkbox(
                    " ",
                    value=st.session_state.get(f"sec_sel_{key}", True),
                    key=f"sec_sel_{key}",
                    help=title,
                    label_visibility="visible",
                )
            with col_title:
                st.markdown(
                    f'<div class="section-header">{emoji} {title}</div>',
                    unsafe_allow_html=True,
                )

            parts   = text.split("---HE---", 1)
            en_text = parts[0].strip()
            he_text = parts[1].strip() if len(parts) > 1 else ""

            # Hebrew window (top)
            col_he_lbl, col_he_btn = st.columns([7, 2])
            with col_he_lbl:
                st.markdown('<div class="lang-badge">🇮🇱 עברית — לצוות היצירתי</div>', unsafe_allow_html=True)
            with col_he_btn:
                copy_button(he_text, uid=f"{uid_prefix}_{i}_he")
            safe_he = html_lib.escape(he_text)
            st.markdown(f'<div class="he-image-prompt">{safe_he}</div>', unsafe_allow_html=True)

            st.markdown('<div style="margin-bottom:6px;"></div>', unsafe_allow_html=True)

            # English window (bottom)
            col_en_lbl, col_en_btn = st.columns([7, 2])
            with col_en_lbl:
                st.markdown('<div class="lang-badge">🇬🇧 English — AI Generator</div>', unsafe_allow_html=True)
            with col_en_btn:
                copy_button(en_text, uid=f"{uid_prefix}_{i}_en")
            safe_en = html_lib.escape(en_text)
            st.markdown(f'<div class="ltr-output">{safe_en}</div>', unsafe_allow_html=True)
        else:
            col_chk, col_title, col_btn = st.columns([1, 6, 2])
            with col_chk:
                st.checkbox(
                    " ",
                    value=st.session_state.get(f"sec_sel_{key}", True),
                    key=f"sec_sel_{key}",
                    help=title,
                    label_visibility="visible",
                )
            with col_title:
                st.markdown(
                    f'<div class="section-header">{emoji} {title}</div>',
                    unsafe_allow_html=True,
                )
            with col_btn:
                copy_button(text, uid=f"{uid_prefix}_{i}")

            css_class = "ltr-output" if key == "image_prompt" else "rtl-output"
            safe = html_lib.escape(text)
            st.markdown(f'<div class="{css_class}">{safe}</div>', unsafe_allow_html=True)

        if i < len(cfg) - 1:
            st.markdown('<div style="margin-bottom:6px;"></div>', unsafe_allow_html=True)


# =============================================================
# COMPACT HISTORY
# =============================================================
def display_compact_history(messages_list: list):
    display_list = messages_list[:-1] if (
        messages_list and messages_list[-1]["role"] == "assistant"
    ) else messages_list

    for msg in display_list:
        if msg["role"] == "user":
            safe = html_lib.escape(msg["content"])
            st.markdown(f'<div class="user-bubble">💬 {safe}</div>', unsafe_allow_html=True)
        else:
            label = msg.get("label", "🤖")
            st.caption(f"🤖 {label}")
            sections = parse_content_sections(msg["content"])
            preview  = sections.get("caption", msg["content"])
            preview  = (preview[:300] + "...") if len(preview) > 300 else preview
            safe = html_lib.escape(preview)
            st.markdown(
                f'<div class="rtl-output" style="font-size:13px;line-height:1.6;min-height:40px;">'
                f'{safe}</div>', unsafe_allow_html=True,
            )


# =============================================================
# STREAMING
# =============================================================
def do_stream(messages: list, system_prompt: str, use_thinking: bool = False) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error(t["api_error"])
        return ""

    placeholder = st.empty()
    full_text   = ""

    kwargs = {
        "model":      "claude-opus-4-6",
        "max_tokens": 8000 if use_thinking else 3000,
        "system":     system_prompt,
        "messages":   messages,
    }
    if use_thinking:
        kwargs["thinking"] = {"type": "adaptive"}

    try:
        with client.messages.stream(**kwargs) as stream:
            for chunk in stream.text_stream:
                full_text += chunk
                safe = html_lib.escape(full_text)
                placeholder.markdown(
                    f'<div class="rtl-stream">{safe}▌</div>',
                    unsafe_allow_html=True,
                )
        safe = html_lib.escape(full_text)
        placeholder.markdown(
            f'<div class="rtl-stream">{safe}</div>', unsafe_allow_html=True,
        )
    except anthropic.AuthenticationError:
        full_text = t["auth_error"]
        placeholder.error(full_text)
    except anthropic.RateLimitError:
        full_text = t["rate_error"]
        placeholder.error(full_text)
    except Exception as e:
        full_text = f"❌ Error: {str(e)}"
        placeholder.error(full_text)

    return full_text


def display_full_history_for_streaming(messages_list: list):
    for msg in messages_list:
        if msg["role"] == "user":
            safe = html_lib.escape(msg["content"])
            st.markdown(f'<div class="user-bubble">💬 {safe}</div>', unsafe_allow_html=True)
        else:
            label = msg.get("label", "🤖")
            st.markdown(f'<div class="version-label">{label}</div>', unsafe_allow_html=True)
            safe = html_lib.escape(msg["content"])
            st.markdown(f'<div class="rtl-stream">{safe}</div>', unsafe_allow_html=True)


# =============================================================
# PROMPT BUILDERS
# =============================================================
def _build_events_section(brand: dict) -> str:
    """Inject active scheduled events for the current month into the prompt."""
    from datetime import datetime as _dt
    current_month = str(_dt.now().month)
    events = brand.get("scheduled_events", {}).get(current_month, [])
    active = [e["text"] for e in events if e.get("active", True) and e.get("text", "").strip()]
    if not active:
        return ""
    lines = "\n".join(f"  🗓️ {e}" for e in active)
    return (
        "\n\n═══════════════════════════════════════\n"
        " 📅 אירועים פעילים החודש\n"
        "═══════════════════════════════════════\n\n"
        "האירועים הבאים מתוכננים לחודש הנוכחי — שלב אותם בתוכן כשרלוונטי:\n\n"
        + lines
    )


# Emoji headers used when reconstructing selective-save content
_SECTION_HEADERS = {
    "caption":      "📝 כיתוב ראשי",
    "hashtags":     "#️⃣ האשטגים",
    "visual":       "🎬 כיוון ויזואלי",
    "story":        "📱 גרסת סטורי",
    "image_prompt": "🖼️ פרומפט לתמונה",
}


def build_save_content(content: str) -> str:
    """Return content string containing only the user-selected sections."""
    sections = parse_content_sections(content)
    result = ""
    for key, emoji, title in SECTION_CONFIG:
        if st.session_state.get(f"sec_sel_{key}", True) and sections.get(key):
            result += _SECTION_HEADERS.get(key, f"{emoji} {title}") + "\n"
            result += sections[key] + "\n\n"
    return result.strip() or content


def _build_product_links_section(product_links: str) -> str:
    if not product_links or not product_links.strip():
        return ""
    return (
        "\n\n═══════════════════════════════════════\n"
        " 🔗 מוצרים וקישורים אמיתיים מאתר המותג\n"
        "═══════════════════════════════════════\n\n"
        "⚠️ חוק ברזל — קישורים:\n"
        "הרשימה הבאה נסרקה ישירות מאתר המותג ומכילה שמות מוצרים וכתובות URL אמיתיות.\n"
        "כאשר מבקשים לכלול קישורים בתוכן — השתמש אך ורק בכתובות URL המופיעות כאן.\n"
        "אסור בהחלט להמציא, לשנות, או לנחש כתובות URL — גם אם נראות הגיוניות.\n"
        "אם מוצר מוזכר אך אין לו קישור ברשימה — אל תכלול קישור כלל.\n\n"
        + product_links
    )


def build_system_prompt(brand_key: str, web_awareness: str = "", product_links: str = "") -> str:
    brand = BRAND_PROFILES[brand_key]

    products_str = "\n".join([f"  • {p}" for p in brand["products"]])
    usp_str      = "\n".join([f"  • {u}" for u in brand["usp"]])
    do_str       = "\n".join([f"  ✅ {d}" for d in brand["voice"]["do"]])
    dont_str     = "\n".join([f"  ❌ {d}" for d in brand["voice"]["dont"]])

    platform_str = ""
    for pname, details in brand["platforms"].items():
        platform_str += (
            f"\n  {pname.upper()} ({details['priority']} platform):\n"
            f"    - סוגי תוכן: {', '.join(details['content_types'])}\n"
            f"    - אורך כיתוב: {details['caption_length']}\n"
            f"    - כמות האשטגים: {details['hashtag_count']}\n"
        )

    return f"""אתה מומחה השיווק הדיגיטלי של {brand['name']} ({brand['hebrew_name']}) — {brand['type']} בישראל.
הבן את ה-DNA של המותג לעומק ויצור תוכן שמרגיש אותנטי, ישראלי, ובדיוק בסגנון הנכון.

═══════════════════════════════════════
 פרופיל המותג: {brand['name']}
═══════════════════════════════════════

סוג: {brand['type']}
חברת אם: {brand.get('parent_company', 'N/A')}
שפה: {brand['language']} — כל התוכן חייב להיות בעברית

מוצרים שאנחנו מוכרים:
{products_str}

מה מייחד אותנו (USP):
{usp_str}

═══════════════════════════════════════
 קהל היעד שלנו
═══════════════════════════════════════

גיל: {brand['audience']['age']}
מגדר: {brand['audience']['gender']}
תחומי עניין: {', '.join(brand['audience']['interests'])}

פסיכוגרפיה:
{brand['audience']['psychographic']}

מה מניע אותם לקנות:
{brand['audience']['motivation']}

═══════════════════════════════════════
 קול המותג
═══════════════════════════════════════

טון: {brand['voice']['tone']}
סגנון: {brand['voice']['style']}
הנחיות שפה: {brand['voice']['language_notes']}

מה לעשות:
{do_str}

מה לא לעשות:
{dont_str}

═══════════════════════════════════════
 הנחיות לפלטפורמות
═══════════════════════════════════════
{platform_str}

תוכן שעובד טוב: {', '.join(brand['content_that_works'])}
תוכן להימנע ממנו: {', '.join(brand['content_to_avoid'])}

═══════════════════════════════════════
 כללי כתיבה
═══════════════════════════════════════

כתוב כמו פאן אמיתי שעובד ב-{brand['name']} — לא כמו מחלקת שיווק קורפורטיבית.
אתה מבין את התרבות, את הרפרנסים, ואת השפה של הקהל.
כל פוסט צריך להרגיש כאילו כתב אותו מישהו שבאמת אוהב את הנושא.

כשמתבקש לשנות או לשפר תוכן:
- שמור על אותו פורמט (📝 כיתוב ראשי / #️⃣ האשטגים / 🎬 כיוון ויזואלי / 📱 גרסת סטורי / 🖼️ פרומפט לתמונה)
- אלא אם התבקשת במפורש לשנות את הפורמט
- החזר את הפוסט המעודכן במלואו, מוכן לפרסום
{_build_knowledge_base_section(brand)}{_build_product_links_section(product_links)}{_build_events_section(brand)}{_build_web_awareness_section(web_awareness)}"""


def _build_knowledge_base_section(brand: dict) -> str:
    kb = brand.get("knowledge_base", {})
    if not kb:
        return ""
    sections = []
    if kb.get("what_works"):
        sections.append("מה עובד טוב (לפי ניסיון הצוות):\n" +
                        "\n".join(f"  ✅ {x}" for x in kb["what_works"]))
    if kb.get("what_doesnt"):
        sections.append("מה לא עובד (לפי ניסיון הצוות):\n" +
                        "\n".join(f"  ❌ {x}" for x in kb["what_doesnt"]))
    if kb.get("competitors"):
        sections.append("מתחרים — שים לב להתבדל מהם:\n" +
                        "\n".join(f"  🏆 {x}" for x in kb["competitors"]))
    if kb.get("team_notes"):
        sections.append("הערות מצוות השיווק:\n" +
                        "\n".join(f"  📝 {x}" for x in kb["team_notes"]))
    if kb.get("approved_hashtags"):
        sections.append("האשטגים מאושרים לשימוש:\n" +
                        "  " + "  ".join(f"#{x}" for x in kb["approved_hashtags"]))
    if not sections:
        return ""
    return ("\n\n═══════════════════════════════════════\n"
            " ידע נצבר מניסיון הצוות\n"
            "═══════════════════════════════════════\n\n" +
            "\n\n".join(sections))


def _build_web_awareness_section(awareness: str) -> str:
    if not awareness or not awareness.strip():
        return ""
    return ("\n\n═══════════════════════════════════════\n"
            " 🌐 מה קורה עכשיו — נסרק ממקורות המותג\n"
            "═══════════════════════════════════════\n\n"
            "המידע הבא נסרק זה עתה מהמקורות המאושרים של המותג.\n"
            "השתמש בו כדי להפוך את התוכן לרלוונטי ועדכני:\n\n"
            + awareness)


def build_initial_user_prompt(
    brand_key, platform, content_type, brief, additional_notes="", num_versions=1
):
    brand            = BRAND_PROFILES[brand_key]
    content_info     = CONTENT_TYPES.get(content_type, {})
    platform_details = brand["platforms"].get(platform.lower(), {})

    versions_instruction = (
        f"\nצור {num_versions} גרסאות שונות, ממוספרות בבירור."
        if num_versions > 1 else ""
    )

    weekly_plan_section = ""
    if content_type == "weekly_content_plan":
        weekly_plan_section = """
פורמט תוכנית שבועית:
ליום א׳ עד שבת, ציין לכל יום:
- פלטפורמה מומלצת
- סוג תוכן
- נושא / רעיון קצר
- הוק או כיתוב לדוגמה (2-3 שורות)
"""

    return f"""צור {content_info.get('label', content_type)} עבור {brand['name']} לפרסום ב-{platform.upper()}.

הבריף:
{brief}

{"הערות נוספות: " + additional_notes if additional_notes else ""}

{versions_instruction}

פרטי הפלטפורמה:
- אורך כיתוב: {platform_details.get('caption_length', 'בינוני')}
- כמות האשטגים: {platform_details.get('hashtag_count', '10')}

{weekly_plan_section}

מה לספק (בסדר הזה):

📝 כיתוב ראשי
הכיתוב המלא בעברית, מוכן להעתקה ופרסום. כלול אימוג'י היכן שמתאים.

#️⃣ האשטגים
{platform_details.get('hashtag_count', '10')} האשטגים — תערובת עברית ואנגלית רלוונטית.

🎬 כיוון ויזואלי
תיאור קצר (1-2 משפטים) של מה הצילום/הסרטון צריך להראות.

📱 גרסת סטורי (קצרה)
גרסה מקוצרת ומדויקת לסטורי (1-3 שורות + CTA).

🖼️ פרומפט לתמונה (AI Image Generator)
Provide TWO versions of the image prompt:

ENGLISH (for AI image generator):
A detailed, ready-to-use prompt for Midjourney / DALL-E / Artlist / Canva.
Include: subject, style, mood, lighting, colors, composition. Make it on-brand for {brand['name']}.
Format: one flowing paragraph, max 80 words.

---HE---

עברית (לצוות היצירתי):
תרגום מדויק ומותאם של הפרומפט לעברית — לשימוש הצוות היצירתי הישראלי.
פסקה אחת, עד 80 מילים.

---
כתוב בעברית בלבד (חוץ מהפרומפט לתמונה). שמור על הטון האותנטי של {brand['name']}.
"""


# =============================================================
# LAYOUT CONSTANTS
# =============================================================
platform_display = {
    "instagram": "📸 Instagram",
    "tiktok":    "🎵 TikTok",
    "facebook":  "👥 Facebook",
}

# Reload brands fresh on every render
BRAND_PROFILES = load_brands() or _FALLBACK_PROFILES

# =============================================================
# PAGE HEADER + LANGUAGE TOGGLE
# =============================================================
col_hdr, col_lang = st.columns([11, 1])

with col_hdr:
    st.markdown(
        f"""
        <div class="main-header">
            <h1>🚀 Marketing Hub</h1>
            <p style="color:#666; font-size:18px;">
                {t['subtitle']} — Myst | Prime51
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_lang:
    st.markdown("<div style='padding-top:18px;'>", unsafe_allow_html=True)
    lang_choice = st.radio(
        "lang",
        options=["עב", "EN"],
        index=0 if lang == "he" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    new_lang = "he" if lang_choice == "עב" else "en"
    if new_lang != lang:
        st.session_state.lang = new_lang
        st.rerun()

st.divider()
col_output, col_controls = st.columns([10, 9], gap="large")


# ──────────────────────────────────────────────────────────────
# RIGHT COLUMN — Controls
# ──────────────────────────────────────────────────────────────
with col_controls:

    if st.session_state.has_content:
        st.info(f"{t['edit_mode_label']} **{st.session_state.saved_brand}**")
        if st.button(t["new_content_btn"], use_container_width=True):
            for k in ["api_messages","chat_display","system_prompt","has_content",
                      "latest_content","approved","pending_refinement","saved_brand",
                      "saved_brand_key","saved_brand_emoji","saved_platform",
                      "saved_type","saved_brief","library_saved"]:
                st.session_state[k] = [] if k in ("api_messages","chat_display") \
                    else "" if isinstance(st.session_state[k], str) \
                    else False if isinstance(st.session_state[k], bool) \
                    else None
            st.session_state.input_counter = 0
            # Reset section selection checkboxes
            for sec_key in list(st.session_state.keys()):
                if sec_key.startswith("sec_sel_"):
                    del st.session_state[sec_key]
            st.rerun()
        st.divider()

    st.markdown(
        '<div style="background:#f4f4fb;border-radius:12px;padding:18px 20px 10px 20px;margin-bottom:12px;">',
        unsafe_allow_html=True,
    )
    st.markdown(f"#### {t['settings_header']}")

    brand_display_map  = {k: f"{v['emoji']} {v['name']}" for k, v in BRAND_PROFILES.items()}
    selected_brand_key = st.selectbox(
        t["brand_label"],
        options=list(brand_display_map.keys()),
        format_func=lambda x: brand_display_map[x],
        disabled=st.session_state.has_content,
    )
    selected_brand = BRAND_PROFILES[selected_brand_key]

    primary_platform = next(
        p for p, d in selected_brand["platforms"].items() if d["priority"] == "primary"
    )
    selected_platform = st.selectbox(
        t["platform_label"],
        options=list(platform_display.keys()),
        format_func=lambda x: platform_display[x],
        index=list(platform_display.keys()).index(primary_platform),
        disabled=st.session_state.has_content,
    )
    plat_priority = selected_brand["platforms"].get(selected_platform, {}).get("priority", "")
    st.caption(t["primary_platform_cap"] if plat_priority == "primary" else t["secondary_platform_cap"])

    content_display_map   = {k: f"{v['emoji']} {v['label']}" for k, v in CONTENT_TYPES.items()}
    selected_content_type = st.selectbox(
        t["content_type_label"],
        options=list(content_display_map.keys()),
        format_func=lambda x: content_display_map[x],
        disabled=st.session_state.has_content,
    )
    st.caption(CONTENT_TYPES[selected_content_type]["description"])

    with st.expander(t["advanced_options"]):
        num_versions = st.slider(
            t["num_versions_label"], min_value=1, max_value=3, value=1,
            disabled=st.session_state.has_content,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"#### {t['brief_header']}")

    brief = st.text_area(
        t["brief_what"],
        placeholder=t["brief_placeholder"],
        height=150,
        label_visibility="collapsed",
        disabled=st.session_state.has_content,
    )

    additional_notes = st.text_area(
        t["extra_notes_label"],
        placeholder=t["extra_notes_placeholder"],
        height=70,
        disabled=st.session_state.has_content,
    )

    with st.expander(t["tips_brief_header"]):
        st.markdown(t["tips_brief_table"])

    st.divider()

    can_generate = bool(brief.strip()) and not st.session_state.has_content
    btn_label = (
        t["generate_btn_multi"].format(n=num_versions)
        if num_versions > 1
        else t["generate_btn_single"].format(
            emoji=CONTENT_TYPES[selected_content_type]["emoji"],
            label=CONTENT_TYPES[selected_content_type]["label"],
        )
    )
    generate = st.button(
        btn_label, type="primary", disabled=not can_generate, use_container_width=True,
    )
    if not brief.strip() and not st.session_state.has_content:
        st.warning(t["fill_brief_warning"])

    st.caption(t["powered_by"])

    if st.session_state.has_content:
        st.markdown("---")
        st.markdown(f"#### {t['tips_refine_header']}")
        with st.expander(t["tips_refine_expander"]):
            st.markdown(t["tips_refine_content"])


# ──────────────────────────────────────────────────────────────
# LEFT COLUMN — Output
# ──────────────────────────────────────────────────────────────
with col_output:
    st.markdown(f"#### {t['content_chat_header']}")

    # ══ CASE 1: Generate initial content ══════════════════════
    if generate and can_generate:

        # ── Scan real product links from brand website ─────────
        product_links = ""
        brand_website = selected_brand.get("website", "").strip()
        if brand_website:
            with st.spinner("🔗 סורק מוצרים מאתר המותג..."):
                product_links = get_product_links(selected_brand)

        # ── Phase 2: scan curated web sources ──────────────────
        web_awareness  = ""
        active_sources = [
            s for s in selected_brand.get("web_sources", [])
            if s.get("active", True) and str(s.get("url", "")).strip()
        ]
        if active_sources:
            n      = len(active_sources)
            suffix = "ות" if (lang == "he" and n > 1) else ("s" if n > 1 else "")
            spinner_msg = t["scanning_sources"].format(n=n, suffix=suffix)
            with st.spinner(spinner_msg):
                web_awareness = get_brand_awareness(selected_brand)

        system_prompt = build_system_prompt(
            selected_brand_key,
            web_awareness=web_awareness,
            product_links=product_links,
        )
        user_prompt   = build_initial_user_prompt(
            selected_brand_key, selected_platform, selected_content_type,
            brief, additional_notes, num_versions,
        )

        scan_note = (t["scan_note"].format(n=len(active_sources)) if active_sources else "")
        label_str  = CONTENT_TYPES[selected_content_type]["label"]
        st.caption(f"**{label_str}** · **{selected_brand['name']}** · **{platform_display[selected_platform]}**{scan_note}")

        st.session_state.system_prompt     = system_prompt
        st.session_state.api_messages      = [{"role": "user", "content": user_prompt}]
        st.session_state.saved_brand       = selected_brand["name"]
        st.session_state.saved_brand_key   = selected_brand_key
        st.session_state.saved_brand_emoji = selected_brand.get("emoji", "🏢")
        st.session_state.saved_platform    = platform_display[selected_platform]
        st.session_state.saved_type        = label_str
        st.session_state.saved_brief       = brief.strip()
        st.session_state.library_saved     = False

        response_text = do_stream(st.session_state.api_messages, system_prompt, use_thinking=True)

        if response_text and not response_text.startswith("❌"):
            st.session_state.api_messages.append({"role": "assistant", "content": response_text})
            st.session_state.chat_display = [{
                "role":    "assistant",
                "content": response_text,
                "label":   t["first_version_label"].format(label=label_str),
            }]
            st.session_state.latest_content = response_text
            st.session_state.has_content    = True
            st.rerun()

    # ══ CASE 2: Refinement pending ════════════════════════════
    elif st.session_state.has_content and st.session_state.pending_refinement:
        refinement_text                     = st.session_state.pending_refinement
        st.session_state.pending_refinement = None

        display_full_history_for_streaming(st.session_state.chat_display)

        version_num = sum(1 for m in st.session_state.chat_display if m["role"] == "assistant") + 1
        st.caption(t["updating_version"].format(n=version_num))

        response_text = do_stream(
            st.session_state.api_messages,
            st.session_state.system_prompt,
            use_thinking=False,
        )

        if response_text and not response_text.startswith("❌"):
            st.session_state.api_messages.append({"role": "assistant", "content": response_text})
            st.session_state.chat_display.append({
                "role":    "assistant",
                "content": response_text,
                "label":   t["version_label"].format(n=version_num),
            })
            st.session_state.latest_content = response_text
            st.session_state.approved       = False
            st.rerun()

    # ══ CASE 3: Normal display ════════════════════════════════
    elif st.session_state.has_content:

        improvement_count = sum(1 for m in st.session_state.chat_display if m["role"] == "user")
        if len(st.session_state.chat_display) > 1:
            impr_word = (
                t["improvement_plural"] if improvement_count != 1 else t["improvement_singular"]
            )
            with st.expander(
                t["history_expander"].format(n=improvement_count, word=impr_word),
                expanded=False,
            ):
                display_compact_history(st.session_state.chat_display)

        latest_msg   = next(
            (m for m in reversed(st.session_state.chat_display) if m["role"] == "assistant"), None,
        )
        latest_label = latest_msg.get("label", "") if latest_msg else ""
        st.markdown(
            f'<div class="version-label current">📄 {latest_label}</div>',
            unsafe_allow_html=True,
        )

        display_content_sections(
            st.session_state.latest_content,
            uid_prefix=f"v{improvement_count}",
            section_config=SECTION_CONFIG,
        )

        # ── Refinement input ──────────────────────────────────
        if not st.session_state.approved:
            st.markdown('<div class="refine-box">', unsafe_allow_html=True)
            st.markdown(
                f'<div style="direction:{D};text-align:{A};font-size:13px;'
                f'font-weight:600;color:#4a4a8a;margin-bottom:6px;">'
                f'{t["refine_prompt"]}</div>',
                unsafe_allow_html=True,
            )

            refine_key  = f"refine_ta_{st.session_state.input_counter}"
            refine_text = st.text_area(
                "refine",
                placeholder=t["refine_placeholder"],
                height=85,
                label_visibility="collapsed",
                key=refine_key,
            )
            col_send, _ = st.columns([3, 1])
            with col_send:
                send_btn = st.button(t["send_refine_btn"], type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if send_btn and refine_text.strip():
                st.session_state.api_messages.append({"role": "user", "content": refine_text.strip()})
                st.session_state.chat_display.append({"role": "user", "content": refine_text.strip()})
                st.session_state.pending_refinement = refine_text.strip()
                st.session_state.input_counter += 1
                st.rerun()

        # ── Approve / Save ────────────────────────────────────
        st.markdown("---")

        if st.session_state.approved:
            st.success(t["approved_success"])

            if st.session_state.library_saved:
                st.info(t["library_saved_info"])
            else:
                # Section selection hint
                sections_exist = bool(
                    parse_content_sections(st.session_state.latest_content)
                )
                if sections_exist:
                    st.markdown(
                        f'<div style="font-size:12px;color:#888;margin-bottom:4px;">'
                        f'{t["sec_select_label"]}</div>',
                        unsafe_allow_html=True,
                    )

                if st.button(t["save_library_btn"], type="primary", use_container_width=True):
                    content_to_save = build_save_content(st.session_state.latest_content)
                    add_to_library({
                        "brand_key":    st.session_state.saved_brand_key,
                        "brand_name":   st.session_state.saved_brand,
                        "brand_emoji":  st.session_state.saved_brand_emoji,
                        "platform":     st.session_state.saved_platform,
                        "content_type": st.session_state.saved_type,
                        "brief":        st.session_state.saved_brief,
                        "content":      content_to_save,
                        "notes":        "",
                    })
                    st.session_state.library_saved = True
                    st.rerun()

            st.download_button(
                t["download_approved_btn"],
                data=st.session_state.latest_content,
                file_name=f"{st.session_state.saved_brand.replace(' ', '_')}_approved.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            col_approve, col_save = st.columns(2)
            with col_approve:
                if st.button(t["approve_btn"], type="primary", use_container_width=True):
                    st.session_state.approved = True
                    st.rerun()
            with col_save:
                st.download_button(
                    t["save_draft_btn"],
                    data=st.session_state.latest_content,
                    file_name=f"{st.session_state.saved_brand.replace(' ', '_')}_draft.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

    # ══ CASE 4: Empty state ════════════════════════════════════
    else:
        st.markdown(
            f"""
            <div style="
                background:linear-gradient(135deg,#f8f9ff 0%,#f0f2ff 100%);
                border-radius:12px; padding:60px 30px; text-align:center;
                color:#aaa; border:2px dashed #d0d5ff; margin-top:8px;
                min-height:400px; display:flex; flex-direction:column;
                align-items:center; justify-content:center;">
                <div style="font-size:60px;margin-bottom:16px;">💬</div>
                <div style="font-size:20px;color:#888;font-weight:600;">{t['empty_chat_title']}</div>
                <div style="font-size:14px;color:#bbb;margin-top:10px;">
                    {t['empty_chat_sub']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================
# FOOTER — Status bar
# =============================================================
st.divider()
improvement_count_footer = sum(1 for m in st.session_state.chat_display if m["role"] == "user")
col_f1, col_f2, col_f3, col_f4 = st.columns(4)
col_f1.metric(t["brand_metric"],       st.session_state.saved_brand or selected_brand["name"])
col_f2.metric(t["platform_metric"],    (st.session_state.saved_platform or platform_display[selected_platform]).split(" ")[-1])
col_f3.metric(t["improvements_metric"], improvement_count_footer)
col_f4.metric(
    t["status_metric"],
    t["status_approved"] if st.session_state.approved
    else (t["status_working"] if st.session_state.has_content else t["status_waiting"]),
)
