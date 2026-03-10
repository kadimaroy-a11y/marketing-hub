# =============================================================
# 🌍 TRANSLATIONS — עברית (HEB) / English (EN)
# =============================================================
# UI strings only — generated content always stays in Hebrew
# =============================================================

TRANSLATIONS = {

    # ──────────────────────────────────────────────────────────
    # HEBREW — עברית (RTL)
    # ──────────────────────────────────────────────────────────
    "he": {
        "dir":   "rtl",
        "align": "right",

        # Header
        "subtitle": "יוצר תוכן חכם לסושיאל מדיה",

        # Settings panel
        "settings_header":          "⚙️ הגדרות",
        "brand_label":              "🏷️ מותג",
        "platform_label":           "📡 פלטפורמה",
        "content_type_label":       "📄 סוג תוכן",
        "advanced_options":         "🔧 אפשרויות מתקדמות",
        "num_versions_label":       "מספר גרסאות",
        "primary_platform_cap":     "⭐ פלטפורמה ראשית",
        "secondary_platform_cap":   "📌 פלטפורמה משנית",

        # Brief
        "brief_header":             "📝 הבריף שלך",
        "brief_what":               "מה אתה רוצה לפרסם?",
        "brief_placeholder": (
            "לדוגמה:\nהגיעו לנו פאנקו חדשים של ספיידרמן אקרוס דה ספיידר ורס. "
            "יש 5 דמויות — מיילס מוראלס, גוון, ספיידר-פאנק, ספיידר-וומן. "
            'מחיר 89 ש"ח ליחידה.'
        ),
        "extra_notes_label":        "הערות נוספות (אופציונלי)",
        "extra_notes_placeholder":  "לדוגמה: יש מלאי מוגבל, יש מבצע השבוע...",
        "tips_brief_header":        "💡 טיפים לבריף טוב",
        "tips_brief_table": """\
| סוג | מה לכלול |
|---|---|
| **מוצר חדש** | שם + מה מיוחד + מחיר |
| **אירוע** | תאריך + שעה + למי |
| **מבצע** | מה + כמה % + עד מתי |
| **אנבוקסינג** | תאר מה נפתח |
| **טרנד** | לאיזה סרט/סדרה קשור |""",

        # Generate button
        "generate_btn_multi":       "✨ צור {n} גרסאות",
        "generate_btn_single":      "✨ צור {emoji} {label}",
        "fill_brief_warning":       "⬆️ מלא את הבריף כדי להפעיל",
        "powered_by":               "Powered by Claude AI · 💬 Chat Mode v2.1",

        # Refinement tips
        "tips_refine_header":       "💡 טיפים לשיפור",
        "tips_refine_expander":     "מה אפשר לבקש?",
        "tips_refine_content": """\
- 🎭 **טון**: `יותר מצחיק` / `יותר רציני` / `יותר אנרגטי`
- ✂️ **אורך**: `קצר יותר` / `הרחב את הכיתוב`
- ⚡ **FOMO**: `הוסף תחושת דחיפות ומלאי מוגבל`
- 🔁 **מבנה**: `שנה את הפתיחה` / `הוסף CTA חזק יותר`
- #️⃣ **האשטגים**: `שנה את האשטגים`
- 🎨 **ויזואל**: `כיוון ויזואלי שונה / יותר דרמטי`
- 📱 **סטורי**: `סטורי קצר ומצחיק יותר`""",

        # Output area
        "content_chat_header":      "🎨 שיחת תוכן",
        "edit_mode_label":          "📝 מצב עריכה:",
        "new_content_btn":          "🆕 התחל תוכן חדש",
        "history_expander":         "📜 היסטוריית שיחה — {n} {word}",
        "improvement_singular":     "שיפור",
        "improvement_plural":       "שיפורים",
        "updating_version":         "מעדכן לגרסה {n}...",
        "first_version_label":      "✨ גרסה ראשונה — {label}",
        "version_label":            "✏️ גרסה {n}",

        # Refinement box
        "refine_prompt":            "💬 רוצה לשנות משהו?",
        "refine_placeholder":       "לדוגמה: 'יותר מצחיק' / 'קצר יותר' / 'הוסף FOMO' / 'שנה את הפתיחה' / 'שנה את האשטגים'...",
        "send_refine_btn":          "שלח שיפור ↩️",

        # Approve / save
        "approve_btn":              "✅ אשר תוכן זה",
        "save_draft_btn":           "💾 שמור טיוטה",
        "approved_success":         "✅ תוכן אושר! מוכן לפרסום.",
        "save_library_btn":         "📚 שמור לספריית התוכן",
        "library_saved_info":       "📚 נשמר בספריית התוכן!",
        "download_approved_btn":    "⬇️ הורד תוכן מאושר",

        # Footer metrics
        "brand_metric":             "מותג",
        "platform_metric":          "פלטפורמה",
        "improvements_metric":      "שיפורים",
        "status_metric":            "סטטוס",
        "status_approved":          "✅ מאושר",
        "status_working":           "📝 בעבודה",
        "status_waiting":           "⏳ ממתין",

        # Empty state
        "empty_chat_title":         "מצב שיחה",
        "empty_chat_sub":           "צור תוכן ואז שוחח עם הסוכן<br>לשיפורים עד שהתוצאה מושלמת ✅",

        # Section headers
        "sec_caption":              "כיתוב ראשי",
        "sec_hashtags":             "האשטגים",
        "sec_visual":               "כיוון ויזואלי",
        "sec_story":                "גרסת סטורי",
        "sec_image":                "פרומפט לתמונה (AI)",

        # Copy button JS labels
        "copy_btn":                 "📋 העתק",
        "copied_btn":               "✅ הועתק!",

        # Errors
        "api_error":    "❌ שגיאה: לא נמצא מפתח API. בדוק שקובץ .env קיים.",
        "auth_error":   "❌ מפתח API לא תקין.",
        "rate_error":   "❌ הגעת למגבלת קריאות. נסה שוב בעוד כמה שניות.",

        # Web scanning
        "scanning_sources": "🌐 סורק {n} מקור{suffix} מידע...",
        "scan_note":        " · 🌐 {n} מקורות נסרקו",
    },

    # ──────────────────────────────────────────────────────────
    # ENGLISH (LTR)
    # ──────────────────────────────────────────────────────────
    "en": {
        "dir":   "ltr",
        "align": "left",

        # Header
        "subtitle": "Smart Social Media Content Generator",

        # Settings panel
        "settings_header":          "⚙️ Settings",
        "brand_label":              "🏷️ Brand",
        "platform_label":           "📡 Platform",
        "content_type_label":       "📄 Content Type",
        "advanced_options":         "🔧 Advanced Options",
        "num_versions_label":       "Number of Versions",
        "primary_platform_cap":     "⭐ Primary Platform",
        "secondary_platform_cap":   "📌 Secondary Platform",

        # Brief
        "brief_header":             "📝 Your Brief",
        "brief_what":               "What do you want to post?",
        "brief_placeholder": (
            "Example:\nNew Spider-Man Funko Pops just arrived — "
            "Spider-Man Across the Spider-Verse. 5 characters — "
            "Miles Morales, Gwen, Spider-Punk, Spider-Woman. "
            "Price ₪89 each."
        ),
        "extra_notes_label":        "Additional Notes (optional)",
        "extra_notes_placeholder":  "Example: Limited stock, sale this week...",
        "tips_brief_header":        "💡 Tips for a Good Brief",
        "tips_brief_table": """\
| Type | What to Include |
|---|---|
| **New Product** | Name + what's special + price |
| **Event** | Date + time + who it's for |
| **Sale** | What + % off + until when |
| **Unboxing** | Describe what was opened |
| **Trend** | Which movie/series it's tied to |""",

        # Generate button
        "generate_btn_multi":       "✨ Generate {n} Versions",
        "generate_btn_single":      "✨ Generate {emoji} {label}",
        "fill_brief_warning":       "⬆️ Fill in the brief to activate",
        "powered_by":               "Powered by Claude AI · 💬 Chat Mode v2.1",

        # Refinement tips
        "tips_refine_header":       "💡 Refinement Tips",
        "tips_refine_expander":     "What can you ask for?",
        "tips_refine_content": """\
- 🎭 **Tone**: `more funny` / `more serious` / `more energetic`
- ✂️ **Length**: `shorter` / `expand the caption`
- ⚡ **FOMO**: `add urgency and scarcity`
- 🔁 **Structure**: `change the opening` / `stronger CTA`
- #️⃣ **Hashtags**: `change the hashtags`
- 🎨 **Visual**: `different visual direction / more dramatic`
- 📱 **Story**: `shorter funnier story`""",

        # Output area
        "content_chat_header":      "🎨 Content Chat",
        "edit_mode_label":          "📝 Edit Mode:",
        "new_content_btn":          "🆕 Start New Content",
        "history_expander":         "📜 Chat History — {n} {word}",
        "improvement_singular":     "refinement",
        "improvement_plural":       "refinements",
        "updating_version":         "Updating to version {n}...",
        "first_version_label":      "✨ Version 1 — {label}",
        "version_label":            "✏️ Version {n}",

        # Refinement box
        "refine_prompt":            "💬 Want to change something?",
        "refine_placeholder":       "E.g., 'more funny' / 'shorter' / 'add urgency' / 'change the opening'...",
        "send_refine_btn":          "Send Refinement ↩️",

        # Approve / save
        "approve_btn":              "✅ Approve Content",
        "save_draft_btn":           "💾 Save Draft",
        "approved_success":         "✅ Content approved! Ready to publish.",
        "save_library_btn":         "📚 Save to Content Library",
        "library_saved_info":       "📚 Saved to Content Library!",
        "download_approved_btn":    "⬇️ Download Approved Content",

        # Footer metrics
        "brand_metric":             "Brand",
        "platform_metric":          "Platform",
        "improvements_metric":      "Refinements",
        "status_metric":            "Status",
        "status_approved":          "✅ Approved",
        "status_working":           "📝 In Progress",
        "status_waiting":           "⏳ Waiting",

        # Empty state
        "empty_chat_title":         "Chat Mode",
        "empty_chat_sub":           "Generate content then chat with the agent<br>to refine until it's perfect ✅",

        # Section headers
        "sec_caption":              "Main Caption",
        "sec_hashtags":             "Hashtags",
        "sec_visual":               "Visual Direction",
        "sec_story":                "Story Version",
        "sec_image":                "AI Image Prompt",

        # Copy button JS labels
        "copy_btn":                 "📋 Copy",
        "copied_btn":               "✅ Copied!",

        # Errors
        "api_error":    "❌ Error: API key not found. Check your .env file.",
        "auth_error":   "❌ Invalid API key.",
        "rate_error":   "❌ Rate limit reached. Please try again in a few seconds.",

        # Web scanning
        "scanning_sources": "🌐 Scanning {n} source{suffix}...",
        "scan_note":        " · 🌐 {n} sources scanned",
    },
}


def get_t(lang: str) -> dict:
    """Return translation dict for the given language code."""
    return TRANSLATIONS.get(lang, TRANSLATIONS["he"])


def get_section_config(lang: str) -> list:
    """Return SECTION_CONFIG with labels in the correct language."""
    t = get_t(lang)
    return [
        ("caption",      "📝",  t["sec_caption"]),
        ("hashtags",     "#️⃣", t["sec_hashtags"]),
        ("visual",       "🎬",  t["sec_visual"]),
        ("story",        "📱",  t["sec_story"]),
        ("image_prompt", "🖼️", t["sec_image"]),
    ]
