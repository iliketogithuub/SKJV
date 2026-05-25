#!/usr/bin/env python3
import os
import re

BOOKS_DIR = "/home/charlie/Desktop/Websites/SKJV/books"

# Map of corrupted words to their correct modern equivalents
CORRUPTIONS_MAP = {
    # Ordinals
    'eightis': 'eightieth',
    'fiftis': 'fiftieth',
    'fortis': 'fortieth',
    'thirtis': 'thirtieth',
    'twentis': 'twentieth',
    'seventis': 'seventieth',
    'ninetis': 'ninetieth',
    'sixtis': 'sixtieth',
    
    # Verbs ending in 'is'
    'carris': 'carries',
    'cris': 'cries',
    'denis': 'denies',
    'despis': 'despises',
    'dris': 'dries',
    'envis': 'envies',
    'flis': 'flies',
    'glorifis': 'glorifies',
    'gloris': 'glories',
    'justifis': 'justifies',
    'lis': 'lies',
    'marris': 'marries',
    'multiplis': 'multiplies',
    'occupis': 'occupies',
    'pacifis': 'pacifies',
    'pitis': 'pities',
    'prophesis': 'prophesies',
    'purifis': 'purifies',
    'sanctifis': 'sanctifies',
    'satisfis': 'satisfies',
    'signifis': 'signifies',
    'studis': 'studies',
    'supplis': 'supplies',
    'tarris': 'tarries',
    'testifis': 'testifies',
    'tris': 'tries',
    'wearis': 'wearies',
    'edifis': 'edifies',
    
    # Double consonant and other suffix errors
    'abhorrs': 'abhors',
    'begetts': 'begets',
    'blesss': 'blesses',
    'blotts': 'blots',
    'clapps': 'claps',
    'committs': 'commits',
    'compasss': 'compasses',
    'confesss': 'confesses',
    'cutts': 'cuts',
    'deferrs': 'defers',
    'diggs': 'digs',
    'dipps': 'dips',
    'disannulls': 'disannuls',
    'dresss': 'dresses',
    'dropps': 'drops',
    'excells': 'excels',
    'fitts': 'fits',
    'forgetts': 'forgets',
    'fretts': 'frets',
    'getts': 'gets',
    'lapps': 'laps',
    'letts': 'lets',
    'oppresss': 'oppresses',
    'passs': 'passes',
    'pisss': 'pisses',
    'plotts': 'plots',
    'possesss': 'possesses',
    'presss': 'presses',
    'putts': 'puts',
    'robbs': 'robs',
    'runns': 'runs',
    'setts': 'sets',
    'shedds': 'sheds',
    'shutts': 'shuts',
    'sinns': 'sins',
    'sitts': 'sits',
    'slipps': 'slips',
    'stepps': 'steps',
    'stirrs': 'stirs',
    'stopps': 'stops',
    'swimms': 'swims',
    'transgresss': 'transgresses',
    'travells': 'travels',
    'warrs': 'wars',
    'winns': 'wins',
    'witnesss': 'witnesses',
    'worshipps': 'worships',
    'wotts': 'knows',
    'choos': 'chooses',
}

def preserve_case(old, new):
    if old.isupper():
        return new.upper()
    if old and old[0].isupper():
        return new[0].upper() + new[1:]
    return new

def fix_corruptions(text):
    lines = text.split('\n')
    new_lines = []
    
    for line in lines:
        # Avoid changing comparison blocks or insights
        if "[Operational Insight:" in line or "KJV Skeleton:" in line or "Traditional KJV:" in line or "Classic KJV:" in line:
            new_lines.append(line)
            continue
            
        for old, new in CORRUPTIONS_MAP.items():
            line = re.sub(r'\b' + re.escape(old) + r'\b', lambda m, n=new: preserve_case(m.group(0), n), line, flags=re.IGNORECASE)
            
        new_lines.append(line)
        
    return '\n'.join(new_lines)

def main():
    files = sorted([f for f in os.listdir(BOOKS_DIR) if f.endswith('.md')])
    print(f"Fixing ordinals and verb corruptions in {len(files)} books...")
    
    modified_count = 0
    total_replacements = 0
    
    for fname in files:
        fpath = os.path.join(BOOKS_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = fix_corruptions(content)
        if new_content != content:
            # Count changes
            changes = 0
            for old in CORRUPTIONS_MAP:
                changes += len(re.findall(r'\b' + re.escape(old) + r'\b', content, flags=re.IGNORECASE))
            
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_count += 1
            total_replacements += changes
            print(f"  🔧 {fname}: applied {changes} fixes")
            
    print(f"\nCompleted! Fixed {total_replacements} corrupted words across {modified_count} books.")

if __name__ == "__main__":
    main()
