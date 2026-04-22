import fs from 'fs';
import path from 'path';

/**
 * Compiles a raw word list (one word per line) into a compressed Trie JSON structure.
 * Usage: node scripts/compile.js <input-file> <output-file>
 */

const buildTrie = (words) => {
  const root = {};
  for (let word of words) {
    word = word.trim().toLowerCase();
    if (!word) continue;
    
    let node = root;
    for (const char of word) {
      if (!node[char]) node[char] = {};
      node = node[char];
    }
    node._ = 1; // Mark end of word
  }
  return root;
};

const compile = () => {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node scripts/compile.js <input.txt> <output.json>');
    process.exit(1);
  }

  const [inputPath, outputPath] = args;

  try {
    console.log(`Reading words from ${inputPath}...`);
    const content = fs.readFileSync(inputPath, 'utf8');
    const words = content.split('\n');
    
    console.log(`Building Trie for ${words.length} words...`);
    const trie = buildTrie(words);
    
    console.log(`Writing compressed JSON to ${outputPath}...`);
    fs.writeFileSync(outputPath, JSON.stringify(trie));
    
    console.log('Done!');
  } catch (err) {
    console.error('Compilation failed:', err.message);
    process.exit(1);
  }
};

compile();
