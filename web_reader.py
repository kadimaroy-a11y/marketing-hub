# =============================================================
# 🌐 WEB READER — Phase 2 / Stage 2A: Curated Source Scanner
# =============================================================
# Fetches approved brand URLs, extracts clean text,
# and asks Claude (Haiku) to summarize what's relevant
# for social media content creation.
#
# Each brand has a "web_sources" list in brands_db.json:
#   { "active": true, "name": "...", "url": "...",
#     "focus": "what to look for", "ignore": "what to skip" }
# =============================================================

import os
import requests
import anthropic
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


# ── Page fetcher ──────────────────────────────────────────────
def fetch_page(url: str, max_chars: int = 4000) -> str:
    """
    Fetch a URL and return clean readable text.
    Strips scripts, styles, nav, footer etc.
    Returns error message string if fetch fails.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=12, allow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove noise elements
        for tag in soup(["script", "style", "nav", "footer",
                         "header", "aside", "meta", "noscript",
                         "iframe", "form", "button"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        # Keep only lines with real content (>15 chars)
        lines = [ln.strip() for ln in text.split("\n") if len(ln.strip()) > 15]
        clean = "\n".join(lines)

        return clean[:max_chars]

    except requests.exceptions.Timeout:
        return f"[timeout — {url}]"
    except requests.exceptions.HTTPError as e:
        return f"[HTTP {e.response.status_code} — {url}]"
    except Exception as e:
        return f"[שגיאה: {type(e).__name__} — {url}]"


# ── Link extractor ────────────────────────────────────────────
def extract_links(soup, base_url: str) -> list:
    """
    Extract all internal anchor links with their text from a parsed page.
    Returns list of {"name": str, "url": str} dicts, deduplicated.
    """
    seen_urls = set()
    links = []
    base_domain = urlparse(base_url).netloc

    for a in soup.find_all("a", href=True):
        href = a.get("href", "").strip()
        text = a.get_text(strip=True)

        # Skip empties, anchors, js, mailto, tel
        if not href or not text:
            continue
        if href.startswith(("#", "javascript:", "mailto:", "tel:", "whatsapp:")):
            continue
        # Skip very short or very long anchor text
        if len(text) < 2 or len(text) > 120:
            continue

        # Resolve relative URLs
        full_url = urljoin(base_url, href)

        # Only keep same-domain links
        link_domain = urlparse(full_url).netloc
        if base_domain not in link_domain:
            continue

        # Deduplicate by URL
        clean_url = full_url.split("?")[0].rstrip("/")
        if clean_url in seen_urls or clean_url == base_url.rstrip("/"):
            continue
        seen_urls.add(clean_url)

        links.append({"name": text, "url": full_url})

    return links


# ── Product link scanner ───────────────────────────────────────
def get_product_links(brand: dict) -> str:
    """
    Fetch the brand's website and extract real product links.
    Returns a formatted string "• Product Name: URL" for each product found.
    Injects into the system prompt so Claude uses REAL links, never invented ones.
    """
    website = brand.get("website", "").strip()
    if not website:
        return ""
    if not website.startswith("http"):
        website = "https://" + website

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(website, headers=headers, timeout=14, allow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Build base URL from the final redirected URL
        parsed   = urlparse(resp.url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        # Remove noise before extracting links
        for tag in soup(["script", "style", "meta", "noscript", "iframe"]):
            tag.decompose()

        all_links = extract_links(soup, base_url)

        # ── Priority 1: URL patterns that clearly indicate product pages ──
        product_url_keywords = [
            "/product/", "/products/", "/item/", "/items/",
            "/p/", "/shop/", "/catalog/",
            "/מוצר/", "/מוצרים/", "/קטלוג/",
        ]
        product_links = [
            lnk for lnk in all_links
            if any(kw in lnk["url"].lower() for kw in product_url_keywords)
        ]

        # ── Priority 2: Any internal sub-page that isn't nav/utility ──
        if not product_links:
            skip_keywords = [
                "contact", "about", "login", "register", "cart",
                "checkout", "account", "search", "tag", "blog",
                "news", "faq", "terms", "privacy", "policy",
                "צור-קשר", "אודות", "עגלה", "כניסה",
            ]
            product_links = [
                lnk for lnk in all_links
                if not any(kw in lnk["url"].lower() for kw in skip_keywords)
            ]

        if not product_links:
            return ""

        # Build formatted output, dedup by name
        seen_names = set()
        lines = []
        for lnk in product_links[:40]:   # cap at 40 products
            name = lnk["name"]
            if name in seen_names:
                continue
            seen_names.add(name)
            lines.append(f"• {name}: {lnk['url']}")

        return "\n".join(lines)

    except Exception:
        return ""


# ── Main awareness function ───────────────────────────────────
def get_brand_awareness(brand: dict) -> str:
    """
    Read all active web sources for a brand.
    Returns a Hebrew bullet-point summary of what's new and relevant.
    Returns empty string if no sources configured or all fail.
    """
    sources = [
        s for s in brand.get("web_sources", [])
        if s.get("active", True) and str(s.get("url", "")).strip()
    ]

    if not sources:
        return ""

    # ── Fetch all pages ───────────────────────────────────────
    blocks = []
    for src in sources:
        content = fetch_page(src["url"])
        block = f"=== {src.get('name', src['url'])} ===\n"
        if src.get("focus"):
            block += f"חפש: {src['focus']}\n"
        if src.get("ignore"):
            block += f"התעלם מ: {src['ignore']}\n"
        block += content
        blocks.append(block)

    if not blocks:
        return ""

    # ── Summarize with Claude Haiku (fast + cheap) ────────────
    brand_name    = brand.get("name", "")
    hebrew_name   = brand.get("hebrew_name", brand_name)
    product_types = ", ".join(brand.get("products", [])[:5])
    combined      = "\n\n".join(blocks)

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=700,
            messages=[{
                "role": "user",
                "content": (
                    f"אתה עוזר שיווק של {brand_name} ({hebrew_name}) בישראל.\n"
                    f"קטגוריות מוצרים: {product_types or 'לא צוין'}\n\n"
                    f"סרקת את המקורות הבאים:\n\n{combined}\n\n"
                    f"סכם בעברית בנקודות (מקסימום 8), רק מה שרלוונטי "
                    f"לתוכן סושיאל מדיה עבור {brand_name} ישראל:\n"
                    f"• מוצרים חדשים שהגיעו / מחירים / מבצעים\n"
                    f"• טרנדים או אירועים שהמותג יכול לרכוב עליהם\n"
                    f"• חדשות ענף רלוונטיות לשוק הישראלי\n\n"
                    f"התעלם ממידע שאינו רלוונטי לשוק הישראלי.\n"
                    f"אם אין כלום מעניין — כתוב בקצרה 'לא נמצאו עדכונים חדשים'."
                )
            }]
        )
        return msg.content[0].text.strip()

    except anthropic.AuthenticationError:
        return ""
    except anthropic.RateLimitError:
        return ""
    except Exception:
        return ""
