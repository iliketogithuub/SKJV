#!/usr/bin/env python3
import os
import re
import json

def generate():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    books_dir = os.path.abspath(os.path.join(script_dir, "..", "books"))
    output_file = os.path.abspath(os.path.join(script_dir, "..", "book_layout", "bible_data.js"))
    
    if not os.path.exists(books_dir):
        print(f"Books directory not found: {books_dir}")
        return
        
    bible_data = {}
    
    # Sort files naturally
    files = sorted([f for f in os.listdir(books_dir) if f.endswith('.md')])
    print(f"Parsing {len(files)} books...")
    
    for fname in files:
        fpath = os.path.join(books_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Get book name (extract from filename or top header)
        # e.g., "01 - Genesis - BKJV.md" -> "Genesis"
        book_name_match = re.match(r'^\d+\s+-\s+(.*?)\s+-\s+BKJV\.md$', fname)
        if book_name_match:
            book_name = book_name_match.group(1).strip()
        else:
            book_name = fname.replace(".md", "")
            
        bible_data[book_name] = {}
        
        # Split by chapter headers: "## [Book Name] Chapter [Number]"
        # Allow optional "The Gospel According to" in header matches
        chapter_regex = r'(##\s+.*?Chapter\s+(\d+))'
        parts = re.split(chapter_regex, content)
        
        # parts[0] is intro text before Chapter 1
        for i in range(len(parts) // 3):
            chapter_num = parts[i*3 + 2]
            chapter_text = parts[i*3 + 3].strip()
            
            # Remove trailing eof or formatting notes
            chapter_text = re.sub(r'##\s+eof.*$', '', chapter_text, flags=re.IGNORECASE).strip()
            
            bible_data[book_name][chapter_num] = {
                "verses": {},
                "insight": None
            }
            
            # Extract Operational Insight if present
            insight_match = re.search(r'\[Operational Insight:\s*(.*?)\]', chapter_text, re.DOTALL | re.IGNORECASE)
            if insight_match:
                bible_data[book_name][chapter_num]["insight"] = insight_match.group(1).strip()
                # Remove insight block from main text to avoid double-printing
                chapter_text = re.sub(r'\[Operational Insight:\s*.*?\]', '', chapter_text, flags=re.DOTALL | re.IGNORECASE).strip()
                
            # Extract verses: lines starting with a number
            lines = chapter_text.split('\n')
            for line in lines:
                line = line.strip()
                verse_match = re.match(r'^(\d+)\s+(.*)$', line)
                if verse_match:
                    v_num = verse_match.group(1)
                    v_text = verse_match.group(2).strip()
                    bible_data[book_name][chapter_num]["verses"][v_num] = v_text
                    
    # Write as JS file exporting a global constant
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("// BKJV Bible Database (Generated Offline)\n")
        f.write("const BIBLE_DATA = ")
        f.write(json.dumps(bible_data, indent=2, ensure_ascii=False))
        f.write(";\n")
        
    print(f"Successfully generated database at: {output_file}")

if __name__ == "__main__":
    generate()
