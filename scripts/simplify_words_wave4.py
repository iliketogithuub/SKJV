#!/usr/bin/env python3
import os
import re

BOOKS_DIR = "/home/charlie/Desktop/Websites/SKJV/books"

# Simple word replacements
SIMPLE_REPLACEMENTS = {
    'spake': 'spoke',
    'shew': 'show',
    'slew': 'killed',
    'shewed': 'showed',
    'brake': 'broke',
    'nought': 'nothing',
    'gat': 'got',
    'shewing': 'showing',
    'oft': 'often',
    'similitude': 'likeness',
    'wot': 'know',
    'heretofore': 'previously',
    'dearth': 'famine',
    'afore': 'before',
    'aforetime': 'before',
    'subtilty': 'cunning',
    'goodman': 'master of the house',
    'matrix': 'womb',
    'holpen': 'helped',
    'ofttimes': 'often',
    'naught': 'nothing',
    'seemly': 'proper',
    'anon': 'immediately',
    'unseemly': 'improperly',
    'trow': 'think',
    'superfluity': 'excess',
    'eschew': 'avoid',
    
    # Helper verbs
    'didst': 'did',
    'hadst': 'had',
    'canst': 'can',
    'wert': 'were',
}

def preserve_case(old, new):
    if old.isupper():
        return new.upper()
    if old and old[0].isupper():
        return new[0].upper() + new[1:]
    return new

def apply_replacements(text, book_name):
    # Split text into lines to process them individually and avoid touching comparison blocks
    lines = text.split('\n')
    new_lines = []
    
    for line in lines:
        # Exclude comparison lines or insights
        if "[Operational Insight:" in line or "KJV Skeleton:" in line or "Traditional KJV:" in line or "Classic KJV:" in line:
            new_lines.append(line)
            continue
            
        # Apply context-dependent replacements first
        
        # 1. Clave
        line = re.sub(r'\bclave to\b', lambda m: preserve_case(m.group(0), 'clung to'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bclave apart\b', lambda m: preserve_case(m.group(0), 'split apart'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bclave the wood\b', lambda m: preserve_case(m.group(0), 'split the wood'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bclave the rocks?\b', lambda m: preserve_case(m.group(0), 'split the rock' + ('s' if 'rocks' in m.group(0).lower() else '')), line, flags=re.IGNORECASE)
        line = re.sub(r'\bclave an hollow\b', lambda m: preserve_case(m.group(0), 'split a hollow'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bclave\b', lambda m: preserve_case(m.group(0), 'clung'), line, flags=re.IGNORECASE)
        
        # 2. Travail / Travailed / Travailing
        line = re.sub(r'\bwoman in travail\b', lambda m: preserve_case(m.group(0), 'woman in labor'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bin travail\b', lambda m: preserve_case(m.group(0), 'in labor'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bwoman that travails\b', lambda m: preserve_case(m.group(0), 'woman in labor'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bwoman with child and her that travails with child\b', lambda m: preserve_case(m.group(0), 'woman with child and her who is in labor'), line, flags=re.IGNORECASE)
        line = re.sub(r'\btravailing woman\b', lambda m: preserve_case(m.group(0), 'woman in labor'), line, flags=re.IGNORECASE)
        line = re.sub(r'\btravail with child\b', lambda m: preserve_case(m.group(0), 'labor with child'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bwork and labour and travail\b', lambda m: preserve_case(m.group(0), 'work and labor and hardship'), line, flags=re.IGNORECASE)
        line = re.sub(r'\blabour and travail\b', lambda m: preserve_case(m.group(0), 'labor and hardship'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bsore travail\b', lambda m: preserve_case(m.group(0), 'difficult labor'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bevil travail\b', lambda m: preserve_case(m.group(0), 'misfortune'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bwith gall and travail\b', lambda m: preserve_case(m.group(0), 'with bitterness and hardship'), line, flags=re.IGNORECASE)
        line = re.sub(r'\btravails in pain\b', lambda m: preserve_case(m.group(0), 'groans in labor'), line, flags=re.IGNORECASE)
        line = re.sub(r'\btravailing in birth\b', lambda m: preserve_case(m.group(0), 'in labor'), line, flags=re.IGNORECASE)
        line = re.sub(r'\btravail in birth\b', lambda m: preserve_case(m.group(0), 'labor in birth'), line, flags=re.IGNORECASE)
        
        # specific for travailed
        if "Isaiah" in book_name:
            line = re.sub(r'\btravailed\b', lambda m: preserve_case(m.group(0), 'went into labor'), line, flags=re.IGNORECASE)
        else:
            line = re.sub(r'\btravailed\b', lambda m: preserve_case(m.group(0), 'gave birth'), line, flags=re.IGNORECASE)
            
        line = re.sub(r'\btravails\b', lambda m: preserve_case(m.group(0), 'labors'), line, flags=re.IGNORECASE)
        line = re.sub(r'\btravailing\b', lambda m: preserve_case(m.group(0), 'laboring'), line, flags=re.IGNORECASE)
        line = re.sub(r'\btravail\b', lambda m: preserve_case(m.group(0), 'labor'), line, flags=re.IGNORECASE)
        
        # 3. Hence
        line = re.sub(r'\bfrom hence\b', lambda m: preserve_case(m.group(0), 'from here'), line, flags=re.IGNORECASE)
        line = re.sub(r'\bhence\b', lambda m: preserve_case(m.group(0), 'from here'), line, flags=re.IGNORECASE)
        
        # 4. Simple replacements
        for old, new in SIMPLE_REPLACEMENTS.items():
            line = re.sub(r'\b' + re.escape(old) + r'\b', lambda m, n=new: preserve_case(m.group(0), n), line, flags=re.IGNORECASE)
            
        new_lines.append(line)
        
    return '\n'.join(new_lines)

def main():
    files = sorted([f for f in os.listdir(BOOKS_DIR) if f.endswith('.md')])
    print(f"Running Wave 4 Modernization Sweep on {len(files)} files...")
    
    modified_count = 0
    for fname in files:
        fpath = os.path.join(BOOKS_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = apply_replacements(content, fname)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_count += 1
            
    print(f"Sweep complete! Modernized {modified_count} books.")

if __name__ == "__main__":
    main()
