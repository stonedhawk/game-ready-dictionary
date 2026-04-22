# 📚 Game-Ready Dictionary

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

A high-performance, multi-tiered dictionary and Trie-based validation engine designed specifically for modern web-based word games. This repository provides pre-compiled assets across three complexity tiers, optimized for instant integration into high-performance game loops.

---

## ⚖️ Dual-License Architecture

1.  **Codebase (MIT License):** All source code and the Trie implementation are licensed under the [MIT License](./LICENSE).
2.  **Dictionary Data (Public Domain / UNLICENSE):** The compiled word lists and Trie JSON files are dedicated to the [Public Domain](./UNLICENSE).

---

## 🚀 Complexity Tiers

We provide three distinct tiers to balance vocabulary depth with asset size:

| Tier | Size | Description | Best For |
| :--- | :--- | :--- | :--- |
| **Small** | ~7,000 words | Intersection of 12Dicts and Top 10k Google English list. | Casual mobile games, ultra-fast loading. |
| **Medium** | ~60,000 words | The full 12Dicts (5desk) base list, cleaned and filtered. | Standard crosswords, word search, roguelites. |
| **Large** | ~172,000 words | The ENABLE1 word list, the industry standard for word games. | Complex lexical analysis, deep-strategy games. |

---

## 📦 Output Formats (Medium Tier)

The Medium tier is exported in three formats to suit different development needs:

- `data/medium_array.json` / `data/large_array.json`: A standard alphabetical array of all valid words.
- `data/medium_by_length.json` / `data/large_by_length.json`: An object keyed by word length.
- `data/medium_trie.json` / `data/large_trie.json`: A nested JSON Trie structure optimized for $O(m)$ lookups.

---

## ⚡ High-Performance Usage

The dictionary is provided as a **pre-compiled Trie**, allowing for $O(m)$ lookup time.

### Quick Start (Trie)
```javascript
import { TrieEngine } from 'game-ready-dictionary';
import trieData from 'game-ready-dictionary/data/medium_trie.json';

const trie = new TrieEngine(trieData);

// O(m) Validation
if (trie.validate('antigravity')) {
  console.log('Valid word found!');
}

// Prefix Search
const suggestions = trie.getPrefixMatches('anti');
```

---

## 🛠️ Data Pipeline

You can regenerate the dictionary assets or use your own word lists via our Python pipeline:

```bash
pip install requests better_profanity
python3 pipeline.py
```

The pipeline automatically:
- Converts to lowercase.
- Drops words with hyphens, apostrophes, or digits.
- Removes offensive terms via `better_profanity`.
- Strips non-dictionary brand names from our `TRADEMARK_BLOCKLIST`.

---

## ⭐ Support the Project

If this dictionary saved you development hours or helped you ship your game, please consider **starring the repository**. 

[🌟 Star on GitHub](https://github.com/stonedhawk/game-ready-dictionary)

---

Built with ❤️ for the game dev community.
