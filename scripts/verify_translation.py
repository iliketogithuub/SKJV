#!/usr/bin/env python3
import os
import re
import sys

# List of forbidden archaisms (must not appear as independent words)
FORBIDDEN_WORDS = [
    (r'\bthee\b', "thee"),
    (r'\bthou\b', "thou"),
    (r'\bye\b', "ye"),
    (r'\bthy\b', "thy"),
    (r'\bthine\b', "thine"),
    (r'\bunto\b', "unto"),
    (r'\bhath\b', "hath"),
    (r'\bhast\b', "hast"),
    (r'\bdoth\b', "doth"),
    (r'\bdost\b', "dost"),
    (r'\bwherefore\b', "wherefore"),
    (r'\blest\b', "lest"),
    (r'\bHoly Ghost\b', "Holy Ghost"),
    # Archaic verb endings -eth / -est (excluding common modern words)
    (r'\b(?!(?:teeth|seth|japheth|seventh|twentieth|thirtieth|fortieth|fiftieth|sixtieth|seventieth|eightieth|ninetieth)\b)\w+eth\b', "-eth ending (e.g., saith, walketh)"),
    (r'\b(?!(?:greatest|highest|lowest|deepest|strongest|longest|oldest|youngest|sweetest|latest|chiefest|least|best|west|rest|priest|forest|tempest|request|honest|earnest|manifest|harvest|guest|nest|test|chest|crest|jest|protest|contest|digest|suggest|invest|arrest|holiest|straitest|mightiest|eldest|goodliest|valiantest|meetest|basest|choicest|faintest|fewest|modest|wrest|smallest|closest|dishonest|fairest|finest|hottest|poorest)\b)\w+est\b', "-est ending (e.g., walkest)")
]

def verify_file(file_path):
    print(f"Verifying file: {file_path}")
    if not os.path.exists(file_path):
        print(f"FAIL: File does not exist: {file_path}")
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        
    errors = 0
    warnings = 0
    
    # 1. Check basic headers
    if not re.search(r'^#\s+.*?\s+-\s+Simple\s+King\s+James\s+Version\s+\(SKJV\)', content, re.MULTILINE):
        print("WARNING: Missing or malformed top title header '# [Book Name] - Simple King James Version (SKJV)'")
        warnings += 1
        
    if not re.search(r'##\s+eof', content, re.IGNORECASE):
        print("FAIL: Missing '## eof' marker at the end of the file")
        errors += 1
        
    # 2. Scan for forbidden archaic words
    for pattern, name in FORBIDDEN_WORDS:
        for idx, line in enumerate(lines, 1):
            matches = re.findall(pattern, line, re.IGNORECASE)
            if matches:
                # Exclude matching if inside an Operational Insight block (which describes the old text for comparison)
                if "[Operational Insight:" in line or "KJV Skeleton:" in line or "Traditional KJV:" in line or "Classic KJV:" in line:
                    continue
                print(f"FAIL: Found forbidden word '{name}' on line {idx}: \"{line.strip()}\"")
                errors += 1
                
    # 3. Check for successful mappings of key covenant terms in relevant books/chapters
    filename = os.path.basename(file_path)
    if "Mark" in filename:
        # Check for grudge and sins replacements in Mark 11
        if not re.search(r'\bgrudge\b', content, re.IGNORECASE):
            print("WARNING: Covenant term 'grudge' (Mark 11:25 replacement) not found in Mark translation.")
            warnings += 1
        if not re.search(r'\bsins\b', content, re.IGNORECASE):
            print("WARNING: Covenant term 'sins' (Mark 11:25-26 replacement) not found in Mark translation.")
            warnings += 1
            
    if "Acts" in filename:
        # Check for supernatural power or Holy Spirit
        if not re.search(r'supernatural power', content, re.IGNORECASE):
            print("WARNING: Covenant term 'supernatural power' (Acts 1:8 replacement) not found in Acts translation.")
            warnings += 1
            
    # Print results
    if errors == 0:
        print(f"SUCCESS: {file_path} passed verification with 0 errors. (Warnings: {warnings})")
        return True
    else:
        print(f"FAILED: {file_path} has {errors} verification error(s). (Warnings: {warnings})")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: verify_translation.py <path_to_skjv_markdown_file>")
        sys.exit(1)
        
    success = verify_file(sys.argv[1])
    sys.exit(0 if success else 1)
