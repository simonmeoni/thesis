---
name: bib-check
description: Check bibliography for technical issues like syntax errors, duplicates, and undefined citations. Use when debugging citation errors or before submission.
---

# LaTeX Bibliography Check Skill

## Instructions

You are a bibliography checking assistant. Your job is to check the bibliography file for common issues and inconsistencies.

### Steps:

1. **Read bibliography.bib** and analyze it for issues

2. **Check for common problems:**

   a. **Duplicate entries:**
      - Look for entries with the same citation key
      - Look for entries with very similar titles (potential duplicates)

   b. **Missing required fields:**
      - @article: author, title, journal, year
      - @inproceedings: author, title, booktitle, year
      - @book: author/editor, title, publisher, year
      - @phdthesis: author, title, school, year

   c. **Formatting issues:**
      - Inconsistent capitalization in titles (should use {Title Case} for acronyms)
      - Missing {} around special characters or capitals
      - Empty fields
      - Malformed author names

   d. **Special characters:**
      - URLs not wrapped in \url{}
      - Missing escapes for &, %, #, etc.
      - Accented characters not properly encoded

   e. **Year issues:**
      - Missing year fields
      - Non-numeric years
      - Future years (typos)

3. **Check citations in chapters:**
   ```bash
   # Find all \cite commands in chapters
   grep -r "\\\\cite" sources/chapters/*.tex | \
     sed 's/.*\\cite[tp]\?{\([^}]*\)}.*/\1/' | \
     sort -u
   ```

   Then verify each cited key exists in bibliography.bib:
   ```bash
   for key in $(grep -oh '\\cite[tp]\?{[^}]*}' sources/chapters/*.tex | \
                sed 's/.*{\(.*\)}/\1/' | tr ',' '\n' | sort -u); do
     if ! grep -q "@.*{$key," bibliography.bib; then
       echo "Missing: $key"
     fi
   done
   ```

4. **Report findings:**

   ```
   Bibliography Check Results:

   ✓ Total entries: 142
   ✓ Citations in text: 138

   Issues found:

   ⚠ Duplicate entries:
   - johnson_mimic_2016 and johnson_mimic-iii_2016 (similar titles)

   ⚠ Missing required fields:
   - smith_study_2022: missing 'journal' field

   ⚠ Uncited entries (defined but not used):
   - doe_unused_2019
   - jones_forgotten_2020

   ⚠ Undefined citations (used but not defined):
   - missing_ref_2023 (in introduction.tex:45)

   ⚠ Formatting issues:
   - Use {NLP} instead of NLP in titles to preserve capitalization
   - Entry 'wong_study_2021' has special character & not escaped
   ```

5. **Suggestions:**
   - Recommend fixing critical issues first (undefined citations)
   - Suggest tools like biber or bibtool for cleanup
   - Recommend JabRef or Zotero for bibliography management

### Common BibTeX Issues and Fixes:

| Issue | Problem | Fix |
|-------|---------|-----|
| Capitalization | "natural language processing" → "natural language processing" | Use {Natural Language Processing} or {NLP} |
| Special chars | "Smith & Jones" | "Smith \\& Jones" |
| URLs | url = example.com | url = {https://example.com} or \\url{...} |
| Author names | "John Smith and Mary Jones" | "Smith, John and Jones, Mary" |
| Empty fields | publisher = {} | Remove the line entirely |

### Important Notes:

- Focus on errors that will cause compilation failures or citation issues
- Low priority: stylistic inconsistencies (unless they're widespread)
- Some warnings from bibtex are harmless (e.g., missing optional fields)
- The user's settings already have some bibliography checks pre-approved

### Never:

- Don't modify bibliography.bib without explicit permission
- Don't remove entries that appear unused (they might be cited in excluded sections)
- Don't reformat the entire file for style consistency without asking
