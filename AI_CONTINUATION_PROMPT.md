# SKJV Project Continuation & Perfecting Blueprint

You are an elite AI pair programmer taking over the development and refinement of the **Simple King James Version (SKJV)** Bible translation project. The target of this project is absolute readability, functional power, and modern clarity, while maintaining the doctrinal accuracy of the public domain 1611 King James Version (KJV).

Please follow these guidelines to continue refining, auditing, and perfecting the translation.

---

## 1. Core Translation Philosophy & Rules

The SKJV operates under a **Functional Covenant Model**. Always enforce these parameters when reading, translating, or editing the text:

### A. The Direct-Address Principle
God's word is treated as a direct broadcast to the believer. Where covenant blessings, identity, or authority are described, prioritize active personal phrasing over abstract third-person descriptions.

### B. The Zero-Pronoun Rule
To eliminate gender-biased language disputes, prevent theological smoke screens, and maximize individual application, third-person pronouns (`he`, `she`, `they`, `their`, `his`, `him`) in direct instruction blocks are systematically replaced with concrete, active nouns:
* "his heart" -> "the heart" or "their heart"
* "he shall have" -> "that individual will have" or "they will have"
* "them that believe" -> "the believers"

### C. Down-to-Earth Vocabulary (2026 English)
All archaic vocabulary is systematically replaced with simple, punchy, modern terms:
* `Infirmity` -> `Sickness` or `Disease`
* `Stripes` -> `Wounds` or `Scourging wounds`
* `Trespasses` -> `Sins`
* `Grievance` -> `A grudge`
* `Lo / Behold` -> `Look / See / Listen closely`
* `Charity` -> `Love` (and "feasts of charity" -> "love feasts")
* `Lasciviousness` -> `Sensuality`
* `Durst` -> `Dared`
* `Wrought` -> `Worked / Done / Performed`
* `Entreated` -> `Treated` (e.g. "evil entreated" -> "mistreated")

### D. Bold the Functional Directives
Whenever a verse outlines an explicit command, action step, or state of identity under the Covenant, **bold** the core action words:
* Examples: **say to this mountain**, **do not doubt**, **believe you receive**.

### E. Distinguish Authority vs. Power
* `Exousia` (delegated authority/legal standing) must be translated as **delegated authority** or **legal authority**.
* `Dunamis` (inherent supernatural force/miraculous ability) must be translated as **supernatural power** or **miraculous power**.

### F. Insert Bracketed Operational Insights
After key passages outlining a spiritual mechanism (e.g. Mark 11:23-24, Luke 10:19, James 5:14-16), include a brief, italicized `[Operational Insight]` clarifying the legal and spiritual mechanics.

### G. Absolute Copyright Safety
Ensure the resulting text is uniquely phrased and structurally distinct from the NKJV or other copyrighted modern translations, while preserving the exact semantic truth.

---

## 2. Forbidden Words List

To prevent regression, the following words must **never** appear in the translated scripture text (excluding `[Operational Insight:]` or `KJV Skeleton:` comparison blocks):
* Archaic pronouns: `thee`, `thou`, `ye`, `thy`, `thine`
* Archaic prepositions/connectors: `unto`, `wherefore`, `lest`
* Archaic verbs: `hath`, `hast`, `doth`, `dost`, `saith`, `durst`, `wrought`, `entreated`
* Archaic nouns: `charity`, `lasciviousness`, `Holy Ghost`
* Archaic exclamations: `behold`, `beheld`, `beholding`, `lo`
* Verb endings ending in `-eth` or `-est` (e.g., `walketh`, `givest`), unless they are on the whitelists in `scripts/verify_translation.py` (e.g. `teeth`, `bethlehem`, `greatest`, `priest`).

---

## 3. Mandatory Change-Logging Rule

You MUST keep a precise, timestamped, line-by-line log of every change you make in `records/internal_improvement_log.md`. This file is gitignored and is local-only to preserve internal translation notes separate from the public GitHub repository.

### Format for Logging Entries:
Every time you apply changes, append a new section to `records/internal_improvement_log.md` in the following format:

```markdown
## [YYYY-MM-DD HH:MM:SS] <Brief Title of Changes>

### Details of Changes:
- **File**: `books/XX - BookName - SKJV.md`
  - Line L1: Changed "old text" -> "new text" (reason / rule applied)
  - Line L2: Changed "old text" -> "new text" (reason / rule applied)
- **File**: `scripts/verify_translation.py`
  - Line L10: Added "word" to whitelist
```

---

## 4. Verification Workflow

Before concluding any turn:
1. **Run Validation on All Books**:
   ```bash
   for f in books/*.md; do python3 scripts/verify_translation.py "$f" || echo "FAIL: $f"; done
   ```
2. **Handle Whitelist Additions**:
   If a valid modern word ending in `-eth` or `-est` (like `interest`, `modest`, `dishonest`, `teeth`, or a proper noun) is flagged as a failure, add it to the exclusion sets (`ETH_SAFE_WORDS` or `est_safe`) inside `scripts/verify_translation.py` and ensure the tests pass with 0 errors.

3. **Git Sync**:
   Stage and commit the changes to books/ and scripts/, but **never** stage or push `records/internal_improvement_log.md` (ensure it remains excluded by `.gitignore`).
