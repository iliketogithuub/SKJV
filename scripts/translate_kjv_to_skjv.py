#!/usr/bin/env python3
import os
import re
import sys

# Pre-defined translations for showcase verses to guarantee accuracy offline
PREDEFINED_VERSES = {
    # Mark 11:22-26
    "Mark 11:22": '22 Jesus answered and said, "Have faith in God.',
    "Mark 11:23": '23 For truly I tell you, whoever **says to this mountain**, \'Be lifted up and thrown into the sea,\' and **does not doubt within their heart**, but fully **believes that the words spoken with their mouth will happen**—they will have exactly what they have spoken come to pass.',
    "Mark 11:24": '24 Therefore I tell you, whatever things you desire when you pray, **believe that those things have been received**, and those things will manifest.',
    "Mark 11:25": '25 And whenever you **stand to pray**, if you **hold a grudge** against anyone, **forgive them**, so that your Father in heaven may also forgive your sins.',
    "Mark 11:26": '26 But if you do not forgive, neither will your Father in heaven forgive your sins.',
    
    # Isaiah 53:4-5
    "Isaiah 53:4": '4 Surely He has carried our sicknesses and borne our pains; yet we considered Him punished, struck down by God, and afflicted.',
    "Isaiah 53:5": '5 But He was pierced for our rebellion, He was crushed for our sins; the punishment that brought us peace was laid upon Him, and by His wounds we are healed.',
    
    # Matthew 8:16-17
    "Matthew 8:16": '16 When evening came, many who were bound by demons were brought to Jesus. He cast out the spirits with a spoken word and healed everyone who was sick.',
    "Matthew 8:17": '17 This completely fulfilled what was spoken through the prophet Isaiah: “He personally took our sicknesses and carried away our diseases.”',
    
    # 1 Peter 2:24
    "1 Peter 2:24": '24 He personally carried our sins in His own body on the cross, so that we, having died to sin, can live for righteousness—by His wounds you were healed.',
    
    # Luke 10:19
    "Luke 10:19": '19 Listen closely: I have given you delegated authority to trample on serpents and scorpions, and over all the supernatural power of the enemy—and absolutely nothing will harm you.',
    
    # Acts 1:8
    "Acts 1:8": '8 But you will receive supernatural power when the Holy Spirit comes upon you; and you will be witnesses for Me both in Jerusalem, and in all Judea, and in Samaria, and to the very ends of the earth.',
    
    # Acts 2:1-4, 37-39
    "Acts 2:1": '1 When the day of Pentecost fully arrived, all the believers were gathered together in complete unity in one place.',
    "Acts 2:2": '2 And suddenly a sound came from heaven like a rushing, violent wind, filling the entire house where the believers were sitting.',
    "Acts 2:3": '3 Then, separating tongues that looked like fire appeared and rested upon every single individual.',
    "Acts 2:4": '4 Instantly, everyone was filled with the Holy Spirit and began to speak in other tongues, exactly as the Spirit granted the ability to speak.',
    "Acts 2:37": '37 When the crowd heard this, conviction cut deeply into every heart. The people asked Peter and the rest of the apostles, “Brothers, what must we do?”',
    "Acts 2:38": '38 Peter answered, “Repent and be baptized, every single one of you, in the name of Jesus Christ for the forgiveness of your sins; and you will receive the gift of the Holy Spirit.',
    "Acts 2:39": '39 Because this promise is directly for you, for your children, and for everyone far away—as many as the Lord our God will call.”'
}

# Pre-defined Operational Insights for chapters
PREDEFINED_INSIGHTS = {
    "Mark 11": "\n\n[Operational Insight: A double-minded heart forces a double-tongued confession. To doubt within the heart is to speak words of alignment one moment and words of destruction the next. Because the mouth prints exactly what is settled in the heart, an individual must eliminate the double-minded loop to ensure the words spoken with the mouth carry absolute execution power.]",
    "Isaiah 53": "\n\n[Operational Insight: The original Hebrew words used here—\"choliy\" and \"makob\"—literally mean physical sickness and physical pain. Jesus did not just die to take people to heaven; His scourging wounds were the exact, legal currency used to pay for physical health.]",
    "Matthew 8": "\n\n[Operational Insight: This verse is the legal proof. Jesus did not heal people just to prove He was God; He healed them to execute the eviction notice on sickness that Isaiah prophesied. He treated physical disease as something He was legally required to carry away from the human race.]",
    "1 Peter 2": "\n\n[Operational Insight: Look at the tense shift. Isaiah said \"we are healed\" (looking forward to the payment). Peter looks back at the whipping post and declares \"you were healed\" (past tense). It is a finished legal transaction. Healing is no longer something God is deciding to do; it is a historical fact that the believer must now enforce with the mouth.]",
    "Luke 10": "\n\n[Operational Insight: Traditional religion uses \"power\" for both sides, which causes believers to beg God for more strength to fight the enemy. But the text reveals a finished legal chain: you have the legal right (authority) and the enemy only has a defeated force (power). You do not pray for victory; you enforce the authority you have already been handed.]",
    "Acts 1": "\n\n[Operational Insight: The Greek word for power here is Dunamis—inherent, miraculous, explosive energy. Notice that Jesus does not say you will receive a new religion, a theological degree, or a passive emotion. He declares an objective, physical infusion of supernatural muscle. This supernatural power is given for a single mechanical purpose: to make you an unshakeable witness of the New Covenant administration across the globe.]",
    "Acts 2": "\n\n[Operational Insight: Notice the immediate shift in verse 38. Peter doesn't give them an abstract theological theory; he gives a direct, multi-step action plan. The archaic text used 'remission of sins' and 'Holy Ghost'—terms that distance modern readers. The SKJV downloads this straight into your present reality: forgiveness of sins and the gift of the Holy Spirit. Verse 39 explicitly locks you into the contract: this promise wasn't just for ancient Israel; it is addressed directly to you right now.]"
}

def rule_based_translate_text(text, book_name, chapter_num):
    """
    Offline fallback translator that uses regex and dictionary mappings
    to modernize KJV and strip out basic archaisms.
    """
    # Replace archaic words (simple mappings)
    replacements = {
        r'\bthee\b': 'you',
        r'\bthou\b': 'you',
        r'\bye\b': 'you',
        r'\bthy\b': 'your',
        r'\bthine\b': 'your',
        r'\bunto\b': 'to',
        r'\bhath\b': 'has',
        r'\bhast\b': 'have',
        r'\bdoth\b': 'does',
        r'\bdost\b': 'do',
        r'\bart\b': 'are',
        r'\bshalt\b': 'will',
        r'\bshall\b': 'will',
        r'\bwilt\b': 'will',
        r'\bwherefore\b': 'therefore',
        r'\blest\b': 'otherwise',
        r'\bHoly Ghost\b': 'Holy Spirit',
        r'\bcharity\b': 'love',
    }
    
    lines = text.split('\n')
    translated_lines = []
    
    for line in lines:
        match = re.match(r'^(\d+)\s+(.*)$', line)
        if match:
            v_num = match.group(1)
            v_text = match.group(2)
            
            # Check if this specific verse has a predefined translation
            norm_book_name = book_name
            if "Mark" in book_name:
                norm_book_name = "Mark"
            elif "Acts" in book_name:
                norm_book_name = "Acts"
            elif "Isaiah" in book_name:
                norm_book_name = "Isaiah"
            elif "Matthew" in book_name:
                norm_book_name = "Matthew"
            elif "Peter" in book_name:
                norm_book_name = "1 Peter"
            elif "Luke" in book_name:
                norm_book_name = "Luke"
                
            key = f"{norm_book_name} {chapter_num}:{v_num}"
            if key in PREDEFINED_VERSES:
                translated_lines.append(PREDEFINED_VERSES[key])
                continue
                
            # Apply rule-based replacements
            for pattern, replacement in replacements.items():
                v_text = re.sub(pattern, replacement, v_text, flags=re.IGNORECASE)
            
            # Replace common -eth / -est verb endings
            v_text = re.sub(r'\b(\w+)eth\b', r'\1s', v_text, flags=re.IGNORECASE)
            v_text = re.sub(r'\b(\w+)est\b', r'\1', v_text, flags=re.IGNORECASE)
            # Fix common verb replacements resulting from -eth mapping
            v_text = re.sub(r'\bsays\b', 'says', v_text)
            v_text = re.sub(r'\bdoess\b', 'does', v_text)
            v_text = re.sub(r'\bhavs\b', 'has', v_text)
            v_text = re.sub(r'\bgos\b', 'goes', v_text)
            
            translated_lines.append(f"{v_num} {v_text}")
        else:
            translated_lines.append(line)
            
    translated_text = '\n'.join(translated_lines)
    
    # Check for chapter-level insight
    norm_book_name = book_name
    if "Mark" in book_name:
        norm_book_name = "Mark"
    elif "Acts" in book_name:
        norm_book_name = "Acts"
    elif "Isaiah" in book_name:
        norm_book_name = "Isaiah"
    elif "Matthew" in book_name:
        norm_book_name = "Matthew"
    elif "Peter" in book_name:
        norm_book_name = "1 Peter"
    elif "Luke" in book_name:
        norm_book_name = "Luke"
        
    chap_key = f"{norm_book_name} {chapter_num}"
    if chap_key in PREDEFINED_INSIGHTS:
        translated_text += PREDEFINED_INSIGHTS[chap_key]
        
    return translated_text

def translate_via_api(text, book_name, chapter_num, api_key):
    """
    Translates KJV text to SKJV using the Google Gemini API.
    """
    try:
        import google.generativeai as genai
    except ImportError:
        print("google-generativeai module not found. Installing it first...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
        import google.generativeai as genai
        
    genai.configure(api_key=api_key)
    
    prompt = f"""You are an elite Biblical linguist and communications expert translating the New Testament from the public domain 1611 King James Version (KJV). Your target audience is modern, direct, action-oriented individuals who demand absolute clarity, precision, and zero religious fluff.

Strict Vocabulary & Formatting Parameters:
1. Eliminate All Archaisms: Completely banish words like "lo," "behold," "thee," "thou," "ye," "lest," "wherefore," and verbs ending in "-eth" or "-est."
2. Zero Third-Person Pronouns Rule: Systematically replace third-person pronouns (he, she, they, their, his, him) in instruction blocks with active, functional targets (that individual, the believer, the mouth, their mouth, those things) to make scriptures read as universal spiritual laws.
3. Covenant Terminology Mapping:
   - exousia -> "delegated authority" or "legal authority"
   - dunamis -> "supernatural power" or "miraculous power"
   - astheneia (infirmities) -> "sicknesses" and "diseases"
   - stripes -> "wounds" or "scourging wounds"
   - trespasses -> "sins"
   - grievance -> "a grudge"
   - Maintain key covenant terms like "good works" and "dead works" exactly as written. Do not change them.
4. Bold the Functional Directives: Whenever a verse outlines an explicit command, action step, or state of identity, bold the core words (e.g. **say to this mountain**, **do not doubt**, **believe you receive**).
5. Append Operational Insights: For chapters containing key covenant mechanisms (like faith commands, divine healing, or authority), append a brief, italicized `[Operational Insight]` explaining the legal/spiritual mechanism.
6. Absolute Copyright Safety: Ensure the final phrasing is completely original and does not clone modern copyrighted translations like the NKJV, while achieving peak modern clarity.

Translate the following KJV text for {book_name} Chapter {chapter_num} into the Simple King James Version (SKJV) according to these rules. Preserve the verse numbering at the start of each line:
{text}
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    
    # If the API succeeds, parse the response
    if response and response.text:
        return response.text.strip()
    else:
        raise Exception("Empty response from API")

def process_file(source_path, target_path, api_key=None):
    """
    Reads a KJV book file, splits it into chapters, translates each chapter,
    and writes it to the target file.
    """
    print(f"Processing source file: {source_path}")
    if not os.path.exists(source_path):
        print(f"Error: Source file does not exist: {source_path}")
        return False
        
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Get Book Name from filename or top header
    book_match = re.search(r'^#\s+(.*)$', content, re.MULTILINE)
    book_name = book_match.group(1).strip() if book_match else "Book"
    print(f"Book identified: {book_name}")
    
    # Split content by Chapter headers: ## [Book Name] Chapter [Number]
    # e.g., "## Ruth Chapter 1" or "## Mark Chapter 11"
    chapter_regex = r'(##\s+.*?Chapter\s+(\d+))'
    parts = re.split(chapter_regex, content)
    
    # parts format:
    # parts[0]: Text before Chapter 1 (e.g., "# Ruth")
    # Then triplets:
    # parts[i*3 + 1]: Header (e.g., "## Ruth Chapter 1")
    # parts[i*3 + 2]: Chapter Number (e.g., "1")
    # parts[i*3 + 3]: Chapter text content
    
    new_content_parts = []
    
    # Add main book title
    new_content_parts.append(f"# {book_name} - Simple King James Version (SKJV)\n")
    
    for i in range(len(parts) // 3):
        header = parts[i*3 + 1]
        chapter_num = parts[i*3 + 2]
        chapter_text = parts[i*3 + 3].strip()
        
        # Remove trailing "## eof" or similar from the last chapter if it is present
        chapter_text = re.sub(r'##\s+eof.*$', '', chapter_text, flags=re.IGNORECASE).strip()
        
        print(f"Translating {book_name} Chapter {chapter_num}...")
        
        translated_text = ""
        # Check if we should use the API
        if api_key:
            try:
                translated_text = translate_via_api(chapter_text, book_name, chapter_num, api_key)
            except Exception as e:
                print(f"API Translation failed: {e}. Falling back to rule-based offline translation.")
                translated_text = rule_based_translate_text(chapter_text, book_name, chapter_num)
        else:
            translated_text = rule_based_translate_text(chapter_text, book_name, chapter_num)
            
        new_content_parts.append(f"{header}\n\n{translated_text}\n")
        
    new_content_parts.append("\n## eof\n")
    
    # Write the target file
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_content_parts))
        
    print(f"Successfully wrote translated book to: {target_path}")
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Translate KJV Markdown Bible to Simple King James Version (SKJV)")
    parser.add_argument("--source", required=True, help="Path to source KJV file")
    parser.add_argument("--target", required=True, help="Path to output SKJV file")
    parser.add_argument("--api-key", default=os.environ.get("GEMINI_API_KEY"), help="Google Gemini API Key")
    
    args = parser.parse_args()
    success = process_file(args.source, args.target, args.api_key)
    sys.exit(0 if success else 1)
