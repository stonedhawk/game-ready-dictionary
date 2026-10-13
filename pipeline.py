import hashlib
import json
import os
import re
import sys
from collections import defaultdict

import requests

try:
    from better_profanity import profanity
except ImportError:
    # Without the filter the word lists would ship unfiltered, so stop here.
    sys.exit("better_profanity is required: pip install better_profanity")

# Upstream word lists, pinned to fixed commits so builds reproduce.
# Each download is checked against its SHA-256; a mismatch stops the build.
# en_US.txt and en_GB-ise.txt are ESDB (SCOWL) speller lists from en-wl/wordlist-diff
# commit 3e3a454 (2026-03-18), built from en-wl/wordlist commit d0600b4.
SOURCES = {
    "desk": {
        "url": "https://raw.githubusercontent.com/mattwarren/Spelling-Corrector/db65ff52cdef7e3b726b4e89da648f0fd1a785ba/SpellingCorrector/WordLists/5desk.txt",
        "file": "sources/5desk.txt",
        "sha256": "d6060e356971aa7069f0fb320f1314f64a5b919e620b44f841a00be5773ba9d2",
    },
    "freq": {
        "url": "https://raw.githubusercontent.com/first20hours/google-10000-english/d0736d492489198e4f9d650c7ab4143bc14c1e9e/google-10000-english.txt",
        "file": "sources/google-10000.txt",
        "sha256": "9c965d384526facc59260e94f8ccff1582633fa385004abe1455ed457062acbc",
    },
    "enable": {
        "url": "https://raw.githubusercontent.com/dolph/dictionary/233d25a56b9ac8bef906916ccf091a976995cce0/enable1.txt",
        "file": "sources/enable1.txt",
        "sha256": "3f16130220645692ed49c7134e24a18504c2ca55b3c012f7290e3e77c63b1a89",
    },
    "us": {
        "url": "https://raw.githubusercontent.com/en-wl/wordlist-diff/3e3a45426cb72461b822962c834406783f36d49f/en_US.txt",
        "file": "sources/en_US.txt",
        "sha256": "b705f5f72209208b648f3596242f3e84095751277a454023adb0b8e84f46408a",
    },
    "uk": {
        "url": "https://raw.githubusercontent.com/en-wl/wordlist-diff/3e3a45426cb72461b822962c834406783f36d49f/en_GB-ise.txt",
        "file": "sources/en_GB.txt",
        "sha256": "bbb5b239fd3565cd2b403afd9361e34187cc17fb284ab36a05c07768afa079f3",
    },
}

# Hardcoded array of non-dictionary brand names to block
TRADEMARK_BLOCKLIST = [
    "facebook", "google", "microsoft", "netflix", 
    "twitter", "instagram", "tiktok", "disney", "nintendo", "sony",
    "adidas", "nike", "pepsi", "coca-cola", "mcdonalds", "starbucks",
    "tesla", "uber", "airbnb", "spotify", "adobe", "nvidia", "intel",
    "lexus", "toyota", "samsung", "iphone", "ipad"
]

def download_file(url, filename, sha256):
    """Downloads a file and verifies its SHA-256. Raises on any failure."""
    print(f"🚀 Downloading {filename} from: {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    digest = hashlib.sha256(response.content).hexdigest()
    if digest != sha256:
        raise ValueError(f"Checksum mismatch for {filename}: expected {sha256}, got {digest}")
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"✅ Download complete: {filename}")

def require_words(words, name, minimum):
    """Fails the build if a tier comes out empty or suspiciously small."""
    if len(words) < minimum:
        raise ValueError(f"{name} has {len(words)} words, expected at least {minimum}")

def clean_words(raw_words):
    """Cleans the word list based on standard rules."""
    cleaned = []
    forbidden_pattern = re.compile(r"[-'0-9]")
    profanity.load_censor_words()

    for word in raw_words:
        word = word.strip().lower()
        if not word or forbidden_pattern.search(word):
            continue
        if profanity.contains_profanity(word):
            continue
        if word in TRADEMARK_BLOCKLIST:
            continue
        cleaned.append(word)
            
    return sorted(list(set(cleaned)))

def build_trie(words):
    """Creates a nested JSON Trie structure using '_' to denote valid word boundaries."""
    trie = {}
    for word in words:
        node = trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['_'] = 1
    return trie

def build_by_length(words):
    """Groups words by their character length."""
    by_length = defaultdict(list)
    for word in words:
        by_length[len(word)].append(word)
    return dict(sorted(by_length.items()))

def main():
    DESK_FILE = SOURCES["desk"]["file"]
    FREQ_FILE = SOURCES["freq"]["file"]
    ENABLE_FILE = SOURCES["enable"]["file"]
    US_FILE = SOURCES["us"]["file"]
    UK_FILE = SOURCES["uk"]["file"]

    # Step 0: Ensure directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("sources", exist_ok=True)

    # Step 1: Download pinned resources (checksum-verified)
    for source in SOURCES.values():
        download_file(source["url"], source["file"], source["sha256"])

    # Step 2: Load and Clean Medium Tier (Full 12Dicts)
    with open(DESK_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        medium_raw = f.readlines()
    medium_words = clean_words(medium_raw)
    
    # Step 3: Load and Process Small Tier (Top 10k Intersection)
    with open(FREQ_FILE, 'r', encoding='utf-8') as f:
        freq_raw = f.readlines()
    freq_words = set(word.strip().lower() for word in freq_raw)
    small_words = sorted(list(set(medium_words) & freq_words))
    require_words(medium_words, "Medium tier", 50000)
    require_words(small_words, "Small tier", 5000)
    
    # Step 4: Save Small Tier
    print(f"💾 Saving Small tier ({len(small_words)} words)...")
    with open("data/small_tier.json", "w") as f:
        json.dump(small_words, f, indent=2)
    with open("data/small_trie.json", "w") as f:
        json.dump(build_trie(small_words), f)

    # Step 5: Process and Save Medium Tier Outputs
    print(f"💾 Processing Medium tier ({len(medium_words)} words)...")
    
    # 5a: Standard Array
    with open("data/medium_array.json", "w") as f:
        json.dump(medium_words, f, indent=2)
        
    # 5b: Length-indexed object
    with open("data/medium_by_length.json", "w") as f:
        json.dump(build_by_length(medium_words), f, indent=2)
        
    # 5c: Nested Trie structure
    with open("data/medium_trie.json", "w") as f:
        json.dump(build_trie(medium_words), f) # No indent for compression
        
    # Step 6: Process and Save Large Tier
    print(f"💾 Processing Large tier... (loading ENABLE1)")
    with open(ENABLE_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        large_raw = f.readlines()
    large_words_raw = clean_words(large_raw)
    large_words = sorted(list(set(large_words_raw) | set(medium_words)))
    require_words(large_words, "Large tier", 150000)
    print(f"💾 Saving Large tier ({len(large_words)} words)...")

    # 6a: Standard Array
    with open("data/large_array.json", "w") as f:
        json.dump(large_words, f, indent=2)

    # 6b: Length-indexed object
    with open("data/large_by_length.json", "w") as f:
        json.dump(build_by_length(large_words), f, indent=2)

    # 6c: Nested Trie structure
    with open("data/large_trie.json", "w") as f:
        json.dump(build_trie(large_words), f)

    # Step 7: Process Dialects (US/UK)
    print("💾 Processing Dialect: US English...")
    with open(US_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        us_raw = f.readlines()
    us_words = clean_words(us_raw)
    require_words(us_words, "US dialect", 50000)
    with open("data/us_array.json", "w") as f:
        json.dump(us_words, f, indent=2)
    with open("data/us_trie.json", "w") as f:
        json.dump(build_trie(us_words), f)

    print("💾 Processing Dialect: UK English...")
    with open(UK_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        uk_raw = f.readlines()
    uk_words = clean_words(uk_raw)
    require_words(uk_words, "UK dialect", 50000)
    with open("data/uk_array.json", "w") as f:
        json.dump(uk_words, f, indent=2)
    with open("data/uk_trie.json", "w") as f:
        json.dump(build_trie(uk_words), f)

    print("\n✨ All tiers and dialects generated successfully!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error during pipeline execution: {e}", file=sys.stderr)
        sys.exit(1)
