# =============================================================
# 🎨 PAGE BUILDER — AI Web Page Generator
# =============================================================
# Generates complete, responsive HTML/CSS landing pages,
# product pages, event pages, and more — branded and ready
# to deploy. Uses Claude's web design expertise + brand DNA.
# =============================================================

import streamlit as st
import streamlit.components.v1 as components
import anthropic
import os
import re
from dotenv import load_dotenv
from db import load_brands
from brand_profiles import BRAND_PROFILES as _FALLBACK_PROFILES
from web_design_brain import build_web_design_prompt, PAGE_TYPES, BRAND_WEB_STYLES
from translations import get_t

load_dotenv()

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="🎨 Page Builder",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ───────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "he"
if "pb_html" not in st.session_state:
    st.session_state.pb_html = ""
if "pb_messages" not in st.session_state:
    st.session_state.pb_messages = []
if "pb_chat_display" not in st.session_state:
    st.session_state.pb_chat_display = []
if "pb_system_prompt" not in st.session_state:
    st.session_state.pb_system_prompt = ""
if "pb_pending_refinement" not in st.session_state:
    st.session_state.pb_pending_refinement = None

lang = st.session_state.lang
t = get_t(lang)
D = t["dir"]
A = t["align"]

BRAND_PROFILES = load_brands() or _FALLBACK_PROFILES
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── UI Strings ──────────────────────────────────────────────
UI = {
    "he": {
        "title": "בונה דפים 🎨",
        "subtitle": "צור דפי נחיתה, מוצר, אירוע ועוד — מותאמים למותג, מוכנים לפרסום",
        "brand": "מותג 🏷️",
        "page_type": "סוג דף 📄",
        "brief": "תאר את הדף שאתה רוצה 📝",
        "brief_placeholder": "לדוגמה: דף נחיתה למבצע פאנקו פופ — 30% הנחה על כל הקולקציה, מלאי מוגבל, כולל countdown timer ותמונות מוצרים",
        "generate": "🚀 צור דף",
        "generating": "מעצב את הדף...",
        "preview": "תצוגה מקדימה 👀",
        "code": "קוד HTML 💻",
        "download": "⬇️ הורד HTML",
        "refine": "שפר את הדף ✨",
        "refine_placeholder": "מה לשנות? לדוגמה: תגדיל את הכפתור, תשנה את הצבע לכחול, תוסיף section של ביקורות...",
        "refine_send": "שלח 🔄",
        "tips_title": "💡 טיפים לבריף טוב",
        "tips": [
            "תאר את המטרה: מכירה? הרשמה? מידע?",
            "ציין מוצרים/תכנים ספציפיים",
            "ציין אם יש מבצע, countdown, או תאריך",
            "ציין CTA רצוי: 'קנה עכשיו', 'הירשם', 'צור קשר'",
            "ציין sections שאתה רוצה: hero, benefits, FAQ...",
        ],
        "new_page": "🔄 דף חדש",
        "chat_title": "💬 שיחת עיצוב",
        "settings": "⚙️ הגדרות",
        "include_dark": "כלול Dark Mode",
        "include_animations": "כלול אנימציות",
        "language_dir": "כיוון שפה",
    },
    "en": {
        "title": "Page Builder 🎨",
        "subtitle": "Create landing pages, product pages, event pages & more — branded and ready to publish",
        "brand": "Brand 🏷️",
        "page_type": "Page Type 📄",
        "brief": "Describe the page you want 📝",
        "brief_placeholder": "e.g.: Landing page for a Funko Pop sale — 30% off entire collection, limited stock, include countdown timer and product images",
        "generate": "🚀 Generate Page",
        "generating": "Designing your page...",
        "preview": "Preview 👀",
        "code": "HTML Code 💻",
        "download": "⬇️ Download HTML",
        "refine": "Refine Page ✨",
        "refine_placeholder": "What to change? e.g.: make the button bigger, change color to blue, add a reviews section...",
        "refine_send": "Send 🔄",
        "tips_title": "💡 Tips for a good brief",
        "tips": [
            "Describe the goal: sale? signup? info?",
            "Mention specific products/content",
            "Mention any sale, countdown, or date",
            "Specify desired CTA: 'Buy Now', 'Sign Up', 'Contact Us'",
            "Specify sections you want: hero, benefits, FAQ...",
        ],
        "new_page": "🔄 New Page",
        "chat_title": "💬 Design Chat",
        "settings": "⚙️ Settings",
        "include_dark": "Include Dark Mode",
        "include_animations": "Include Animations",
        "language_dir": "Language Direction",
    }
}

ui = UI[lang]


# =============================================================
# HELPER FUNCTIONS
# =============================================================

def extract_html(text: str) -> str:
    """Extract HTML from Claude's response (between ```html and ``` or full response)."""
    # Try to find ```html ... ``` block
    match = re.search(r'```html\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Try to find <!DOCTYPE or <html
    match = re.search(r'(<!DOCTYPE.*</html>)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Return as-is if it looks like HTML
    if '<html' in text.lower() or '<!doctype' in text.lower():
        return text.strip()
    return text


def build_page_system_prompt(brand_key: str, page_type: str, include_dark: bool, include_animations: bool, lang_dir: str) -> str:
    """Build the full system prompt for page generation."""
    brand = BRAND_PROFILES.get(brand_key, {})

    # Get brand basics
    brand_name = brand.get("name", brand_key)
    brand_type = brand.get("type", "")
    brand_products = "\n".join(f"  • {p}" for p in brand.get("products", []))
    brand_usp = "\n".join(f"  • {u}" for u in brand.get("usp", []))
    brand_voice_tone = brand.get("voice", {}).get("tone", "")
    brand_voice_style = brand.get("voice", {}).get("style", "")

    # Web design expertise
    web_expertise = build_web_design_prompt(page_type, brand_key, "he" if lang_dir == "rtl" else "en")

    # Build prompt
    prompt = f"""אתה מעצב ווב מומחה ומפתח Front-End בכיר שיוצר דפי אינטרנט מדהימים.
אתה בונה דף עבור: {brand_name} — {brand_type}

{web_expertise}

═══════════════════════════════════════
 📋 הנחיות טכניות
═══════════════════════════════════════

חובה:
  • צור קובץ HTML אחד שלם ועצמאי (Single File) עם CSS inline ב-<style>
  • Responsive — עובד מושלם במובייל, טאבלט ודסקטופ
  • Semantic HTML5: <header>, <main>, <section>, <footer>
  • dir="{lang_dir}" על ה-html tag
  • Google Fonts: Heebo (כותרות, weight 700-900) + Assistant (גוף, weight 400-600)
  • CSS Variables: --primary, --secondary, --accent, --bg, --text, --card-bg
  • כל הטקסט {"בעברית" if lang_dir == "rtl" else "in English"} (חוץ מ-branding)
  • תמונות: השתמש ב-placeholder מ-https://placehold.co (עם טקסט תיאורי)
  • אייקונים: Font Awesome 6 CDN (כבר כולל) או אימוג'י
  • {"כלול Dark Mode toggle עם CSS variables + JS" if include_dark else "Light mode בלבד"}
  • {"כלול אנימציות Scroll (IntersectionObserver) + Hover effects" if include_animations else "ללא אנימציות מיוחדות, רק transitions בסיסיים"}

מוצרי המותג:
{brand_products}

מה מייחד אותנו:
{brand_usp}

טון: {brand_voice_tone}
סגנון: {brand_voice_style}

═══════════════════════════════════════
 ⚠️ חשוב!
═══════════════════════════════════════

• החזר רק את קוד ה-HTML המלא — בלי הסברים, בלי markdown
• התחל ב- <!DOCTYPE html> וסיים ב- </html>
• הדף חייב להיראות מקצועי ומוכן לפרסום
• אל תשתמש ב-Lorem Ipsum — כתוב תוכן אמיתי ורלוונטי למותג
• כל כפתור CTA צריך href="#" עם onclick="alert('Coming soon!')"
"""
    return prompt


# =============================================================
# UI LAYOUT
# =============================================================

# ── Language toggle ─────────────────────────────────────────
col_lang_l, col_lang_r = st.columns([8, 2])
with col_lang_r:
    col_he, col_en = st.columns(2)
    with col_he:
        if st.checkbox("עב", value=(lang == "he"), key="pb_he"):
            if lang != "he":
                st.session_state.lang = "he"
                st.rerun()
    with col_en:
        if st.checkbox("EN", value=(lang == "en"), key="pb_en"):
            if lang != "en":
                st.session_state.lang = "en"
                st.rerun()

# ── Title ───────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding: 20px 0 10px;">
    <h1 style="font-size:2.5rem; margin:0">{ui['title']}</h1>
    <p style="color:#888; font-size:1.1rem">{ui['subtitle']}</p>
</div>
<hr style="border: none; border-top: 1px solid #eee; margin-bottom: 30px">
""", unsafe_allow_html=True)

# ── Main layout: Preview | Settings ─────────────────────────
col_preview, col_settings = st.columns([3, 1])

with col_settings:
    st.markdown(f"### {ui['settings']}")

    # Brand selection
    brand_options = {k: f"{v.get('emoji', '🏢')} {v.get('name', k)}" for k, v in BRAND_PROFILES.items()}
    selected_brand_key = st.selectbox(
        ui["brand"],
        options=list(brand_options.keys()),
        format_func=lambda x: brand_options[x],
        key="pb_brand",
    )

    # Page type selection
    page_type_options = {k: f"{v['emoji']} {v['he_label'] if lang == 'he' else v['label']}" for k, v in PAGE_TYPES.items()}
    selected_page_type = st.selectbox(
        ui["page_type"],
        options=list(page_type_options.keys()),
        format_func=lambda x: page_type_options[x],
        key="pb_page_type",
    )

    # Settings
    lang_dir = st.radio(
        ui["language_dir"],
        options=["rtl", "ltr"],
        format_func=lambda x: "עברית (RTL)" if x == "rtl" else "English (LTR)",
        horizontal=True,
        key="pb_lang_dir",
    )
    include_dark = st.checkbox(ui["include_dark"], value=False, key="pb_dark")
    include_animations = st.checkbox(ui["include_animations"], value=True, key="pb_animations")

    st.markdown("---")

    # Brief
    st.markdown(f"### {ui['brief']}")
    brief = st.text_area(
        ui["brief"],
        placeholder=ui["brief_placeholder"],
        height=150,
        key="pb_brief",
        label_visibility="collapsed",
    )

    # Tips
    with st.expander(ui["tips_title"]):
        for tip in ui["tips"]:
            st.markdown(f"• {tip}")

    # Generate button
    generate_clicked = st.button(ui["generate"], type="primary", use_container_width=True)

    # New page button
    if st.session_state.pb_html:
        if st.button(ui["new_page"], use_container_width=True):
            st.session_state.pb_html = ""
            st.session_state.pb_messages = []
            st.session_state.pb_chat_display = []
            st.session_state.pb_system_prompt = ""
            st.rerun()


# =============================================================
# GENERATION LOGIC
# =============================================================

if generate_clicked and brief.strip():
    system_prompt = build_page_system_prompt(
        selected_brand_key, selected_page_type,
        include_dark, include_animations, lang_dir,
    )
    st.session_state.pb_system_prompt = system_prompt

    user_msg = f"צור {PAGE_TYPES[selected_page_type]['he_label']} עבור {BRAND_PROFILES[selected_brand_key].get('name', selected_brand_key)}.\n\nבריף:\n{brief}"

    st.session_state.pb_messages = [{"role": "user", "content": user_msg}]
    st.session_state.pb_chat_display = [{"role": "user", "content": brief}]

    with col_preview:
        with st.spinner(ui["generating"]):
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=12000,
                system=system_prompt,
                messages=st.session_state.pb_messages,
            )
            result = response.content[0].text
            html_code = extract_html(result)
            st.session_state.pb_html = html_code
            st.session_state.pb_messages.append({"role": "assistant", "content": result})
            st.session_state.pb_chat_display.append({"role": "assistant", "content": "✅ הדף נוצר!"})
            st.rerun()


# =============================================================
# PREVIEW & CODE DISPLAY
# =============================================================

with col_preview:
    if st.session_state.pb_html:
        tab_preview, tab_code = st.tabs([ui["preview"], ui["code"]])

        with tab_preview:
            # Render HTML preview in iframe
            components.html(st.session_state.pb_html, height=800, scrolling=True)

        with tab_code:
            st.code(st.session_state.pb_html, language="html")
            st.download_button(
                label=ui["download"],
                data=st.session_state.pb_html,
                file_name=f"{selected_brand_key}_{selected_page_type}.html",
                mime="text/html",
                use_container_width=True,
            )

        # ── Refinement Chat ────────────────────────────────
        st.markdown(f"### {ui['chat_title']}")

        # Show chat history
        for msg in st.session_state.pb_chat_display:
            role_label = "👤" if msg["role"] == "user" else "🎨"
            st.markdown(f"**{role_label}** {msg['content']}")

        # Refinement input
        refinement = st.text_input(
            ui["refine"],
            placeholder=ui["refine_placeholder"],
            key=f"pb_refine_{len(st.session_state.pb_chat_display)}",
        )

        if st.button(ui["refine_send"], type="primary") and refinement.strip():
            refine_msg = f"{refinement}\n\nחשוב: החזר את כל קוד ה-HTML המלא המעודכן — מ-<!DOCTYPE html> עד </html>. בלי הסברים."

            st.session_state.pb_messages.append({"role": "user", "content": refine_msg})
            st.session_state.pb_chat_display.append({"role": "user", "content": refinement})

            with st.spinner(ui["generating"]):
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=12000,
                    system=st.session_state.pb_system_prompt,
                    messages=st.session_state.pb_messages,
                )
                result = response.content[0].text
                html_code = extract_html(result)
                st.session_state.pb_html = html_code
                st.session_state.pb_messages.append({"role": "assistant", "content": result})
                st.session_state.pb_chat_display.append({"role": "assistant", "content": "✅ הדף עודכן!"})
                st.rerun()

    else:
        # Empty state
        st.markdown(f"""
        <div style="text-align:center; padding: 100px 20px; color: #aaa;">
            <div style="font-size: 4rem; margin-bottom: 20px">🎨</div>
            <h3>{"בחר מותג, סוג דף, וכתוב בריף" if lang == "he" else "Select brand, page type, and write a brief"}</h3>
            <p>{"הדף ייוצר כאן — מוכן לתצוגה והורדה" if lang == "he" else "Your page will appear here — ready to preview and download"}</p>
        </div>
        """, unsafe_allow_html=True)
