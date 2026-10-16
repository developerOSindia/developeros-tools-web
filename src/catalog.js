/**
 * DeveloperOS Tools Web Directory - Catalog Engine
 * Client-side instant search, category filtering, tool card rendering,
 * interactive in-browser mini-playgrounds, offline catalog exporter,
 * and keyboard shortcut command palette.
 * 
 * 100% In-Memory Offline Client-Side Execution. Zero Telemetry.
 */

(function () {
  let allTools = [];
  let currentCategory = "All";
  let searchQuery = "";

  const searchInput = document.getElementById("toolSearch");
  const chipsContainer = document.getElementById("categoryChips");
  const toolGrid = document.getElementById("toolGrid");
  const countDisplay = document.getElementById("toolCount");

  const PLAYGROUND_TOOLS = {
    "json-formatter": "json",
    "json-validator": "json",
    "base64-codec": "base64",
    "hash-calculator": "hash",
    "uuid-generator": "uuid",
    "jwt-decoder": "jwt",
  };

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

    // Real-time input listeners for mini-playground
    const hashInput = document.getElementById("hashPlaygroundInput");
    if (hashInput) {
      hashInput.addEventListener("input", () => {
        window.updateHashes();
      });
    }

    // Global click listener to close dropdowns
    document.addEventListener("click", (e) => {
      const exportDropdown = document.getElementById("exportDropdown");
      if (exportDropdown && !exportDropdown.contains(e.target)) {
        window.closeExportDropdown();
      }
    });

    // Global Keyboard shortcuts
    window.addEventListener("keydown", (e) => {
      const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : "";
      const isEditable =
        activeTag === "input" ||
        activeTag === "textarea" ||
        (document.activeElement && document.activeElement.isContentEditable);

      // Escape always closes drawers and modals
      if (e.key === "Escape") {
        e.preventDefault();
        window.closeShortcutsModal();
        window.closePlayground();
        window.closeExportDropdown();
        if (searchInput && document.activeElement === searchInput) {
          searchInput.blur();
        }
        return;
      }

      // If user is typing in an input or textarea, don't trigger other hotkeys
      if (isEditable) return;

      // '?' opens shortcuts cheat sheet modal
      if (e.key === "?" || (e.shiftKey && e.key === "/")) {
        e.preventDefault();
        window.toggleShortcutsModal();
        return;
      }

      // '/' to focus search input
      if (e.key === "/") {
        e.preventDefault();
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
        return;
      }

      // 'p' or 'P' to open mini-playground
      if (e.key.toLowerCase() === "p") {
        e.preventDefault();
        window.openPlayground();
        return;
      }

      // 'e' or 'E' to toggle export catalog menu
      if (e.key.toLowerCase() === "e") {
        e.preventDefault();
        window.toggleExportDropdown();
        return;
      }

      // '1' to '9' for category quick selection
      if (e.key >= "1" && e.key <= "9") {
        const idx = parseInt(e.key, 10) - 1;
        const chips = document.querySelectorAll("#categoryChips .chip");
        if (chips && chips[idx]) {
          e.preventDefault();
          chips[idx].click();
          chips[idx].scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
          window.triggerToast(`Category: ${chips[idx].textContent} 🏷️`);
        }
        return;
      }
    });

    // Auto-open playground if requested via query parameter (e.g. ?playground=json)
    try {
      const params = new URLSearchParams(window.location.search);
      const pg = params.get("playground");
      if (pg) {
        window.openPlayground(pg);
      }
    } catch (_) {}
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

  let toastTimer = null;
  window.triggerToast = function (message) {
    let toast = document.getElementById("quick-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "quick-toast";
      toast.className = "quick-toast";
      toast.innerHTML = `<span class="quick-toast-icon">✓</span><span id="quick-toast-msg"></span>`;
      document.body.appendChild(toast);
    }
    const msgEl = document.getElementById("quick-toast-msg");
    if (msgEl) msgEl.textContent = message;
    toast.classList.add("show");
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove("show");
    }, 2400);
  };

  window.copyToolLink = function (url, name) {
    const fullUrl = url.startsWith("http") ? url : (window.location.origin + "/" + url.replace(/^\//, ""));
    navigator.clipboard.writeText(fullUrl).then(() => {
      window.triggerToast(`Copied ${name} link! 📋`);
    }).catch(() => {
      window.triggerToast(`Link: ${fullUrl}`);
    });
  };

  window.copyCliCommand = function (slug) {
    const cmd = `devos ${slug}`;
    navigator.clipboard.writeText(cmd).then(() => {
      window.triggerToast(`Copied CLI: ${cmd} 🚀`);
    }).catch(() => {
      window.triggerToast(`CLI: ${cmd}`);
    });
  };

  function renderToolCard(tool) {
    const isLive = tool.availability_status === "verified_live" && Boolean(tool.live_url);
    const statusLabel = isLive ? "Verified Live" : "Staged Offline";
    const statusClass = isLive ? "status-live" : "status-staged";
    const targetUrl = tool.live_url || `tools/${tool.seo_slug}.html`;

    const launchButton = isLive
      ? `<a href="${tool.live_url}" target="_blank" rel="noopener noreferrer" class="btn-launch">⚡ Launch Tool ↗</a>`
      : `<a href="tools/${tool.seo_slug}.html" class="btn-launch" style="background-color: var(--color-surface-elevated); color: var(--color-text); border: 1px solid var(--color-border);">📖 View Docs</a>`;

    const safeName = tool.name.replace(/'/g, "\\'");

    const playgroundKey = PLAYGROUND_TOOLS[tool.seo_slug];
    const testInBrowserBtn = playgroundKey
      ? `<button type="button" class="btn-test-browser" onclick="window.openPlayground('${playgroundKey}')" title="Test in browser">⚡ Test In Browser</button>`
      : "";

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
          ${testInBrowserBtn}
          ${launchButton}
          <button type="button" class="btn-quick-copy" onclick="window.copyToolLink('${targetUrl}', '${safeName}')" title="Copy Tool Link to Clipboard">
            📋 Copy Link
          </button>
          <button type="button" class="btn-cli-copy" onclick="window.copyCliCommand('${tool.seo_slug}')" title="Copy CLI Command">
            &gt;_ CLI
          </button>
          <a href="tools/${tool.seo_slug}.html" class="btn-doc" title="Tool Details">Details</a>
          <a href="${tool.repository_url}" target="_blank" rel="noopener noreferrer" class="btn-doc" title="View Source on GitHub">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" style="vertical-align: middle;">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
            </svg>
          </a>
        </div>
      </article>
    `;
  }

  // ==========================================================================
  // Interactive Live Playground Drawer Logic
  // ==========================================================================
  window.openPlayground = function (tabKey) {
    const overlay = document.getElementById("playgroundOverlay");
    if (!overlay) return;

    overlay.classList.add("open");
    overlay.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";

    if (tabKey) {
      window.switchPlaygroundTab(tabKey);
    } else {
      const activeTab = document.querySelector(".playground-tab.active");
      const key = activeTab ? activeTab.getAttribute("data-tab") : "json";
      window.switchPlaygroundTab(key);
    }
  };

  window.closePlayground = function () {
    const overlay = document.getElementById("playgroundOverlay");
    if (!overlay) return;
    overlay.classList.remove("open");
    overlay.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  };

  window.handlePlaygroundOverlayClick = function (e) {
    if (e.target.id === "playgroundOverlay") {
      window.closePlayground();
    }
  };

  window.switchPlaygroundTab = function (tabKey) {
    const tabs = document.querySelectorAll(".playground-tab");
    const panels = document.querySelectorAll(".playground-panel");

    tabs.forEach((tab) => {
      const isTarget = tab.getAttribute("data-tab") === tabKey;
      tab.classList.toggle("active", isTarget);
      tab.setAttribute("aria-selected", isTarget ? "true" : "false");
    });

    panels.forEach((panel) => {
      const isTarget = panel.id === `panel-${tabKey}`;
      panel.classList.toggle("active", isTarget);
    });

    // Auto-initialize samples if fields are empty
    if (tabKey === "json") {
      const input = document.getElementById("jsonPlaygroundInput");
      if (input && !input.value) window.loadJsonSample();
    } else if (tabKey === "base64") {
      const input = document.getElementById("base64PlaygroundInput");
      if (input && !input.value) window.loadBase64Sample();
    } else if (tabKey === "hash") {
      const input = document.getElementById("hashPlaygroundInput");
      if (input && !input.value) window.loadHashSample();
    } else if (tabKey === "uuid") {
      const container = document.getElementById("uuidOutputContainer");
      if (container && container.children.length === 0) window.generateUuids();
    } else if (tabKey === "jwt") {
      const input = document.getElementById("jwtPlaygroundInput");
      if (input && !input.value) window.loadJwtSample();
    }
  };

  // 1. JSON Formatter & Minifier
  window.formatJson = function (spaces) {
    const inputEl = document.getElementById("jsonPlaygroundInput");
    const outputEl = document.getElementById("jsonPlaygroundOutput");
    const errorEl = document.getElementById("jsonPlaygroundError");
    const statsEl = document.getElementById("jsonStats");
    if (!inputEl || !outputEl) return;

    const raw = inputEl.value.trim();
    if (!raw) {
      if (errorEl) {
        errorEl.textContent = "Please enter some JSON to format.";
        errorEl.style.display = "block";
      }
      outputEl.value = "";
      if (statsEl) statsEl.textContent = "";
      return;
    }

    try {
      const parsed = JSON.parse(raw);
      const formatted = JSON.stringify(parsed, null, spaces || 2);
      outputEl.value = formatted;
      if (errorEl) errorEl.style.display = "none";

      const inBytes = new TextEncoder().encode(raw).length;
      const outBytes = new TextEncoder().encode(formatted).length;
      if (statsEl) {
        statsEl.textContent = `Valid JSON • ${inBytes} B ➔ ${outBytes} B`;
      }
      window.triggerToast("JSON beautified successfully! ✨");
    } catch (err) {
      if (errorEl) {
        errorEl.textContent = "JSON Syntax Error: " + err.message;
        errorEl.style.display = "block";
      }
      if (statsEl) statsEl.textContent = "Invalid JSON";
    }
  };

  window.minifyJson = function () {
    const inputEl = document.getElementById("jsonPlaygroundInput");
    const outputEl = document.getElementById("jsonPlaygroundOutput");
    const errorEl = document.getElementById("jsonPlaygroundError");
    const statsEl = document.getElementById("jsonStats");
    if (!inputEl || !outputEl) return;

    const raw = inputEl.value.trim();
    if (!raw) {
      if (errorEl) {
        errorEl.textContent = "Please enter some JSON to minify.";
        errorEl.style.display = "block";
      }
      outputEl.value = "";
      if (statsEl) statsEl.textContent = "";
      return;
    }

    try {
      const parsed = JSON.parse(raw);
      const minified = JSON.stringify(parsed);
      outputEl.value = minified;
      if (errorEl) errorEl.style.display = "none";

      const inBytes = new TextEncoder().encode(raw).length;
      const outBytes = new TextEncoder().encode(minified).length;
      const diff = inBytes - outBytes;
      const pct = inBytes > 0 ? Math.round((diff / inBytes) * 100) : 0;
      if (statsEl) {
        statsEl.textContent = `Minified • Saved ${diff} B (${pct}%)`;
      }
      window.triggerToast("JSON minified! ⚡");
    } catch (err) {
      if (errorEl) {
        errorEl.textContent = "JSON Syntax Error: " + err.message;
        errorEl.style.display = "block";
      }
      if (statsEl) statsEl.textContent = "Invalid JSON";
    }
  };

  window.loadJsonSample = function () {
    const sample = {
      developer_os: "DeveloperOS Tools Ecosystem",
      version: "2.4.0",
      privacy_policy: "100% In-Memory Offline Client-Side",
      top_utilities: [
        { name: "JSON Formatter", status: "instant_ready" },
        { name: "Base64 Codec", status: "instant_ready" },
        { name: "Hash Generator", status: "instant_ready" },
        { name: "UUID Generator", status: "instant_ready" },
        { name: "JWT Inspector", status: "instant_ready" }
      ],
      features: {
        telemetry: false,
        cloud_storage: false,
        offline_capable: true
      }
    };
    const inputEl = document.getElementById("jsonPlaygroundInput");
    if (inputEl) {
      inputEl.value = JSON.stringify(sample);
      window.formatJson(2);
    }
  };

  window.clearJson = function () {
    const inEl = document.getElementById("jsonPlaygroundInput");
    const outEl = document.getElementById("jsonPlaygroundOutput");
    const errEl = document.getElementById("jsonPlaygroundError");
    const statsEl = document.getElementById("jsonStats");
    if (inEl) inEl.value = "";
    if (outEl) outEl.value = "";
    if (errEl) errEl.style.display = "none";
    if (statsEl) statsEl.textContent = "";
  };

  window.copyJsonOutput = function () {
    const outEl = document.getElementById("jsonPlaygroundOutput");
    if (outEl && outEl.value) {
      navigator.clipboard.writeText(outEl.value).then(() => {
        window.triggerToast("Copied JSON result! 📋");
      });
    } else {
      window.triggerToast("No JSON output to copy.");
    }
  };

  // 2. Base64 Encoder / Decoder
  let base64Mode = "encode";

  window.setBase64Mode = function (mode) {
    base64Mode = mode;
    const btnEnc = document.getElementById("b64ModeEncode");
    const btnDec = document.getElementById("b64ModeDecode");
    const inLbl = document.getElementById("base64InputLabel");
    const outLbl = document.getElementById("base64OutputLabel");
    const convBtn = document.getElementById("b64ConvertBtn");
    const inEl = document.getElementById("base64PlaygroundInput");
    const errEl = document.getElementById("base64PlaygroundError");

    if (errEl) errEl.style.display = "none";

    if (mode === "encode") {
      if (btnEnc) btnEnc.classList.add("active");
      if (btnDec) btnDec.classList.remove("active");
      if (inLbl) inLbl.textContent = "Plaintext Input (UTF-8)";
      if (outLbl) outLbl.textContent = "Base64 Output";
      if (convBtn) convBtn.textContent = "Encode Now";
      if (inEl) inEl.placeholder = "Enter plaintext to encode (supports emoji & multilingual UTF-8)...";
    } else {
      if (btnDec) btnDec.classList.add("active");
      if (btnEnc) btnEnc.classList.remove("active");
      if (inLbl) inLbl.textContent = "Base64 Input";
      if (outLbl) outLbl.textContent = "Decoded Plaintext (UTF-8)";
      if (convBtn) convBtn.textContent = "Decode Now";
      if (inEl) inEl.placeholder = "Enter base64 string to decode...";
    }

    window.runBase64();
  };

  window.runBase64 = function () {
    const inEl = document.getElementById("base64PlaygroundInput");
    const outEl = document.getElementById("base64PlaygroundOutput");
    const errEl = document.getElementById("base64PlaygroundError");
    if (!inEl || !outEl) return;

    const raw = inEl.value;
    if (!raw) {
      outEl.value = "";
      if (errEl) errEl.style.display = "none";
      return;
    }

    try {
      if (base64Mode === "encode") {
        // UTF-8 to Base64
        const bytes = new TextEncoder().encode(raw);
        let binString = "";
        for (let i = 0; i < bytes.length; i++) {
          binString += String.fromCharCode(bytes[i]);
        }
        outEl.value = btoa(binString);
        if (errEl) errEl.style.display = "none";
        window.triggerToast("Encoded to Base64! 🔤");
      } else {
        // Base64 to UTF-8
        const clean = raw.trim().replace(/\s+/g, "");
        const binString = atob(clean);
        const bytes = new Uint8Array(binString.length);
        for (let i = 0; i < binString.length; i++) {
          bytes[i] = binString.charCodeAt(i);
        }
        outEl.value = new TextDecoder().decode(bytes);
        if (errEl) errEl.style.display = "none";
        window.triggerToast("Decoded from Base64! 🔓");
      }
    } catch (err) {
      if (errEl) {
        errEl.textContent = `Base64 ${base64Mode === "encode" ? "Encoding" : "Decoding"} Error: ${err.message}`;
        errEl.style.display = "block";
      }
    }
  };

  window.loadBase64Sample = function () {
    const inEl = document.getElementById("base64PlaygroundInput");
    if (!inEl) return;
    if (base64Mode === "encode") {
      inEl.value = "DeveloperOS 🚀 — High-performance, offline-first developer suite with 25+ tools!";
    } else {
      inEl.value = "RGV2ZWxvcGVyT1Mg8J+agCDigJQgSGlnaC1wZXJmb3JtYW5jZSwgb2ZmbGluZS1maXJzdCBkZXZlbG9wZXIgc3VpdGUgd2l0aCAyNSsgdG9vbHMh";
    }
    window.runBase64();
  };

  window.clearBase64 = function () {
    const inEl = document.getElementById("base64PlaygroundInput");
    const outEl = document.getElementById("base64PlaygroundOutput");
    const errEl = document.getElementById("base64PlaygroundError");
    if (inEl) inEl.value = "";
    if (outEl) outEl.value = "";
    if (errEl) errEl.style.display = "none";
  };

  window.copyBase64Output = function () {
    const outEl = document.getElementById("base64PlaygroundOutput");
    if (outEl && outEl.value) {
      navigator.clipboard.writeText(outEl.value).then(() => {
        window.triggerToast("Copied Base64 output! 📋");
      });
    } else {
      window.triggerToast("No output to copy.");
    }
  };

  // 3. Hash Generator
  window.updateHashes = async function () {
    const inEl = document.getElementById("hashPlaygroundInput");
    const sha256El = document.getElementById("hashOutputSha256");
    const sha1El = document.getElementById("hashOutputSha1");
    const sha512El = document.getElementById("hashOutputSha512");
    if (!inEl) return;

    const text = inEl.value;
    if (!text) {
      if (sha256El) sha256El.value = "";
      if (sha1El) sha1El.value = "";
      if (sha512El) sha512El.value = "";
      return;
    }

    const data = new TextEncoder().encode(text);

    if (window.crypto && window.crypto.subtle) {
      try {
        const b256 = await crypto.subtle.digest("SHA-256", data);
        if (sha256El) {
          sha256El.value = Array.from(new Uint8Array(b256))
            .map((b) => b.toString(16).padStart(2, "0"))
            .join("");
        }
      } catch (e) {
        if (sha256El) sha256El.value = "Error: " + e.message;
      }

      try {
        const b1 = await crypto.subtle.digest("SHA-1", data);
        if (sha1El) {
          sha1El.value = Array.from(new Uint8Array(b1))
            .map((b) => b.toString(16).padStart(2, "0"))
            .join("");
        }
      } catch (e) {
        if (sha1El) sha1El.value = "Error: " + e.message;
      }

      try {
        const b512 = await crypto.subtle.digest("SHA-512", data);
        if (sha512El) {
          sha512El.value = Array.from(new Uint8Array(b512))
            .map((b) => b.toString(16).padStart(2, "0"))
            .join("");
        }
      } catch (e) {
        if (sha512El) sha512El.value = "Error: " + e.message;
      }
    } else {
      if (sha256El) sha256El.value = "Web Crypto API not available in current context";
    }
  };

  window.loadHashSample = function () {
    const inEl = document.getElementById("hashPlaygroundInput");
    if (inEl) {
      inEl.value = "developeros-security-offline-crypto";
      window.updateHashes();
    }
  };

  window.copyHash = function (algo) {
    let targetId = "";
    if (algo === "sha256") targetId = "hashOutputSha256";
    else if (algo === "sha1") targetId = "hashOutputSha1";
    else if (algo === "sha512") targetId = "hashOutputSha512";

    const el = document.getElementById(targetId);
    if (el && el.value) {
      navigator.clipboard.writeText(el.value).then(() => {
        window.triggerToast(`Copied ${algo.toUpperCase()} hash! #️⃣`);
      });
    }
  };

  // 4. UUID Generator
  let currentUuidQty = 5;

  window.setUuidQty = function (qty) {
    currentUuidQty = qty;
    document.querySelectorAll(".uuid-qty-selector .qty-btn").forEach((btn) => {
      btn.classList.toggle("active", parseInt(btn.getAttribute("data-qty"), 10) === qty);
    });
    window.generateUuids();
  };

  window.generateUuids = function () {
    const container = document.getElementById("uuidOutputContainer");
    if (!container) return;

    const uppercase = document.getElementById("uuidOptUppercase")?.checked || false;
    const hyphens = document.getElementById("uuidOptHyphens")?.checked !== false;

    const results = [];
    for (let i = 0; i < currentUuidQty; i++) {
      let u = "";
      if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
        u = crypto.randomUUID();
      } else {
        u = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
          const r = (Math.random() * 16) | 0;
          const v = c === "x" ? r : (r & 0x3) | 0x8;
          return v.toString(16);
        });
      }
      if (!hyphens) u = u.replace(/-/g, "");
      if (uppercase) u = u.toUpperCase();
      results.push(u);
    }

    container.innerHTML = results
      .map(
        (uuid, idx) => `
        <div class="uuid-row" role="listitem">
          <span class="uuid-idx">${idx + 1}</span>
          <code class="uuid-code">${uuid}</code>
          <button type="button" class="btn-mini btn-subtle" onclick="window.copySingleUuid('${uuid}')" title="Copy UUID">
            📋 Copy
          </button>
        </div>
      `
      )
      .join("");

    window.triggerToast(`Generated ${currentUuidQty} UUID${currentUuidQty > 1 ? "s" : ""}! 🆔`);
  };

  window.copySingleUuid = function (val) {
    navigator.clipboard.writeText(val).then(() => {
      window.triggerToast("UUID copied to clipboard! 📋");
    });
  };

  window.copyAllUuids = function () {
    const codes = Array.from(document.querySelectorAll("#uuidOutputContainer .uuid-code")).map(
      (el) => el.textContent
    );
    if (codes.length > 0) {
      navigator.clipboard.writeText(codes.join("\n")).then(() => {
        window.triggerToast(`Copied ${codes.length} UUIDs to clipboard! 📋`);
      });
    } else {
      window.triggerToast("No UUIDs to copy.");
    }
  };

  // 5. JWT Claims Inspector
  window.inspectJwt = function () {
    const inEl = document.getElementById("jwtPlaygroundInput");
    const errEl = document.getElementById("jwtPlaygroundError");
    const resEl = document.getElementById("jwtPlaygroundResult");
    const metaEl = document.getElementById("jwtMetaStatus");
    const hOut = document.getElementById("jwtHeaderOutput");
    const pOut = document.getElementById("jwtPayloadOutput");
    const sOut = document.getElementById("jwtSignatureOutput");

    if (!inEl) return;
    const token = inEl.value.trim();

    if (!token) {
      if (errEl) {
        errEl.textContent = "Please enter a JWT token to decode.";
        errEl.style.display = "block";
      }
      if (resEl) resEl.style.display = "none";
      return;
    }

    const parts = token.split(".");
    if (parts.length < 2) {
      if (errEl) {
        errEl.textContent = "Invalid JWT structure: Token must contain Header and Payload separated by a dot ('.').";
        errEl.style.display = "block";
      }
      if (resEl) resEl.style.display = "none";
      return;
    }

    try {
      const b64Decode = (str) => {
        let output = str.replace(/-/g, "+").replace(/_/g, "/");
        while (output.length % 4) output += "=";
        const bin = atob(output);
        const bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) {
          bytes[i] = bin.charCodeAt(i);
        }
        return JSON.parse(new TextDecoder().decode(bytes));
      };

      const header = b64Decode(parts[0]);
      const payload = b64Decode(parts[1]);
      const signature = parts[2] || "";

      if (errEl) errEl.style.display = "none";
      if (resEl) resEl.style.display = "block";

      if (hOut) hOut.textContent = JSON.stringify(header, null, 2);
      if (pOut) pOut.textContent = JSON.stringify(payload, null, 2);
      if (sOut) sOut.textContent = signature || "(No signature string provided)";

      if (metaEl) {
        let metaHtml = "";
        if (payload.exp) {
          const expDate = new Date(payload.exp * 1000);
          const isExpired = Date.now() > payload.exp * 1000;
          metaHtml += `
            <div class="jwt-badge-row">
              <span class="jwt-status-tag ${isExpired ? "tag-expired" : "tag-active"}">
                ${isExpired ? "⚠️ EXPIRED" : "✓ ACTIVE TOKEN"}
              </span>
              <span class="jwt-time-desc">Expires: ${expDate.toLocaleString()}</span>
            </div>
          `;
        }
        if (payload.iat) {
          const iatDate = new Date(payload.iat * 1000);
          metaHtml += `<div class="jwt-time-info"><span>Issued at (iat):</span> <strong>${iatDate.toLocaleString()}</strong></div>`;
        }
        if (payload.sub) {
          metaHtml += `<div class="jwt-time-info"><span>Subject (sub):</span> <code>${payload.sub}</code></div>`;
        }
        metaEl.innerHTML = metaHtml || `<div class="jwt-time-info">Decoded ${Object.keys(payload).length} claims.</div>`;
      }

      window.triggerToast("JWT claims decoded! 🔑");
    } catch (err) {
      if (errEl) {
        errEl.textContent = "JWT Decoding Error: " + err.message;
        errEl.style.display = "block";
      }
      if (resEl) resEl.style.display = "none";
    }
  };

  window.loadJwtSample = function () {
    const inEl = document.getElementById("jwtPlaygroundInput");
    if (inEl) {
      inEl.value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXZvc19lbmdpbmVlcl80MiIsIm5hbWUiOiJQcml5YSBTaGFybWEiLCJyb2xlIjoiU2VuaW9yIFBsYXRmb3JtIEVuZ2luZWVyIiwib3JnIjoiRGV2ZWxvcGVyT1MiLCJpYXQiOjE3NjAwMDAwMDAsImV4cCI6MjA3NTY3MzYwMH0.MEQCICqZ72xL4X4xO3q_DeveloperOS_MockSignature_3fK8nB1";
      window.inspectJwt();
    }
  };

  window.clearJwt = function () {
    const inEl = document.getElementById("jwtPlaygroundInput");
    const errEl = document.getElementById("jwtPlaygroundError");
    const resEl = document.getElementById("jwtPlaygroundResult");
    if (inEl) inEl.value = "";
    if (errEl) errEl.style.display = "none";
    if (resEl) resEl.style.display = "none";
  };

  window.copyJwtPart = function (part) {
    const id = part === "header" ? "jwtHeaderOutput" : "jwtPayloadOutput";
    const el = document.getElementById(id);
    if (el && el.textContent) {
      navigator.clipboard.writeText(el.textContent).then(() => {
        window.triggerToast(`Copied JWT ${part}! 📋`);
      });
    }
  };

  // ==========================================================================
  // Offline Catalog Exporter (JSON & Markdown)
  // ==========================================================================
  window.toggleExportDropdown = function (e) {
    if (e) e.stopPropagation();
    const dropdown = document.getElementById("exportDropdown");
    const menu = document.getElementById("exportDropdownMenu");
    const btn = document.getElementById("exportDropdownBtn");
    if (!menu) return;

    const isOpen = menu.classList.contains("show");
    if (isOpen) {
      menu.classList.remove("show");
      if (dropdown) dropdown.classList.remove("open");
      if (btn) btn.setAttribute("aria-expanded", "false");
    } else {
      menu.classList.add("show");
      if (dropdown) dropdown.classList.add("open");
      if (btn) btn.setAttribute("aria-expanded", "true");
    }
  };

  window.closeExportDropdown = function () {
    const dropdown = document.getElementById("exportDropdown");
    const menu = document.getElementById("exportDropdownMenu");
    const btn = document.getElementById("exportDropdownBtn");
    if (menu) menu.classList.remove("show");
    if (dropdown) dropdown.classList.remove("open");
    if (btn) btn.setAttribute("aria-expanded", "false");
  };

  window.exportCatalog = function (format) {
    if (!allTools || allTools.length === 0) {
      const dataElement = document.getElementById("registryData");
      if (dataElement) {
        try {
          const raw = JSON.parse(dataElement.textContent);
          allTools = raw.tools || [];
        } catch (_) {}
      }
    }

    if (format === "json") {
      const exportData = {
        name: "DeveloperOS Tools Registry",
        ecosystem: "DeveloperOS",
        url: "https://toolkit.developeros.in",
        license: "MIT",
        exported_at: new Date().toISOString(),
        total_tools: allTools.length,
        tools: allTools
      };
      const content = JSON.stringify(exportData, null, 2);
      downloadFile(content, "developeros-tools.json", "application/json");
      window.triggerToast("Exported developeros-tools.json (offline registry) 📥");
    } else if (format === "md") {
      let md = "# DeveloperOS Tools Catalog\n\n";
      md += "> Comprehensive offline reference of 100% free, offline-first developer utilities.\n\n";
      md += `- **Ecosystem**: [DeveloperOS](https://developeros.in)\n`;
      md += `- **Live Directory**: [https://toolkit.developeros.in](https://toolkit.developeros.in)\n`;
      md += `- **Total Utilities**: ${allTools.length}\n`;
      md += `- **Exported At**: ${new Date().toISOString()}\n`;
      md += `- **License**: MIT\n\n`;
      md += `## Table of Contents\n\n`;

      const categories = Array.from(new Set(allTools.map((t) => t.category))).sort();
      categories.forEach((cat) => {
        const anchor = cat.toLowerCase().replace(/[^a-z0-9]+/g, "-");
        md += `- [${cat}](#${anchor})\n`;
      });
      md += "\n---\n\n";

      categories.forEach((cat) => {
        const anchor = cat.toLowerCase().replace(/[^a-z0-9]+/g, "-");
        md += `<a id="${anchor}"></a>\n`;
        md += `## ${cat}\n\n`;
        const toolsInCat = allTools.filter((t) => t.category === cat);
        toolsInCat.forEach((t) => {
          md += `### ${t.name}\n\n`;
          md += `- **Description**: ${t.short_description}\n`;
          md += `- **SEO Slug**: \`${t.seo_slug}\`\n`;
          md += `- **Category**: ${t.category}\n`;
          md += `- **Framework**: ${t.framework}\n`;
          md += `- **Status**: ${t.availability_status}\n`;
          if (t.live_url) {
            md += `- **Live URL**: [${t.live_url}](${t.live_url})\n`;
          }
          md += `- **CLI Command**: \`devos ${t.seo_slug}\`\n`;
          md += `- **Repository**: [${t.repository_url}](${t.repository_url})\n`;
          md += `- **Privacy**: ${t.privacy_classification}\n\n`;
        });
        md += "---\n\n";
      });

      md += "Built with ❤️ by [DeveloperOS](https://developeros.in) • 100% In-Memory Offline Security.\n";
      downloadFile(md, "developeros-tools.md", "text/markdown");
      window.triggerToast("Exported developeros-tools.md (offline reference) 📥");
    }

    window.closeExportDropdown();
  };

  function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: `${mimeType};charset=utf-8` });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  // ==========================================================================
  // Keyboard Shortcut Cheat Sheet Modal
  // ==========================================================================
  window.openShortcutsModal = function () {
    const overlay = document.getElementById("shortcutsModalOverlay");
    if (overlay) {
      overlay.classList.add("open");
      overlay.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }
  };

  window.closeShortcutsModal = function () {
    const overlay = document.getElementById("shortcutsModalOverlay");
    if (overlay) {
      overlay.classList.remove("open");
      overlay.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }
  };

  window.toggleShortcutsModal = function () {
    const overlay = document.getElementById("shortcutsModalOverlay");
    if (overlay && overlay.classList.contains("open")) {
      window.closeShortcutsModal();
    } else {
      window.openShortcutsModal();
    }
  };

  window.handleShortcutsOverlayClick = function (e) {
    if (e.target.id === "shortcutsModalOverlay") {
      window.closeShortcutsModal();
    }
  };

  // Run on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCatalog);
  } else {
    initCatalog();
  }
})();
