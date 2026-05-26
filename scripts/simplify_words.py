#!/usr/bin/env python3
"""
BKJV Hard Word Simplifier
===========================
Replaces archaic, obscure, and unnecessarily difficult English words
across all 66 BKJV book files with simple, clear modern equivalents.
The "Based" King James Version must be instantly understandable.
"""
import os
import re

BOOKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "books"))

# ===========================================================================
# Hard word → simple word mapping
# Format: (regex_pattern, replacement, description)
# Ordered by category for clarity
# ===========================================================================
HARD_WORDS = [
    # --- Archaic connectors / conjunctions ---
    (r'\bAlbeit\b', 'Even though', 'albeit'),
    (r'\balbeit\b', 'even though', 'albeit'),
    (r'\bHowbeit\b', 'However', 'howbeit'),
    (r'\bhowbeit\b', 'however', 'howbeit'),
    (r'\bNotwithstanding\b', 'Nevertheless', 'notwithstanding'),
    (r'\bnotwithstanding\b', 'nevertheless', 'notwithstanding'),
    (r'\bForasmuch\b', 'Since', 'forasmuch'),
    (r'\bforasmuch\b', 'since', 'forasmuch'),
    (r'\bInasmuch\b', 'Since', 'inasmuch'),
    (r'\binasmuch\b', 'since', 'inasmuch'),
    (r'\bInsomuch\b', 'So much so', 'insomuch'),
    (r'\binsomuch\b', 'so much so', 'insomuch'),
    (r'\bPeradventure\b', 'Perhaps', 'peradventure'),
    (r'\bperadventure\b', 'perhaps', 'peradventure'),
    (r'\bSundry\b', 'Various', 'sundry'),
    (r'\bsundry\b', 'various', 'sundry'),

    # --- Archaic location / direction words ---
    (r'\bHither\b', 'Here', 'hither'),
    (r'\bhither\b', 'here', 'hither'),
    (r'\bThither\b', 'There', 'thither'),
    (r'\bthither\b', 'there', 'thither'),
    (r'\bWhither\b', 'Where', 'whither'),
    (r'\bwhither\b', 'where', 'whither'),
    (r'\bWhence\b', 'From where', 'whence'),
    (r'\bwhence\b', 'from where', 'whence'),
    (r'\bThence\b', 'From there', 'thence'),
    (r'\bthence\b', 'from there', 'thence'),
    (r'\bHitherto\b', 'Until now', 'hitherto'),
    (r'\bhitherto\b', 'until now', 'hitherto'),
    (r'\bHenceforth\b', 'From now on', 'henceforth'),
    (r'\bhenceforth\b', 'from now on', 'henceforth'),
    (r'\bThenceforth\b', 'From then on', 'thenceforth'),
    (r'\bthenceforth\b', 'from then on', 'thenceforth'),
    (r'\bNigh\b', 'Near', 'nigh'),
    (r'\bnigh\b', 'near', 'nigh'),

    # --- Archaic compound prepositions ---
    (r'\bTherein\b', 'In it', 'therein'),
    (r'\btherein\b', 'in it', 'therein'),
    (r'\bThereof\b', 'Of it', 'thereof'),
    (r'\bthereof\b', 'of it', 'thereof'),
    (r'\bTherewith\b', 'With it', 'therewith'),
    (r'\btherewith\b', 'with it', 'therewith'),
    (r'\bThereto\b', 'To it', 'thereto'),
    (r'\bthereto\b', 'to it', 'thereto'),
    (r'\bThereby\b', 'By that', 'thereby'),
    (r'\bthereby\b', 'by that', 'thereby'),
    (r'\bHerein\b', 'In this', 'herein'),
    (r'\bherein\b', 'in this', 'herein'),
    (r'\bWherein\b', 'In which', 'wherein'),
    (r'\bwherein\b', 'in which', 'wherein'),
    (r'\bWherewith\b', 'With what', 'wherewith'),
    (r'\bwherewith\b', 'with what', 'wherewith'),

    # --- Archaic time/manner words ---
    (r'\bStraightway\b', 'Immediately', 'straightway'),
    (r'\bstraightway\b', 'immediately', 'straightway'),
    (r'\bEventide\b', 'Evening', 'eventide'),
    (r'\beventide\b', 'evening', 'eventide'),

    # --- Archaic verbs ---
    (r'\bsmote\b', 'struck', 'smote'),
    (r'\bSmote\b', 'Struck', 'smote'),
    (r'\bwist\b', 'knew', 'wist'),
    (r'\bWist\b', 'Knew', 'wist'),
    (r'\bwaxed\b', 'grew', 'waxed'),
    (r'\bWaxed\b', 'Grew', 'waxed'),
    (r'\bhaply\b', 'perhaps', 'haply'),
    (r'\bHaply\b', 'Perhaps', 'haply'),
    (r'\bhearken\b', 'listen', 'hearken'),
    (r'\bHearken\b', 'Listen', 'hearken'),
    (r'\bhearkened\b', 'listened', 'hearkened'),
    (r'\bHearkened\b', 'Listened', 'hearkened'),

    # --- Archaic nouns ---
    (r'\bbrethren\b', 'brothers', 'brethren'),
    (r'\bBrethren\b', 'Brothers', 'brethren'),
    (r'\bdamsel\b', 'young woman', 'damsel'),
    (r'\bDamsel\b', 'Young woman', 'damsel'),
    (r'\braiment\b', 'clothing', 'raiment'),
    (r'\bRaiment\b', 'Clothing', 'raiment'),
    (r'\btwain\b', 'two', 'twain'),
    (r'\bTwain\b', 'Two', 'twain'),
    (r'\bsepulchres\b', 'tombs', 'sepulchres'),
    (r'\bSepulchres\b', 'Tombs', 'sepulchres'),
    (r'\bsepulchre\b', 'tomb', 'sepulchre'),
    (r'\bSepulchre\b', 'Tomb', 'sepulchre'),
    (r'\bbetwixt\b', 'between', 'betwixt'),
    (r'\bBetwixt\b', 'Between', 'betwixt'),
    (r'\basunder\b', 'apart', 'asunder'),
    (r'\bAsunder\b', 'Apart', 'asunder'),
    (r'\bensample\b', 'example', 'ensample'),
    (r'\bEnsamples?\b', 'Examples', 'ensample'),
    (r'\bprivily\b', 'secretly', 'privily'),
    (r'\bPrivily\b', 'Secretly', 'privily'),
    (r'\bespoused\b', 'engaged', 'espoused'),
    (r'\bEspoused\b', 'Engaged', 'espoused'),
    (r'\bgirdle\b', 'belt', 'girdle'),
    (r'\bGirdle\b', 'Belt', 'girdle'),
    (r'\bgainsaying\b', 'rebellion', 'gainsaying'),
    (r'\bGainsaying\b', 'Rebellion', 'gainsaying'),
    (r'\bvisage\b', 'face', 'visage'),
    (r'\bVisage\b', 'Face', 'visage'),
    (r'\btumult\b', 'uproar', 'tumult'),
    (r'\bTumult\b', 'Uproar', 'tumult'),
    (r'\bcomeliness\b', 'beauty', 'comeliness'),
    (r'\bComeliness\b', 'Beauty', 'comeliness'),
    (r'\bchamberlain\b', 'court official', 'chamberlain'),
    (r'\bChamberlain\b', 'Court official', 'chamberlain'),

    # --- "Verily" → "Truly" (112 instances, mostly Jesus speaking) ---
    (r'\bVerily\b', 'Truly', 'verily'),
    (r'\bverily\b', 'truly', 'verily'),

    # --- "Begat" → "fathered" / "was the father of" ---
    (r'\bbegat\b', 'fathered', 'begat'),
    (r'\bBegat\b', 'Fathered', 'begat'),

    # --- "Wroth" → "furious" / "angry" ---
    (r'\bwroth\b', 'furious', 'wroth'),
    (r'\bWroth\b', 'Furious', 'wroth'),

    # --- "Charger" (a platter, not a horse) ---
    (r'\bcharger\b', 'platter', 'charger'),
    (r'\bCharger\b', 'Platter', 'charger'),

    # --- "Abode" → "stayed" ---
    (r'\babode\b', 'stayed', 'abode'),
    (r'\bAbode\b', 'Stayed', 'abode'),

    # --- "Supplications" → "prayers" ---
    (r'\bsupplications\b', 'prayers', 'supplications'),
    (r'\bSupplications\b', 'Prayers', 'supplications'),
    (r'\bsupplication\b', 'prayer', 'supplication'),
    (r'\bSupplication\b', 'Prayer', 'supplication'),

    # --- "Concupiscence" → "sinful desire" ---
    (r'\bconcupiscence\b', 'sinful desire', 'concupiscence'),
    (r'\bConcupiscence\b', 'Sinful desire', 'concupiscence'),

    # --- "Bowels" (used to mean compassion/gut feelings) → "compassion" / "deep feelings" ---
    # Be careful: sometimes literal (2 Sam 20:10). We do a basic replacement.
    (r'\bbowels of mercies\b', 'tender compassion', 'bowels'),
    (r'\bbowels of compassion\b', 'deep compassion', 'bowels'),
    (r'\bmy bowels\b', 'my heart', 'bowels'),
    (r'\bhis bowels\b', 'his insides', 'bowels'),

    # --- "Peculiar" (KJV means "treasured" or "special", not "weird") ---
    (r'\bpeculiar people\b', 'treasured people', 'peculiar'),
    (r'\bpeculiar treasure\b', 'special treasure', 'peculiar'),
    (r'\bpeculiar\b', 'special', 'peculiar'),

    # --- "Husbandman" → "farmer" ---
    (r'\bhusbandman\b', 'farmer', 'husbandman'),
    (r'\bHusbandman\b', 'Farmer', 'husbandman'),
    (r'\bhusbandmen\b', 'farmers', 'husbandmen'),
    (r'\bHusbandmen\b', 'Farmers', 'husbandmen'),

    # --- "Chastise/chastisement" → "discipline/punishment" ---
    (r'\bchastisement\b', 'punishment', 'chastisement'),
    (r'\bChastisement\b', 'Punishment', 'chastisement'),
    (r'\bchastised?\b', 'discipline', 'chastise'),
    (r'\bChastised?\b', 'Discipline', 'chastise'),

    # --- "Reprove" → "correct" ---
    (r'\breprove\b', 'correct', 'reprove'),
    (r'\bReprove\b', 'Correct', 'reprove'),
    (r'\breproved\b', 'corrected', 'reproved'),
    (r'\bReproved\b', 'Corrected', 'reproved'),

    # --- "Recompense" → "repay" / "reward" ---
    (r'\brecompense\b', 'repay', 'recompense'),
    (r'\bRecompense\b', 'Repay', 'recompense'),

    # --- "Abhor" → "despise" / "hate" ---
    (r'\babhor\b', 'despise', 'abhor'),
    (r'\bAbhor\b', 'Despise', 'abhor'),
    (r'\babhorred\b', 'despised', 'abhorred'),
    (r'\bAbhorred\b', 'Despised', 'abhorred'),

    # --- "Molten" → "melted" ---
    (r'\bmolten\b', 'melted', 'molten'),
    (r'\bMolten\b', 'Melted', 'molten'),
]


def process_file(filepath):
    """Apply all hard-word simplifications to one file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    original = text
    fix_counts = {}

    for pattern, replacement, name in HARD_WORDS:
        hits = len(re.findall(pattern, text))
        if hits > 0:
            text = re.sub(pattern, replacement, text)
            fix_counts[name] = fix_counts.get(name, 0) + hits

    if text != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

    return fix_counts


def main():
    print("=" * 60)
    print("BKJV Hard Word Simplifier")
    print("=" * 60)

    total_fixes = 0
    files_changed = 0
    grand_counts = {}

    book_files = sorted([f for f in os.listdir(BOOKS_DIR) if f.endswith('.md')])

    for filename in book_files:
        filepath = os.path.join(BOOKS_DIR, filename)
        counts = process_file(filepath)
        file_total = sum(counts.values())

        if file_total > 0:
            print(f"  🔧 {filename}: {file_total} simplifications")
            files_changed += 1
            total_fixes += file_total
            for word, cnt in counts.items():
                grand_counts[word] = grand_counts.get(word, 0) + cnt
        else:
            print(f"  ✅ {filename}: clean")

    print(f"\n{'=' * 60}")
    print(f"SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Total simplifications: {total_fixes}")
    print(f"  Files modified:        {files_changed}")
    print(f"\n  Top replacements:")
    for word, cnt in sorted(grand_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"    {word}: {cnt}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
