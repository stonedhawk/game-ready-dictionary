import unittest
import json
import os
import re
from unittest import mock

import pipeline

class TestPipeline(unittest.TestCase):
    def setUp(self):
        # Paths based on reorganized structure
        self.medium_array_path = 'data/medium_array.json'
        self.medium_trie_path = 'data/medium_trie.json'
        self.large_array_path = 'data/large_array.json'
        
        # Load data for testing
        with open(self.medium_array_path, 'r') as f:
            self.medium_array = json.load(f)
        with open(self.medium_trie_path, 'r') as f:
            self.medium_trie = json.load(f)
        with open(self.large_array_path, 'r') as f:
            self.large_array = json.load(f)

    def test_no_numbers_or_uppercase(self):
        """1. Verify medium_array.json (clean_base) does not contain numbers or uppercase letters."""
        pattern = re.compile(r"[^a-z]")
        for word in self.medium_array:
            self.assertFalse(pattern.search(word), f"Word '{word}' contains invalid characters")

    def test_trie_structure(self):
        """2. Verify medium_trie.json correctly implements the '_': 1 terminal node structure."""
        # Check a few words by navigating the trie
        def check_word(word):
            node = self.medium_trie
            for char in word:
                self.assertIn(char, node, f"Character '{char}' from word '{word}' not found in Trie")
                node = node[char]
            self.assertEqual(node.get('_'), 1, f"Word '{word}' does not have terminal marker '_'")

        # Test words that should be in the medium set
        check_word('apple')
        check_word('dictionary')

    def test_trademark_blocklist(self):
        """3. Verify TRADEMARK_BLOCKLIST successfully removed designated words."""
        # Words that MUST be blocked
        blocked = ['facebook', 'google', 'microsoft', 'netflix', 'tiktok']
        for word in blocked:
            self.assertNotIn(word, self.medium_array, f"Blocked word '{word}' found in Medium array")
            self.assertNotIn(word, self.large_array, f"Blocked word '{word}' found in Large array")

class TestPipelineFailsLoudly(unittest.TestCase):
    def test_checksum_mismatch_raises(self):
        """4. A download whose SHA-256 does not match the pin stops the build."""
        fake = mock.Mock(content=b"tampered", raise_for_status=mock.Mock())
        with mock.patch.object(pipeline.requests, "get", return_value=fake), \
             mock.patch("builtins.open", mock.mock_open()) as opened:
            with self.assertRaises(ValueError):
                pipeline.download_file("https://example.invalid/x.txt", "sources/x.txt", "0" * 64)
            opened.assert_not_called()

    def test_small_tier_raises(self):
        """5. A tier that comes out nearly empty stops the build."""
        with self.assertRaises(ValueError):
            pipeline.require_words(["apple"], "Medium tier", 50000)

    def test_sources_are_pinned(self):
        """6. Every source URL is pinned to a commit SHA and has a checksum."""
        for name, source in pipeline.SOURCES.items():
            self.assertRegex(source["url"], r"/[0-9a-f]{40}/", f"{name} is not pinned to a commit")
            self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$", f"{name} has no SHA-256")

if __name__ == '__main__':
    unittest.main()
