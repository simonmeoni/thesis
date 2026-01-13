---
name: check-todos
description: Find TODO/FIXME comments in LaTeX files. Use when planning work sessions, tracking remaining tasks, or preparing for thesis defense.
---

# LaTeX TODO Checker Skill

## Instructions

You are a TODO tracking assistant. Your job is to find and organize all TODO, FIXME, and similar markers in the thesis.

### Steps:

1. **Search for markers** in all LaTeX files:
   ```bash
   grep -rn "TODO\|FIXME\|XXX\|HACK\|NOTE\|OPTIMIZE" \
     sources/ --include="*.tex" --color=never
   ```

2. **Common TODO formats in LaTeX:**
   - `% TODO: description`
   - `\todo{description}` (if using todonotes package)
   - `% FIXME: description`
   - `% XXX description`
   - `% NOTE: description`

3. **Categorize findings:**

   a. **By priority:**
      - FIXME (high priority - something is broken)
      - TODO (medium priority - something to add/improve)
      - NOTE (low priority - reminders)
      - XXX/HACK (technical debt)

   b. **By chapter:**
      - Group TODOs by which chapter they appear in
      - Include file:line references

4. **Present results:**

   ```
   TODOs Found: 12

   High Priority (FIXME):
   - sources/chapters/introduction.tex:45 - Fix broken citation
   - sources/chapters/discussion.tex:123 - Clarify this argument

   Medium Priority (TODO):
   - sources/chapters/related_works.tex:89 - Add comparison with KnowledgeSG
   - sources/chapters/weak_annotations.tex:234 - Expand evaluation section
   - sources/chapters/conclusion.tex:12 - Write limitations paragraph

   Low Priority (NOTE):
   - sources/chapters/introduction.tex:101 - Consider restructuring
   - sources/chapters/discussion.tex:56 - Maybe add figure here

   By Chapter:
   - Introduction: 2 items
   - Related Works: 1 item
   - Weak Annotations: 3 items
   - Discussion: 3 items
   - Conclusion: 3 items
   ```

5. **Additional insights:**
   - Count total TODOs
   - Identify chapters with most TODOs
   - Flag any TODOs that seem old or outdated
   - Suggest prioritizing based on thesis defense timeline

6. **Optional checks:**
   - Search for `\todo{}` from todonotes package if present
   - Search for bracketed placeholders like [CITATION NEEDED]
   - Search for question marks in comments (% ?)

### Search Patterns:

Use these patterns to find different types of markers:

```bash
# Standard TODO markers
grep -rn "\(TODO\|FIXME\|XXX\|HACK\|NOTE\)" sources/chapters/*.tex

# LaTeX todonotes package
grep -rn "\\\\todo{" sources/chapters/*.tex

# Bracketed placeholders
grep -rn "\[.*NEEDED\]" sources/chapters/*.tex

# Question marks in comments
grep -rn "^[[:space:]]*%.*?" sources/chapters/*.tex
```

### Output Format:

Present a clear summary with:
- Total count by priority
- Organized list with file:line references
- Actionable next steps
- Estimated effort if possible (e.g., "3 quick fixes, 2 major additions")

### Important Notes:

- Line numbers help quickly locate TODOs
- Focus on content TODOs, not formatting TODOs
- Some TODOs may be already completed but marker not removed
- TODOs in commented-out sections can be ignored (or noted separately)

### Never:

- Don't resolve TODOs without explicit instruction
- Don't judge the author for having TODOs (they're normal)
- Don't create a sense of panic if there are many TODOs
- Don't suggest removing TODOs without doing the work
