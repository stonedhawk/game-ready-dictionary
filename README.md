# 🎮 Game-Ready Dictionary

[![npm version](https://img.shields.io/npm/v/@rahulmrx/game-ready-dictionary.svg)](https://www.npmjs.com/package/@rahulmrx/game-ready-dictionary)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://github.com/stonedhawk/game-ready-dictionary/actions/workflows/release.yml/badge.svg)](https://github.com/stonedhawk/game-ready-dictionary/actions)

**Game-Ready Dictionary** is a pre-compiled, Trie-based English word validation library for web-based word games.

![Game-Ready Dictionary demo: install, validate words, prefix search, US and UK spelling, 100k lookups in about 6 ms](https://raw.githubusercontent.com/stonedhawk/game-ready-dictionary/main/docs/demo.gif)

Use it for word puzzles, word-search or crossword games, or any game mechanic that needs to check whether a string is an English word. Lookups are O(m), where m is the word length, and the package has no runtime dependencies.

---

## 🚀 Key Features

- **⚡ Fast lookups**: about 0.0001 ms per lookup on the Medium and Large tries (see Performance Benchmarks below).
- **🌍 Dialect Support**: separate **US (American)** and **UK (British)** English word lists, so *color* and *colour* validate in the right dialect.
- **📦 Tiered Word Lists**: `Small`, `Medium`, and `Large` tiers trade bundle size against vocabulary depth. See Dictionary Tiers below for which ones the package exports.
- **🛡️ Filtered at build time**: the data pipeline drops words flagged by the `better_profanity` word list and a hardcoded trademark blocklist in [`pipeline.py`](pipeline.py).
- **🛠️ Plain ES module**: the engine has no Node-specific APIs. Bundlers that handle JSON imports, such as Vite, bundle it for the browser. Node needs a JSON import attribute (see Usage).
- **📊 Open word lists**: built from ENABLE1, 12Dicts and SCOWL/ESDB word lists (see Data sources below).

---

## 📦 Installation

```bash
npm install @rahulmrx/game-ready-dictionary
```

---

## 📖 Usage

### Standard Validation (Trie-based)

```javascript
import { TrieEngine } from '@rahulmrx/game-ready-dictionary';
// The /data export is the Medium tier.
// Node needs the import attribute. Bundlers such as Vite also accept it, or let you drop it.
import trieData from '@rahulmrx/game-ready-dictionary/data' with { type: 'json' };

const trie = new TrieEngine(trieData);

// O(m) validation: cost depends on word length, not dictionary size
if (trie.validate('apple')) {
  console.log('Valid word found!');
}

// Prefix search for autocomplete or pruning search paths (returns up to 50 matches by default)
const suggestions = trie.getPrefixMatches('anti');

// Prefix check for pruning recursive word searches
trie.isPrefix('ant'); // true
```

### Dialect-Specific Usage
Handle spelling variations like *color* vs *colour*.

```javascript
import { TrieEngine } from '@rahulmrx/game-ready-dictionary';
import usData from '@rahulmrx/game-ready-dictionary/us' with { type: 'json' };
import ukData from '@rahulmrx/game-ready-dictionary/uk' with { type: 'json' };

const usTrie = new TrieEngine(usData);
const ukTrie = new TrieEngine(ukData);

console.log(usTrie.validate('color')); // true
console.log(ukTrie.validate('color')); // false
```

---

## 📊 Dictionary Tiers

| Tier | Word Count | Data Source | Package export | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 6,966 | 12Dicts (5desk) ∩ Google top 10,000 English words | not exported (array file in `data/`) | Casual mobile games, Wordle-style games. |
| **Medium** | 59,955 | 12Dicts (5desk) | `@rahulmrx/game-ready-dictionary/data` | Standard crosswords, word search, roguelites. |
| **Large** | 182,008 | ENABLE1 + Medium tier (superset) | not exported (trie and array files in `data/`) | Larger vocabularies, deep-strategy games. |
| **US** | 88,723 | SCOWL/ESDB `en_US` (size 60) | `@rahulmrx/game-ready-dictionary/us` | US spelling (color). |
| **UK** | 88,553 | SCOWL/ESDB `en_GB-ise` (size 60) | `@rahulmrx/game-ready-dictionary/uk` | UK spelling (colour). |

Word counts are from the JSON files in this repository.

The package's `exports` map only exposes the Medium, US and UK tries. The Small and Large files ship in the package's `data/` folder, but Node and bundlers that enforce `exports` will refuse to import them by path, so copy the file into your project to use those tiers. The Small tier is a plain word array (no trie).

---

## ⏱️ Performance Benchmarks

Measured with `npm run benchmark` ([`scripts/benchmark.js`](scripts/benchmark.js)) on Node.js 25 on an Apple M4 Pro:

| Metric | Small Tier | Medium Tier | Large Tier |
| :--- | :--- | :--- | :--- |
| **Load Time** | 0.8 ms | 26 ms | 73 ms |
| **Avg Lookup** | 0.004 ms | 0.0001 ms | 0.0001 ms |

The Small tier is benchmarked as a plain array lookup (`Array.includes`), not a trie. For Medium and Large, load time includes reading the matching word-array file the script uses for word counts. Your numbers will vary with hardware and runtime.

---

## 🔧 Rebuilding the data

```bash
pip install requests better_profanity
npm run compile        # runs python3 pipeline.py
npm test               # integrity checks on the generated files
python3 -m unittest test_pipeline.py
```

The pipeline downloads its source lists on every run (overwriting `sources/`). The US and UK lists come from the live `en-wl/wordlist-diff` branch, so they can change between builds.

---

## 📚 Data sources

| Tier | Source file | Downloaded from |
| :--- | :--- | :--- |
| Medium | `5desk.txt` (12Dicts) | [mattwarren/Spelling-Corrector](https://github.com/mattwarren/Spelling-Corrector) |
| Small | `google-10000-english.txt` | [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english) |
| Large | `enable1.txt` | [dolph/dictionary](https://github.com/dolph/dictionary) |
| US / UK | `en_US.txt`, `en_GB-ise.txt` (SCOWL/ESDB) | [en-wl/wordlist-diff](https://github.com/en-wl/wordlist-diff) |

---

## 📄 License

- **Code**: [MIT](LICENSE). Copyright (c) 2026 Rahul M Shah.
- **Small, Medium and Large data**: dedicated to the public domain under the [UNLICENSE](UNLICENSE). ENABLE1 and 12Dicts are public domain. The Small tier's word selection also uses the google-10000-english frequency list. That list's README says it is derived from the Google Web Trillion Word Corpus under the LDC license and does not recommend commercial use without an LDC license, so check its terms for commercial projects.
- **US and UK data**: derived from the English Speller Database (ESDB, formerly SCOWL), Copyright 2000-2026 Kevin Atkinson. ESDB allows use, modification and redistribution provided its copyright notice is kept. That notice is in [NOTICE](NOTICE).

---

## 🤝 Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

Designed with ❤️ for Game Developers.
