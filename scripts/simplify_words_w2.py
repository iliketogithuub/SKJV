#!/usr/bin/env python3
"""
SKJV Hard Word Simplifier - Wave 2
====================================
Second pass catching more hard words discovered after wave 1.
"""
import os
import re

BOOKS_DIR = "/home/charlie/Desktop/Websites/SKJV/books"

HARD_WORDS_W2 = [
    # --- Archaic verbs ---
    (r'\bbeseech\b', 'urge', 'beseech'),
    (r'\bBeseech\b', 'Urge', 'beseech'),
    (r'\bbesought\b', 'urged', 'besought'),
    (r'\bBesought\b', 'Urged', 'besought'),
    (r'\benjoin\b', 'require', 'enjoin'),
    (r'\bEnjoin\b', 'Require', 'enjoin'),
    (r'\bwithal\b', 'also', 'withal'),
    (r'\bWithal\b', 'Also', 'withal'),
    (r'\bentreat\b', 'plead with', 'entreat'),
    (r'\bEntreat\b', 'Plead with', 'entreat'),

    # --- Archaic adjectives ---
    (r'\bfroward\b', 'stubborn', 'froward'),
    (r'\bFroward\b', 'Stubborn', 'froward'),
    (r'\bdivers\b', 'various', 'divers'),
    (r'\bDivers\b', 'Various', 'divers'),

    # --- Archaic nouns/phrases ---
    (r'\bfellowlabourer\b', 'co-worker', 'fellowlabourer'),
    (r'\bfellowlabourers\b', 'co-workers', 'fellowlabourers'),
    (r'\bfellowsoldier\b', 'fellow soldier', 'fellowsoldier'),
    (r'\bfellowprisoner\b', 'fellow prisoner', 'fellowprisoner'),
    (r'\bfellowprisoners\b', 'fellow prisoners', 'fellowprisoners'),
    (r'\bFellowlabourer\b', 'Co-worker', 'fellowlabourer'),
    (r'\bFellowlabourers\b', 'Co-workers', 'fellowlabourers'),
    (r'\bFellowsoldier\b', 'Fellow soldier', 'fellowsoldier'),
    (r'\bFellowprisoner\b', 'Fellow prisoner', 'fellowprisoner'),
    (r'\bbishoprick\b', 'position of leadership', 'bishoprick'),
    (r'\bBishoprick\b', 'Position of leadership', 'bishoprick'),
    (r'\bdissimulation\b', 'hypocrisy', 'dissimulation'),
    (r'\bDissimulation\b', 'Hypocrisy', 'dissimulation'),
    (r'\bsoothsayer\b', 'fortune-teller', 'soothsayer'),
    (r'\bSoothsayer\b', 'Fortune-teller', 'soothsayer'),
    (r'\bsoothsayers\b', 'fortune-tellers', 'soothsayers'),
    (r'\bcircumspect\b', 'careful', 'circumspect'),
    (r'\bCircumspect\b', 'Careful', 'circumspect'),
    (r'\bdispensation\b', 'administration', 'dispensation'),
    (r'\bDispensation\b', 'Administration', 'dispensation'),

    # --- "Hereafter" / "hereunto" ---
    (r'\bhereafter\b', 'from now on', 'hereafter'),
    (r'\bHereafter\b', 'From now on', 'hereafter'),
    (r'\bhereunto\b', 'for this purpose', 'hereunto'),
    (r'\bHereunto\b', 'For this purpose', 'hereunto'),

    # --- "Salute" (KJV meaning = greet) ---
    (r'\bsalute\b', 'greet', 'salute'),
    (r'\bSalute\b', 'Greet', 'salute'),
    (r'\bsaluted\b', 'greeted', 'saluted'),
    (r'\bSaluted\b', 'Greeted', 'saluted'),
    (r'\bsalutations\b', 'greetings', 'salutations'),
    (r'\bSalutations\b', 'Greetings', 'salutations'),
    (r'\bsalutation\b', 'greeting', 'salutation'),
    (r'\bSalutation\b', 'Greeting', 'salutation'),

    # --- "Effectual" → "powerful" / "effective" ---
    (r'\beffectual\b', 'effective', 'effectual'),
    (r'\bEffectual\b', 'Effective', 'effectual'),

    # --- "Consolation" → "comfort" / "encouragement" ---
    (r'\bconsolation\b', 'comfort', 'consolation'),
    (r'\bConsolation\b', 'Comfort', 'consolation'),

    # --- "Propitiation" → "atoning sacrifice" ---
    (r'\bpropitiation\b', 'atoning sacrifice', 'propitiation'),
    (r'\bPropitiation\b', 'Atoning sacrifice', 'propitiation'),

    # --- "Tribulation" → "suffering" / "hardship" ---
    (r'\btribulation\b', 'suffering', 'tribulation'),
    (r'\bTribulation\b', 'Suffering', 'tribulation'),
    (r'\btribulations\b', 'sufferings', 'tribulations'),
    (r'\bTribulations\b', 'Sufferings', 'tribulations'),

    # --- "Condemnation" → "judgment" ---
    (r'\bcondemnation\b', 'judgment', 'condemnation'),
    (r'\bCondemnation\b', 'Judgment', 'condemnation'),

    # --- "Transgression" → "sin" / "violation" ---
    (r'\btransgressions\b', 'sins', 'transgressions'),
    (r'\bTransgressions\b', 'Sins', 'transgressions'),
    (r'\btransgression\b', 'sin', 'transgression'),
    (r'\bTransgression\b', 'Sin', 'transgression'),
    (r'\btransgressed\b', 'sinned', 'transgressed'),
    (r'\bTransgressed\b', 'Sinned', 'transgressed'),
    (r'\btransgressors\b', 'sinners', 'transgressors'),
    (r'\bTransgressors\b', 'Sinners', 'transgressors'),

    # --- "Provocation" → "rebellion" / "defiance" ---
    (r'\bprovocation\b', 'rebellion', 'provocation'),
    (r'\bProvocation\b', 'Rebellion', 'provocation'),

    # --- "Impute/imputed" → "credit/credited" ---
    (r'\bimputed\b', 'credited', 'imputed'),
    (r'\bImputed\b', 'Credited', 'imputed'),
    (r'\bimpute\b', 'credit', 'impute'),
    (r'\bImpute\b', 'Credit', 'impute'),

    # --- "Exhort" → "encourage" / "urge" ---
    (r'\bexhort\b', 'encourage', 'exhort'),
    (r'\bExhort\b', 'Encourage', 'exhort'),
    (r'\bexhorted\b', 'encouraged', 'exhorted'),
    (r'\bExhorted\b', 'Encouraged', 'exhorted'),
    (r'\bexhortation\b', 'encouragement', 'exhortation'),
    (r'\bExhortation\b', 'Encouragement', 'exhortation'),
    (r'\bexhorting\b', 'encouraging', 'exhorting'),
    (r'\bExhorting\b', 'Encouraging', 'exhorting'),

    # --- "Remission" → "forgiveness" ---
    (r'\bremission\b', 'forgiveness', 'remission'),
    (r'\bRemission\b', 'Forgiveness', 'remission'),

    # --- Fix "bowels" that survived wave 1 ---
    (r'\bbowels\b', 'deep affection', 'bowels'),
    (r'\bBowels\b', 'Deep affection', 'bowels'),

    # --- Fix double ## eof markers ---
]


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    original = text
    fix_counts = {}

    for pattern, replacement, name in HARD_WORDS_W2:
        hits = len(re.findall(pattern, text))
        if hits > 0:
            text = re.sub(pattern, replacement, text)
            fix_counts[name] = fix_counts.get(name, 0) + hits

    # Fix double ## eof
    text = re.sub(r'(## eof\s*){2,}', '## eof\n', text)

    if text != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
    return fix_counts


def main():
    print("=" * 60)
    print("SKJV Hard Word Simplifier — Wave 2")
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
    print(f"WAVE 2 SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Total simplifications: {total_fixes}")
    print(f"  Files modified:        {files_changed}")
    print(f"\n  Top replacements:")
    for word, cnt in sorted(grand_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"    {word}: {cnt}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
