/**
 * DeveloperOS Tools Web Directory - Catalog Engine
 * Client-side instant search, category filtering, and tool card rendering.
 */

(function () {
  let allTools = [];
  let currentCategory = "All";
  let searchQuery = "";

  const searchInput = document.getElementById("toolSearch");
  const chipsContainer = document.getElementById("categoryChips");
  const toolGrid = document.getElementById("toolGrid");
  const countDisplay = document.getElementById("toolCount");

  // Load registry data from embedded JSON script tag
  function initCatalog() {
    const dataElement = document.getElementById("registryData");
    if (dataElement) {
      try {
        const raw = JSON.parse(dataElement.textContent);
        allTools = raw.tools || [];
      } catch (e) {
        console.error("Failed to parse embedded registry data:", e);
      }
    }

    renderCategoryChips();
    filterAndRender();

    // Event listeners
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        searchQuery = e.target.value.trim().toLowerCase();
        filterAndRender();
      });
    }

    // Keyboard shortcut '/' to search
    window.addEventListener("keydown", (e) => {
      if (e.key === "/" && document.activeElement !== searchInput) {
        e.preventDefault();
        if (searchInput) searchInput.focus();
      }
    });
  }

  function renderCategoryChips() {
    if (!chipsContainer) return;
    const categories = ["All", ...Array.from(new Set(allTools.map((t) => t.category))).sort()];

    chipsContainer.innerHTML = "";
    categories.forEach((cat) => {
      const chip = document.createElement("button");
      chip.className = `chip ${cat === currentCategory ? "active" : ""}`;
      chip.textContent = cat;
      chip.addEventListener("click", () => {
        currentCategory = cat;
        document.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
        chip.classList.add("active");
        filterAndRender();
      });
      chipsContainer.appendChild(chip);
    });
  }

  function filterAndRender() {
    if (!toolGrid) return;

    const filtered = allTools.filter((tool) => {
      const matchCategory = currentCategory === "All" || tool.category === currentCategory;
      if (!matchCategory) return false;

      if (!searchQuery) return true;

      const haystack = `${tool.name} ${tool.short_description} ${tool.category} ${tool.framework} ${tool.seo_slug}`.toLowerCase();
      return haystack.includes(searchQuery);
    });

    if (countDisplay) {
      countDisplay.textContent = `Showing ${filtered.length} of ${allTools.length} developer tools`;
    }

    if (filtered.length === 0) {
      toolGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: var(--color-text-dim);">
          <div style="font-size: 2.5rem; margin-bottom: 12px;">🔍</div>
          <h3 style="color: var(--color-text); margin-bottom: 8px;">No tools matching "${searchQuery}"</h3>
          <p>Try searching for a different keyword or selecting another category.</p>
        </div>
      `;
      return;
    }

    toolGrid.innerHTML = filtered.map(renderToolCard).join("");
  }

  function renderToolCard(tool) {
    const isLive = tool.availability_status === "verified_live" && Boolean(tool.live_url);
    const statusLabel = isLive ? "Verified Live" : "Staged Offline";
    const statusClass = isLive ? "status-live" : "status-staged";

    const launchButton = isLive
      ? `<a href="${tool.live_url}" target="_blank" rel="noopener noreferrer" class="btn-launch">⚡ Launch Tool</a>`
      : `<a href="tools/${tool.seo_slug}.html" class="btn-launch" style="background-color: var(--color-surface-elevated); color: var(--color-text); border: 1px solid var(--color-border);">📖 View Documentation</a>`;

    return `
      <article class="tool-card" id="card-${tool.seo_slug}">
        <div class="card-top">
          <div class="card-header-line">
            <h3 class="card-title">
              <a href="tools/${tool.seo_slug}.html">${tool.name}</a>
            </h3>
            <span class="card-badge-category">${tool.category}</span>
          </div>
          <p class="card-desc">${tool.short_description}</p>
          <div class="card-meta-line">
            <span class="meta-pill ${statusClass}">● ${statusLabel}</span>
            <span class="meta-pill">${tool.framework}</span>
            <span class="meta-pill">Client-Side</span>
          </div>
        </div>
        <div class="card-actions">
          ${launchButton}
          <a href="tools/${tool.seo_slug}.html" class="btn-doc">Details</a>
          <a href="${tool.repository_url}" target="_blank" rel="noopener noreferrer" class="btn-doc" title="View Source on GitHub">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" style="vertical-align: middle;">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
            </svg>
          </a>
        </div>
      </article>
    `;
  }

  // Run on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCatalog);
  } else {
    initCatalog();
  }
})();
