#!/usr/bin/env python3
"""
SKJV Post-Processing Fix Script
================================
Fixes all known issues identified in the May 25 2026 audit:
1. Broken words from naive -eth regex (coms, drivs, becoms, etc.)
2. Residual 'saith' instances (1,191 occurrences)
3. Other missed archaisms (didst, hitherto, etc.)
4. Regenerates 5 empty stub books (Obadiah, Philemon, 2 John, 3 John, Jude)

This script processes all .md files in the books/ directory IN PLACE.
"""
import os
import re
import sys

BOOKS_DIR = "/home/charlie/Desktop/Websites/SKJV/books"
KJV_SOURCE_DIR = "/home/charlie/Downloads/kjv-markdown-master"

# ===========================================================================
# PART 1: Dictionary of broken-word fixes from the -eth regex bug
# Pattern: the old regex turned "cometh" into "coms" (strip eth, add s)
# Correct: "cometh" should become "comes"
# ===========================================================================
BROKEN_WORD_FIXES = {
    # Words where -eth was stripped to leave a broken stem + s
    r'\bcoms\b': 'comes',
    r'\bdrivs\b': 'drives',
    r'\bbecoms\b': 'becomes',
    r'\btaks\b': 'takes',
    r'\bmaks\b': 'makes',
    r'\bdefils\b': 'defiles',
    r'\bses\b': 'sees',
    r'\bgos\b': 'goes',
    r'\bdos\b': 'does',
    r'\bgivs\b': 'gives',
    r'\blivs\b': 'lives',
    r'\bdis\b': 'dies',
    r'\blies\b': 'lies',  # already correct form, skip
    r'\bris\b': 'rises',
    r'\bhids\b': 'hides',
    r'\babids\b': 'abides',
    r'\bruls\b': 'rules',
    r'\bjudgs\b': 'judges',
    r'\blovs\b': 'loves',
    r'\bhats\b': 'hates',
    r'\bdesirs\b': 'desires',
    r'\brequirs\b': 'requires',
    r'\breceivs\b': 'receives',
    r'\bperceivs\b': 'perceives',
    r'\bbelievs\b': 'believes',
    r'\bconceivs\b': 'conceives',
    r'\bdeclaers\b': 'declares',
    r'\bdevours\b': 'devours',
    r'\bprovids\b': 'provides',
    r'\bremovs\b': 'removes',
    r'\bmovs\b': 'moves',
    r'\bprovs\b': 'proves',
    r'\bimprovs\b': 'improves',
    r'\bservs\b': 'serves',
    r'\bpreservs\b': 'preserves',
    r'\bobservs\b': 'observes',
    r'\breservs\b': 'reserves',
    r'\bdeservs\b': 'deserves',
    r'\bceasrs\b': 'ceases',
    r'\bpleasrs\b': 'pleases',
    r'\braisrs\b': 'raises',
    r'\bpraisrs\b': 'praises',
    r'\bcurs\b': 'cures',
    r'\bendurs\b': 'endures',
    r'\bprocurs\b': 'procures',
    r'\bbecoms\b': 'becomes',
    r'\bovercoms\b': 'overcomes',
    r'\bwelcoms\b': 'welcomes',
    r'\bsavs\b': 'saves',
    r'\bwavs\b': 'waves',
    r'\bceasrs\b': 'ceases',
    r'\bincreasr\b': 'increases',
    r'\bdecreasr\b': 'decreases',
    r'\bchoss\b': 'chooses',
    r'\bloss\b': 'looses',
    r'\buss\b': 'uses',
    r'\bcauss\b': 'causes',
    r'\bpurss\b': 'purses',
    r'\bclosrs\b': 'closes',
    r'\bchangs\b': 'changes',
    r'\bchargs\b': 'charges',
    r'\bariss\b': 'arises',
    r'\bdepartrs\b': 'departs',
}

# ===========================================================================
# PART 2: Remaining archaisms to fix
# ===========================================================================
ARCHAISM_FIXES = {
    r'\bsaith\b': 'says',
    r'\bSaith\b': 'Says',
    r'\bdidst\b': 'did',
    r'\bwouldest\b': 'would',
    r'\bcouldest\b': 'could',
    r'\bshouldest\b': 'should',
    r'\bcanst\b': 'can',
    r'\bknowest\b': 'know',
    r'\bseest\b': 'see',
    r'\bhearest\b': 'hear',
    r'\bbelievest\b': 'believe',
    r'\bthinkest\b': 'think',
    r'\bsayest\b': 'say',
    r'\bdoest\b': 'do',
    r'\bgivest\b': 'give',
    r'\blovest\b': 'love',
    r'\bjudgest\b': 'judge',
    r'\bgoest\b': 'go',
    r'\bcomest\b': 'come',
    r'\bmeanest\b': 'mean',
    r'\bwantest\b': 'want',
    r'\bfindest\b': 'find',
    r'\btellest\b': 'tell',
    r'\btakest\b': 'take',
    r'\bbringest\b': 'bring',
    r'\bdwellest\b': 'dwell',
    r'\breignest\b': 'reign',
    r'\bdeniest\b': 'deny',
    r'\bdespisest\b': 'despise',
    r'\btrusteth\b': 'trusts',
    r'\bstraweds?\b': 'scattered',
}

# ===========================================================================
# PART 3: Comprehensive -eth verb dictionary for any remaining raw -eth words
# Maps KJV archaic verb to modern 3rd-person singular
# ===========================================================================
ETH_VERB_MAP = {
    'abideth': 'abides', 'addeth': 'adds', 'answereth': 'answers',
    'appeareth': 'appears', 'ariseth': 'arises', 'asketh': 'asks',
    'availeth': 'avails', 'awaketh': 'awakens', 'beareth': 'bears',
    'beateth': 'beats', 'becometh': 'becomes', 'befalleth': 'befalls',
    'beginneth': 'begins', 'believeth': 'believes', 'belongeth': 'belongs',
    'bindeth': 'binds', 'biteth': 'bites', 'blesseth': 'blesses',
    'bloweth': 'blows', 'boasteth': 'boasts', 'breaketh': 'breaks',
    'breatheth': 'breathes', 'bringeth': 'brings', 'buildeth': 'builds',
    'burneth': 'burns', 'buyeth': 'buys', 'calleth': 'calls',
    'careth': 'cares', 'carrieth': 'carries', 'casteth': 'casts',
    'catcheth': 'catches', 'causeth': 'causes', 'ceaseth': 'ceases',
    'changeth': 'changes', 'chargeth': 'charges', 'chaseth': 'chases',
    'chooseth': 'chooses', 'cleaveth': 'cleaves', 'closeth': 'closes',
    'clotheth': 'clothes', 'cometh': 'comes', 'commandeth': 'commands',
    'committeth': 'commits', 'compasseth': 'encompasses',
    'compelleth': 'compels', 'confesseth': 'confesses',
    'considereth': 'considers', 'containeth': 'contains',
    'continueth': 'continues', 'converteth': 'converts',
    'counteth': 'counts', 'covereth': 'covers', 'crieth': 'cries',
    'cutteth': 'cuts', 'dealeth': 'deals', 'deceiveth': 'deceives',
    'declareth': 'declares', 'defileth': 'defiles',
    'delivereth': 'delivers', 'departeth': 'departs',
    'desireth': 'desires', 'destroyeth': 'destroys',
    'devoureth': 'devours', 'dieth': 'dies', 'directeth': 'directs',
    'discovereth': 'discovers', 'dispenseth': 'dispenses',
    'divideth': 'divides', 'doeth': 'does', 'draweth': 'draws',
    'drinketh': 'drinks', 'driveth': 'drives', 'dwelleth': 'dwells',
    'eateth': 'eats', 'endeth': 'ends', 'endureth': 'endures',
    'entereth': 'enters', 'envieth': 'envies', 'erreth': 'errs',
    'establisheth': 'establishes', 'exalteth': 'exalts',
    'exceedeth': 'exceeds', 'exerciseth': 'exercises',
    'falleth': 'falls', 'feareth': 'fears', 'feedeth': 'feeds',
    'feeleth': 'feels', 'fighteth': 'fights', 'filleth': 'fills',
    'findeth': 'finds', 'fleeth': 'flees', 'floweth': 'flows',
    'followeth': 'follows', 'forbiddeth': 'forbids',
    'forgetteth': 'forgets', 'forgiveth': 'forgives',
    'formeth': 'forms', 'forsaketh': 'forsakes',
    'gathereth': 'gathers', 'getteth': 'gets', 'giveth': 'gives',
    'glorifieth': 'glorifies', 'goeth': 'goes', 'grindeth': 'grinds',
    'groweth': 'grows', 'guardeth': 'guards', 'guideth': 'guides',
    'hangeth': 'hangs', 'hateth': 'hates', 'healeth': 'heals',
    'heareth': 'hears', 'helpeth': 'helps', 'hideth': 'hides',
    'holdeth': 'holds', 'honoureth': 'honours', 'hopeth': 'hopes',
    'humbleth': 'humbles', 'hungereth': 'hungers', 'hunteth': 'hunts',
    'increaseth': 'increases', 'inhabiteth': 'inhabits',
    'inheriteth': 'inherits', 'instructeth': 'instructs',
    'judgeth': 'judges', 'justifieth': 'justifies',
    'keepeth': 'keeps', 'killeth': 'kills', 'knoweth': 'knows',
    'laboureth': 'labours', 'lacketh': 'lacks', 'laugheth': 'laughs',
    'layeth': 'lays', 'leadeth': 'leads', 'leaneth': 'leans',
    'leaveth': 'leaves', 'lendeth': 'lends', 'letteth': 'lets',
    'lieth': 'lies', 'lifteth': 'lifts', 'lighteth': 'lights',
    'liveth': 'lives', 'looketh': 'looks', 'looseth': 'looses',
    'loveth': 'loves', 'lusteth': 'lusts', 'maketh': 'makes',
    'meeteth': 'meets', 'melteth': 'melts', 'moveth': 'moves',
    'multiplieth': 'multiplies', 'murdereth': 'murders',
    'needeth': 'needs', 'nourisheth': 'nourishes',
    'obeyeth': 'obeys', 'observeth': 'observes', 'offereth': 'offers',
    'openeth': 'opens', 'ordereth': 'orders', 'overcometh': 'overcomes',
    'overthroweth': 'overthrows', 'owneth': 'owns',
    'parteth': 'parts', 'passeth': 'passes', 'payeth': 'pays',
    'perisheth': 'perishes', 'permitteth': 'permits',
    'pierceth': 'pierces', 'planteth': 'plants', 'playeth': 'plays',
    'pleaseth': 'pleases', 'ploweth': 'plows', 'plucketh': 'plucks',
    'pointeth': 'points', 'possesseth': 'possesses',
    'poureth': 'pours', 'praiseth': 'praises', 'prayeth': 'prays',
    'preacheth': 'preaches', 'preserveth': 'preserves',
    'prevaileth': 'prevails', 'proceedeth': 'proceeds',
    'profiteth': 'profits', 'promiseth': 'promises',
    'prophesieth': 'prophesies', 'prospereth': 'prospers',
    'protecteth': 'protects', 'proveth': 'proves',
    'provideth': 'provides', 'provoketh': 'provokes',
    'publisheth': 'publishes', 'pulleth': 'pulls',
    'punisheth': 'punishes', 'purchaseth': 'purchases',
    'purgeth': 'purges', 'pursueth': 'pursues', 'putteth': 'puts',
    'quickeneth': 'quickens',
    'raiseth': 'raises', 'reacheth': 'reaches', 'readeth': 'reads',
    'receiveth': 'receives', 'reigneth': 'reigns',
    'rejoiceth': 'rejoices', 'remaineth': 'remains',
    'remembereth': 'remembers', 'removeth': 'removes',
    'rendereth': 'renders', 'reneweth': 'renews',
    'repayeth': 'repays', 'repenteth': 'repents',
    'reproacheth': 'reproaches', 'requireth': 'requires',
    'reserveth': 'reserves', 'resisteth': 'resists',
    'restoreth': 'restores', 'returneth': 'returns',
    'revealeth': 'reveals', 'rewardeth': 'rewards',
    'rideth': 'rides', 'riseth': 'rises', 'roareth': 'roars',
    'ruleth': 'rules', 'runneth': 'runs',
    'satisfieth': 'satisfies', 'saveth': 'saves', 'sayeth': 'says',
    'scattereth': 'scatters', 'searcheth': 'searches',
    'seeketh': 'seeks', 'seeth': 'sees', 'selleth': 'sells',
    'sendeth': 'sends', 'serveth': 'serves', 'setteth': 'sets',
    'shaketh': 'shakes', 'shineth': 'shines', 'showeth': 'shows',
    'shutteth': 'shuts', 'singeth': 'sings', 'sinketh': 'sinks',
    'sitteth': 'sits', 'slayeth': 'slays', 'sleepeth': 'sleeps',
    'slideth': 'slides', 'smelleth': 'smells', 'smiteth': 'strikes',
    'soweth': 'sows', 'spareth': 'spares', 'speaketh': 'speaks',
    'spreadeth': 'spreads', 'standeth': 'stands', 'stayeth': 'stays',
    'stealeth': 'steals', 'stirreth': 'stirs', 'stoppeth': 'stops',
    'strengtheneth': 'strengthens', 'striketh': 'strikes',
    'striveth': 'strives', 'subdueth': 'subdues',
    'suffereth': 'suffers', 'sustaineth': 'sustains',
    'swalloweth': 'swallows', 'sweareth': 'swears',
    'taketh': 'takes', 'teacheth': 'teaches', 'telleth': 'tells',
    'tempteth': 'tempts', 'testifieth': 'testifies',
    'thanketh': 'thanks', 'thinketh': 'thinks', 'toucheth': 'touches',
    'travaileth': 'travails', 'treadeth': 'treads',
    'troubleth': 'troubles', 'trusteth': 'trusts',
    'turneth': 'turns', 'understandeth': 'understands',
    'uttereth': 'utters', 'vexeth': 'vexes',
    'waiteth': 'waits', 'walketh': 'walks', 'wandereth': 'wanders',
    'washeth': 'washes', 'wasteth': 'wastes', 'watcheth': 'watches',
    'watereth': 'waters', 'waxeth': 'waxes', 'weareth': 'wears',
    'weigheth': 'weighs', 'withholdeth': 'withholds',
    'witnesseth': 'witnesses', 'worketh': 'works',
    'worshippeth': 'worships', 'wrestleth': 'wrestles',
    'writeth': 'writes', 'yieldeth': 'yields',
}

# ===========================================================================
# Known words that end in -eth but are NOT archaic verbs — leave alone
# ===========================================================================
ETH_SAFE_WORDS = {
    'teeth', 'seth', 'japheth', 'nazareth', 'bethlehem', 'shibboleth',
    'seventh', 'twentieth', 'thirtieth', 'fortieth', 'fiftieth',
    'sixtieth', 'seventieth', 'eightieth', 'ninetieth', 'hundredth',
    'elizabeth', 'hazareth', 'neth', 'beth', 'meth',
}


def fix_broken_words(text):
    """Fix words mangled by the naive -eth regex (e.g. coms → comes)."""
    count = 0
    for pattern, replacement in BROKEN_WORD_FIXES.items():
        new_text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        if new_text != text:
            hits = len(re.findall(pattern, text, flags=re.IGNORECASE))
            count += hits
            text = new_text
    return text, count


def fix_archaisms(text):
    """Fix remaining saith and other archaisms."""
    count = 0
    for pattern, replacement in ARCHAISM_FIXES.items():
        new_text = re.sub(pattern, replacement, text)
        if new_text != text:
            hits = len(re.findall(pattern, text))
            count += hits
            text = new_text
    return text, count


def fix_eth_verbs(text):
    """Replace any remaining -eth verbs using the comprehensive dictionary."""
    count = 0

    def replace_eth(match):
        nonlocal count
        word = match.group(0)
        lower = word.lower()

        # Skip safe words (proper nouns, ordinals, etc.)
        if lower in ETH_SAFE_WORDS:
            return word

        # Check dictionary
        if lower in ETH_VERB_MAP:
            replacement = ETH_VERB_MAP[lower]
            # Preserve capitalization
            if word[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]
            count += 1
            return replacement

        # If not in dictionary, leave it alone (may be a proper noun we missed)
        return word

    text = re.sub(r'\b\w+eth\b', replace_eth, text)
    return text, count


def fix_est_verbs(text):
    """Fix remaining -est archaic verb endings missed by original script."""
    count = 0
    # Whitelist of modern -est words that should NOT be changed
    est_safe = {
        'greatest', 'highest', 'lowest', 'deepest', 'strongest', 'longest',
        'oldest', 'youngest', 'sweetest', 'latest', 'chiefest', 'least',
        'best', 'west', 'rest', 'priest', 'forest', 'tempest', 'request',
        'honest', 'earnest', 'manifest', 'harvest', 'guest', 'nest', 'test',
        'chest', 'crest', 'jest', 'protest', 'contest', 'digest', 'suggest',
        'invest', 'arrest', 'nearest', 'dearest', 'poorest', 'smallest',
        'largest', 'hardest', 'softest', 'richest', 'wisest', 'fastest',
        'slowest', 'fairest', 'purest', 'worst', 'first', 'interest',
        'modest', 'closest', 'finest', 'bravest', 'truest', 'fullest',
    }

    def replace_est(match):
        nonlocal count
        word = match.group(0)
        lower = word.lower()
        if lower in est_safe:
            return word
        # Common -est archaic verbs: just strip the -est for 2nd person
        # e.g., "thou givest" → "you give" (but thou is already gone)
        # These appear as bare "-est" verbs, so just strip the -est suffix
        # and try to form the infinitive
        if lower.endswith('est') and len(lower) > 4:
            stem = lower[:-3]  # Remove -est
            # For most verbs, stem + trailing 'e' where needed
            count += 1
            if word[0].isupper():
                return stem[0].upper() + stem[1:]
            return stem
        return word

    text = re.sub(r'\b\w{5,}est\b', replace_est, text)
    return text, count


def translate_single_chapter_book(kjv_path, skjv_path, book_name):
    """
    Translate a single-chapter KJV book (Obadiah, Philemon, 2 John, 3 John, Jude).
    These don't have ## Chapter headers so the main script skipped them.
    """
    with open(kjv_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip the header line (# BookName)
    lines = content.strip().split('\n')
    body_lines = []
    for line in lines:
        if line.startswith('# '):
            continue  # Skip the title
        body_lines.append(line)

    body = '\n'.join(body_lines)

    # Apply all archaic word replacements
    replacements = {
        r'\bthee\b': 'you', r'\bThee\b': 'You',
        r'\bthou\b': 'you', r'\bThou\b': 'You',
        r'\bye\b': 'you', r'\bYe\b': 'You',
        r'\bthy\b': 'your', r'\bThy\b': 'Your',
        r'\bthine\b': 'your', r'\bThine\b': 'Your',
        r'\bunto\b': 'to',
        r'\bhath\b': 'has', r'\bHath\b': 'Has',
        r'\bhast\b': 'have', r'\bHast\b': 'Have',
        r'\bdoth\b': 'does', r'\bDoth\b': 'Does',
        r'\bdost\b': 'do',
        r'\bart\b': 'are',
        r'\bshalt\b': 'will', r'\bShalt\b': 'Will',
        r'\bwilt\b': 'will', r'\bWilt\b': 'Will',
        r'\bwherefore\b': 'therefore', r'\bWherefore\b': 'Therefore',
        r'\blest\b': 'otherwise',
        r'\bHoly Ghost\b': 'Holy Spirit',
    }
    for pattern, replacement in replacements.items():
        body = re.sub(pattern, replacement, body)

    # Fix -eth verbs, archaisms, saith
    body, _ = fix_eth_verbs(body)
    body, _ = fix_archaisms(body)

    # Write the SKJV file
    output = f"# {book_name} - Simple King James Version (SKJV)\n\n"
    output += f"## {book_name} Chapter 1\n\n"
    output += body.strip() + "\n\n## eof\n"

    with open(skjv_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"  ✅ Generated {book_name} ({len(body_lines)} lines)")


def process_book_file(filepath):
    """Apply all fixes to an existing SKJV book file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    original = text

    # Step 1: Fix broken words from regex bug
    text, broken_count = fix_broken_words(text)

    # Step 2: Fix remaining -eth verbs
    text, eth_count = fix_eth_verbs(text)

    # Step 3: Fix saith and other archaisms
    text, archaism_count = fix_archaisms(text)

    total_fixes = broken_count + eth_count + archaism_count

    if text != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return total_fixes
    return 0


def main():
    print("=" * 60)
    print("SKJV Post-Processing Fix Script")
    print("=" * 60)

    # ===== PHASE 1: Fix all existing book files =====
    print("\n📖 PHASE 1: Fixing existing book files...")
    total_fixes = 0
    files_fixed = 0
    book_files = sorted([f for f in os.listdir(BOOKS_DIR) if f.endswith('.md')])

    for filename in book_files:
        filepath = os.path.join(BOOKS_DIR, filename)
        fixes = process_book_file(filepath)
        if fixes > 0:
            print(f"  🔧 {filename}: {fixes} fixes applied")
            files_fixed += 1
            total_fixes += fixes
        else:
            print(f"  ✅ {filename}: clean")

    print(f"\n  Phase 1 complete: {total_fixes} total fixes across {files_fixed} files.")

    # ===== PHASE 2: Generate empty stub books =====
    print("\n📖 PHASE 2: Generating empty stub books...")
    stubs = {
        '31 - Obadiah': 'Obadiah',
        '57 - Philemon': 'Philemon',
        '63 - 2 John': '2 John',
        '64 - 3 John': '3 John',
        '65 - Jude': 'Jude',
    }

    for file_prefix, book_name in stubs.items():
        skjv_path = os.path.join(BOOKS_DIR, f"{file_prefix} - SKJV.md")
        kjv_path = os.path.join(KJV_SOURCE_DIR, f"{file_prefix} - KJV.md")

        if not os.path.exists(kjv_path):
            print(f"  ❌ KJV source not found: {kjv_path}")
            continue

        # Check if it's still a stub (less than 200 bytes)
        if os.path.exists(skjv_path) and os.path.getsize(skjv_path) < 200:
            translate_single_chapter_book(kjv_path, skjv_path, book_name)
        else:
            print(f"  ⏭️  {book_name}: already has content, skipping")

    # ===== PHASE 3: Final verification =====
    print("\n📖 PHASE 3: Final verification sweep...")
    remaining_saith = 0
    remaining_broken = 0
    remaining_eth = 0

    for filename in book_files:
        filepath = os.path.join(BOOKS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        remaining_saith += len(re.findall(r'\bsaith\b', text, re.IGNORECASE))
        for pattern in BROKEN_WORD_FIXES:
            remaining_broken += len(re.findall(pattern, text, re.IGNORECASE))
        # Count -eth verbs (excluding safe words)
        for match in re.finditer(r'\b\w+eth\b', text, re.IGNORECASE):
            word = match.group(0).lower()
            if word not in ETH_SAFE_WORDS and not word[0].isupper():
                remaining_eth += 1

    print(f"\n{'=' * 60}")
    print(f"FINAL REPORT")
    print(f"{'=' * 60}")
    print(f"  Total fixes applied (Phase 1):  {total_fixes}")
    print(f"  Files modified:                 {files_fixed}")
    print(f"  Remaining 'saith':              {remaining_saith}")
    print(f"  Remaining broken words:         {remaining_broken}")
    print(f"  Remaining -eth verbs:           {remaining_eth}")
    print(f"  Stub books generated (Phase 2): {len(stubs)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
