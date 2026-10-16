# DeveloperOS Central Tools Web Directory (`developeros-tools-web`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ecosystem: DeveloperOS](https://img.shields.io/badge/Ecosystem-DeveloperOS-6366f1.svg)](https://developeros.in)
[![Tools Directory](https://img.shields.io/badge/Tools%20Directory-Online-10b981.svg)](https://toolkit.developeros.in)
[![Privacy: Client--Side](https://img.shields.io/badge/Privacy-Zero--Storage-10b981.svg)](https://developeros.in/privacy)
[![CI](https://github.com/developerOSindia/tools-directory/actions/workflows/ci.yml/badge.svg)](https://github.com/developerOSindia/tools-directory/actions)

The official, zero-backend, statically generated web portal and search directory for the DeveloperOS tool ecosystem.

Deployed to **`https://toolkit.developeros.in`** via Cloudflare Pages.

---

## 🖥️ Features

- **Instant Search & Filtering**: Client-side, zero-latency fuzzy search across all tools, algorithms, and categories with keyboard shortcut (`/` to search).
- **Dedicated SEO Landing Pages**: Pre-rendered static HTML (`tools/<seo_slug>.html`) with Schema.org `SoftwareApplication` JSON-LD structured data and OpenGraph tags for search engines.
- **DeveloperOS Design System**: Official styling using dark theme tokens (`#6366f1` indigo primary, `#0f172a` canvas, `#1e293b` surface).
- **XML Sitemap & robots.txt**: Automated generation of `dist/sitemap.xml` and `dist/robots.txt`.
- **Zero Backend / Serverless**: 100% static output for hosting on Cloudflare Pages free tier.
- **Verified URLs Only**: Public live launch buttons are only activated once an application is verified live.

---

## 🚀 Local Development

```bash
# 1. Build the static distribution
python3 build.py

# 2. Preview locally
python3 -m http.server 8080 -d dist
```
Visit `http://localhost:8080`.

---

## 🧪 Automated Testing

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## ☁️ Cloudflare Pages Deployment Configuration

- **Framework preset**: `None`
- **Build command**: `python3 build.py`
- **Build output directory**: `dist`
- **Environment variables**: `PYTHON_VERSION=3.12`
- **Custom domain**: `toolkit.developeros.in` (CNAME `tools` -> `<project>.pages.dev`)

---

## 🏷️ Recommended GitHub Topics

`tools-directory` `developer-utilities` `web-portal` `cloudflare-pages` `offline-first` `developeros` `open-source`

---

## 📜 License & Ecosystem

Licensed under [MIT](LICENSE). Part of [DeveloperOS](https://developeros.in).
- **Main Website**: [https://developeros.in](https://developeros.in)
- **Central Tools Directory**: [https://toolkit.developeros.in](https://toolkit.developeros.in)
- **GitHub Organization**: [https://github.com/developerOSindia](https://github.com/developerOSindia)
