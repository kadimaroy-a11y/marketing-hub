# Marketing Hub — Full Evolution Roadmap
# From Content Generator → AI Marketing Management Platform

---

## Current State ✅
- Streamlit + Claude API + Supabase
- Brand DNA system (Myst, Prime51)
- Content generation with refinement chat
- Content Library with save/rate
- Web awareness scanning
- Hebrew/English bilingual UI

---

## PHASE 1 — Learning Engine 🧠
**Timeline: 2-3 weeks | Complexity: Easy-Medium**
**No new API keys needed**

### What it does
Makes Claude smarter over time from your team's feedback. Every rated post teaches the AI what works for each brand.

### New Supabase Tables
```sql
-- Structured performance data (queryable, not buried in JSONB)
performance_metrics: content_id, brand_key, platform, content_type, rating, rating_note, brief_summary, likes, comments, shares, reach, impressions, saves, engagement_rate

-- AI-generated brand insights
learning_snapshots: brand_key, snapshot_type, content, generated_at, applied
```

### New Files
- `performance_db.py` — Structured performance CRUD + analytics queries
- `learning_engine.py` — AI pattern analysis ("your best posts are short + FOMO + prices")
- `pages/03_Performance_Dashboard.py` — Charts, trends, "Generate Insights" button

### Changes to Existing Files
- `app.py` — Enhanced prompt injection with learning context + pattern analysis
- `pages/02_Content_Library.py` — Auto-record structured ratings

### User Flow
1. Create content → Save to library (existing)
2. Post on social → Rate it in Content Library (existing UI)
3. Ratings auto-stored in structured table (NEW)
4. Next generation: Claude sees top examples + pattern analysis (NEW)
5. Performance Dashboard shows trends over time (NEW)
6. "Generate Insights" button → AI summarizes what works → one-click apply to brand DNA (NEW)

---

## PHASE 2 — Direct Integrations 🔌
**Timeline: 6-8 weeks | Complexity: Hard**
**Start in parallel with Phase 1**

### Sub-phases (in priority order)

#### 2a: Meta (Instagram + Facebook) — Highest Impact
- Post directly from the hub
- Pull real engagement stats back
- Auto-rate content based on actual performance
- **Needs:** Facebook Developer App + review process

#### 2b: Google Drive + Sheets
- Browse brand assets (images, videos) from Drive
- Content calendar in Google Sheets (import/export)
- **Needs:** Google Cloud Console OAuth2 credentials

#### 2c: TikTok + YouTube
- Post TikTok videos + YouTube Shorts
- Pull video analytics
- **Needs:** TikTok Developer App, YouTube Data API key

#### 2d: Canva (Stretch Goal)
- Generate visual templates from text
- **Needs:** Canva Connect API access

### New Supabase Tables
```
platform_credentials — API tokens per brand per platform
published_posts — Track every post published through the hub
post_analytics — Real engagement data from platform APIs
brand_assets — Google Drive file references
```

### New Files
```
integrations/
  meta_api.py         — Instagram + Facebook posting & analytics
  tiktok_api.py       — TikTok posting & analytics
  youtube_api.py      — YouTube Shorts upload & analytics
  google_drive_api.py — Brand asset management
  google_sheets_api.py — Content calendar sync
  canva_api.py        — Design generation (stretch)
  credentials_manager.py — Token storage & refresh
  analytics_puller.py — Background analytics sync
```

### New Streamlit Pages
```
pages/04_Publish.py   — Publish to platforms, schedule, track status
pages/05_Analytics.py — Real engagement dashboards
pages/06_Assets.py    — Browse Google Drive brand assets
pages/07_Calendar.py  — Content calendar (weekly/monthly view)
```

### Credentials Needed
| Service | How to Get |
|---------|------------|
| Meta | developers.facebook.com → Create App → Request permissions |
| Google | console.cloud.google.com → Enable Drive/Sheets/YouTube APIs → OAuth2 |
| TikTok | developers.tiktok.com → Register App |
| Canva | canva.com/developers → Apply for API access |

---

## PHASE 3 — Smart Optimization 🎯
**Timeline: 3-4 weeks (after 4-6 weeks of Phase 2 data) | Complexity: Medium-Hard**
**Requires Phase 1 + Phase 2 data**

### What it does
Uses accumulated data to automatically optimize content strategy.

### New Supabase Tables
```
posting_analysis — Best times heatmap data (day + hour + engagement)
ab_tests — A/B test tracking (variants, hypothesis, winner)
trend_alerts — Detected trends with suggested actions
content_plans — AI-generated weekly plans with performance tracking
```

### New Files
```
optimization/
  posting_optimizer.py   — Best posting times analysis + heatmap
  ab_testing.py          — A/B test framework + AI suggestions
  trend_detector.py      — Trend identification from web + performance data
  calendar_generator.py  — AI weekly plans using all accumulated data
```

### New Streamlit Pages
```
pages/08_Optimizer.py — Best times heatmap, A/B tests, trend alerts
```

### Features
- **Best Posting Times** — Heatmap showing when engagement peaks per platform
- **A/B Testing** — AI suggests tests ("try short vs. long captions"), tracks results
- **Trend Alerts** — "Spider-Verse 2 trailer dropped → create content now"
- **Smart Weekly Plans** — AI generates data-driven content plan considering:
  - Best performing content types
  - Optimal posting times
  - Active A/B tests
  - Detected trends
  - Scheduled brand events
  - Israeli holidays

---

## Phase Dependencies

```
Phase 1 (Learning) ──────────┐
  Can start NOW               │
  2-3 weeks                    ├──→ Phase 3 (Optimization)
                               │    Needs data from both
Phase 2 (Integrations) ──────┘    3-4 weeks
  Can start in parallel
  6-8 weeks

  Let data accumulate 4-6 weeks
  before starting Phase 3
```

## Total Timeline: 3-5 months for full platform
Phase 1 delivers value within 2-3 weeks.

---

## Architecture Notes
- New modules organized: `integrations/` and `optimization/` directories
- All modules use shared `supabase_client.py` for database access
- Every new page needs Hebrew+English translations in `translations.py`
- OAuth on Streamlit Cloud: use "paste token" flow (simpler than redirect)
- Keep JSONB for flexible brand data; use proper columns for queryable analytics
