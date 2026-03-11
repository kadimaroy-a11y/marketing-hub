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

        # Shared / sidebar
        "lang_toggle_label": "🌐 שפה",

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

        # ── Brand Manager ──────────────────────────────────────────
        "bm_title":                 "🏢 ניהול מותגים",
        "bm_subtitle":              "הוסף מותגים חדשים, ערוך פרופילים קיימים, ובנה את **בסיס הידע** שמחכים לו הסוכן.",
        "bm_no_brands_info":        "אין מותגים עדיין. לחץ על '➕ מותג חדש' להתחיל.",
        "bm_new_brand_btn":         "➕ מותג חדש",
        "bm_new_brand_title":       "✨ מותג חדש",
        "bm_brand_name_en_label":   "שם המותג (באנגלית)",
        "bm_brand_hname_label":     "שם בעברית",
        "bm_emoji_label":           "אמוג'י",
        "bm_type_cat_label":        "סוג / קטגוריה",
        "bm_type_placeholder":      "לדוגמה: חנות קמעונאית / מותג ייבוא",
        "bm_create_btn":            "✅ צור מותג",
        "bm_cancel_btn":            "ביטול",
        "bm_brand_exists_err":      "מותג עם מזהה '{key}' כבר קיים.",
        "bm_brand_name_warning":    "נא להזין שם מותג.",
        "bm_save_ok_msg":           "✅ המותג נשמר בהצלחה!",
        "bm_not_found_err":         "המותג לא נמצא. אולי נמחק?",
        # Tabs
        "bm_tab_basic":             "🏷️ בסיס",
        "bm_tab_products":          "📦 מוצרים",
        "bm_tab_audience":          "👥 קהל יעד",
        "bm_tab_voice":             "🎤 קול המותג",
        "bm_tab_platforms":         "📱 פלטפורמות",
        "bm_tab_kb":                "🧠 בסיס ידע",
        "bm_tab_web":               "🌐 מקורות אינטרנט",
        # Basic tab
        "bm_basic_header":          "#### 🏷️ פרטי בסיס",
        "bm_name_label":            "שם המותג",
        "bm_hname_label":           "שם בעברית",
        "bm_type_label":            "סוג / קטגוריה",
        "bm_parent_label":          "חברת אם",
        "bm_website_label":         "אתר אינטרנט",
        "bm_freq_label":            "תדירות פרסום",
        "bm_content_lang_label":    "שפת תוכן",
        # Products tab
        "bm_products_header":       "#### 📦 מוצרים ומיצוב",
        "bm_products_list_label":   "**מוצרים** (שורה לכל מוצר)",
        "bm_ctw_label":             "**מה עובד בתוכן** (שורה לכל סוג)",
        "bm_usp_label":             "**יתרונות ייחודיים — USP** (שורה לכל יתרון)",
        "bm_cta_label":             "**מה להימנע בתוכן** (שורה לכל סוג)",
        # Audience tab
        "bm_audience_header":       "#### 👥 קהל יעד",
        "bm_age_label":             "גיל",
        "bm_gender_label":          "מגדר",
        "bm_interests_label":       "**תחומי עניין** (שורה לכל עניין)",
        "bm_psycho_label":          "**פסיכוגרפיה** — מי הם באמת?",
        "bm_motiv_label":           "**מה מניע אותם לקנות?**",
        # Voice tab
        "bm_voice_header":          "#### 🎤 קול המותג",
        "bm_tone_label":            "**טון**",
        "bm_style_label":           "**סגנון**",
        "bm_lang_notes_label":      "**הנחיות שפה**",
        "bm_do_label":              "**✅ לעשות תמיד** (שורה לכל הנחיה)",
        "bm_dont_label":            "**❌ לא לעשות לעולם** (שורה לכל הנחיה)",
        # Platforms tab
        "bm_platforms_header":      "#### 📱 פלטפורמות",
        "bm_priority_label":        "עדיפות",
        "bm_hashtag_count_label":   "כמות האשטגים",
        "bm_content_types_label":   "**סוגי תוכן** (שורה לכל סוג)",
        "bm_caption_length_label":  "אורך כיתוב",
        "bm_pri_primary":           "⭐ ראשי",
        "bm_pri_secondary":         "📌 משני",
        "bm_pri_disabled":          "🚫 כבוי",
        # KB tab
        "bm_kb_header":             "#### 🧠 בסיס הידע — המוח שגדל עם הזמן",
        "bm_kb_caption":            "כל מה שמכניסים כאן הסוכן ישתמש בו אוטומטית בכל יצירת תוכן למותג זה.",
        "bm_kb_works_label":        "**✅ מה עובד** — לפי ניסיון הצוות (שורה לכל פריט)",
        "bm_kb_doesnt_label":       "**❌ מה לא עובד** — לפי ניסיון הצוות (שורה לכל פריט)",
        "bm_kb_comp_label":         "**🏆 מתחרים** — שמות / אתרים (שורה לכל אחד)",
        "bm_kb_news_label":         "**📰 מקורות חדשות** — לעקוב אחריהם (שורה לכל אחד)",
        "bm_kb_links_label":        "**🔗 לינקים ללמידה** — מאמרים / מקורות (שורה לכל לינק)",
        "bm_kb_hashtags_label":     "**#️⃣ האשטגים מאושרים** (שורה לכל האשטג, ללא #)",
        "bm_kb_notes_label":        "**📝 הערות צוות שיווק** (שורה לכל הערה)",
        # Web sources tab
        "bm_web_header":            "#### 🌐 מקורות אינטרנט — הסוכן יקרא אלה לפני כל יצירת תוכן",
        "bm_web_caption":           "הוסף כתובות URL שהסוכן יסרוק לפני כל פוסט — אתר המותג, חדשות, דפי מוצר. בכל מקור ציין **מה לחפש** ומה **להתעלם** ממנו.",
        "bm_no_sources":            "אין מקורות עדיין. לחץ ➕ להוסיף מקור ראשון.",
        "bm_src_active_label":      "פעיל",
        "bm_src_name_label":        "שם המקור",
        "bm_src_name_placeholder":  "לדוגמה: אתר מיסט / Razor Facebook Israel",
        "bm_src_focus_label":       "🔍 מה לחפש",
        "bm_src_focus_placeholder": "מוצרים חדשים, מחירים, מבצעים",
        "bm_src_ignore_label":      "🚫 מה להתעלם",
        "bm_src_ignore_placeholder":"מוצרים לא ישראליים, מידע ישן",
        "bm_src_delete_btn":        "🗑️ מחק מקור זה",
        "bm_add_source_btn":        "➕ הוסף מקור חדש",
        "bm_tips_sources_expander": "💡 טיפים למקורות טובים",
        "bm_tips_sources_table": """\
| סוג | דוגמה לURL | מה לכתוב ב"מה לחפש" |
|-----|-----------|-------------------|
| **אתר המותג** | `myst.co.il` | מוצרים חדשים, מחירים, מבצעים |
| **דף פייסבוק** | `facebook.com/RazorIsrael` | פוסטים חדשים, מוצרים |
| **אתר חדשות** | `ign.com/news` | טרנדים, הודעות חדשות |
| **מתחרה** | `competitor.co.il` | מה הם מפרסמים השבוע |
| **דף מוצר** | `amazon.co.il/product/...` | מחיר, זמינות, ביקורות |""",
        "bm_src_default":           "מקור {i}",
        # Save / delete
        "bm_save_btn":              "💾 שמור מותג",
        "bm_delete_btn":            "🗑️ מחק מותג",
        "bm_delete_confirm_msg":    "למחוק את **{name}** לצמיתות?",
        "bm_confirm_delete_btn":    "✅ כן, מחק",
        # Summary metrics
        "bm_summary_header":        "#### 📊 סיכום מותג",
        "bm_products_metric":       "מוצרים",
        "bm_active_plat_metric":    "פלטפורמות פעילות",
        "bm_knowledge_metric":      "פריטי ידע",
        "bm_hashtags_metric":       "האשטגים מאושרים",
        # Empty state
        "bm_empty_title":           "אין מותגים עדיין",
        "bm_empty_sub":             "לחץ על ➕ מותג חדש כדי להתחיל",
        # Scheduled Events tab
        "bm_tab_events":            "📅 אירועים",
        "bm_events_header":         "#### 📅 אירועים מתוכננים לפי חודש",
        "bm_events_caption":        "סמן אירועים פעילים — הם יוזרקו אוטומטית לתוכן שנוצר באותו חודש.",
        "bm_events_add_btn":        "➕ הוסף",
        "bm_events_new_placeholder":"שם האירוע...",
        "bm_events_no_events":      "אין אירועים. לחץ ➕ להוסיף.",
        "bm_events_current_badge":  "🟢 החודש",
        "bm_months": [
            "ינואר","פברואר","מרץ","אפריל","מאי","יוני",
            "יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר",
        ],
        # Section selection (app.py save area)
        "sec_select_label":         "📌 בחר סקשנים לשמירה:",
        # Content Library brand grouping
        "cl_brand_all_header":      "📁 כל התכנים — לפי מותג",
        "cl_expand_brand":          "הצג",

        # ── Content Library ────────────────────────────────────────
        "cl_title":                 "📚 ספריית תוכן",
        "cl_subtitle":              "כל התכנים שאושרו ונשמרו — מוכנים לשימוש חוזר בכל עת.",
        "cl_total_metric":          "סה״כ פריטים שמורים",
        "cl_brands_metric":         "מותגים עם תוכן",
        "cl_available_metric":      "זמינים לשימוש",
        "cl_all_brands":            "📋 כל המותגים",
        "cl_all_platforms":         "📡 כל הפלטפורמות",
        "cl_newest":                "🆕 החדש ביותר",
        "cl_oldest":                "🕰️ הישן ביותר",
        "cl_search_placeholder":    "חפש לפי בריף, מותג, תוכן...",
        "cl_no_filter_match":       "לא נמצאו פריטים התואמים לסינון הנוכחי.",
        "cl_empty_title":           "הספרייה ריקה",
        "cl_empty_sub":             "צור תוכן בדף הראשי → אשר אותו → לחץ \"שמור לספריית התוכן\"",
        "cl_items_count":           "{n} פריטים",
        "cl_saved_label":           "📅 נשמר:",
        "cl_copy_full_caption":     "^ העתק תוכן מלא",
        "cl_notes_label":           "📝 הערות אישיות",
        "cl_notes_placeholder":     "לדוגמה: השתמשנו בזה ב-03/03, קיבל 200 לייקים...",
        "cl_save_notes_btn":        "💾 שמור הערה",
        "cl_delete_btn":            "🗑️ מחק פריט",
        "cl_notes_saved":           "✅ הערה נשמרה!",
        "cl_footer":                "📚 ספריית תוכן · {n} פריטים שמורים · Marketing Hub",
        "cl_copy_btn":              "📋 העתק",
        "cl_copied_btn":            "✅ הועתק!",
    },

    # ──────────────────────────────────────────────────────────
    # ENGLISH (LTR)
    # ──────────────────────────────────────────────────────────
    "en": {
        "dir":   "ltr",
        "align": "left",

        # Shared / sidebar
        "lang_toggle_label": "🌐 Language",

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

        # ── Brand Manager ──────────────────────────────────────────
        "bm_title":                 "🏢 Brand Manager",
        "bm_subtitle":              "Add new brands, edit existing profiles, and build the **Knowledge Base** the agent relies on.",
        "bm_no_brands_info":        "No brands yet. Click '➕ New Brand' to get started.",
        "bm_new_brand_btn":         "➕ New Brand",
        "bm_new_brand_title":       "✨ New Brand",
        "bm_brand_name_en_label":   "Brand Name (English)",
        "bm_brand_hname_label":     "Hebrew Name",
        "bm_emoji_label":           "Emoji",
        "bm_type_cat_label":        "Type / Category",
        "bm_type_placeholder":      "E.g.: Retail store / Import brand",
        "bm_create_btn":            "✅ Create Brand",
        "bm_cancel_btn":            "Cancel",
        "bm_brand_exists_err":      "Brand with key '{key}' already exists.",
        "bm_brand_name_warning":    "Please enter a brand name.",
        "bm_save_ok_msg":           "✅ Brand saved successfully!",
        "bm_not_found_err":         "Brand not found. Maybe deleted?",
        # Tabs
        "bm_tab_basic":             "🏷️ Basic",
        "bm_tab_products":          "📦 Products",
        "bm_tab_audience":          "👥 Audience",
        "bm_tab_voice":             "🎤 Brand Voice",
        "bm_tab_platforms":         "📱 Platforms",
        "bm_tab_kb":                "🧠 Knowledge Base",
        "bm_tab_web":               "🌐 Web Sources",
        # Basic tab
        "bm_basic_header":          "#### 🏷️ Basic Info",
        "bm_name_label":            "Brand Name",
        "bm_hname_label":           "Hebrew Name",
        "bm_type_label":            "Type / Category",
        "bm_parent_label":          "Parent Company",
        "bm_website_label":         "Website",
        "bm_freq_label":            "Posting Frequency",
        "bm_content_lang_label":    "Content Language",
        # Products tab
        "bm_products_header":       "#### 📦 Products & Positioning",
        "bm_products_list_label":   "**Products** (one per line)",
        "bm_ctw_label":             "**What works in content** (one per line)",
        "bm_usp_label":             "**Unique Advantages — USP** (one per line)",
        "bm_cta_label":             "**What to avoid in content** (one per line)",
        # Audience tab
        "bm_audience_header":       "#### 👥 Target Audience",
        "bm_age_label":             "Age",
        "bm_gender_label":          "Gender",
        "bm_interests_label":       "**Interests** (one per line)",
        "bm_psycho_label":          "**Psychographics** — who are they really?",
        "bm_motiv_label":           "**What motivates them to buy?**",
        # Voice tab
        "bm_voice_header":          "#### 🎤 Brand Voice",
        "bm_tone_label":            "**Tone**",
        "bm_style_label":           "**Style**",
        "bm_lang_notes_label":      "**Language Guidelines**",
        "bm_do_label":              "**✅ Always Do** (one per line)",
        "bm_dont_label":            "**❌ Never Do** (one per line)",
        # Platforms tab
        "bm_platforms_header":      "#### 📱 Platforms",
        "bm_priority_label":        "Priority",
        "bm_hashtag_count_label":   "Hashtag Count",
        "bm_content_types_label":   "**Content Types** (one per line)",
        "bm_caption_length_label":  "Caption Length",
        "bm_pri_primary":           "⭐ Primary",
        "bm_pri_secondary":         "📌 Secondary",
        "bm_pri_disabled":          "🚫 Disabled",
        # KB tab
        "bm_kb_header":             "#### 🧠 Knowledge Base — The brain that grows over time",
        "bm_kb_caption":            "Everything added here will be used by the agent automatically for every content creation for this brand.",
        "bm_kb_works_label":        "**✅ What Works** — based on team experience (one per line)",
        "bm_kb_doesnt_label":       "**❌ What Doesn't Work** — based on team experience (one per line)",
        "bm_kb_comp_label":         "**🏆 Competitors** — names / websites (one per line)",
        "bm_kb_news_label":         "**📰 News Sources** — to follow (one per line)",
        "bm_kb_links_label":        "**🔗 Learning Links** — articles / sources (one per line)",
        "bm_kb_hashtags_label":     "**#️⃣ Approved Hashtags** (one per line, without #)",
        "bm_kb_notes_label":        "**📝 Marketing Team Notes** (one per line)",
        # Web sources tab
        "bm_web_header":            "#### 🌐 Web Sources — Agent reads these before every content creation",
        "bm_web_caption":           "Add URLs the agent will scan before every post — brand site, news, product pages. For each source specify **what to look for** and what to **ignore**.",
        "bm_no_sources":            "No sources yet. Click ➕ to add the first source.",
        "bm_src_active_label":      "Active",
        "bm_src_name_label":        "Source Name",
        "bm_src_name_placeholder":  "E.g.: Myst Website / Razor Facebook Israel",
        "bm_src_focus_label":       "🔍 What to look for",
        "bm_src_focus_placeholder": "New products, prices, sales",
        "bm_src_ignore_label":      "🚫 What to ignore",
        "bm_src_ignore_placeholder":"Non-Israeli products, outdated info",
        "bm_src_delete_btn":        "🗑️ Delete this source",
        "bm_add_source_btn":        "➕ Add New Source",
        "bm_tips_sources_expander": "💡 Tips for good sources",
        "bm_tips_sources_table": """\
| Type | URL Example | What to write in "What to look for" |
|-----|-----------|-------------------------------------|
| **Brand Site** | `myst.co.il` | New products, prices, sales |
| **Facebook Page** | `facebook.com/RazorIsrael` | New posts, products |
| **News Site** | `ign.com/news` | Trends, announcements |
| **Competitor** | `competitor.co.il` | What they're posting this week |
| **Product Page** | `amazon.co.il/product/...` | Price, availability, reviews |""",
        "bm_src_default":           "Source {i}",
        # Save / delete
        "bm_save_btn":              "💾 Save Brand",
        "bm_delete_btn":            "🗑️ Delete Brand",
        "bm_delete_confirm_msg":    "Permanently delete **{name}**?",
        "bm_confirm_delete_btn":    "✅ Yes, Delete",
        # Summary metrics
        "bm_summary_header":        "#### 📊 Brand Summary",
        "bm_products_metric":       "Products",
        "bm_active_plat_metric":    "Active Platforms",
        "bm_knowledge_metric":      "Knowledge Items",
        "bm_hashtags_metric":       "Approved Hashtags",
        # Empty state
        "bm_empty_title":           "No Brands Yet",
        "bm_empty_sub":             "Click ➕ New Brand to get started",
        # Scheduled Events tab
        "bm_tab_events":            "📅 Events",
        "bm_events_header":         "#### 📅 Scheduled Events by Month",
        "bm_events_caption":        "Check active events — they are automatically injected into content generated that month.",
        "bm_events_add_btn":        "➕ Add",
        "bm_events_new_placeholder":"Event name...",
        "bm_events_no_events":      "No events. Click ➕ to add.",
        "bm_events_current_badge":  "🟢 This Month",
        "bm_months": [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December",
        ],
        # Section selection (app.py save area)
        "sec_select_label":         "📌 Select sections to save:",
        # Content Library brand grouping
        "cl_brand_all_header":      "📁 All Content — by Brand",
        "cl_expand_brand":          "Show",

        # ── Content Library ────────────────────────────────────────
        "cl_title":                 "📚 Content Library",
        "cl_subtitle":              "All approved and saved content — ready to reuse anytime.",
        "cl_total_metric":          "Total Saved Items",
        "cl_brands_metric":         "Brands with Content",
        "cl_available_metric":      "Available to Use",
        "cl_all_brands":            "📋 All Brands",
        "cl_all_platforms":         "📡 All Platforms",
        "cl_newest":                "🆕 Newest First",
        "cl_oldest":                "🕰️ Oldest First",
        "cl_search_placeholder":    "Search by brief, brand, content...",
        "cl_no_filter_match":       "No items match the current filter.",
        "cl_empty_title":           "Library is Empty",
        "cl_empty_sub":             "Create content on main page → Approve it → Click \"Save to Content Library\"",
        "cl_items_count":           "{n} items",
        "cl_saved_label":           "📅 Saved:",
        "cl_copy_full_caption":     "^ Copy full content",
        "cl_notes_label":           "📝 Personal Notes",
        "cl_notes_placeholder":     "E.g.: Used on 03/03, got 200 likes...",
        "cl_save_notes_btn":        "💾 Save Note",
        "cl_delete_btn":            "🗑️ Delete Item",
        "cl_notes_saved":           "✅ Note saved!",
        "cl_footer":                "📚 Content Library · {n} saved items · Marketing Hub",
        "cl_copy_btn":              "📋 Copy",
        "cl_copied_btn":            "✅ Copied!",
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
