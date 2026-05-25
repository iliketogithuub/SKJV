#!/usr/bin/env python3
import os
import re

BOOKS_DIR = "/home/charlie/Desktop/Websites/SKJV/books"

def simplify_line(line):
    # Skip lines that are part of Operational Insights or skeletons
    if "[Operational Insight:" in line or "KJV Skeleton:" in line or "Traditional KJV:" in line or "Classic KJV:" in line:
        return line

    # 1. Durst -> Dared
    line = re.sub(r'\bdurst\s+no\s+man\b', 'no one dared', line, flags=re.IGNORECASE)
    line = re.sub(r'\bdurst\s+not\b', 'dared not', line, flags=re.IGNORECASE)
    line = re.sub(r'\bdurst\s+ask\b', 'dared ask', line, flags=re.IGNORECASE)
    line = re.sub(r'\bdurst\s+presume\b', 'dared presume', line, flags=re.IGNORECASE)
    line = re.sub(r'\bdurst\b', 'dared', line)
    line = re.sub(r'\bDurst\b', 'Dared', line)

    # 2. Lasciviousness -> Sensuality
    line = re.sub(r'\blasciviousness\b', 'sensuality', line)
    line = re.sub(r'\bLasciviousness\b', 'Sensuality', line)

    # 3. Entreated -> Treated
    line = re.sub(r'\bevil\s+entreated\b', 'mistreated', line, flags=re.IGNORECASE)
    line = re.sub(r'\bcourteously\s+entreated\b', 'courteously treated', line, flags=re.IGNORECASE)
    line = re.sub(r'\bspitefully\s+entreated\b', 'spitefully treated', line, flags=re.IGNORECASE)
    line = re.sub(r'\bentreated\s+Abram\s+well\b', 'treated Abram well', line, flags=re.IGNORECASE)
    line = re.sub(r'\bentreated\s+him\s+shamefully\b', 'treated him shamefully', line, flags=re.IGNORECASE)
    line = re.sub(r'\bentreated\s+them\s+spitefully\b', 'treated them spitefully', line, flags=re.IGNORECASE)
    line = re.sub(r'\bshamefully\s+entreated\b', 'shamefully treated', line, flags=re.IGNORECASE)
    line = re.sub(r'\bentreated\b', 'treated', line)
    line = re.sub(r'\bEntreated\b', 'Treated', line)

    # 4. Charity -> Love / Love feasts
    line = re.sub(r'\bfeasts\s+of\s+charity\b', 'love feasts', line, flags=re.IGNORECASE)
    line = re.sub(r'\bcharity\b', 'love', line)
    line = re.sub(r'\bCharity\b', 'Love', line)

    # 5. Wrought -> Worked / Done / Performed
    line = re.sub(r'\bwrought\s+folly\b', 'done folly', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+wickedness\b', 'done wickedness', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+confusion\b', 'done confusion', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+miracles\b', 'performed miracles', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+onyx\s+stones\b', 'crafted onyx stones', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+jewels\b', 'crafted jewels', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+with\s+needlework\b', 'worked with needlework', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+needlework\b', 'worked with needlework', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeen\s+wrought\s+with\b', 'worked', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+righteousness\b', 'worked righteousness', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+effectually\b', 'worked effectively', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+a\s+good\s+work\b', 'done a good work', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+but\s+one\s+hour\b', 'worked only one hour', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+death\b', 'produced death', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+in\s+Egypt\b', 'done in Egypt', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+in\s+Israel\b', 'done in Israel', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\s+among\b', 'performed among', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwere\s+wrought\b', 'were performed', line, flags=re.IGNORECASE)
    line = re.sub(r'\bhad\s+wrought\b', 'had done', line, flags=re.IGNORECASE)
    line = re.sub(r'\bhas\s+wrought\b', 'has done', line, flags=re.IGNORECASE)
    line = re.sub(r'\bhave\s+wrought\b', 'have done', line, flags=re.IGNORECASE)
    line = re.sub(r'\bThen\s+wrought\b', 'Then worked', line, flags=re.IGNORECASE)
    line = re.sub(r'\bthat\s+wrought\b', 'who worked', line, flags=re.IGNORECASE)
    line = re.sub(r'\bthem\s+that\s+wrought\b', 'those who worked', line, flags=re.IGNORECASE)
    line = re.sub(r'\bthey\s+wrought\b', 'they worked', line, flags=re.IGNORECASE)
    line = re.sub(r'\bfaith\s+wrought\b', 'faith worked', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwrought\b', 'worked', line)
    line = re.sub(r'\bWrought\b', 'Worked', line)

    # 6. Beheld -> Saw / Looked
    line = re.sub(r'\bI\s+beheld\s+till\b', 'I looked until', line, flags=re.IGNORECASE)
    line = re.sub(r'\bI\s+beheld\s+even\s+till\b', 'I looked even until', line, flags=re.IGNORECASE)
    line = re.sub(r'\bI\s+beheld\s+then\b', 'I looked then', line, flags=re.IGNORECASE)
    line = re.sub(r'\bI\s+beheld,\s+and\b', 'I looked, and', line, flags=re.IGNORECASE)
    line = re.sub(r'\bI\s+beheld\b', 'I saw', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeheld\s+the\b', 'saw the', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeheld\s+him\b', 'saw him', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeheld\s+them\b', 'saw them', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeheld\s+it\b', 'saw it', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeheld\s+her\b', 'saw her', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeheld\s+his\b', 'saw his', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeheld\s+your\b', 'saw your', line, flags=re.IGNORECASE)
    line = re.sub(r'\bhad\s+beheld\b', 'had seen', line, flags=re.IGNORECASE)
    line = re.sub(r'\bBeheld\b', 'Saw', line)
    line = re.sub(r'\bbeheld\b', 'saw', line)

    # 7. Beholding -> Looking / Seeing / Observing
    line = re.sub(r'\bbeholding\s+his\b', 'looking at his', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeholding\s+the\b', 'watching the', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeholding\s+as\s+in\s+a\s+glass\b', 'looking as in a mirror', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeholding\s+your\b', 'observing your', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeholding\s+vanity\b', 'looking at vanity', line, flags=re.IGNORECASE)
    line = re.sub(r'\bstood\s+beholding\b', 'stood watching', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeholding\s+these\s+things\b', 'watching these things', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeholding\s+the\s+things\b', 'watching the things', line, flags=re.IGNORECASE)
    line = re.sub(r'\bbeholding\b', 'looking', line)
    line = re.sub(r'\bBeholding\b', 'Looking', line)

    # 8. Behold -> Look / See
    line = re.sub(r'\bto\s+behold\b', 'to see', line, flags=re.IGNORECASE)
    line = re.sub(r'\bshall\s+behold\b', 'will see', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwill\s+behold\b', 'will see', line, flags=re.IGNORECASE)
    line = re.sub(r'\bmay\s+behold\b', 'may see', line, flags=re.IGNORECASE)
    line = re.sub(r'\bshould\s+behold\b', 'should see', line, flags=re.IGNORECASE)
    line = re.sub(r'\bcould\s+behold\b', 'could see', line, flags=re.IGNORECASE)
    line = re.sub(r'\bwould\s+behold\b', 'would see', line, flags=re.IGNORECASE)
    line = re.sub(r'\bdared\s+not\s+behold\b', 'dared not look', line, flags=re.IGNORECASE)
    line = re.sub(r'\bdurst\s+not\s+behold\b', 'dared not look', line, flags=re.IGNORECASE)

    line = re.sub(r'\bBehold\s+(the|my|your|his|her|their|our|me|him|them|it|you|us)\b', r'Look at \1', line)
    line = re.sub(r'\bbehold\s+(the|my|your|his|her|their|our|me|him|them|it|you|us)\b', r'look at \1', line)

    line = re.sub(r'\bBehold,\b', 'Look,', line)
    line = re.sub(r'\bbehold,\b', 'look,', line)
    line = re.sub(r'\bBehold!\b', 'Look!', line)
    line = re.sub(r'\bbehold!\b', 'look!', line)

    line = re.sub(r'\bBehold\s+(I|there|he|she|they|we|you|a|in|now|here|thy|thine)\b', r'Look, \1', line)
    line = re.sub(r'\bbehold\s+(I|there|he|she|they|we|you|a|in|now|here|thy|thine)\b', r'look, \1', line)

    line = re.sub(r'\bBehold\b', 'Look', line)
    line = re.sub(r'\bbehold\b', 'look', line)

    # 9. Lo -> Look
    line = re.sub(r'\bLo,\b', 'Look,', line)
    line = re.sub(r'\blo,\b', 'look,', line)
    line = re.sub(r'\bLo!\b', 'Look!', line)
    line = re.sub(r'\blo!\b', 'look!', line)
    line = re.sub(r'\bLo\s+(I|there|he|she|they|we|you|a|in|now|here|thy|thine)\b', r'Look, \1', line)
    line = re.sub(r'\blo\s+(I|there|he|she|they|we|you|a|in|now|here|thy|thine)\b', r'look, \1', line)
    line = re.sub(r'\bLo\b', 'Look', line)
    line = re.sub(r'\blo\b', 'look', line)

    return line

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    changes = 0

    for line in lines:
        new_line = simplify_line(line)
        if new_line != line:
            changes += 1
        new_lines.append(new_line)

    if changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
    return changes

def main():
    files = sorted([f for f in os.listdir(BOOKS_DIR) if f.endswith('.md')])
    total_files = 0
    total_changes = 0

    for fname in files:
        fpath = os.path.join(BOOKS_DIR, fname)
        changes = process_file(fpath)
        if changes > 0:
            total_files += 1
            total_changes += changes
            print(f"  🔧 {fname}: applied {changes} lines of changes")

    print(f"\nSweep completed: {total_changes} line modifications across {total_files} files.")

if __name__ == "__main__":
    main()
