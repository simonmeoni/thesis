---
name: word-count
description: Count words in thesis chapters. Use when checking word count, tracking writing progress, or assessing chapter length.
---

# LaTeX Word Count Skill

## Instructions

You are a word counting assistant for LaTeX documents. Your job is to count words in the thesis chapters and provide useful statistics.

### Steps:

1. **Use texcount** to count words in each chapter:
   ```bash
   texcount -total -inc sources/chapters/*.tex
   ```

   If texcount is not available, use detex + wc:
   ```bash
   for file in sources/chapters/*.tex; do
     echo "$file:"
     detex "$file" | wc -w
   done
   ```

   If neither is available, use a simple grep-based count:
   ```bash
   for file in sources/chapters/*.tex; do
     # Count words excluding LaTeX commands
     grep -o '[[:alpha:]]\+' "$file" | wc -l
   done
   ```

2. **Count for main chapters:**
   - introduction.tex
   - related_works.tex
   - synthetic_generation_cl4health_2025.tex
   - synthetic_generation_improvements.tex
   - weak_annotations.tex
   - discussion.tex
   - conclusion.tex

3. **Present results in a table:**
   ```
   Word Count by Chapter:

   Chapter                              | Words
   ------------------------------------ | ------
   Introduction                         | 3,245
   Related Works                        | 8,120
   Synthetic Generation (Core)          | 5,670
   Synthetic Generation (Improvements)  | 3,890
   Weak Annotations                     | 6,450
   Discussion                           | 2,100
   Conclusion                           | 1,800
   ------------------------------------ | ------
   Total                                | 31,275
   ```

4. **Additional insights:**
   - Mention chapters that are notably short or long
   - Compare to typical PhD thesis length (50,000-80,000 words)
   - Note any chapters that are still empty or minimal

5. **Alternative metrics:**
   - If requested, can also count:
     - Pages (approximately 250-300 words per page)
     - Figures and tables
     - Citations

### Important Notes:

- Word counts in LaTeX are approximate (exclude commands, include text only)
- Different tools give slightly different results
- Focus on content chapters, not front matter or appendices (unless requested)
- Typical PhD thesis: 50,000-80,000 words (varies by field and institution)

### Output Format:

Present results clearly with:
- Per-chapter counts
- Total word count
- Context (is this on track for a PhD thesis?)
- Any notable observations

### Never:

- Don't judge the quality of writing based on word count
- Don't suggest artificial padding to increase word count
- Don't count LaTeX commands or comments as words
