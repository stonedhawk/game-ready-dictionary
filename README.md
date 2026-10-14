# 🎮 Game-Ready Dictionary

[![npm version](https://img.shields.io/npm/v/@rahulmrx/game-ready-dictionary.svg)](https://www.npmjs.com/package/@rahulmrx/game-ready-dictionary)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://github.com/stonedhawk/game-ready-dictionary/actions/workflows/release.yml/badge.svg)](https://github.com/stonedhawk/game-ready-dictionary/actions)

**Game-Ready Dictionary** is a pre-compiled, Trie-based English word validation library for web-based word games.

![Game-Ready Dictionary demo: install, validate words, prefix search, US and UK spelling, 100k lookups in about 6 ms](https://raw.githubusercontent.com/stonedhawk/game-ready-dictionary/main/docs/demo.gif)

Use it for word puzzles, word-search or crossword games, or any game mechanic that needs to check whether a string is an English word. Lookups are O(m), where m is the word length, and the package has no runtime dependencies.

---

## 🚀 Key Features

- **⚡ Fast lookups**: about 0.0001 ms per lookup on every tier (see Performance Benchmarks below).
- **🌍 Dialect Support**: separate **US (American)** and **UK (British)** English word lists, so *color* and *colour* validate in the right dialect.
- **📦 Tiered Word Lists**: `Small`, `Medium`, and `Large` tiers trade bundle size against vocabulary depth. Each tier is exported as a ready-to-use trie.
- **🛡️ Filtered at build time**: the data pipeline drops words flagged by the `better_profanity` word list and a hardcoded trademark blocklist in [`pipeline.py`](pipeline.py). The build stops if the filter is not installed.
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

### Choosing a Tier

```javascript
import small from '@rahulmrx/game-ready-dictionary/small' with { type: 'json' };   // 6,966 words
import medium from '@rahulmrx/game-ready-dictionary/medium' with { type: 'json' }; // 59,955 words (same as /data)
import large from '@rahulmrx/game-ready-dictionary/large' with { type: 'json' };   // 182,008 words

const trie = new TrieEngine(large);

// Plain word arrays and length-indexed lists are also available under /data/
import words from '@rahulmrx/game-ready-dictionary/data/small_tier.json' with { type: 'json' };
```

---

## 📊 Dictionary Tiers

| Tier | Word Count | Data Source | Package export | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Small** | 6,966 | 12Dicts (5desk) ∩ Google top 10,000 English words | `/small` | Casual mobile games, Wordle-style games. |
| **Medium** | 59,955 | 12Dicts (5desk) | `/medium` (also `/data`) | Standard crosswords, word search, roguelites. |
| **Large** | 182,008 | ENABLE1 + Medium tier (superset) | `/large` | Larger vocabularies, deep-strategy games. |
| **US** | 88,723 | SCOWL/ESDB `en_US` (size 60) | `/us` | US spelling (color). |
| **UK** | 88,553 | SCOWL/ESDB `en_GB-ise` (size 60) | `/uk` | UK spelling (colour). |

Word counts are from the JSON files in this repository. Every export is a trie for `TrieEngine`. The `/data/*` path exposes the other generated files: `small_tier.json`, `medium_array.json` and `large_array.json` (word arrays), `medium_by_length.json` and `large_by_length.json` (words grouped by length), and `us_array.json` / `uk_array.json`.

---

### Download size

Size of each tier's trie JSON, raw and gzip-compressed (what a browser downloads from a server or CDN that gzips JSON). 1 KB = 1,024 bytes.

| Tier | Import | File | Raw | gzip -6 | gzip -9 |
| :--- | :--- | :--- | ---: | ---: | ---: |
| **Small** | `/small` | `data/small_trie.json` | 189 KB | 23 KB | 20 KB |
| **Medium** | `/medium`, `/data` | `data/medium_trie.json` | 1,679 KB | 182 KB | 161 KB |
| **Large** | `/large` | `data/large_trie.json` | 4,249 KB | 373 KB | 328 KB |
| **US** | `/us` | `data/us_trie.json` | 2,121 KB | 202 KB | 178 KB |
| **UK** | `/uk` | `data/uk_trie.json` | 2,117 KB | 201 KB | 177 KB |

Level 6 is the default for gzip and for most web servers.

---

## ⏱️ Performance Benchmarks

Measured with `npm run benchmark` ([`scripts/benchmark.js`](scripts/benchmark.js)) on Node.js 25 on an Apple M4 Pro, three runs:

| Metric | Small Tier | Medium Tier | Large Tier |
| :--- | :--- | :--- | :--- |
| **Load Time** | 3.4 ms | 23 ms | 57 to 72 ms |
| **Avg Lookup** | 0.0001 ms | 0.0001 ms | 0.0001 ms |

All three tiers are benchmarked as tries through `TrieEngine`. Load time includes reading the matching word-array file the script uses for word counts. Your numbers will vary with hardware and runtime.

---

## 🔧 Rebuilding the data

```bash
pip install better_profanity==0.7.0   # the version the committed data was built with
npm run compile        # python3 pipeline.py: builds data/ from the vendored files in sources/
npm test               # integrity checks on the generated files
pip install requests && python3 -m unittest test_pipeline.py
```

The source lists are vendored in `sources/`, so a build needs no network. Each file is pinned to a fixed upstream commit and checked against a SHA-256 in [`pipeline.py`](pipeline.py), and a rebuild reproduces the committed `data/` files byte for byte (the release workflow fails if it does not). The pipeline exits with a non-zero status if a source is missing or does not match its checksum, `better_profanity` is missing, or a tier comes out too small.

To re-download the pinned files from upstream, run `npm run compile:refresh` (`python3 pipeline.py --refresh`, needs `requests`). To move to a newer word list, update its URL and SHA-256 in `SOURCES`, run with `--refresh`, and commit the new `sources/` and `data/` files together.

---

## 📚 Data sources

| Tier | Source file | Downloaded from | Pinned version |
| :--- | :--- | :--- | :--- |
| Medium | `5desk.txt` (12Dicts) | [mattwarren/Spelling-Corrector](https://github.com/mattwarren/Spelling-Corrector) | commit `db65ff5` |
| Small | `google-10000-english.txt` | [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english) | commit `d0736d4` |
| Large | `enable1.txt` | [dolph/dictionary](https://github.com/dolph/dictionary) | commit `233d25a` |
| US / UK | `en_US.txt`, `en_GB-ise.txt` (SCOWL/ESDB) | [en-wl/wordlist-diff](https://github.com/en-wl/wordlist-diff) | commit `3e3a454` (2026-03-18), generated from [en-wl/wordlist](https://github.com/en-wl/wordlist) commit `d0600b4` |

Copies of all five files are committed in `sources/`, so builds do not depend on these repositories staying online. `en-wl/wordlist-diff` warns that its history may be regenerated, which would change commit IDs; only `--refresh` would be affected. Re-pin to the regenerated commit for `en-wl/wordlist` commit `d0600b4`; the checksum confirms the file is unchanged.

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
