import fs from 'fs';
import { TrieEngine } from '../src/index.js';

const small = JSON.parse(fs.readFileSync('./data/small_tier.json', 'utf8'));
const medium = JSON.parse(fs.readFileSync('./data/medium_array.json', 'utf8'));
const large = JSON.parse(fs.readFileSync('./data/large_array.json', 'utf8'));

const smallSet = new Set(small);
const mediumSet = new Set(medium);
const largeSet = new Set(large);

console.log('🧪 Starting Integrity Tests...\n');

// 1. Subset Checks
const isSubset = (smaller, larger, name1, name2) => {
    const missing = [...smaller].filter(word => !larger.has(word));
    if (missing.length === 0) {
        console.log(`✅ ${name1} is a subset of ${name2}`);
    } else {
        console.error(`❌ ${name1} contains ${missing.length} words NOT in ${name2}`);
        console.error('Example missing words:', missing.slice(0, 5));
        return false;
    }
    return true;
};

const s1 = isSubset(smallSet, mediumSet, 'Small', 'Medium');
const s2 = isSubset(mediumSet, largeSet, 'Medium', 'Large');

// 2. Character Sanity
const checkChars = (words, name) => {
    const pattern = /[^a-z]/;
    const invalid = words.filter(word => pattern.test(word));
    if (invalid.length === 0) {
        console.log(`✅ ${name} contains only lowercase a-z`);
    } else {
        console.error(`❌ ${name} contains ${invalid.length} invalid words`);
        console.error('Example invalid words:', invalid.slice(0, 5));
        return false;
    }
    return true;
};

const c1 = checkChars(small, 'Small');
const c2 = checkChars(medium, 'Medium');
const c3 = checkChars(large, 'Large');

// 3. Trie Structure Check
const checkTrie = (filename) => {
    const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
    const engine = new TrieEngine(data);
    
    // Check a few known words
    const testWord = 'apple';
    if (engine.validate(testWord)) {
        console.log(`✅ Trie ${filename} is functional (validated "${testWord}")`);
    } else {
        console.error(`❌ Trie ${filename} failed to validate "${testWord}"`);
        return false;
    }
    return true;
};

const t1 = checkTrie('./data/medium_trie.json');
const t2 = checkTrie('./data/large_trie.json');
const t3 = checkTrie('./data/us_trie.json');
const t4 = checkTrie('./data/uk_trie.json');

// 4. Blocklist Check (Sanity)
const blocklist = ['facebook', 'google', 'fuck']; // Sample blocked terms
const checkBlocklist = (words, name) => {
    const found = words.filter(word => blocklist.includes(word));
    if (found.length === 0) {
        console.log(`✅ ${name} passes blocklist sanity check`);
    } else {
        console.error(`❌ ${name} contains blocked terms:`, found);
        return false;
    }
    return true;
};

const b1 = checkBlocklist(large, 'Large');

// 5. Dialect Variation Check (color vs colour)
const checkDialects = () => {
    const usTrie = new TrieEngine(JSON.parse(fs.readFileSync('./data/us_trie.json', 'utf8')));
    const ukTrie = new TrieEngine(JSON.parse(fs.readFileSync('./data/uk_trie.json', 'utf8')));
    
    const isUsValid = usTrie.validate('color');
    const isUkValid = ukTrie.validate('colour');
    const isUsUkInvalid = !usTrie.validate('colour');
    const isUkUsInvalid = !ukTrie.validate('color');

    if (isUsValid && isUkValid && isUsUkInvalid && isUkUsInvalid) {
        console.log('✅ Dialect separation verified (color vs colour)');
        return true;
    } else {
        console.error('❌ Dialect separation failed');
        console.log('US valid color:', isUsValid);
        console.log('UK valid colour:', isUkValid);
        console.log('US invalid colour:', isUsUkInvalid);
        console.log('UK invalid color:', isUkUsInvalid);
        return false;
    }
};

const d1 = checkDialects();

console.log('\n--- Result Summary ---');
if (s1 && s2 && c1 && c2 && c3 && t1 && t2 && t3 && t4 && b1 && d1) {
    console.log('🌟 ALL INTEGRITY TESTS PASSED 🌟');
    process.exit(0);
} else {
    console.error('🛑 SOME TESTS FAILED 🛑');
    process.exit(1);
}
