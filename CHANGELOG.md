# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed
- README, CONTRIBUTING and LICENSE audited against the repository: corrected Node import example, documented which tiers the package exports, replaced benchmark figures with measured values, and corrected the data license section.

### Added
- `NOTICE` with the ESDB (SCOWL) copyright notice required for the US and UK word lists.

## [1.0.8] - 2026-04-22

### Added
- US and UK English dialect word lists (`data/us_*.json`, `data/uk_*.json`) built from SCOWL/ESDB data, exported as `./us` and `./uk`.

## [1.0.7] - 2026-04-22

### Changed
- Published under the verified npm scope `@rahulmrx` (`@rahulmrx/game-ready-dictionary`).

## [1.0.6] - 2026-04-22

### Changed
- Reverted to the unscoped package name (superseded by 1.0.7).
- `pipeline.py` creates `data/` and `sources/` if they are missing.

## [1.0.5] - 2026-04-22

### Added
- Package `exports` map, Python pipeline tests (`test_pipeline.py`).

### Changed
- `.gitignore` excludes Python cache files.

## [1.0.4] - 2026-04-22

### Changed
- Reorganized repository structure (`src/`, `scripts/`, `sources/`, `data/`).

## [1.0.3] - 2026-04-22

### Added
- Comprehensive verification suite in `scripts/test_integrity.js`.
- Performance benchmarking tool in `scripts/benchmark.js`.
- `npm test` and `npm run benchmark` commands.

### Changed
- Refined `TRADEMARK_BLOCKLIST` to allow common words like "apple".
- Standardized Large tier filenames to `large_array.json`, `large_by_length.json`, and `large_trie.json`.
- Ensured Large tier is a strict superset of Medium tier.

## [1.0.2] - 2026-04-22

### Added
- Implemented **Large Tier** dictionary using the ENABLE1 word list (about 172k words before merging with Medium; 182,008 words in the current Large tier).
- Generated array, length-indexed, and Trie formats for the Large tier.
- Updated release workflow to include Large tier assets.

## [1.0.1] - 2026-04-22

### Fixed
- Fixed release workflow failure where `npm version` errored if the version was already set.
- Added `--allow-same-version` to `npm version`.
- Addressed Node.js 20 deprecation warnings in GitHub Actions.

## [1.0.0] - 2026-04-22

### Added
- Initial release with Small and Medium tiered dictionaries.
- `TrieEngine` for high-performance word validation and prefix searching.
- Automated Python data pipeline for cleaning and compiling word lists.
- Dual-license architecture (MIT/Public Domain).
