/**
 * TrieEngine - High-performance word validation for game development.
 * Designed for O(m) lookups and memory-efficient prefix searching.
 */
export class TrieEngine {
  /**
   * @param {Object} data - Pre-compiled Trie JSON data.
   */
  constructor(data = {}) {
    this.root = data;
  }

  /**
   * Validates if a word exists in the dictionary.
   * @param {string} word - The word to validate.
   * @returns {boolean}
   */
  validate(word) {
    if (!word) return false;
    let node = this.root;
    const lowerWord = word.toLowerCase();
    
    for (let i = 0; i < lowerWord.length; i++) {
      const char = lowerWord[i];
      if (!node[char]) return false;
      node = node[char];
    }
    
    return node._ === 1;
  }

  /**
   * Checks if a prefix exists in the dictionary.
   * Useful for pruning recursive search paths.
   * @param {string} prefix - The prefix to check.
   * @returns {boolean}
   */
  isPrefix(prefix) {
    if (!prefix) return true;
    let node = this.root;
    const lowerPrefix = prefix.toLowerCase();

    for (let i = 0; i < lowerPrefix.length; i++) {
      const char = lowerPrefix[i];
      if (!node[char]) return false;
      node = node[char];
    }

    return true;
  }

  /**
   * Returns all words matching a given prefix.
   * @param {string} prefix - The search prefix.
   * @param {number} limit - Maximum results to return.
   * @returns {string[]}
   */
  getPrefixMatches(prefix, limit = 50) {
    let node = this.root;
    const lowerPrefix = prefix.toLowerCase();
    const results = [];

    // Navigate to the end of the prefix
    for (let i = 0; i < lowerPrefix.length; i++) {
      const char = lowerPrefix[i];
      if (!node[char]) return [];
      node = node[char];
    }

    // Depth-first search to find all leaf nodes
    const dfs = (currentNode, currentPath) => {
      if (results.length >= limit) return;
      if (currentNode._ === 1) results.push(currentPath);

      for (const char in currentNode) {
        if (char === '_') continue;
        dfs(currentNode[char], currentPath + char);
      }
    };

    dfs(node, lowerPrefix);
    return results;
  }
}
