#!/usr/bin/env python3
import os
import re
import glob

KJV_DIR = "/home/charlie/Downloads/kjv-markdown-master"
SKJV_DIR = "/home/charlie/Desktop/Websites/SKJV/books"

# Strict whitelist of words we want to restore to the SKJV.
# If a word in KJV ends in -est but is NOT in this list, it is treated as an
# archaic verb (like walkest, believest) and will NOT be restored.
RESTORE_WORDS = {
    'priest', 'priests', "priest's", "priests'",
    'rest', 'rests', "rest's",
    'west', 'wests',
    'best', 'bests',
    'forest', 'forests', "forest's",
    'harvest', 'harvests',
    'tempest', 'tempests',
    'earnest',
    'manifest',
    'guest', 'guests',
    'honest',
    'request', 'requests',
    'protest', 'protests',
    'chest', 'chests',
    'least', 'leasts',
    'east', 'easts',
    'beast', 'beasts', "beast's", "beasts'",
    'interest', 'interests',
    'test', 'tests',
    'nest', 'nests',
    'pest', 'pests',
    'crest', 'crests',
    'jest', 'jests',
    'contest', 'contests',
    'arrest', 'arrests',
    'invest', 'invests',
    'divest', 'suggest', 'suggests',
    'digest', 'digests',
    'detest', 'detests',
    'wrest', 'wrests',
    'modest',
    'dishonest',
    # Superlatives
    'greatest', 'highest', 'lowest', 'strongest', 'longest', 'oldest', 'youngest',
    'sweetest', 'latest', 'chiefest', 'nearest', 'dearest', 'poorest', 'smallest',
    'largest', 'hardest', 'softest', 'richest', 'wisest', 'slowest',
    'fairest', 'purest', 'fullest', 'bravest', 'truest', 'sharpest', 'finest',
    'brightest', 'lightest', 'darkest', 'coldest', 'hottest', 'clearest', 'cleanest',
    'plainest', 'wildest', 'proudest', 'boldest', 'loveliest', 'worthiest', 'holiest',
    'mightiest', 'heaviest', 'earliest', 'eldest', 'goodliest', 'valiantest',
    'straitest', 'meetest', 'basest', 'choicest', 'faintest', 'fewest'
}

# Mapping of unique stems to replace globally (only for stems that are not real words)
GLOBAL_STEM_MAP = {
    r'\bpri\b': 'priest',
    r'\bPri\b': 'Priest',
    r'\bpri\'s\b': "priest's",
    r'\bPri\'s\b': "Priest's",
    r'\br\b': 'rest',
    r'\bR\b': 'Rest',
    r'\bw\b': 'west',
    r'\bW\b': 'West',
    r'\bb\b': 'best',
    r'\bB\b': 'Best',
    r'\bharv\b': 'harvest',
    r'\bHarv\b': 'Harvest',
    r'\btemp\b': 'tempest',
    r'\bTemp\b': 'Tempest',
    r'\bearn\b': 'earnest',
    r'\bEarn\b': 'Earnest',
    r'\bmanif\b': 'manifest',
    r'\bManif\b': 'Manifest',
    r'\bgu\b': 'guest',
    r'\bGu\b': 'Guest',
    r'\bhon\b': 'honest',
    r'\bHon\b': 'Honest',
    r'\brequ\b': 'request',
    r'\bRequ\b': 'Request',
    r'\bprot\b': 'protest',
    r'\bProt\b': 'Protest',
    r'\bch\b': 'chest',
    r'\bCh\b': 'Chest',
    r'\beld\b': 'eldest',
    r'\bEld\b': 'Eldest',
    r'\bholi\b': 'holiest',
    r'\bHoli\b': 'Holiest',
    r'\bmighti\b': 'mightiest',
    r'\bMighti\b': 'Mightiest',
    r'\bloveli\b': 'loveliest',
    r'\bLoveli\b': 'Loveliest',
    r'\bworthi\b': 'worthiest',
    r'\bWorthi\b': 'Worthiest',
    r'\bheavi\b': 'heaviest',
    r'\bHeavi\b': 'Heaviest',
    r'\bearli\b': 'earliest',
    r'\bEarli\b': 'Earliest',
}

def clean_word(word):
    cleaned = re.sub(r"^[^\w']+", "", word)
    cleaned = re.sub(r"[^\w']+$", "", cleaned)
    return cleaned

def parse_file_to_verses(lines):
    verse_map = {}
    current_chapter = 0
    for idx, line in enumerate(lines):
        line_str = line.strip()
        chap_match = re.match(r'^##\s+(?:.*\s+)?Chapter\s+(\d+)', line_str, re.IGNORECASE)
        if chap_match:
            current_chapter = int(chap_match.group(1))
            continue
            
        verse_match = re.match(r'^(\d+)\s+', line_str)
        if verse_match and current_chapter > 0:
            verse_num = int(verse_match.group(1))
            verse_map[(current_chapter, verse_num)] = idx
            
    return verse_map

def fix_book(kjv_path, skjv_path):
    if not os.path.exists(skjv_path):
        return 0
        
    with open(kjv_path, 'r', encoding='utf-8') as f:
        kjv_lines = f.readlines()
        
    with open(skjv_path, 'r', encoding='utf-8') as f:
        skjv_lines = f.readlines()
        
    kjv_map = parse_file_to_verses(kjv_lines)
    skjv_map = parse_file_to_verses(skjv_lines)
    
    fixes_count = 0
    modified = False
    
    # 1. Verse-level alignment for whitelisted -est words
    for (chapter, verse), kjv_idx in kjv_map.items():
        if (chapter, verse) not in skjv_map:
            continue
            
        skjv_idx = skjv_map[(chapter, verse)]
        kjv_line = kjv_lines[kjv_idx]
        skjv_line = skjv_lines[skjv_idx]
        
        kjv_tokens = kjv_line.split()
        skjv_tokens = skjv_line.split()
        
        line_modified = False
        
        for idx, kjv_token in enumerate(kjv_tokens):
            kjv_word = clean_word(kjv_token)
            
            # If it ends in -est, check if it's in the RESTORE_WORDS whitelist
            if kjv_word.lower().endswith('est') and len(kjv_word) > 3:
                if kjv_word.lower() not in RESTORE_WORDS:
                    continue
                    
                # We want to restore this word
                stem = kjv_word[:-3]
                
                # Check near idx in SKJV tokens
                search_start = max(0, idx - 3)
                search_end = min(len(skjv_tokens), idx + 4)
                
                for s_idx in range(search_start, search_end):
                    skjv_token_to_check = skjv_tokens[s_idx]
                    skjv_word = clean_word(skjv_token_to_check)
                    
                    if skjv_word.lower() == stem.lower():
                        prefix_match = re.match(r"^([^\w']+)", skjv_token_to_check)
                        suffix_match = re.search(r"([^\w']+)$", skjv_token_to_check)
                        prefix = prefix_match.group(1) if prefix_match else ""
                        suffix = suffix_match.group(1) if suffix_match else ""
                        
                        restored_word = kjv_word
                        if skjv_word.isupper():
                            restored_word = restored_word.upper()
                        elif skjv_word[0].isupper():
                            restored_word = restored_word[0].upper() + restored_word[1:]
                            
                        new_token = prefix + restored_word + suffix
                        
                        if skjv_tokens[s_idx] != new_token:
                            skjv_tokens[s_idx] = new_token
                            line_modified = True
                            fixes_count += 1
                        break
                        
        if line_modified:
            skjv_lines[skjv_idx] = " ".join(skjv_tokens) + "\n"
            modified = True
            
    # 2. Global clean-up sweep of unique stems (only for those in RESTORE_WORDS / GLOBAL_STEM_MAP)
    for i in range(len(skjv_lines)):
        line = skjv_lines[i]
        orig_line = line
        
        # We do case-sensitive global word boundary replacements for unique stems
        for pattern, replacement in GLOBAL_STEM_MAP.items():
            line = re.sub(pattern, replacement, line)
            
        if line != orig_line:
            skjv_lines[i] = line
            modified = True
            fixes_count += 1
            
    if modified:
        with open(skjv_path, 'w', encoding='utf-8') as f:
            f.writelines(skjv_lines)
            
    return fixes_count

def main():
    print("=" * 60)
    print("SKJV Refactored Est Corruptions Restoration Script")
    print("=" * 60)
    
    total_fixes = 0
    files_fixed = 0
    
    book_files = sorted([f for f in os.listdir(SKJV_DIR) if f.endswith('.md')])
    
    for filename in book_files:
        kjv_filename = filename.replace("- SKJV.md", "- KJV.md")
        kjv_path = os.path.join(KJV_DIR, kjv_filename)
        skjv_path = os.path.join(SKJV_DIR, filename)
        
        if not os.path.exists(kjv_path):
            continue
            
        fixes = fix_book(kjv_path, skjv_path)
        total_fixes += fixes
        
        if fixes > 0:
            print(f"  🔧 {filename}: Restored {fixes} occurrences")
            files_fixed += 1
            
    print(f"\n{'=' * 60}")
    print(f"COMPREHENSIVE SUMMARY OF CORRUPTIONS FIXED")
    print(f"{'=' * 60}")
    print(f"  Total words restored: {total_fixes}")
    print(f"  Files modified:       {files_fixed}")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
