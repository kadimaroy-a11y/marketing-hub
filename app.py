# =============================================================
# 🚀 MARKETING HUB — Main Application v2.1 (Chat + Sections)
# =============================================================
# Powered by Claude AI
# Built for: Pupik Group — Myst & Prime51
# v2.1: Inline chat refinement + parsed section boxes with copy
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
# STYLING
# =============================================================
st.markdown("""
<style>
    /* ── Page header ── */
    .main-header { text-align: center; padding: 10px 0 20px 0; }

    /* ── RTL: All text inputs ── */
    textarea {
        direction: rtl !important;
        text-align: right !important;
        font-family: Arial, Helvetica, sans-serif !important;
    }

    /* ── Section header label ── */
    .section-header {
        direction: rtl;
        text-align: right;
        font-weight: 700;
        font-size: 14px;
        color: #4a4a8a;
        margin: 14px 0 4px 0;
        letter-spacing: 0.3px;
    }

    /* ── Main content box (per section) ── */
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

    /* ── Streaming / single-box (used during generation) ── */
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

    /* ── User refinement bubble ── */
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

    /* ── Version label ── */
    .version-label {
        direction: rtl;
        text-align: right;
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

    @keyframes blink { 50% { opacity: 0; } }

    /* ── RTL: Labels, captions, text ── */
    label,
    .stCaption p,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stText"] {
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
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


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
        "saved_platform":     "",
        "saved_type":         "",
        "input_counter":      0,   # incremented to clear refinement textarea
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


# =============================================================
# SECTION PARSING
# =============================================================
SECTION_CONFIG = [
    ("caption",  "📝", "כיתוב ראשי"),
    ("hashtags", "#️⃣", "האשטגים"),
    ("visual",   "🎬", "כיוון ויזואלי"),
    ("story",    "📱", "גרסת סטורי"),
]


def parse_content_sections(content: str) -> dict:
    """Split Claude output into named sections using emoji markers."""
    sections = {}
    marker_emojis = {
        "caption":  ["📝"],
        "hashtags": ["#️⃣", "️⃣", "#⃣"],
        "visual":   ["🎬"],
        "story":    ["📱"],
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
        content_end = positions[i + 1][0] if i + 1 < len(positions) else len(content)
        text = content[content_start:content_end].strip().rstrip('-').strip()
        sections[key] = text

    return sections


# =============================================================
# COPY BUTTON (JS clipboard — works on localhost + HTTPS)
# =============================================================
def copy_button(text: str, uid: str):
    """Render a copy-to-clipboard button inside an iframe component."""
    safe_js = json.dumps(text)   # handles all escaping correctly
    btn_id  = f"btn_{uid}"

    components.html(f"""
    <button id="{btn_id}"
        onclick="
            var t = {safe_js};
            var btn = document.getElementById('{btn_id}');
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(t).then(function() {{
                    btn.innerHTML = '✅ הועתק!';
                    btn.style.background = '#4CAF50';
                    setTimeout(function() {{
                        btn.innerHTML = '📋 העתק';
                        btn.style.background = '#6c63ff';
                    }}, 2000);
                }});
            }} else {{
                var el = document.createElement('textarea');
                el.value = t;
                el.style.position = 'fixed';
                el.style.opacity = '0';
                document.body.appendChild(el);
                el.select();
                document.execCommand('copy');
                document.body.removeChild(el);
                btn.innerHTML = '✅ הועתק!';
                setTimeout(function() {{ btn.innerHTML = '📋 העתק'; }}, 2000);
            }}
        "
        style="
            background: #6c63ff;
            color: white;
            border: none;
            padding: 5px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-family: Arial;
        "
    >📋 העתק</button>
    """, height=36, scrolling=False)


# =============================================================
# SECTION DISPLAY — parsed boxes with copy buttons
# =============================================================
def display_content_sections(content: str, uid_prefix: str = "sec"):
    """Parse content and render each section as its own box + copy button."""
    sections = parse_content_sections(content)

    if not sections:
        # Fallback: full content in one box
        safe = html_lib.escape(content)
        st.markdown(f'<div class="rtl-stream">{safe}</div>', unsafe_allow_html=True)
        return

    for i, (key, emoji, hebrew_title) in enumerate(SECTION_CONFIG):
        text = sections.get(key, "")
        if not text:
            continue

        # Header row: title left, copy button right
        col_title, col_btn = st.columns([7, 2])
        with col_title:
            st.markdown(
                f'<div class="section-header">{emoji} {hebrew_title}</div>',
                unsafe_allow_html=True,
            )
        with col_btn:
            copy_button(text, uid=f"{uid_prefix}_{i}")

        # Content box
        safe = html_lib.escape(text)
        st.markdown(f'<div class="rtl-output">{safe}</div>', unsafe_allow_html=True)

        if i < len(SECTION_CONFIG) - 1:
            st.markdown(
                '<div style="margin-bottom: 6px;"></div>',
                unsafe_allow_html=True,
            )


# =============================================================
# COMPACT HISTORY — shown in expander for previous versions
# =============================================================
def display_compact_history(messages_list: list):
    """Show previous chat exchanges (all except the latest AI response)."""
    # Drop the last assistant message — that's displayed separately
    display_list = messages_list[:-1] if (
        messages_list and messages_list[-1]["role"] == "assistant"
    ) else messages_list

    for msg in display_list:
        if msg["role"] == "user":
            safe = html_lib.escape(msg["content"])
            st.markdown(
                f'<div class="user-bubble">💬 {safe}</div>',
                unsafe_allow_html=True,
            )
        else:
            label = msg.get("label", "גרסה")
            st.caption(f"🤖 {label}")
            # Show only the caption portion to keep it compact
            sections = parse_content_sections(msg["content"])
            preview = sections.get("caption", msg["content"])
            preview = (preview[:300] + "...") if len(preview) > 300 else preview
            safe = html_lib.escape(preview)
            st.markdown(
                f'<div class="rtl-output" style="font-size:13px; line-height:1.6; min-height:40px;">'
                f'{safe}</div>',
                unsafe_allow_html=True,
            )


# =============================================================
# STREAMING — renders into current column context
# =============================================================
def do_stream(messages: list, system_prompt: str, use_thinking: bool = False) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("❌ שגיאה: לא נמצא מפתח API. בדוק שקובץ .env קיים.")
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
        # Remove cursor on completion
        safe = html_lib.escape(full_text)
        placeholder.markdown(
            f'<div class="rtl-stream">{safe}</div>',
            unsafe_allow_html=True,
        )
    except anthropic.AuthenticationError:
        full_text = "❌ מפתח API לא תקין."
        placeholder.error(full_text)
    except anthropic.RateLimitError:
        full_text = "❌ הגעת למגבלת קריאות. נסה שוב בעוד כמה שניות."
        placeholder.error(full_text)
    except Exception as e:
        full_text = f"❌ שגיאה: {str(e)}"
        placeholder.error(full_text)

    return full_text


# =============================================================
# STREAMING — chat history renderer (used while pending)
# =============================================================
def display_full_history_for_streaming(messages_list: list):
    """Show full thread (all messages) while a new response is streaming."""
    for msg in messages_list:
        if msg["role"] == "user":
            safe = html_lib.escape(msg["content"])
            st.markdown(
                f'<div class="user-bubble">💬 {safe}</div>',
                unsafe_allow_html=True,
            )
        else:
            label = msg.get("label", "🤖 גרסה")
            st.markdown(
                f'<div class="version-label">{label}</div>',
                unsafe_allow_html=True,
            )
            safe = html_lib.escape(msg["content"])
            st.markdown(
                f'<div class="rtl-stream">{safe}</div>',
                unsafe_allow_html=True,
            )


# =============================================================
# PROMPT BUILDERS (unchanged from v2.0)
# =============================================================
def build_system_prompt(brand_key: str) -> str:
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
- שמור על אותו פורמט (📝 כיתוב ראשי / #️⃣ האשטגים / 🎬 כיוון ויזואלי / 📱 גרסת סטורי)
- אלא אם התבקשת במפורש לשנות את הפורמט
- החזר את הפוסט המעודכן במלואו, מוכן לפרסום
{_build_knowledge_base_section(brand)}"""


def _build_knowledge_base_section(brand: dict) -> str:
    """Append accumulated brand knowledge to the system prompt if any exists."""
    kb = brand.get("knowledge_base", {})
    if not kb:
        return ""

    sections = []

    if kb.get("what_works"):
        sections.append(
            "מה עובד טוב (לפי ניסיון הצוות):\n" +
            "\n".join(f"  ✅ {x}" for x in kb["what_works"])
        )
    if kb.get("what_doesnt"):
        sections.append(
            "מה לא עובד (לפי ניסיון הצוות):\n" +
            "\n".join(f"  ❌ {x}" for x in kb["what_doesnt"])
        )
    if kb.get("competitors"):
        sections.append(
            "מתחרים — שים לב להתבדל מהם:\n" +
            "\n".join(f"  🏆 {x}" for x in kb["competitors"])
        )
    if kb.get("team_notes"):
        sections.append(
            "הערות מצוות השיווק:\n" +
            "\n".join(f"  📝 {x}" for x in kb["team_notes"])
        )
    if kb.get("approved_hashtags"):
        sections.append(
            "האשטגים מאושרים לשימוש:\n" +
            "  " + "  ".join(f"#{x}" for x in kb["approved_hashtags"])
        )

    if not sections:
        return ""

    return (
        "\n\n═══════════════════════════════════════\n"
        " ידע נצבר מניסיון הצוות\n"
        "═══════════════════════════════════════\n\n" +
        "\n\n".join(sections)
    )


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

---
כתוב בעברית בלבד. שמור על הטון האותנטי של {brand['name']}.
"""


# =============================================================
# LAYOUT CONSTANTS
# =============================================================
platform_display = {
    "instagram": "📸 Instagram",
    "tiktok":    "🎵 TikTok",
    "facebook":  "👥 Facebook",
}

# Reload brands fresh on every render so Brand Manager edits show immediately
BRAND_PROFILES = load_brands() or _FALLBACK_PROFILES

# =============================================================
# PAGE HEADER
# =============================================================
st.markdown(
    """
    <div class="main-header">
        <h1>🚀 Marketing Hub</h1>
        <p style="color: #666; font-size: 18px;">
            יוצר תוכן חכם לסושיאל מדיה — Myst | Prime51
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

col_output, col_controls = st.columns([10, 9], gap="large")


# ──────────────────────────────────────────────────────────────
# RIGHT COLUMN — Controls
# ──────────────────────────────────────────────────────────────
with col_controls:

    if st.session_state.has_content:
        st.info(f"📝 מצב עריכה: **{st.session_state.saved_brand}**")
        if st.button("🆕 התחל תוכן חדש", use_container_width=True):
            st.session_state.api_messages       = []
            st.session_state.chat_display       = []
            st.session_state.system_prompt      = ""
            st.session_state.has_content        = False
            st.session_state.latest_content     = ""
            st.session_state.approved           = False
            st.session_state.pending_refinement = None
            st.session_state.saved_brand        = ""
            st.session_state.saved_platform     = ""
            st.session_state.saved_type         = ""
            st.session_state.input_counter      = 0
            st.rerun()
        st.divider()

    st.markdown(
        '<div style="background:#f4f4fb; border-radius:12px; padding:18px 20px 10px 20px; margin-bottom:12px;">',
        unsafe_allow_html=True,
    )
    st.markdown("#### ⚙️ הגדרות")

    brand_display_map = {k: f"{v['emoji']} {v['name']}" for k, v in BRAND_PROFILES.items()}
    selected_brand_key = st.selectbox(
        "🏷️ מותג",
        options=list(brand_display_map.keys()),
        format_func=lambda x: brand_display_map[x],
        disabled=st.session_state.has_content,
    )
    selected_brand = BRAND_PROFILES[selected_brand_key]

    primary_platform = next(
        p for p, d in selected_brand["platforms"].items() if d["priority"] == "primary"
    )
    selected_platform = st.selectbox(
        "📡 פלטפורמה",
        options=list(platform_display.keys()),
        format_func=lambda x: platform_display[x],
        index=list(platform_display.keys()).index(primary_platform),
        disabled=st.session_state.has_content,
    )
    plat_priority = selected_brand["platforms"].get(selected_platform, {}).get("priority", "")
    st.caption("⭐ פלטפורמה ראשית" if plat_priority == "primary" else "📌 פלטפורמה משנית")

    content_display_map = {k: f"{v['emoji']} {v['label']}" for k, v in CONTENT_TYPES.items()}
    selected_content_type = st.selectbox(
        "📄 סוג תוכן",
        options=list(content_display_map.keys()),
        format_func=lambda x: content_display_map[x],
        disabled=st.session_state.has_content,
    )
    st.caption(CONTENT_TYPES[selected_content_type]["description"])

    with st.expander("🔧 אפשרויות מתקדמות"):
        num_versions = st.slider(
            "מספר גרסאות", min_value=1, max_value=3, value=1,
            disabled=st.session_state.has_content,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("#### 📝 הבריף שלך")

    brief = st.text_area(
        "מה אתה רוצה לפרסם?",
        placeholder=(
            "לדוגמה:\n"
            "הגיעו לנו פאנקו חדשים של ספיידרמן אקרוס דה ספיידר ורס. "
            "יש 5 דמויות — מיילס מוראלס, גוון, ספיידר-פאנק, ספיידר-וומן. "
            "מחיר 89 ש\"ח ליחידה."
        ),
        height=150,
        label_visibility="collapsed",
        disabled=st.session_state.has_content,
    )

    additional_notes = st.text_area(
        "הערות נוספות (אופציונלי)",
        placeholder="לדוגמה: יש מלאי מוגבל, יש מבצע השבוע...",
        height=70,
        disabled=st.session_state.has_content,
    )

    with st.expander("💡 טיפים לבריף טוב"):
        st.markdown("""
| סוג | מה לכלול |
|---|---|
| **מוצר חדש** | שם + מה מיוחד + מחיר |
| **אירוע** | תאריך + שעה + למי |
| **מבצע** | מה + כמה % + עד מתי |
| **אנבוקסינג** | תאר מה נפתח |
| **טרנד** | לאיזה סרט/סדרה קשור |
        """)

    st.divider()

    can_generate = bool(brief.strip()) and not st.session_state.has_content
    btn_label = (
        f"✨ צור {num_versions} גרסאות"
        if num_versions > 1
        else f"✨ צור {CONTENT_TYPES[selected_content_type]['emoji']} {CONTENT_TYPES[selected_content_type]['label']}"
    )
    generate = st.button(
        btn_label, type="primary", disabled=not can_generate, use_container_width=True,
    )
    if not brief.strip() and not st.session_state.has_content:
        st.warning("⬆️ מלא את הבריף כדי להפעיל")

    st.caption("Powered by Claude AI · 💬 Chat Mode v2.1")

    if st.session_state.has_content:
        st.markdown("---")
        st.markdown("#### 💡 טיפים לשיפור")
        with st.expander("מה אפשר לבקש?"):
            st.markdown("""
- 🎭 **טון**: `יותר מצחיק` / `יותר רציני` / `יותר אנרגטי`
- ✂️ **אורך**: `קצר יותר` / `הרחב את הכיתוב`
- ⚡ **FOMO**: `הוסף תחושת דחיפות ומלאי מוגבל`
- 🔁 **מבנה**: `שנה את הפתיחה` / `הוסף CTA חזק יותר`
- #️⃣ **האשטגים**: `שנה את האשטגים`
- 🎨 **ויזואל**: `כיוון ויזואלי שונה / יותר דרמטי`
- 📱 **סטורי**: `סטורי קצר ומצחיק יותר`
            """)


# ──────────────────────────────────────────────────────────────
# LEFT COLUMN — Output
# ──────────────────────────────────────────────────────────────
with col_output:
    st.markdown("#### 🎨 שיחת תוכן")

    # ══ CASE 1: Generate initial content ══════════════════════
    if generate and can_generate:
        system_prompt = build_system_prompt(selected_brand_key)
        user_prompt   = build_initial_user_prompt(
            selected_brand_key, selected_platform, selected_content_type,
            brief, additional_notes, num_versions,
        )

        st.caption(
            f"יוצר **{CONTENT_TYPES[selected_content_type]['label']}** "
            f"עבור **{selected_brand['name']}** "
            f"על **{platform_display[selected_platform]}** ..."
        )

        st.session_state.system_prompt  = system_prompt
        st.session_state.api_messages   = [{"role": "user", "content": user_prompt}]
        st.session_state.saved_brand    = selected_brand["name"]
        st.session_state.saved_platform = platform_display[selected_platform]
        st.session_state.saved_type     = CONTENT_TYPES[selected_content_type]["label"]

        response_text = do_stream(
            st.session_state.api_messages, system_prompt, use_thinking=True,
        )

        if response_text and not response_text.startswith("❌"):
            st.session_state.api_messages.append(
                {"role": "assistant", "content": response_text}
            )
            st.session_state.chat_display = [{
                "role":    "assistant",
                "content": response_text,
                "label":   f"✨ גרסה ראשונה — {CONTENT_TYPES[selected_content_type]['label']}",
            }]
            st.session_state.latest_content = response_text
            st.session_state.has_content    = True
            st.rerun()

    # ══ CASE 2: Refinement pending — stream in column ══════════
    elif st.session_state.has_content and st.session_state.pending_refinement:
        refinement_text                     = st.session_state.pending_refinement
        st.session_state.pending_refinement = None

        # Show full thread so far (user bubble is already in chat_display)
        display_full_history_for_streaming(st.session_state.chat_display)

        version_num = sum(
            1 for m in st.session_state.chat_display if m["role"] == "assistant"
        ) + 1
        st.caption(f"מעדכן לגרסה {version_num}...")

        response_text = do_stream(
            st.session_state.api_messages,
            st.session_state.system_prompt,
            use_thinking=False,
        )

        if response_text and not response_text.startswith("❌"):
            st.session_state.api_messages.append(
                {"role": "assistant", "content": response_text}
            )
            st.session_state.chat_display.append({
                "role":    "assistant",
                "content": response_text,
                "label":   f"✏️ גרסה {version_num}",
            })
            st.session_state.latest_content = response_text
            st.session_state.approved       = False
            st.rerun()

    # ══ CASE 3: Normal display ════════════════════════════════
    elif st.session_state.has_content:

        # ── Chat history (collapsed if more than 1 round) ─────
        improvement_count = sum(
            1 for m in st.session_state.chat_display if m["role"] == "user"
        )
        if len(st.session_state.chat_display) > 1:
            with st.expander(
                f"📜 היסטוריית שיחה — {improvement_count} שיפור{'ים' if improvement_count != 1 else ''}",
                expanded=False,
            ):
                display_compact_history(st.session_state.chat_display)

        # ── Latest version label ──────────────────────────────
        latest_msg   = next(
            (m for m in reversed(st.session_state.chat_display) if m["role"] == "assistant"),
            None,
        )
        latest_label = latest_msg.get("label", "גרסה נוכחית") if latest_msg else "גרסה נוכחית"
        st.markdown(
            f'<div class="version-label current">📄 {latest_label}</div>',
            unsafe_allow_html=True,
        )

        # ── Parsed section boxes with copy buttons ────────────
        display_content_sections(
            st.session_state.latest_content,
            uid_prefix=f"v{improvement_count}",
        )

        # ── Refinement input (inline, above confirm) ──────────
        if not st.session_state.approved:
            st.markdown(
                '<div class="refine-box">',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div style="direction:rtl; text-align:right; font-size:13px; '
                'font-weight:600; color:#4a4a8a; margin-bottom:6px;">💬 רוצה לשנות משהו?</div>',
                unsafe_allow_html=True,
            )

            refine_key  = f"refine_ta_{st.session_state.input_counter}"
            refine_text = st.text_area(
                "שיפור",
                placeholder=(
                    "לדוגמה: 'יותר מצחיק' / 'קצר יותר' / "
                    "'הוסף FOMO' / 'שנה את הפתיחה' / 'שנה את האשטגים'..."
                ),
                height=85,
                label_visibility="collapsed",
                key=refine_key,
            )

            col_send, col_spacer = st.columns([3, 1])
            with col_send:
                send_btn = st.button(
                    "שלח שיפור ↩️", type="primary", use_container_width=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            if send_btn and refine_text.strip():
                st.session_state.api_messages.append(
                    {"role": "user", "content": refine_text.strip()}
                )
                st.session_state.chat_display.append(
                    {"role": "user", "content": refine_text.strip()}
                )
                st.session_state.pending_refinement = refine_text.strip()
                st.session_state.input_counter     += 1   # clears textarea on rerun
                st.rerun()

        # ── Approve / Save buttons ────────────────────────────
        st.markdown("---")

        if st.session_state.approved:
            st.success("✅ תוכן אושר! מוכן לפרסום.")
            st.download_button(
                "⬇️ הורד תוכן מאושר",
                data=st.session_state.latest_content,
                file_name=(
                    f"{st.session_state.saved_brand.replace(' ', '_')}_approved.txt"
                ),
                mime="text/plain",
                use_container_width=True,
                type="primary",
            )
        else:
            col_approve, col_save = st.columns(2)
            with col_approve:
                if st.button("✅ אשר תוכן זה", type="primary", use_container_width=True):
                    st.session_state.approved = True
                    st.rerun()
            with col_save:
                st.download_button(
                    "💾 שמור טיוטה",
                    data=st.session_state.latest_content,
                    file_name=(
                        f"{st.session_state.saved_brand.replace(' ', '_')}_draft.txt"
                    ),
                    mime="text/plain",
                    use_container_width=True,
                )

    # ══ CASE 4: Empty state ════════════════════════════════════
    else:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
                border-radius: 12px;
                padding: 60px 30px;
                text-align: center;
                color: #aaa;
                border: 2px dashed #d0d5ff;
                margin-top: 8px;
                min-height: 400px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            ">
                <div style="font-size: 60px; margin-bottom: 16px;">💬</div>
                <div style="font-size: 20px; color: #888; font-weight: 600;">מצב שיחה</div>
                <div style="font-size: 14px; color: #bbb; margin-top: 10px; direction: rtl;">
                    צור תוכן ואז שוחח עם הסוכן<br>
                    לשיפורים עד שהתוצאה מושלמת ✅
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================
# FOOTER — Status bar
# =============================================================
st.divider()
improvement_count_footer = sum(
    1 for m in st.session_state.chat_display if m["role"] == "user"
)
col_f1, col_f2, col_f3, col_f4 = st.columns(4)
col_f1.metric(
    "מותג",
    st.session_state.saved_brand or selected_brand["name"],
)
col_f2.metric(
    "פלטפורמה",
    (st.session_state.saved_platform or platform_display[selected_platform]).split(" ")[-1],
)
col_f3.metric("שיפורים", improvement_count_footer)
col_f4.metric(
    "סטטוס",
    "✅ מאושר"   if st.session_state.approved
    else ("📝 בעבודה" if st.session_state.has_content else "⏳ ממתין"),
)
