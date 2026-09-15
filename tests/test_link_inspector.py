import unittest
from link_inspector import extract_title, normalize_url


class TestLinkInspector(unittest.TestCase):
    def test_normalize_url_adds_https(self):
        self.assertEqual(
            normalize_url("example.com"),
            "https://example.com",
        )

    def test_normalize_url_preserves_scheme(self):
        self.assertEqual(
            normalize_url("http://example.com"),
            "http://example.com",
        )

    def test_extract_title(self):
        html = "<html><head><title>Example Page</title></head></html>"
        self.assertEqual(extract_title(html), "Example Page")

    def test_extract_title_missing(self):
        self.assertEqual(extract_title("<html></html>"), "")


if __name__ == "__main__":
    unittest.main()
