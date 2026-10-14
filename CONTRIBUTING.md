# Contributing to Game-Ready Dictionary

Thank you for your interest in improving the Game-Ready Dictionary! We aim to keep the word lists clean and the engine fast. To keep the data structures and tiers consistent, we follow a strict contribution process.

---

## 🚫 Non-Negotiable Rules for Pull Requests

All Pull Requests must adhere to the following three rules. Failure to comply will result in an immediate request for changes or a closed PR.

### 1. Immutable Output
**Never manually edit the compiled `.json` files.**
The JSON assets in `data/` (Small, Medium, Large, US and UK, in array, length-indexed and Trie formats) are generated programmatically. Any manual changes to these files will be overwritten the next time the pipeline runs. 
- `sources/` holds vendored copies of the upstream lists, each pinned to an upstream commit and a SHA-256 in `SOURCES`. The build fails if a file is edited, so make word additions or removals in **`pipeline.py`**, for example through the **`TRADEMARK_BLOCKLIST`**. To move to a newer upstream list, update its URL and SHA-256 in `SOURCES`, run `python3 pipeline.py --refresh`, and commit the new `sources/` and `data/` files together.
- If the logic of the Trie or tiering needs to change, modify the `pipeline.py` script itself.

### 2. Objective Verification
**New words require dictionary proof.**
We strive for a high-quality "standard" English vocabulary. If you are proposing the addition of a new word to the base lists:
- You **must** include a direct link to a recognized dictionary (e.g., [Wiktionary](https://en.wiktionary.org/), [Merriam-Webster](https://www.merriam-webster.com/), or [Oxford English Dictionary](https://www.oed.com/)).
- The link must prove the word's status as a standard English entry (not slang, highly technical jargon, or obscure regionalisms).

### 3. Trademark Rigor
**Trademark blocks must be exclusive.**
We remove brand names to protect developers from trademark issues, but we do not want to lose valid English nouns (e.g., "apple" is a fruit, even if it's also a company).
- Any PR adding a word to the `TRADEMARK_BLOCKLIST` must include proof that the word is **exclusively** a brand and does not exist as a recognized standard English noun in common dictionaries.

---

## 🛠️ How to Contribute

### Adding or Removing Words
1.  Update the `TRADEMARK_BLOCKLIST` or the processing logic in `pipeline.py`. (Do not edit files in `sources/`: they are checksum-verified and the build will stop.)
2.  Run the pipeline and tests locally to verify the changes:
    ```bash
    pip install requests better_profanity==0.7.0
    python3 pipeline.py
    python3 -m unittest test_pipeline.py
    npm test
    ```
3.  Commit your changes to the source/script files. **Do not** commit the generated `.json` files if your environment produces different checksums; the maintainers will handle the final build.

### Improving the Engine
If you are improving the `TrieEngine` in `src/index.js`:
1.  Ensure all existing game implementation examples in the `README.md` still function correctly.
2.  Maintain the $O(m)$ performance profile.

### Reporting Issues
If you find an offensive word that escaped our filters, please open an issue or a PR immediately following the rules above.

---

## 🚀 Releasing (maintainers)

1.  Bump `version` in `package.json` and add a `CHANGELOG.md` entry in the same PR.
2.  After it merges, tag `main` with `v` plus that version and push the tag, e.g. `git tag -a v1.1.0 -m "v1.1.0" && git push origin v1.1.0`.
3.  The release workflow fails before publishing if the tag does not match `package.json`. It rebuilds `data/` and fails if it differs from the commit, runs the tests, publishes to npm through trusted publishing (no npm token), then creates the GitHub release with `dictionary-data.zip`.

---

By contributing, you agree that your code contributions will be licensed under the **MIT License** and your data contributions will be dedicated to the **Public Domain**.
