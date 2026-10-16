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

        self.assertIn("https://tools.developeros.in/", content)
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
            self.assertIn(f"https://tools.developeros.in/tools/{slug}.html", page_content)

    def test_sitemap_xml(self):
        sitemap_file = DIST_DIR / "sitemap.xml"
        self.assertTrue(sitemap_file.exists())
        content = sitemap_file.read_text(encoding="utf-8")
        self.assertIn("<urlset", content)
        self.assertIn("https://tools.developeros.in/", content)
        self.assertIn("json-formatter.html", content)

    def test_robots_txt(self):
        robots_file = DIST_DIR / "robots.txt"
        self.assertTrue(robots_file.exists())
        content = robots_file.read_text(encoding="utf-8")
        self.assertIn("User-agent: *", content)
        self.assertIn("Sitemap: https://tools.developeros.in/sitemap.xml", content)

    def test_static_assets_present(self):
        self.assertTrue((DIST_DIR / "assets" / "styles.css").exists())
        self.assertTrue((DIST_DIR / "assets" / "catalog.js").exists())


if __name__ == "__main__":
    unittest.main()
