# Changelog

All notable changes to this project will be documented in this file.

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
- Implemented **Large Tier** dictionary using the ENABLE1 word list (~172k words).
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
