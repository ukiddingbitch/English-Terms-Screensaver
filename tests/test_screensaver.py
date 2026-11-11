import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import screensaver as app


class DictionaryTests(unittest.TestCase):
    @patch.object(app, "get_json")
    def test_extracts_ipa_definition_and_source(self, get):
        get.return_value = [{"word": "entropy", "phonetics": [{"text": "/entropy/"}],
                             "meanings": [{"definitions": [{"definition": "A measure of disorder."}]}],
                             "sourceUrls": ["https://en.wiktionary.org/wiki/entropy"]}]
        result = app.lookup("entropy")
        self.assertEqual(result.pronunciation, "entropy")
        self.assertEqual(result.definition, "A measure of disorder.")
        self.assertEqual(result.source, "https://en.wiktionary.org/wiki/entropy")

    @patch.object(app, "get_json")
    def test_does_not_invent_missing_pronunciation(self, get):
        get.return_value = [{"word": "x", "meanings": [{"definitions": [{"definition": "Example"}]}]}]
        self.assertIsNone(app.lookup("x"))

    @patch.object(app, "get_json")
    def test_unknown_word_is_skipped_but_rate_limit_propagates(self, get):
        get.side_effect = HTTPError("url", 404, "Missing", {}, None)
        self.assertIsNone(app.lookup("unknown"))
        get.side_effect = HTTPError("url", 429, "Rate limited", {}, None)
        with self.assertRaises(HTTPError):
            app.lookup("entropy")

    def test_windows_modes(self):
        for args, expected in [([], "show"), (["/s"], "show"), (["/c:123"], "config"),
                               (["/p", "123"], "preview"), (["/P:123"], "preview")]:
            self.assertEqual(app.mode(args), expected)


if __name__ == "__main__":
    unittest.main()
