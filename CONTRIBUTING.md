# Contributing to Game-Ready Dictionary

Thank you for your interest in improving the Game-Ready Dictionary! We aim to provide the most reliable, clean, and high-performance lexical assets for game developers. To maintain the integrity of our data structures and tiers, we enforce a strict contribution process.

---

## 🚫 Non-Negotiable Rules for Pull Requests

All Pull Requests must adhere to the following three rules. Failure to comply will result in an immediate request for changes or a closed PR.

### 1. Immutable Output
**Never manually edit the compiled `.json` files.**
The JSON assets (Small, Medium, and Trie formats) are generated programmatically. Any manual changes to these files will be overwritten the next time the pipeline runs. 
- All additions or deletions of words must target the **raw source text files** or the **`TRADEMARK_BLOCKLIST`** in `pipeline.py`.
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
1.  Modify the appropriate source file (e.g., `5desk.txt`) or update the `TRADEMARK_BLOCKLIST` in `pipeline.py`.
2.  Run the pipeline locally to verify the changes:
    ```bash
    python3 pipeline.py
    ```
3.  Commit your changes to the source/script files. **Do not** commit the generated `.json` files if your environment produces different checksums; the maintainers will handle the final build.

### Improving the Engine
If you are improving the `TrieEngine` in `index.js`:
1.  Ensure all existing game implementation examples in the `README.md` still function correctly.
2.  Maintain the $O(m)$ performance profile.

### Reporting Issues
If you find an offensive word that escaped our filters, please open an issue or a PR immediately following the rules above.

---

By contributing, you agree that your code contributions will be licensed under the **MIT License** and your data contributions will be dedicated to the **Public Domain**.
