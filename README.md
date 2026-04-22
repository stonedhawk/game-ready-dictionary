# 🎮 Game-Ready Dictionary

[![npm version](https://img.shields.io/npm/v/@rahulmrx/game-ready-dictionary.svg)](https://www.npmjs.com/package/@rahulmrx/game-ready-dictionary)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/stonedhawk/game-ready-dictionary/actions/workflows/release.yml/badge.svg)](https://github.com/stonedhawk/game-ready-dictionary/actions)

**Game-Ready Dictionary** is a high-performance, pre-compiled, Trie-based word validation library designed specifically for web-based game development. 

Whether you're building a word puzzle, a roguelite with lexical mechanics, or a professional Scrabble clone, this library provides **O(m) lookup speeds** and **zero-latency** validation with zero external dependencies.

---

## 🚀 Key Features

- **⚡ Blazing Fast**: Lookups in **~0.0001ms** using pre-compiled Trie structures.
- **🌍 Dialect Support**: Built-in support for **US (American)** and **UK (British)** English spelling variations.
- **📦 Tiered Assets**: Choose between `Small`, `Medium`, and `Large` tiers to balance bundle size and vocabulary depth.
- **🛡️ Game-Ready**: Automatically filtered for profanity and restricted trademarks.
- **🛠️ SEO & Web Optimized**: Designed for modern bundlers (Vite, Webpack) and fully environment-agnostic (works in Browser & Node).
- **📊 Professional Data**: Sourced from industry standards like **ENABLE1**, **12Dicts**, and **SCOWL**.

---

## 📦 Installation

```bash
npm install @rahulmrx/game-ready-dictionary
```

---

## 📖 Usage

### Standard Validation (Trie-based)
The most efficient way to validate words in a game loop.

```javascript
import { TrieEngine } from '@rahulmrx/game-ready-dictionary';
import trieData from '@rahulmrx/game-ready-dictionary/data'; // Defaults to Medium

const trie = new TrieEngine(trieData);

// O(m) Validation - Complexity depends on word length, not dictionary size
if (trie.validate('apple')) {
  console.log('Valid word found!');
}

// Prefix Search - Perfect for autocomplete or pruning search paths
const suggestions = trie.getPrefixMatches('anti');
```

### Dialect-Specific Usage
Handle spelling variations like *color* vs *colour* with ease.

```javascript
import usData from '@rahulmrx/game-ready-dictionary/us';
import ukData from '@rahulmrx/game-ready-dictionary/uk';

const usTrie = new TrieEngine(usData);
const ukTrie = new TrieEngine(ukData);

console.log(usTrie.validate('color')); // true
console.log(ukTrie.validate('color')); // false
```

---

## 📊 Dictionary Tiers

| Tier | Word Count | Data Source | Use Case |
| :--- | :--- | :--- | :--- |
| **Small** | ~7,000 | 12Dicts ∩ Top 10k Google English | Casual mobile games, wordle clones. |
| **Medium** | ~60,000 | Full 12Dicts (5desk) | Standard crosswords, word search, roguelites. |
| **Large** | ~182,000 | ENABLE1 + 12Dicts Superset | Pro-grade validation, deep-strategy games. |
| **Dialects** | US / UK | SCOWL (Standard Level 60) | Dialect-specific spelling (color vs colour). |

---

## ⏱️ Performance Benchmarks

Measured on a standard Node.js runtime:

| Metric | Small Tier | Medium Tier | Large Tier |
| :--- | :--- | :--- | :--- |
| **Load Time** | 0.5ms | 25ms | 70ms |
| **Avg Lookup** | 0.004ms | 0.0001ms | 0.0001ms |

*TrieEngine provides sub-microsecond lookups regardless of dictionary size.*

---

## 📄 License

- **Code**: [MIT](LICENSE)
- **Dictionary Data**: Public Domain / [UNLICENSE](UNLICENSE) (Sourced from ENABLE1, 12Dicts, and SCOWL).

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

Designed with ❤️ for Game Developers.
