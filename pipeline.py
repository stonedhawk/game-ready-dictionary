import requests
import json
import re
import os
from collections import defaultdict

try:
    from better_profanity import profanity
except ImportError:
    print("Please install better_profanity: pip install better_profanity")
    class ProfanityFallback:
        def contains_profanity(self, word): return False
        def load_censor_words(self): pass
    profanity = ProfanityFallback()

# Hardcoded array of non-dictionary brand names to block
TRADEMARK_BLOCKLIST = [
    "facebook", "google", "microsoft", "netflix", 
    "twitter", "instagram", "tiktok", "disney", "nintendo", "sony",
    "adidas", "nike", "pepsi", "coca-cola", "mcdonalds", "starbucks",
    "tesla", "uber", "airbnb", "spotify", "adobe", "nvidia", "intel",
    "lexus", "toyota", "samsung", "iphone", "ipad"
]

def download_file(url, filename):
    """Downloads a file from the provided URL."""
    print(f"🚀 Downloading {filename} from: {url}")
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"✅ Download complete: {filename}")

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
    # URLs for resources
    DESK_URL = "https://raw.githubusercontent.com/mattwarren/Spelling-Corrector/master/SpellingCorrector/WordLists/5desk.txt"
    FREQ_URL = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt"
    ENABLE_URL = "https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt"
    
    DESK_FILE = "5desk.txt"
    FREQ_FILE = "google-10000.txt"
    ENABLE_FILE = "enable1.txt"
    
    try:
        # Step 1: Download resources
        download_file(DESK_URL, DESK_FILE)
        download_file(FREQ_URL, FREQ_FILE)
        download_file(ENABLE_URL, ENABLE_FILE)
        
        # Step 2: Load and Clean Medium Tier (Full 12Dicts)
        with open(DESK_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            medium_raw = f.readlines()
        medium_words = clean_words(medium_raw)
        
        # Step 3: Load and Process Small Tier (Top 10k Intersection)
        with open(FREQ_FILE, 'r', encoding='utf-8') as f:
            freq_raw = f.readlines()
        freq_words = set(word.strip().lower() for word in freq_raw)
        small_words = sorted(list(set(medium_words) & freq_words))
        
        # Step 4: Save Small Tier
        print(f"💾 Saving Small tier ({len(small_words)} words)...")
        with open("small_tier.json", "w") as f:
            json.dump(small_words, f, indent=2)

        # Step 5: Process and Save Medium Tier Outputs
        print(f"💾 Processing Medium tier ({len(medium_words)} words)...")
        
        # 5a: Standard Array
        with open("medium_array.json", "w") as f:
            json.dump(medium_words, f, indent=2)
            
        # 5b: Length-indexed object
        with open("medium_by_length.json", "w") as f:
            json.dump(build_by_length(medium_words), f, indent=2)
            
        # 5c: Nested Trie structure
        with open("medium_trie.json", "w") as f:
            json.dump(build_trie(medium_words), f) # No indent for compression
            
        # Step 6: Process and Save Large Tier
        print(f"💾 Processing Large tier... (loading ENABLE1)")
        with open(ENABLE_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            large_raw = f.readlines()
        large_words_raw = clean_words(large_raw)
        large_words = sorted(list(set(large_words_raw) | set(medium_words)))
        print(f"💾 Saving Large tier ({len(large_words)} words)...")

        # 6a: Standard Array
        with open("large_array.json", "w") as f:
            json.dump(large_words, f, indent=2)

        # 6b: Length-indexed object
        with open("large_by_length.json", "w") as f:
            json.dump(build_by_length(large_words), f, indent=2)

        # 6c: Nested Trie structure
        with open("large_trie.json", "w") as f:
            json.dump(build_trie(large_words), f)

        print("\n✨ All tiers and formats generated successfully!")
        
    except Exception as e:
        print(f"❌ Error during pipeline execution: {e}")

if __name__ == "__main__":
    main()
