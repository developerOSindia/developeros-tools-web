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

SITE_URL = "https://toolkit.developeros.in"
MAIN_SITE_URL = "https://developeros.in"
GITHUB_ORG_URL = "https://github.com/developerOSindia"

PLAYGROUND_TOOLS = {
    "json-formatter": "json",
    "json-validator": "json",
    "base64-codec": "base64",
    "hash-calculator": "hash",
    "uuid-generator": "uuid",
    "jwt-decoder": "jwt",
}


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


def render_playground_drawer() -> str:
    return """
  <!-- Interactive Playground Drawer (Obsidian Engine) -->
  <div id="playgroundOverlay" class="playground-overlay" onclick="handlePlaygroundOverlayClick(event)" aria-hidden="true">
    <aside id="playgroundDrawer" class="playground-drawer" role="dialog" aria-modal="true" aria-labelledby="playgroundTitle">
      <div class="playground-header">
        <div class="playground-header-info">
          <div class="playground-tag-line">
            <span class="playground-badge">⚡ Live Sandbox</span>
            <span class="playground-privacy-pill">🔒 100% In-Memory &bull; Zero Telemetry</span>
          </div>
          <h2 id="playgroundTitle" class="playground-title">DeveloperOS Playground</h2>
        </div>
        <button type="button" class="playground-close-btn" onclick="closePlayground()" aria-label="Close Playground" title="Close (Esc)">
          ✕
        </button>
      </div>

      <!-- Playground Tool Tabs -->
      <nav class="playground-tabs" role="tablist" aria-label="Playground Tools">
        <button type="button" class="playground-tab active" data-tab="json" role="tab" id="tab-json" aria-controls="panel-json" aria-selected="true" onclick="switchPlaygroundTab('json')">
          <span class="tab-icon">{ }</span>
          <span class="tab-text">JSON</span>
        </button>
        <button type="button" class="playground-tab" data-tab="base64" role="tab" id="tab-base64" aria-controls="panel-base64" aria-selected="false" onclick="switchPlaygroundTab('base64')">
          <span class="tab-icon">🔤</span>
          <span class="tab-text">Base64</span>
        </button>
        <button type="button" class="playground-tab" data-tab="hash" role="tab" id="tab-hash" aria-controls="panel-hash" aria-selected="false" onclick="switchPlaygroundTab('hash')">
          <span class="tab-icon">#</span>
          <span class="tab-text">Hash</span>
        </button>
        <button type="button" class="playground-tab" data-tab="uuid" role="tab" id="tab-uuid" aria-controls="panel-uuid" aria-selected="false" onclick="switchPlaygroundTab('uuid')">
          <span class="tab-icon">🆔</span>
          <span class="tab-text">UUID</span>
        </button>
        <button type="button" class="playground-tab" data-tab="jwt" role="tab" id="tab-jwt" aria-controls="panel-jwt" aria-selected="false" onclick="switchPlaygroundTab('jwt')">
          <span class="tab-icon">🔑</span>
          <span class="tab-text">JWT</span>
        </button>
      </nav>

      <div class="playground-body">
        <!-- 1. JSON Formatter & Minifier Panel -->
        <section id="panel-json" class="playground-panel active" role="tabpanel" aria-labelledby="tab-json">
          <div class="panel-header">
            <div>
              <h3 class="panel-heading">JSON Formatter &amp; Minifier</h3>
              <p class="panel-desc">Beautify, validate, or compact JSON strings purely in-browser.</p>
            </div>
            <button type="button" class="btn-mini btn-subtle" onclick="loadJsonSample()">Load Sample</button>
          </div>

          <div class="playground-input-group">
            <label for="jsonPlaygroundInput" class="playground-label">JSON Input</label>
            <textarea id="jsonPlaygroundInput" class="playground-textarea" rows="7" placeholder='Paste raw or unformatted JSON here (e.g. {"key": "val"})...'></textarea>
          </div>

          <div class="playground-actions-row">
            <button type="button" class="btn-mini btn-action-primary" onclick="formatJson(2)">Beautify (2 Spaces)</button>
            <button type="button" class="btn-mini btn-action-secondary" onclick="formatJson(4)">Beautify (4 Spaces)</button>
            <button type="button" class="btn-mini btn-action-secondary" onclick="minifyJson()">Minify</button>
            <button type="button" class="btn-mini btn-subtle" onclick="clearJson()">Clear</button>
          </div>

          <div id="jsonPlaygroundError" class="playground-error-banner" style="display: none;" role="alert"></div>

          <div class="playground-output-group">
            <div class="output-header-line">
              <label for="jsonPlaygroundOutput" class="playground-label">Formatted Result</label>
              <div class="output-actions">
                <span id="jsonStats" class="output-stat"></span>
                <button type="button" class="btn-mini btn-subtle" onclick="copyJsonOutput()">📋 Copy</button>
              </div>
            </div>
            <textarea id="jsonPlaygroundOutput" class="playground-textarea output-area" rows="8" readonly placeholder="Formatted or minified output will appear here..."></textarea>
          </div>
        </section>

        <!-- 2. Base64 Codec Panel -->
        <section id="panel-base64" class="playground-panel" role="tabpanel" aria-labelledby="tab-base64">
          <div class="panel-header">
            <div>
              <h3 class="panel-heading">Base64 Encoder / Decoder</h3>
              <p class="panel-desc">Encode or decode strings with full UTF-8 Unicode multilingual support.</p>
            </div>
            <button type="button" class="btn-mini btn-subtle" onclick="loadBase64Sample()">Load Sample</button>
          </div>

          <div class="base64-mode-selector">
            <button type="button" class="mode-tab active" id="b64ModeEncode" onclick="setBase64Mode('encode')">Encode to Base64</button>
            <button type="button" class="mode-tab" id="b64ModeDecode" onclick="setBase64Mode('decode')">Decode from Base64</button>
          </div>

          <div class="playground-input-group">
            <label for="base64PlaygroundInput" id="base64InputLabel" class="playground-label">Plaintext Input (UTF-8)</label>
            <textarea id="base64PlaygroundInput" class="playground-textarea" rows="6" placeholder="Enter plaintext to encode..."></textarea>
          </div>

          <div class="playground-actions-row">
            <button type="button" class="btn-mini btn-action-primary" id="b64ConvertBtn" onclick="runBase64()">Encode Now</button>
            <button type="button" class="btn-mini btn-subtle" onclick="clearBase64()">Clear</button>
          </div>

          <div id="base64PlaygroundError" class="playground-error-banner" style="display: none;" role="alert"></div>

          <div class="playground-output-group">
            <div class="output-header-line">
              <label for="base64PlaygroundOutput" id="base64OutputLabel" class="playground-label">Base64 Output</label>
              <button type="button" class="btn-mini btn-subtle" onclick="copyBase64Output()">📋 Copy</button>
            </div>
            <textarea id="base64PlaygroundOutput" class="playground-textarea output-area" rows="6" readonly placeholder="Output will appear here..."></textarea>
          </div>
        </section>

        <!-- 3. Hash Generator Panel -->
        <section id="panel-hash" class="playground-panel" role="tabpanel" aria-labelledby="tab-hash">
          <div class="panel-header">
            <div>
              <h3 class="panel-heading">Cryptographic Hash Generator</h3>
              <p class="panel-desc">Real-time SHA-256, SHA-1, and SHA-512 hashes via Web Crypto API.</p>
            </div>
            <button type="button" class="btn-mini btn-subtle" onclick="loadHashSample()">Load Sample</button>
          </div>

          <div class="playground-input-group">
            <label for="hashPlaygroundInput" class="playground-label">Input Text</label>
            <textarea id="hashPlaygroundInput" class="playground-textarea" rows="4" placeholder="Type or paste text to compute hashes in real-time..."></textarea>
          </div>

          <div class="hash-results-list">
            <div class="hash-result-card">
              <div class="hash-header">
                <span class="hash-algo">SHA-256</span>
                <span class="hash-len">256-bit &bull; 64 hex chars</span>
                <button type="button" class="btn-mini btn-subtle" onclick="copyHash('sha256')">📋 Copy</button>
              </div>
              <input type="text" id="hashOutputSha256" class="hash-output-field" readonly placeholder="Compute SHA-256..." />
            </div>

            <div class="hash-result-card">
              <div class="hash-header">
                <span class="hash-algo">SHA-1</span>
                <span class="hash-len">160-bit &bull; 40 hex chars</span>
                <button type="button" class="btn-mini btn-subtle" onclick="copyHash('sha1')">📋 Copy</button>
              </div>
              <input type="text" id="hashOutputSha1" class="hash-output-field" readonly placeholder="Compute SHA-1..." />
            </div>

            <div class="hash-result-card">
              <div class="hash-header">
                <span class="hash-algo">SHA-512</span>
                <span class="hash-len">512-bit &bull; 128 hex chars</span>
                <button type="button" class="btn-mini btn-subtle" onclick="copyHash('sha512')">📋 Copy</button>
              </div>
              <input type="text" id="hashOutputSha512" class="hash-output-field" readonly placeholder="Compute SHA-512..." />
            </div>
          </div>
        </section>

        <!-- 4. UUID Generator Panel -->
        <section id="panel-uuid" class="playground-panel" role="tabpanel" aria-labelledby="tab-uuid">
          <div class="panel-header">
            <div>
              <h3 class="panel-heading">UUID / GUID Generator</h3>
              <p class="panel-desc">Cryptographically random Version 4 UUIDs using crypto.randomUUID().</p>
            </div>
          </div>

          <div class="uuid-options-grid">
            <div class="uuid-option-group">
              <label class="playground-label">Quantity</label>
              <div class="uuid-qty-selector">
                <button type="button" class="qty-btn active" data-qty="1" onclick="setUuidQty(1)">1</button>
                <button type="button" class="qty-btn" data-qty="5" onclick="setUuidQty(5)">5</button>
                <button type="button" class="qty-btn" data-qty="10" onclick="setUuidQty(10)">10</button>
                <button type="button" class="qty-btn" data-qty="25" onclick="setUuidQty(25)">25</button>
              </div>
            </div>

            <div class="uuid-checkboxes">
              <label class="custom-checkbox-label">
                <input type="checkbox" id="uuidOptUppercase" onchange="generateUuids()" />
                <span>Uppercase</span>
              </label>
              <label class="custom-checkbox-label">
                <input type="checkbox" id="uuidOptHyphens" checked onchange="generateUuids()" />
                <span>Include Hyphens</span>
              </label>
            </div>
          </div>

          <div class="playground-actions-row">
            <button type="button" class="btn-mini btn-action-primary" onclick="generateUuids()">🔄 Generate New UUIDs</button>
            <button type="button" class="btn-mini btn-subtle" onclick="copyAllUuids()">📋 Copy All</button>
          </div>

          <div class="playground-output-group">
            <div id="uuidOutputContainer" class="uuid-list-container" role="list"></div>
          </div>
        </section>

        <!-- 5. JWT Claims Inspector Panel -->
        <section id="panel-jwt" class="playground-panel" role="tabpanel" aria-labelledby="tab-jwt">
          <div class="panel-header">
            <div>
              <h3 class="panel-heading">JWT Claims Inspector</h3>
              <p class="panel-desc">Parse and decode JSON Web Tokens into header, payload, and claims.</p>
            </div>
            <button type="button" class="btn-mini btn-subtle" onclick="loadJwtSample()">Load Sample</button>
          </div>

          <div class="playground-input-group">
            <label for="jwtPlaygroundInput" class="playground-label">Encoded JWT Token</label>
            <textarea id="jwtPlaygroundInput" class="playground-textarea" rows="4" placeholder="Paste encoded JWT (header.payload.signature)..."></textarea>
          </div>

          <div class="playground-actions-row">
            <button type="button" class="btn-mini btn-action-primary" onclick="inspectJwt()">Inspect Claims</button>
            <button type="button" class="btn-mini btn-subtle" onclick="clearJwt()">Clear</button>
          </div>

          <div id="jwtPlaygroundError" class="playground-error-banner" style="display: none;" role="alert"></div>

          <div id="jwtPlaygroundResult" class="jwt-result-container" style="display: none;">
            <div id="jwtMetaStatus" class="jwt-meta-status"></div>

            <div class="jwt-part-box">
              <div class="jwt-part-header">
                <span class="jwt-part-title" style="color: #f43f5e;">HEADER (Algorithm &amp; Token Type)</span>
                <button type="button" class="btn-mini btn-subtle" onclick="copyJwtPart('header')">📋 Copy</button>
              </div>
              <pre id="jwtHeaderOutput" class="jwt-code-output"></pre>
            </div>

            <div class="jwt-part-box">
              <div class="jwt-part-header">
                <span class="jwt-part-title" style="color: #06b6d4;">PAYLOAD (Claims &amp; Data)</span>
                <button type="button" class="btn-mini btn-subtle" onclick="copyJwtPart('payload')">📋 Copy</button>
              </div>
              <pre id="jwtPayloadOutput" class="jwt-code-output"></pre>
            </div>

            <div class="jwt-part-box">
              <div class="jwt-part-header">
                <span class="jwt-part-title" style="color: #10b981;">SIGNATURE</span>
              </div>
              <pre id="jwtSignatureOutput" class="jwt-code-output signature-output"></pre>
            </div>
          </div>
        </section>
      </div>
    </aside>
  </div>
"""


def render_shortcuts_modal() -> str:
    return """
  <!-- Keyboard Shortcut Cheat Sheet Modal -->
  <div id="shortcutsModalOverlay" class="shortcuts-modal-overlay" onclick="handleShortcutsOverlayClick(event)" aria-hidden="true">
    <div class="shortcuts-modal" role="dialog" aria-modal="true" aria-labelledby="shortcutsModalTitle">
      <div class="shortcuts-modal-header">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="font-size: 1.3rem;">⌨️</span>
          <h3 id="shortcutsModalTitle" class="shortcuts-title">Keyboard Shortcuts</h3>
        </div>
        <button type="button" class="playground-close-btn" onclick="closeShortcutsModal()" aria-label="Close shortcuts modal" title="Close (Esc)">
          ✕
        </button>
      </div>

      <div class="shortcuts-modal-body">
        <p class="shortcuts-intro">Navigate and test DeveloperOS tools with instant keyboard commands:</p>
        <div class="shortcuts-table">
          <div class="shortcut-row">
            <div class="shortcut-keys"><kbd>?</kbd></div>
            <div class="shortcut-desc">Open / close this keyboard shortcuts cheat sheet</div>
          </div>
          <div class="shortcut-row">
            <div class="shortcut-keys"><kbd>/</kbd></div>
            <div class="shortcut-desc">Focus the search bar instantly from anywhere</div>
          </div>
          <div class="shortcut-row">
            <div class="shortcut-keys"><kbd>Esc</kbd></div>
            <div class="shortcut-desc">Close any open drawer, modal, or dropdown</div>
          </div>
          <div class="shortcut-row">
            <div class="shortcut-keys"><kbd>1</kbd> &ndash; <kbd>9</kbd></div>
            <div class="shortcut-desc">Quick-filter categories (1 = All, 2..9 = Categories)</div>
          </div>
          <div class="shortcut-row">
            <div class="shortcut-keys"><kbd>P</kbd></div>
            <div class="shortcut-desc">Open live interactive mini-playground drawer</div>
          </div>
          <div class="shortcut-row">
            <div class="shortcut-keys"><kbd>E</kbd></div>
            <div class="shortcut-desc">Toggle the offline catalog export menu</div>
          </div>
        </div>
      </div>

      <div class="shortcuts-modal-footer">
        <span class="shortcuts-footer-note">Obsidian Engine &bull; Zero Telemetry</span>
        <button type="button" class="btn-shortcuts-done" onclick="closeShortcutsModal()">Got it (Esc)</button>
      </div>
    </div>
  </div>
"""


def build_index_page(registry: dict):
    tools = registry.get("tools", [])
    categories = sorted(list({t["category"] for t in tools}))
    tool_cards_html = []

    for t in tools:
        is_live = t["availability_status"] == "verified_live" and bool(t["live_url"])
        status_label = "Verified Live" if is_live else "Staged Offline"
        status_class = "status-live" if is_live else "status-staged"
        target_url = t["live_url"] if is_live else f"tools/{t['seo_slug']}.html"
        safe_name = t["name"].replace("'", "\\'")

        launch_btn = (
            f'<a href="{t["live_url"]}" target="_blank" rel="noopener noreferrer" class="btn-launch">⚡ Launch Tool ↗</a>'
            if is_live
            else f'<a href="tools/{t["seo_slug"]}.html" class="btn-launch" style="background-color: var(--color-surface-elevated); color: var(--color-text); border: 1px solid var(--color-border);">📖 View Docs</a>'
        )

        playground_btn = ""
        if t["seo_slug"] in PLAYGROUND_TOOLS:
            pg_tab = PLAYGROUND_TOOLS[t["seo_slug"]]
            playground_btn = f'<button type="button" class="btn-test-browser" onclick="openPlayground(\'{pg_tab}\')" title="Test {safe_name} in browser">⚡ Test In Browser</button>'

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
            {playground_btn}
            {launch_btn}
            <button type="button" class="btn-quick-copy" onclick="copyToolLink('{target_url}', '{safe_name}')" title="Copy Tool Link to Clipboard">
              📋 Copy Link
            </button>
            <button type="button" class="btn-cli-copy" onclick="copyCliCommand('{t['seo_slug']}')" title="Copy CLI Command">
              &gt;_ CLI
            </button>
            <a href="tools/{t['seo_slug']}.html" class="btn-doc" title="Tool Details">Details</a>
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
      <div class="tools-bar-actions">
        <!-- Export Catalog Dropdown -->
        <div class="export-dropdown" id="exportDropdown">
          <button type="button" class="btn-export-dropdown" id="exportDropdownBtn" onclick="toggleExportDropdown(event)" aria-haspopup="true" aria-expanded="false" title="Export catalog for offline reference">
            <span>📥 Export Catalog</span>
            <span class="dropdown-chevron">▾</span>
          </button>
          <div class="export-dropdown-menu" id="exportDropdownMenu" role="menu">
            <button type="button" class="export-menu-item" role="menuitem" onclick="exportCatalog('json')">
              <span class="export-badge-format">JSON</span>
              <div class="export-item-text">
                <strong>developeros-tools.json</strong>
                <small>Full offline machine-readable registry</small>
              </div>
            </button>
            <button type="button" class="export-menu-item" role="menuitem" onclick="exportCatalog('md')">
              <span class="export-badge-format" style="color: #06b6d4; border-color: rgba(6, 182, 212, 0.4); background: rgba(6, 182, 212, 0.1);">MD</span>
              <div class="export-item-text">
                <strong>developeros-tools.md</strong>
                <small>Categorized offline Markdown reference</small>
              </div>
            </button>
          </div>
        </div>

        <!-- Shortcuts trigger button -->
        <button type="button" class="btn-toolbar-tool" onclick="openShortcutsModal()" title="Keyboard Shortcuts (?)">
          <kbd class="mini-kbd">?</kbd>
          <span>Shortcuts</span>
        </button>

        <!-- Playground trigger button -->
        <button type="button" class="btn-toolbar-tool btn-toolbar-playground" onclick="openPlayground('json')" title="Open Interactive Mini-Playground">
          <span>⚡ Playground</span>
        </button>
      </div>
    </div>
    <div class="tool-grid" id="toolGrid">
      {"".join(tool_cards_html)}
    </div>

    {render_main_promotional_banner(tool_name=None, depth=0)}
  </main>

  {render_footer()}

  <div id="quick-toast" class="quick-toast" role="status" aria-live="polite">
    <span class="quick-toast-icon">✓</span>
    <span id="quick-toast-msg"></span>
  </div>

  <nav class="mobile-bottom-nav" role="navigation" aria-label="Mobile Navigation">
    <a href="index.html" class="mobile-nav-item active">
      <span style="font-size: 1.15rem;">⚡</span>
      <span>Tools</span>
    </a>
    <a href="https://developeros.in?utm_source=developeros_tools&utm_medium=mobile_dock&utm_campaign=ecosystem_referral" class="mobile-nav-item" target="_blank" rel="noopener noreferrer">
      <span style="font-size: 1.15rem;">🌐</span>
      <span>DeveloperOS</span>
    </a>
    <a href="{GITHUB_ORG_URL}" class="mobile-nav-item" target="_blank" rel="noopener noreferrer">
      <span style="font-size: 1.15rem;">🐙</span>
      <span>GitHub</span>
    </a>
    <a href="{MAIN_SITE_URL}/privacy?utm_source=developeros_tools&utm_medium=mobile_dock&utm_campaign=ecosystem_referral" class="mobile-nav-item" target="_blank" rel="noopener noreferrer">
      <span style="font-size: 1.15rem;">🛡️</span>
      <span>Privacy</span>
    </a>
  </nav>

  {render_playground_drawer()}
  {render_shortcuts_modal()}

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

        playground_link = ""
        if slug in PLAYGROUND_TOOLS:
            pg_tab = PLAYGROUND_TOOLS[slug]
            playground_link = f'<a href="../index.html?playground={pg_tab}" class="btn-test-browser" style="padding: 11px 18px; min-height: 44px; text-decoration: none;">⚡ Test In Browser</a>'

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
        {playground_link}
        {launch_ui}
        <button type="button" class="btn-quick-copy" onclick="copyToolLink('{SITE_URL}/tools/{slug}.html', '{html.escape(tool['name'])}')" style="padding: 11px 18px; min-height: 44px;">
          📋 Copy Tool Link
        </button>
        <button type="button" class="btn-cli-copy" onclick="copyCliCommand('{slug}')" style="padding: 11px 18px; min-height: 44px;">
          &gt;_ Copy CLI
        </button>
        <a href="{tool['repository_url']}" target="_blank" rel="noopener noreferrer" class="btn-doc" style="padding: 11px 18px; min-height: 44px;">
          View Repository on GitHub ↗
        </a>
      </div>
    </div>

    <section class="tool-detail-section">
      <h2>Functionality & Technical Details</h2>
      <p style="color: var(--color-text-muted); font-size: 1rem; line-height: 1.7;">
        {html.escape(tool['long_description'])}
      </p>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 22px; margin-bottom: 8px;">
        <h3 style="font-size: 1.1rem; margin: 0; color: var(--color-text);">Local Execution Guide</h3>
        <button type="button" class="btn-quick-copy" onclick="copyCodeBlock('install-code-{slug}')" style="font-size: 0.78rem; padding: 6px 12px; min-height: 36px;">
          📋 Copy Commands
        </button>
      </div>
      <p style="font-size: 0.9rem; color: var(--color-text-muted);">
        Clone the standalone suite and launch the application locally with full offline security:
      </p>
      <pre class="code-box" id="install-code-{slug}">git clone {tool['repository_url']}.git
cd {Path(tool['repository_url']).name}
pip install -r requirements.txt
streamlit run app.py</pre>
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

  <div id="quick-toast" class="quick-toast" role="status" aria-live="polite">
    <span class="quick-toast-icon">✓</span>
    <span id="quick-toast-msg"></span>
  </div>

  <script>
  let toastTimer = null;
  function triggerToast(msg) {{
    const toast = document.getElementById('quick-toast');
    const msgEl = document.getElementById('quick-toast-msg');
    if (msgEl) msgEl.textContent = msg;
    if (toast) {{
      toast.classList.add('show');
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => toast.classList.remove('show'), 2200);
    }}
  }}
  function copyToolLink(url, name) {{
    navigator.clipboard.writeText(url).then(() => triggerToast('Copied ' + name + ' link! 📋'));
  }}
  function copyCliCommand(slug) {{
    navigator.clipboard.writeText('devos ' + slug).then(() => triggerToast('Copied CLI: devos ' + slug + ' 🚀'));
  }}
  function copyCodeBlock(id) {{
    const el = document.getElementById(id);
    if (el) {{
      navigator.clipboard.writeText(el.textContent.trim()).then(() => triggerToast('Copied install commands! 📋'));
    }}
  }}
  </script>
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
