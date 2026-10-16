#!/usr/bin/env python3
"""
DeveloperOS Tools Web Portal Static Site Generator (SSG)
Builds a production-ready, zero-backend static website for Cloudflare Pages:
- Main searchable directory (dist/index.html)
- 25 dedicated SEO landing pages (dist/tools/<seo_slug>.html)
- Valid XML Sitemap (dist/sitemap.xml)
- robots.txt (dist/robots.txt)
- Assets & Schema.org JSON-LD structured data
"""

import html
import json
import os
import shutil
from pathlib import Path

WEB_ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = WEB_ROOT.parent.parent
REGISTRY_FILE = WORKSPACE_ROOT / "infrastructure" / "developeros-tool-registry" / "registry.json"
DIST_DIR = WEB_ROOT / "dist"
SRC_DIR = WEB_ROOT / "src"

SITE_URL = "https://tools.developeros.in"
MAIN_SITE_URL = "https://developeros.in"
GITHUB_ORG_URL = "https://github.com/developerOSindia"


def load_registry() -> dict:
    if not REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Registry file missing: {REGISTRY_FILE}")
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def setup_dist():
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)
    (DIST_DIR / "tools").mkdir(parents=True)
    (DIST_DIR / "assets").mkdir(parents=True)

    # Copy styles and scripts
    shutil.copy2(SRC_DIR / "styles.css", DIST_DIR / "assets" / "styles.css")
    shutil.copy2(SRC_DIR / "catalog.js", DIST_DIR / "assets" / "catalog.js")

    # Copy logo if available
    logo_src = WORKSPACE_ROOT / "suites" / "developeros-devutils" / "assets" / "logo.svg"
    if logo_src.exists():
        shutil.copy2(logo_src, DIST_DIR / "assets" / "logo.svg")


def render_navbar(depth: int = 0) -> str:
    root_prefix = "../" if depth > 0 else ""
    return f"""
    <nav class="navbar" role="navigation" aria-label="Main Navigation">
      <div class="nav-container">
        <a href="{root_prefix}index.html" class="brand-link">
          <img src="{root_prefix}assets/logo.svg" width="28" height="28" alt="DeveloperOS logo" style="flex-shrink: 0;" />
          DeveloperOS Tools
          <span class="brand-badge">Open Source</span>
        </a>
        <div class="nav-links">
          <a href="{MAIN_SITE_URL}?utm_source=developeros_tools&utm_medium=header_banner&utm_campaign=powered_by" class="compact-header-pill" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 5px; background: rgba(249, 115, 22, 0.12); border: 1px solid rgba(249, 115, 22, 0.35); color: #f97316; font-size: 0.78rem; font-weight: 600; padding: 4px 11px; border-radius: 9999px; text-decoration: none; transition: background 0.15s ease;">
            <span>⚡</span>
            <span>Powered by DeveloperOS ↗</span>
          </a>
          <a href="{root_prefix}index.html" class="nav-item">Catalog</a>
          <a href="{MAIN_SITE_URL}/privacy?utm_source=developeros_tools&utm_medium=nav_link&utm_campaign=ecosystem_referral" class="nav-item" target="_blank" rel="noopener noreferrer">Privacy</a>
          <a href="{GITHUB_ORG_URL}" class="nav-btn-gh" target="_blank" rel="noopener noreferrer">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
            </svg>
            GitHub
          </a>
        </div>
      </div>
    </nav>
    """


def render_main_promotional_banner(tool_name: str = None, depth: int = 0) -> str:
    root_prefix = "../" if depth > 0 else ""
    heading = f"Enjoying {html.escape(tool_name)}?" if tool_name else "Enjoying this free tool?"
    return f"""
    <section class="devos-promotional-banner" role="region" aria-label="DeveloperOS Promotion" style="
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.08) 0%, rgba(244, 63, 94, 0.04) 50%, rgba(6, 182, 212, 0.06) 100%), var(--color-surface, #0c0f15);
        border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
        border-radius: var(--radius-md, 12px);
        padding: 1.5rem 1.75rem;
        margin: 2.5rem 0 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.25rem;
    ">
        <div style="display: flex; align-items: center; gap: 1.25rem; max-width: 650px;">
            <img src="{root_prefix}assets/logo.svg" width="44" height="44" alt="DeveloperOS logo" style="flex-shrink: 0;" />
            <div>
                <h3 style="margin: 0 0 0.35rem 0; font-size: 1.2rem; font-weight: 700; color: var(--color-text, #f8fafc); letter-spacing: -0.01em;">
                    {heading}
                </h3>
                <p style="margin: 0; color: var(--color-text-muted, #94a3b8); font-size: 0.95rem; line-height: 1.5;">
                    Discover more developer tools, AI resources, and automation solutions from DeveloperOS.
                </p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.85rem; flex-wrap: wrap;">
            <a href="{MAIN_SITE_URL}?utm_source=developeros_tools&utm_medium=main_banner&utm_campaign=ecosystem_referral" target="_blank" rel="noopener noreferrer" style="
                background-color: var(--color-primary, #f97316);
                color: #ffffff;
                font-weight: 600;
                font-size: 0.9rem;
                padding: 0.55rem 1.25rem;
                border-radius: var(--radius-sm, 6px);
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                box-shadow: 0 2px 4px rgba(249, 115, 22, 0.25);
            ">
                Explore DeveloperOS &rarr;
            </a>
            <a href="{SITE_URL}?utm_source=developeros_tools&utm_medium=secondary_cta&utm_campaign=tools_directory" target="_blank" rel="noopener noreferrer" style="
                background-color: rgba(255, 255, 255, 0.06);
                border: 1px solid var(--color-border, rgba(255, 255, 255, 0.15));
                color: var(--color-text, #f8fafc);
                font-weight: 600;
                font-size: 0.9rem;
                padding: 0.55rem 1.15rem;
                border-radius: var(--radius-sm, 6px);
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
            ">
                More Free Tools
            </a>
        </div>
    </section>
    """


def render_footer() -> str:
    return f"""
    <footer class="footer" role="contentinfo">
      <div class="footer-content">
        <div>
          <p style="font-size: 1.05rem; font-weight: 700; color: var(--color-text, #f8fafc); margin: 0 0 6px 0;">
            Built with ❤️ by <a href="{MAIN_SITE_URL}?utm_source=developeros_tools&utm_medium=footer_tagline&utm_campaign=ecosystem_referral" target="_blank" rel="noopener noreferrer" style="color: var(--color-primary, #f97316); text-decoration: none; font-weight: 700;">DeveloperOS</a>
          </p>
          <span style="font-size: 0.85rem; color: var(--color-text-dim, #6b7c94);">
            DeveloperOS Open-Source Tools Ecosystem • 100% Free, Offline-First, Zero-Storage Utilities • MIT Licensed
          </span>
        </div>
        <div class="footer-links">
          <a href="{MAIN_SITE_URL}?utm_source=developeros_tools&utm_medium=footer_link&utm_campaign=ecosystem_referral" target="_blank" rel="noopener noreferrer">DeveloperOS Home</a>
          <a href="{SITE_URL}?utm_source=developeros_tools&utm_medium=footer_link&utm_campaign=ecosystem_referral">All Tools Directory</a>
          <a href="{GITHUB_ORG_URL}" target="_blank" rel="noopener noreferrer">GitHub Organization</a>
          <a href="{MAIN_SITE_URL}/privacy?utm_source=developeros_tools&utm_medium=footer_link&utm_campaign=ecosystem_referral" target="_blank" rel="noopener noreferrer">Privacy Policy</a>
        </div>
      </div>
    </footer>
    """


def build_index_page(registry: dict):
    tools = registry.get("tools", [])
    categories = sorted(list({t["category"] for t in tools}))
    tool_cards_html = []

    for t in tools:
        is_live = t["availability_status"] == "verified_live" and bool(t["live_url"])
        status_label = "Verified Live" if is_live else "Staged Offline"
        status_class = "status-live" if is_live else "status-staged"

        launch_btn = (
            f'<a href="{t["live_url"]}" target="_blank" rel="noopener noreferrer" class="btn-launch">⚡ Launch Tool</a>'
            if is_live
            else f'<a href="tools/{t["seo_slug"]}.html" class="btn-launch" style="background-color: var(--color-surface-elevated); color: var(--color-text); border: 1px solid var(--color-border);">📖 View Documentation</a>'
        )

        card = f"""
        <article class="tool-card" id="card-{t['seo_slug']}">
          <div class="card-top">
            <div class="card-header-line">
              <h3 class="card-title">
                <a href="tools/{t['seo_slug']}.html">{html.escape(t['name'])}</a>
              </h3>
              <span class="card-badge-category">{html.escape(t['category'])}</span>
            </div>
            <p class="card-desc">{html.escape(t['short_description'])}</p>
            <div class="card-meta-line">
              <span class="meta-pill {status_class}">● {status_label}</span>
              <span class="meta-pill">{html.escape(t['framework'])}</span>
              <span class="meta-pill">Client-Side</span>
            </div>
          </div>
          <div class="card-actions">
            {launch_btn}
            <a href="tools/{t['seo_slug']}.html" class="btn-doc">Details</a>
            <a href="{t['repository_url']}" target="_blank" rel="noopener noreferrer" class="btn-doc" title="View Source on GitHub">
              <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
              </svg>
            </a>
          </div>
        </article>
        """
        tool_cards_html.append(card)

    json_ld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "DeveloperOS Tools Directory",
        "url": SITE_URL,
        "description": "Comprehensive catalog of 100% free, offline-first, client-side developer utilities.",
        "publisher": {
            "@type": "Organization",
            "name": "DeveloperOS",
            "url": MAIN_SITE_URL
        }
    }

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DeveloperOS Tools Directory — 20+ Free, Offline-First Developer Utilities</title>
  <meta name="description" content="Discover 20+ offline-first, zero-telemetry developer utilities. Format JSON, decode JWTs, convert colors, test regex, and build cron schedules client-side.">
  <link rel="canonical" href="{SITE_URL}/">
  
  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="DeveloperOS Tools Directory — 20+ Free Developer Utilities">
  <meta property="og:description" content="Instant, client-side, zero-telemetry developer utilities. 100% open source under MIT.">
  <meta property="og:url" content="{SITE_URL}/">
  <meta property="og:site_name" content="DeveloperOS">
  
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="DeveloperOS Tools Directory">
  <meta name="twitter:description" content="Instant, client-side, zero-telemetry developer utilities.">
  
  <link rel="stylesheet" href="assets/styles.css">
  
  <!-- Structured Data -->
  <script type="application/ld+json">
  {json.dumps(json_ld, indent=2)}
  </script>
</head>
<body>
  {render_navbar(depth=0)}

  <header class="hero">
    <h1>All Developer Tools in One Place</h1>
    <p>Offline-first, client-side, zero-telemetry utilities for modern engineers. No paywalls, no tracking, completely open source.</p>
    <div class="hero-stats">
      <span class="hero-stat-badge"><span class="dot-live"></span> <strong>{len(tools)}</strong> Utilities Cataloged</span>
      <span>🔒 100% In-Memory Privacy</span>
      <span>⚡ Zero Backend Required</span>
    </div>
  </header>

  <section class="search-section">
    <div class="search-input-wrapper">
      <span class="search-icon">🔍</span>
      <input type="text" id="toolSearch" class="search-input" placeholder="Search utilities by name, category, or algorithm (e.g. JSON, JWT, Hash, Regex)..." autocomplete="off">
      <span class="search-kbd">/</span>
    </div>

    <div class="category-chips" id="categoryChips">
      <button class="chip active">All</button>
      {"".join([f'<button class="chip">{html.escape(c)}</button>' for c in categories])}
    </div>
  </section>

  <main class="catalog-container">
    <div class="tools-count-bar">
      <span id="toolCount">Showing {len(tools)} developer tools</span>
      <span>Ecosystem: <a href="{MAIN_SITE_URL}" target="_blank">developeros.in</a></span>
    </div>
    <div class="tool-grid" id="toolGrid">
      {"".join(tool_cards_html)}
    </div>

    {render_main_promotional_banner(tool_name=None, depth=0)}
  </main>

  {render_footer()}

  <!-- Embedded Registry Data for Instant Client Search -->
  <script type="application/json" id="registryData">
  {json.dumps(registry)}
  </script>
  <script src="assets/catalog.js"></script>
</body>
</html>
"""
    (DIST_DIR / "index.html").write_text(index_html, encoding="utf-8")


def build_tool_pages(registry: dict):
    tools = registry.get("tools", [])

    for tool in tools:
        slug = tool["seo_slug"]
        is_live = tool["availability_status"] == "verified_live" and bool(tool["live_url"])
        status_label = "Verified Live" if is_live else "Staged in Suite (Ready for Local & Cloud Execution)"
        status_color = "var(--color-success)" if is_live else "var(--color-warning)"

        # Find related tools (same category)
        related = [t for t in tools if t["category"] == tool["category"] and t["id"] != tool["id"]][:3]
        related_html = "".join([
            f'<div style="background-color: var(--color-canvas); padding: 14px; border-radius: var(--radius-sm); border: 1px solid var(--color-border); margin-top: 8px;">'
            f'  <strong style="color: var(--color-text);"><a href="{t["seo_slug"]}.html">{html.escape(t["name"])}</a></strong>'
            f'  <p style="font-size: 0.85rem; color: var(--color-text-muted); margin-top: 4px;">{html.escape(t["short_description"])}</p>'
            f'</div>'
            for t in related
        ])

        launch_ui = (
            f'<a href="{tool["live_url"]}" target="_blank" rel="noopener noreferrer" class="btn-launch" style="padding: 12px 24px; font-size: 1rem;">⚡ Launch Live Application</a>'
            if is_live
            else f'<div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: var(--radius-sm); padding: 14px 18px; color: var(--color-warning); font-size: 0.9rem;">'
                 f'  ⚠️ <strong>Status: Staged Locally</strong><br>'
                 f'  This utility is packaged and tested in <a href="{tool["repository_url"]}" target="_blank" style="color: var(--color-warning); text-decoration: underline;">{html.escape(tool["parent_suite"]["name"])}</a>. '
                 f'  Per DeveloperOS safety standards, public live links are only published once deployed and verified. Run locally with <code>streamlit run app.py</code>.'
                 f'</div>'
        )

        tool_schema = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": tool["name"],
            "description": tool["short_description"],
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "All",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
            },
            "author": {
                "@type": "Organization",
                "name": "DeveloperOS",
                "url": MAIN_SITE_URL
            }
        }

        page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(tool['name'])} — Free Online & Offline Developer Tool | DeveloperOS</title>
  <meta name="description" content="{html.escape(tool['short_description'])}">
  <link rel="canonical" href="{SITE_URL}/tools/{slug}.html">
  
  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(tool['name'])} — DeveloperOS">
  <meta property="og:description" content="{html.escape(tool['short_description'])}">
  <meta property="og:url" content="{SITE_URL}/tools/{slug}.html">
  <meta property="og:site_name" content="DeveloperOS Tools">
  
  <!-- Twitter -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{html.escape(tool['name'])}">
  <meta name="twitter:description" content="{html.escape(tool['short_description'])}">
  
  <link rel="stylesheet" href="../assets/styles.css">
  
  <script type="application/ld+json">
  {json.dumps(tool_schema, indent=2)}
  </script>
</head>
<body>
  {render_navbar(depth=1)}

  <main class="tool-page-container">
    <nav class="breadcrumb">
      <a href="../index.html">Tools Directory</a>
      <span>›</span>
      <span>{html.escape(tool['category'])}</span>
      <span>›</span>
      <span style="color: var(--color-text); font-weight: 600;">{html.escape(tool['name'])}</span>
    </nav>

    <div class="tool-header-block">
      <span class="card-badge-category">{html.escape(tool['category'])}</span>
      <h1 style="margin-top: 10px;">{html.escape(tool['name'])}</h1>
      <p style="font-size: 1.15rem; color: var(--color-text-muted);">{html.escape(tool['short_description'])}</p>

      <div class="tool-header-meta">
        <span class="meta-pill" style="color: {status_color}; font-weight: 600;">● {status_label}</span>
        <span class="meta-pill">Framework: {html.escape(tool['framework'])}</span>
        <span class="meta-pill">Suite: {html.escape(tool['parent_suite']['name'])}</span>
        <span class="meta-pill">Privacy: {html.escape(tool['privacy_classification'])}</span>
      </div>

      <div style="margin-top: 24px; display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
        {launch_ui}
        <a href="{tool['repository_url']}" target="_blank" rel="noopener noreferrer" class="btn-doc" style="padding: 11px 18px;">
          View Repository on GitHub ↗
        </a>
      </div>
    </div>

    <section class="tool-detail-section">
      <h2>Functionality & Technical Details</h2>
      <p style="color: var(--color-text-muted); font-size: 1rem; line-height: 1.7;">
        {html.escape(tool['long_description'])}
      </p>

      <h3 style="font-size: 1.1rem; margin-top: 22px; margin-bottom: 8px; color: var(--color-text);">Local Execution Guide</h3>
      <p style="font-size: 0.9rem; color: var(--color-text-muted);">
        Clone the standalone suite and launch the application locally with full offline security:
      </p>
      <div class="code-box">git clone {tool['repository_url']}.git
cd {Path(tool['repository_url']).name}
pip install -r requirements.txt
streamlit run app.py</div>
    </section>

    <section class="tool-detail-section">
      <h2>Privacy & Client-Side Architecture</h2>
      <p style="color: var(--color-text-muted); font-size: 0.95rem; line-height: 1.6;">
        All operations in <strong>{html.escape(tool['name'])}</strong> run strictly in-memory client-side. No input strings, files, or sensitive payloads are ever persisted to disk, transmitted across networks, or sent to tracking third parties.
      </p>
    </section>

    <section class="tool-detail-section">
      <h2>Related Developer Utilities</h2>
      {related_html if related_html else '<p style="color: var(--color-text-dim);">No related tools in this category.</p>'}
    </section>

    {render_main_promotional_banner(tool_name=tool['name'], depth=1)}
  </main>

  {render_footer()}
</body>
</html>
"""
        (DIST_DIR / "tools" / f"{slug}.html").write_text(page_html, encoding="utf-8")


def build_sitemap_and_robots(registry: dict):
    tools = registry.get("tools", [])

    # 1. Sitemap
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f'  <url><loc>{SITE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>',
    ]
    for t in tools:
        sitemap_lines.append(
            f'  <url><loc>{SITE_URL}/tools/{t["seo_slug"]}.html</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>'
        )
    sitemap_lines.append('</urlset>')

    (DIST_DIR / "sitemap.xml").write_text("\n".join(sitemap_lines), encoding="utf-8")

    # 2. Robots.txt
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    (DIST_DIR / "robots.txt").write_text(robots_content, encoding="utf-8")


def main():
    print("=" * 60)
    print("DeveloperOS Tools Web Portal SSG Build")
    print(f"Target URL: {SITE_URL}")
    print("=" * 60)

    reg = load_registry()
    tools = reg.get("tools", [])
    print(f"--> Loaded registry with {len(tools)} tools.")

    setup_dist()
    print("--> Dist directories initialized & assets copied.")

    build_index_page(reg)
    print("--> dist/index.html generated.")

    build_tool_pages(reg)
    print(f"--> Generated {len(tools)} individual SEO landing pages in dist/tools/.")

    build_sitemap_and_robots(reg)
    print("--> dist/sitemap.xml & dist/robots.txt generated.")

    print("\n[SUCCESS] Web directory built successfully in dist/.")


if __name__ == "__main__":
    main()
