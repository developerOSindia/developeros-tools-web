/**
 * DeveloperOS Universal Promotional Banner Component (JavaScript / Web Components)
 * Reusable banner templates for web portals, static sites, and client-side applications.
 */

export const BANNER_CONFIG = {
  mainUrl: "https://developeros.in?utm_source=developeros_tools&utm_medium=main_banner&utm_campaign=ecosystem_referral",
  toolsUrl: "https://tools.developeros.in?utm_source=developeros_tools&utm_medium=secondary_cta&utm_campaign=tools_directory",
  githubUrl: "https://github.com/developerOSindia",
  privacyUrl: "https://developeros.in/privacy?utm_source=developeros_tools&utm_medium=footer_link&utm_campaign=ecosystem_referral",
};

export const DEVOS_LOGO_SVG = `
<svg viewBox="0 0 64 64" width="40" height="40" fill="none" style="flex-shrink: 0;" aria-hidden="true">
  <defs>
    <linearGradient id="webPromoFavGrad" x1="10%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff3b30"/>
      <stop offset="48%" stop-color="#ff5a3d"/>
      <stop offset="100%" stop-color="#ff914d"/>
    </linearGradient>
    <linearGradient id="webPromoPanelGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b1b1f"/>
      <stop offset="100%" stop-color="#242428"/>
    </linearGradient>
  </defs>
  <rect x="34" y="12" width="22" height="10" rx="2.5" fill="url(#webPromoPanelGrad)" stroke="rgba(255,255,255,0.06)"/>
  <rect x="34" y="26" width="22" height="10" rx="2.5" fill="url(#webPromoPanelGrad)" stroke="rgba(255,255,255,0.06)"/>
  <rect x="34" y="40" width="22" height="10" rx="2.5" fill="url(#webPromoPanelGrad)" stroke="rgba(255,255,255,0.06)"/>
  <path d="M15 20.5L33.5 14V49.5L15 46Z" fill="#05070a" stroke="url(#webPromoFavGrad)" stroke-width="2.8" stroke-linejoin="round"/>
  <path d="M15 20.5V46" stroke="url(#webPromoFavGrad)" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M33.5 14V49.5" stroke="url(#webPromoFavGrad)" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M22 23L27 25.8L22 28.6" stroke="#f8fafc" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="23.5" y1="34.2" x2="29.2" y2="34.2" stroke="#f8fafc" stroke-width="2.8" stroke-linecap="round"/>
</svg>`;

export function renderMainPromotionalBanner(options = {}) {
  const heading = options.toolName ? `Enjoying ${options.toolName}?` : (options.heading || "Enjoying this free tool?");
  const description = options.description || "Discover more developer tools, AI resources, and automation solutions from DeveloperOS.";
  const primaryCta = options.primaryCtaText || "Explore DeveloperOS";
  const secondaryCta = options.secondaryCtaText || "More Free Tools";
  const pUrl = options.primaryUrl || BANNER_CONFIG.mainUrl;
  const sUrl = options.secondaryUrl || BANNER_CONFIG.toolsUrl;

  return `
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
            ${DEVOS_LOGO_SVG}
            <div>
                <h3 style="margin: 0 0 0.35rem 0; font-size: 1.2rem; font-weight: 700; color: var(--color-text, #f8fafc); letter-spacing: -0.01em;">
                    ${heading}
                </h3>
                <p style="margin: 0; color: var(--color-text-muted, #94a3b8); font-size: 0.95rem; line-height: 1.5;">
                    ${description}
                </p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.85rem; flex-wrap: wrap;">
            <a href="${pUrl}" target="_blank" rel="noopener noreferrer" style="
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
                ${primaryCta} &rarr;
            </a>
            <a href="${sUrl}" target="_blank" rel="noopener noreferrer" style="
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
                ${secondaryCta}
            </a>
        </div>
    </section>
  `;
}

export function renderCompactHeaderBanner(text = "Powered by DeveloperOS ↗", url = null) {
  const targetUrl = url || "https://developeros.in?utm_source=developeros_tools&utm_medium=header_banner&utm_campaign=powered_by";
  return `
    <a href="${targetUrl}" target="_blank" rel="noopener noreferrer" class="devos-compact-header-banner" style="
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: rgba(249, 115, 22, 0.1);
        border: 1px solid rgba(249, 115, 22, 0.3);
        color: var(--color-primary, #f97316);
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        text-decoration: none;
        letter-spacing: 0.01em;
    ">
        <span>⚡</span>
        <span>${text}</span>
    </a>
  `;
}

export function renderFooterBanner() {
  return `
    <footer class="devos-footer-banner" role="contentinfo" style="
        margin-top: 3.5rem;
        padding: 2rem 0 1.25rem 0;
        border-top: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
        text-align: center;
        color: var(--color-text-muted, #cbd5e1);
        font-size: 0.875rem;
    ">
        <p style="font-size: 1rem; font-weight: 600; color: var(--color-text, #f8fafc); margin: 0 0 0.85rem 0;">
            Built with ❤️ by <a href="${BANNER_CONFIG.mainUrl}" target="_blank" rel="noopener noreferrer" style="color: var(--color-primary, #f97316); text-decoration: none; font-weight: 700;">DeveloperOS</a>
        </p>
        <div style="display: flex; justify-content: center; align-items: center; gap: 1.25rem; flex-wrap: wrap; margin-bottom: 0.85rem;">
            <a href="${BANNER_CONFIG.mainUrl}" target="_blank" rel="noopener noreferrer" style="color: var(--color-accent, #06b6d4); text-decoration: none;">
                DeveloperOS Home
            </a>
            <span style="color: rgba(255, 255, 255, 0.2);">•</span>
            <a href="${BANNER_CONFIG.toolsUrl}" target="_blank" rel="noopener noreferrer" style="color: var(--color-accent, #06b6d4); text-decoration: none;">
                All Tools Directory
            </a>
            <span style="color: rgba(255, 255, 255, 0.2);">•</span>
            <a href="${BANNER_CONFIG.githubUrl}" target="_blank" rel="noopener noreferrer" style="color: var(--color-accent, #06b6d4); text-decoration: none;">
                GitHub Organization
            </a>
            <span style="color: rgba(255, 255, 255, 0.2);">•</span>
            <a href="${BANNER_CONFIG.privacyUrl}" target="_blank" rel="noopener noreferrer" style="color: var(--color-accent, #06b6d4); text-decoration: none;">
                Privacy Policy
            </a>
        </div>
        <p style="margin: 0.35rem 0; color: var(--color-text-dim, #94a3b8); font-size: 0.8rem;">
            DeveloperOS Open-Source Tools Ecosystem • Licensed under the MIT License • Zero Telemetry Guarantee
        </p>
        <p style="margin: 0; color: #6b7c94; font-size: 0.78rem;">
            All processing occurs strictly client-side or in ephemeral in-memory sessions. Zero payload data is persisted.
        </p>
    </footer>
  `;
}
