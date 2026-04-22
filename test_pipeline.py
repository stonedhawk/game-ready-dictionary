import unittest
import json
import os
import re

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

if __name__ == '__main__':
    unittest.main()
