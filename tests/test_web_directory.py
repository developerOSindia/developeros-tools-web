"""
Unit and smoke tests for DeveloperOS Tools Web Directory SSG build output.
"""

import json
import re
import sys
import unittest
from pathlib import Path

WEB_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = WEB_ROOT / "dist"
REGISTRY_FILE = WEB_ROOT.parent / "developeros-tool-registry" / "registry.json"


class TestWebDirectory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Run build if dist doesn't exist
        if not (DIST_DIR / "index.html").exists():
            import subprocess
            subprocess.run(["python3", "build.py"], cwd=WEB_ROOT, check=True)

        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            cls.registry = json.load(f)

    def test_index_html_exists_and_valid(self):
        index_file = DIST_DIR / "index.html"
        self.assertTrue(index_file.exists(), "dist/index.html must exist")
        content = index_file.read_text(encoding="utf-8")

        self.assertIn("https://toolkit.developeros.in/", content)
        self.assertIn("https://developeros.in", content)
        self.assertIn('id="toolSearch"', content)
        self.assertIn('id="categoryChips"', content)
        self.assertIn('id="toolGrid"', content)
        self.assertIn('id="registryData"', content)

    def test_all_tool_seo_pages_generated(self):
        tools = self.registry.get("tools", [])
        self.assertGreaterEqual(len(tools), 20)

        for tool in tools:
            slug = tool["seo_slug"]
            page_path = DIST_DIR / "tools" / f"{slug}.html"
            self.assertTrue(page_path.exists(), f"SEO page missing: {page_path}")

            page_content = page_path.read_text(encoding="utf-8")
            self.assertIn(tool["name"], page_content)
            self.assertIn("https://developeros.in", page_content)
            self.assertIn("SoftwareApplication", page_content)
            self.assertIn(f"https://toolkit.developeros.in/tools/{slug}.html", page_content)

    def test_sitemap_xml(self):
        sitemap_file = DIST_DIR / "sitemap.xml"
        self.assertTrue(sitemap_file.exists())
        content = sitemap_file.read_text(encoding="utf-8")
        self.assertIn("<urlset", content)
        self.assertIn("https://toolkit.developeros.in/", content)
        self.assertIn("json-formatter.html", content)

    def test_robots_txt(self):
        robots_file = DIST_DIR / "robots.txt"
        self.assertTrue(robots_file.exists())
        content = robots_file.read_text(encoding="utf-8")
        self.assertIn("User-agent: *", content)
        self.assertIn("Sitemap: https://toolkit.developeros.in/sitemap.xml", content)

    def test_static_assets_present(self):
        self.assertTrue((DIST_DIR / "assets" / "styles.css").exists())
        self.assertTrue((DIST_DIR / "assets" / "catalog.js").exists())

    def test_interactive_playground_drawer(self):
        index_file = DIST_DIR / "index.html"
        content = index_file.read_text(encoding="utf-8")

        # Playground drawer structural elements
        self.assertIn('id="playgroundOverlay"', content)
        self.assertIn('id="playgroundDrawer"', content)
        self.assertIn('id="playgroundTitle"', content)

        # 5 required playground utility panels
        self.assertIn('id="panel-json"', content)
        self.assertIn('id="panel-base64"', content)
        self.assertIn('id="panel-hash"', content)
        self.assertIn('id="panel-uuid"', content)
        self.assertIn('id="panel-jwt"', content)

        # Interactive controls for each tool
        self.assertIn('id="jsonPlaygroundInput"', content)
        self.assertIn('onclick="formatJson(2)"', content)
        self.assertIn('id="base64PlaygroundInput"', content)
        self.assertIn('onclick="runBase64()"', content)
        self.assertIn('id="hashPlaygroundInput"', content)
        self.assertIn('id="hashOutputSha256"', content)
        self.assertIn('id="hashOutputSha1"', content)
        self.assertIn('onclick="generateUuids()"', content)
        self.assertIn('id="jwtPlaygroundInput"', content)
        self.assertIn('onclick="inspectJwt()"', content)

    def test_test_in_browser_buttons(self):
        index_file = DIST_DIR / "index.html"
        content = index_file.read_text(encoding="utf-8")

        # Top tools must have the "⚡ Test In Browser" button
        top_tools = [
            ("card-json-formatter", "openPlayground('json')"),
            ("card-base64-codec", "openPlayground('base64')"),
            ("card-hash-calculator", "openPlayground('hash')"),
            ("card-uuid-generator", "openPlayground('uuid')"),
            ("card-jwt-decoder", "openPlayground('jwt')"),
        ]

        for card_id, expected_call in top_tools:
            self.assertIn(f'id="{card_id}"', content)
            self.assertIn("⚡ Test In Browser", content)
            self.assertIn(expected_call, content)

    def test_export_catalog_feature(self):
        index_file = DIST_DIR / "index.html"
        content = index_file.read_text(encoding="utf-8")

        # Export dropdown elements
        self.assertIn('id="exportDropdown"', content)
        self.assertIn('id="exportDropdownBtn"', content)
        self.assertIn('id="exportDropdownMenu"', content)

        # Download options for JSON and Markdown
        self.assertIn("developeros-tools.json", content)
        self.assertIn("developeros-tools.md", content)
        self.assertIn("exportCatalog('json')", content)
        self.assertIn("exportCatalog('md')", content)

    def test_keyboard_shortcuts_modal(self):
        index_file = DIST_DIR / "index.html"
        content = index_file.read_text(encoding="utf-8")

        # Shortcuts modal elements
        self.assertIn('id="shortcutsModalOverlay"', content)
        self.assertIn('id="shortcutsModalTitle"', content)

        # Listed shortcuts
        self.assertIn("<kbd>?</kbd>", content)
        self.assertIn("<kbd>/</kbd>", content)
        self.assertIn("<kbd>Esc</kbd>", content)
        self.assertIn("<kbd>1</kbd>", content)
        self.assertIn("<kbd>9</kbd>", content)
        self.assertIn("<kbd>P</kbd>", content)
        self.assertIn("<kbd>E</kbd>", content)

    def test_styles_and_scripts_contain_tokens_and_functions(self):
        css_file = DIST_DIR / "assets" / "styles.css"
        css_content = css_file.read_text(encoding="utf-8")

        # Obsidian Engine tokens and classes
        self.assertIn(".btn-test-browser", css_content)
        self.assertIn(".playground-drawer", css_content)
        self.assertIn(".shortcuts-modal", css_content)
        self.assertIn(".export-dropdown", css_content)
        self.assertIn("#06070a", css_content)
        self.assertIn("#0c0f15", css_content)
        self.assertIn("#f97316", css_content)
        self.assertIn("#06b6d4", css_content)

        js_file = DIST_DIR / "assets" / "catalog.js"
        js_content = js_file.read_text(encoding="utf-8")

        # Client-side functions
        self.assertIn("openPlayground", js_content)
        self.assertIn("formatJson", js_content)
        self.assertIn("runBase64", js_content)
        self.assertIn("updateHashes", js_content)
        self.assertIn("generateUuids", js_content)
        self.assertIn("inspectJwt", js_content)
        self.assertIn("exportCatalog", js_content)
        self.assertIn("openShortcutsModal", js_content)


if __name__ == "__main__":
    unittest.main()

