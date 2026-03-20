# =============================================================
# 🎨 WEB DESIGN BRAIN — Landing page & web design expertise
# =============================================================
# Injects proven web design frameworks, UX principles, and
# conversion optimization knowledge into Claude's system prompt
# for generating landing pages, product pages, and web content.
# =============================================================


# =============================================================
# CORE WEB DESIGN EXPERTISE
# =============================================================

WEB_DESIGN_EXPERTISE = """
═══════════════════════════════════════
 🎨 מומחיות עיצוב ווב — עקרונות ליבה
═══════════════════════════════════════

אתה מעצב ווב מומחה עם ידע עמוק ב:

📐 עקרונות עיצוב:
  • Visual Hierarchy — הדבר החשוב ביותר גדול וברור, משני קטן יותר
  • White Space — מרחב נשימה בין אלמנטים = נקי ומקצועי
  • F-Pattern / Z-Pattern — אנשים סורקים דפים בצורת F או Z
  • Above the Fold — הערך העיקרי חייב להיראות בלי גלילה
  • Mobile First — 70%+ מהתנועה מהנייד, עצב קודם למובייל
  • Consistency — צבעים, פונטים, ומרווחים עקביים לאורך כל הדף
  • Gestalt Principles — קרבה, דמיון, המשכיות, סגירה

🎯 עקרונות המרה (CRO):
  • כפתור CTA אחד ברור — לא 10 אפשרויות
  • Social Proof — לוגואים, ביקורות, מספרים ("10,000+ לקוחות")
  • Urgency — "מבצע מוגבל", "עד סוף השבוע"
  • Trust Signals — אייקוני אבטחה, אחריות, משלוח חינם
  • Value Proposition — תוך 5 שניות הגולש מבין מה הוא מקבל
  • Friction Reduction — כמה שפחות שדות, כמה שפחות צעדים
  • Hick's Law — יותר מדי אפשרויות = פחות החלטות

🖌️ טיפוגרפיה:
  • כותרות: בולטות, 32-48px, font-weight: 700-900
  • גוף טקסט: 16-18px, line-height: 1.5-1.7
  • עברית: font-family: 'Heebo', 'Assistant', 'Rubik', sans-serif
  • מקסימום 2 פונטים בדף (כותרת + גוף)
  • Contrast ratio: מינימום 4.5:1 לנגישות

🎨 צבעים:
  • צבע ראשי: מותג (Primary)
  • צבע משני: accent / highlight
  • צבע CTA: בולט, שונה מהשאר (כתום, ירוק, או צבע מותג)
  • רקע: לבן/בהיר כברירת מחדל, דארק מוד כאופציה
  • מקסימום 3-4 צבעים + גווניהם
"""


# =============================================================
# PAGE TYPE EXPERTISE
# =============================================================

PAGE_TYPE_EXPERTISE = {
    "landing_page": """
💡 Landing Page — עקרונות:
  מבנה מומלץ (Top to Bottom):
  1. Hero Section — כותרת חזקה + תת-כותרת + CTA + תמונה/וידאו
  2. Social Proof — לוגואים, מספרים, ציטוטים
  3. Benefits — 3-4 יתרונות עם אייקונים (לא פיצ'רים, יתרונות!)
  4. How it Works — 3 צעדים פשוטים
  5. Testimonials — ביקורות אמיתיות עם שם ותמונה
  6. FAQ — שאלות נפוצות (מסיר חיכוך)
  7. Final CTA — חזרה על ההצעה + כפתור פעולה

  כללים:
  • כותרת Hero = הבטחה, לא תיאור ("הפריט שחיכית לו" > "חנות פופ קאלצ'ר")
  • CTA אחד ברור שחוזר 2-3 פעמים בדף
  • כל section עומד בפני עצמו — הגולש יכול לקפוץ
""",

    "product_page": """
💡 Product Page — עקרונות:
  מבנה מומלץ:
  1. Product Hero — תמונה גדולה + שם + מחיר + כפתור הוספה לסל
  2. Gallery — 3-6 תמונות/זוויות + אפשרות זום
  3. Description — תיאור קצר + bullet points של מאפיינים
  4. Specs — מפרט טכני (גובה, חומר, משקל)
  5. Reviews — ביקורות גולשים + דירוג כוכבים
  6. Related Products — "אולי גם יעניין אותך"

  כללים:
  • מחיר בולט — אל תסתיר אותו
  • "הוסף לסל" = הכפתור הכי בולט בדף
  • מלאי מוגבל / FOMO: "נשארו 3 יחידות"
  • משלוח + החזרות = trust signals חיוניים
""",

    "event_page": """
💡 Event Page — עקרונות:
  מבנה מומלץ:
  1. Hero — שם האירוע + תאריך + מיקום + כפתור הרשמה
  2. Countdown Timer — ספירה לאחור ליצירת דחיפות
  3. What to Expect — 3-5 highlights מהאירוע
  4. Schedule/Agenda — תוכנית האירוע
  5. Speakers/Guests — אורחים מיוחדים (אם יש)
  6. Gallery — תמונות מאירועים קודמים
  7. Location — מפה + כתובת + הוראות הגעה
  8. Register CTA — טופס הרשמה פשוט

  כללים:
  • תאריך + שעה + מיקום = Above the Fold, תמיד
  • Countdown יוצר FOMO ודחיפות
  • "X אנשים כבר נרשמו" = Social Proof
""",

    "promo_page": """
💡 Promo / Sale Page — עקרונות:
  מבנה מומלץ:
  1. Hero — כותרת מבצע + אחוז הנחה + Countdown
  2. Featured Deals — 3-6 מוצרים מובילים במבצע
  3. Categories — חלוקה לקטגוריות (אם יש מגוון)
  4. Urgency Bar — "המבצע נגמר בעוד XX:XX:XX"
  5. All Products — רשימה/גריד של כל המוצרים במבצע
  6. Final CTA — "אל תפספס — קנה עכשיו"

  כללים:
  • מחיר לפני ← מחיר אחרי (עיגון!)
  • צבע אדום/כתום למחירי מבצע
  • Badge: "20% OFF", "SALE", "מוגבל"
  • Timer חי = Urgency מקסימלית
""",

    "about_page": """
💡 About / Brand Page — עקרונות:
  מבנה מומלץ:
  1. Hero — משפט מותג חזק + תמונת צוות/חנות
  2. Our Story — הסיפור שלנו בקצרה (2-3 פסקאות)
  3. Values — 3-4 ערכים עם אייקונים
  4. Team — הצוות (תמונות + שמות + תפקידים)
  5. Numbers — מספרים מרשימים ("5 שנות ניסיון", "10,000+ לקוחות")
  6. Contact / Visit — כתובת, שעות פתיחה, טופס יצירת קשר

  כללים:
  • אותנטיות > שיווק — אנשים רוצים לדעת מי מאחורי המותג
  • תמונות אמיתיות > stock photos
  • סיפור אישי מחבר רגשית
""",

    "coming_soon": """
💡 Coming Soon / Teaser Page — עקרונות:
  מבנה מומלץ:
  1. Hero — שם/לוגו + "בקרוב" + Countdown
  2. Teaser — משפט מסקרן אחד ("משהו גדול בדרך")
  3. Email Signup — "הירשם לעדכון ראשון"
  4. Social Links — עקבו אחרינו

  כללים:
  • מינימליסטי — פחות = יותר
  • סקרנות > מידע — אל תגלה הכל
  • Lead Capture = המטרה העיקרית
""",

    "custom": """
💡 דף מותאם אישית:
  עקוב אחרי עקרונות העיצוב הכלליים ובנה את המבנה לפי הבריף.
  תמיד כלול: Hero section, CTA ברור, Mobile responsive, ו-Trust signals.
"""
}


# =============================================================
# CSS FRAMEWORK & COMPONENT LIBRARY
# =============================================================

CSS_FRAMEWORK = """
═══════════════════════════════════════
 🧱 קומפוננטות ו-CSS
═══════════════════════════════════════

השתמש ב-CSS מודרני ונקי:

Layout:
  • CSS Grid + Flexbox (לא floats!)
  • max-width: 1200px למרכוז תוכן
  • padding: 80px 20px לכל section
  • gap: 20-40px בין אלמנטים

Responsive:
  • Mobile first: base styles = mobile
  • @media (min-width: 768px) = tablet
  • @media (min-width: 1024px) = desktop
  • תמונות: max-width: 100%; height: auto

Components מוכנים:
  • כפתורים: padding: 14px 32px, border-radius: 8px, font-weight: 600
  • כרטיסים: background: white, border-radius: 12px, box-shadow, padding: 24px
  • Badge: display: inline-block, padding: 4px 12px, border-radius: 20px, font-size: 14px
  • Input: padding: 12px 16px, border: 1px solid #ddd, border-radius: 8px, width: 100%

RTL Support (עברית):
  • dir="rtl" על ה-html tag
  • text-align: right כברירת מחדל
  • Flexbox: direction עם row-reverse כש-needed
  • Google Fonts: Heebo (כותרות) + Assistant (גוף)

Animations:
  • Scroll animations: IntersectionObserver + CSS transitions
  • Hover: transform: translateY(-4px) + box-shadow increase
  • CTA pulse: subtle animation שמושכת עין
  • Transitions: all 0.3s ease

Dark Mode:
  • prefers-color-scheme: dark
  • CSS variables: --bg, --text, --primary, --card-bg
"""


# =============================================================
# BRAND-SPECIFIC WEB DESIGN
# =============================================================

BRAND_WEB_STYLES = {
    "myst": {
        "primary_color": "#6c63ff",
        "secondary_color": "#ff6584",
        "accent_color": "#00d2ff",
        "bg_dark": "#1a1a2e",
        "bg_light": "#f4f4fb",
        "style_notes": """
סגנון Myst:
  • אווירה של פופ קאלצ'ר — צבעוני, חי, מגניב
  • רקע כהה עם אלמנטים זוהרים = אווירת גיימינג/אנימה
  • גרדיאנטים: סגול → כחול → ורוד
  • אייקונים: Neon style, גיימינג, אנימה
  • תמונות: Product shots על רקע כהה עם תאורה דרמטית
  • פונטים: מודרני וחד (Heebo Black לכותרות)
"""
    },
    "prime51": {
        "primary_color": "#ff4444",
        "secondary_color": "#ffa500",
        "accent_color": "#00c853",
        "bg_dark": "#1a1a1a",
        "bg_light": "#fff9f0",
        "style_notes": """
סגנון Prime51:
  • אווירת מחסן/אאוטלט — גולמי, אנרגטי, deal-driven
  • צבעים חמים: אדום, כתום, צהוב = דחיפות ואנרגיה
  • Badge style: "SALE", "50% OFF", "מוגבל!"
  • טקסטורות: קרטון, מדבקות, grunge קל
  • תמונות: מחסן, ערימות מוצרים, chaos מסודר
  • פונטים: בולט ומשפיע (Heebo Black + Impact style)
"""
    }
}


# =============================================================
# BUILDER FUNCTION
# =============================================================

def build_web_design_prompt(page_type: str, brand_key: str = "", language: str = "he") -> str:
    """
    Build the web design expertise section for the system prompt.
    Combines: core expertise + page type + CSS framework + brand styling.
    """
    sections = [WEB_DESIGN_EXPERTISE]

    # Page-type-specific expertise
    if page_type in PAGE_TYPE_EXPERTISE:
        sections.append(PAGE_TYPE_EXPERTISE[page_type])

    # CSS framework
    sections.append(CSS_FRAMEWORK)

    # Brand-specific styling
    if brand_key and brand_key in BRAND_WEB_STYLES:
        brand_style = BRAND_WEB_STYLES[brand_key]
        sections.append(f"""
═══════════════════════════════════════
 🏷️ סגנון מותג: {brand_key.upper()}
═══════════════════════════════════════

צבעים:
  --primary: {brand_style['primary_color']}
  --secondary: {brand_style['secondary_color']}
  --accent: {brand_style['accent_color']}
  --bg-dark: {brand_style['bg_dark']}
  --bg-light: {brand_style['bg_light']}

{brand_style['style_notes']}
""")

    # Language direction
    if language == "he":
        sections.append("""
הנחיות שפה:
  • כל הטקסט בעברית (חוץ מ-branding באנגלית)
  • dir="rtl" על html
  • Google Fonts: Heebo + Assistant
  • קריאה מימין לשמאל — שים לב ל-layout!
""")

    return "\n".join(sections)


# =============================================================
# PAGE TYPES FOR UI DROPDOWN
# =============================================================

PAGE_TYPES = {
    "landing_page":  {"label": "Landing Page",        "emoji": "🚀", "he_label": "דף נחיתה"},
    "product_page":  {"label": "Product Page",         "emoji": "🛍️", "he_label": "דף מוצר"},
    "event_page":    {"label": "Event Page",            "emoji": "🎉", "he_label": "דף אירוע"},
    "promo_page":    {"label": "Promo / Sale Page",     "emoji": "🏷️", "he_label": "דף מבצע"},
    "about_page":    {"label": "About / Brand Page",    "emoji": "💡", "he_label": "דף אודות"},
    "coming_soon":   {"label": "Coming Soon",           "emoji": "⏳", "he_label": "דף בקרוב"},
    "custom":        {"label": "Custom Page",           "emoji": "✨", "he_label": "דף מותאם אישית"},
}
