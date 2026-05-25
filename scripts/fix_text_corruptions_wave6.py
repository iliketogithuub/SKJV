#!/usr/bin/env python3
import os
import re

BOOKS_DIR = "/home/charlie/Desktop/Websites/SKJV/books"

def preserve_case(old, new):
    if old.isupper():
        return new.upper()
    if old and old[0].isupper():
        return new[0].upper() + new[1:]
    return new

def apply_fixes(text):
    lines = text.split('\n')
    new_lines = []
    
    for line in lines:
        # Skip comparison blocks and insights
        if any(x in line for x in ['[Operational Insight:', 'KJV Skeleton:', 'Traditional KJV:', 'Classic KJV:']):
            new_lines.append(line)
            continue
        
        # Skip headers
        if line.startswith('#'):
            new_lines.append(line)
            continue
            
        # 1. Fix 'tes' -> 'teeth'
        line = re.sub(
            r'\btes\b',
            lambda m: preserve_case(m.group(0), 'teeth'),
            line,
            flags=re.IGNORECASE
        )
        
        # 2. Fix truncated verbs
        line = re.sub(r'\bbehavs\b', 'behaves', line)
        line = re.sub(r'\bbehavs\b'.upper(), 'BEHAVES', line)
        
        line = re.sub(r'\bstrivs\b', 'strives', line)
        line = re.sub(r'\bstrivs\b'.upper(), 'STRIVES', line)
        
        line = re.sub(r'\btroubls\b', 'troubles', line)
        line = re.sub(r'\btroubls\b'.upper(), 'TROUBLES', line)
        
        # 'oppos', 'caus', 'dissolv' preceded by 'you' or general
        line = re.sub(r'\byou chooses\b', 'you choose', line, flags=re.IGNORECASE)
        line = re.sub(r'\byou oppos\b', 'you oppose', line, flags=re.IGNORECASE)
        line = re.sub(r'\byou caus\b', 'you cause', line, flags=re.IGNORECASE)
        line = re.sub(r'\bcaus to approach\b', 'cause to approach', line, flags=re.IGNORECASE) # Psalm 65:4
        line = re.sub(r'\byou lift me up to the wind; you cause me to ride upon it, and dissolv\b', 
                      'you lift me up to the wind; you cause me to ride upon it, and dissolve', line, flags=re.IGNORECASE) # Job 30:22
        
        line = re.sub(r'\boppos\b', 'oppose', line, flags=re.IGNORECASE)
        line = re.sub(r'\bdissolv\b', 'dissolve', line, flags=re.IGNORECASE)
        
        # 3. Fix 'shewbread' -> 'showbread'
        line = re.sub(
            r'\bshewbread\b',
            lambda m: preserve_case(m.group(0), 'showbread'),
            line,
            flags=re.IGNORECASE
        )
        
        # 4. Fix 'from from' -> 'from'
        line = re.sub(
            r'\bfrom\s+from\b',
            lambda m: preserve_case(m.group(0).split()[0], 'from'),
            line,
            flags=re.IGNORECASE
        )
        
        # 5. Fix 'you has been forsaken' in Isaiah 60:15
        line = re.sub(r'\bWhereas you has been forsaken\b', 'Whereas you have been forsaken', line, flags=re.IGNORECASE)
        
        new_lines.append(line)
        
    return '\n'.join(new_lines)

def main():
    files = sorted([f for f in os.listdir(BOOKS_DIR) if f.endswith('.md')])
    print(f"Applying wave 6 text corruptions and doubled prepositions fixes across {len(files)} books...")
    
    modified_count = 0
    for fname in files:
        fpath = os.path.join(BOOKS_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = apply_fixes(content)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_count += 1
            print(f"  📖 {fname}: fixed")
            
    print(f"\nCompleted! Fixed text corruptions in {modified_count} books.")

if __name__ == "__main__":
    main()
