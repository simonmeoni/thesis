# LaTeX Thesis Skills

Custom Claude Code skills for managing a LaTeX PhD thesis.

## Available Skills

### `/commit`
Creates a conventional commit with proper format (type(scope): description).

**Use when:**
- After making changes you want to save
- To create clean, well-formatted commits
- Following conventional commit standards

**Example:**
```
User: /commit
Claude: Analyzing changes...
Staged: .claude/skills/*.md, CLAUDE.md

Proposed commit:
  docs(claude): add custom skills for thesis workflow

Proceed? [Y/n]
```

---

### `/push`
Pushes commits to the remote repository safely.

**Use when:**
- After committing changes
- To sync with GitHub/Overleaf
- To backup your work

**Example:**
```
User: /push
Claude: 📤 Pushing to origin/master...
Commits: 2 ahead
✓ Push successful!
```

---

### `/compile`
Compiles the thesis using latexmk and reports errors/warnings clearly.

**Use when:**
- After making changes to LaTeX files
- To check if thesis compiles successfully
- To debug compilation errors

**Example:**
```
User: /compile
Claude: Compiling thesis...
✓ Compilation successful! PDF: out/main.pdf
```

---

### `/word-count`
Counts words in thesis chapters and provides statistics.

**Use when:**
- Tracking writing progress
- Checking if chapters are balanced
- Verifying thesis meets length requirements

**Example:**
```
User: /word-count
Claude: Word Count by Chapter:
        Introduction: 3,245 words
        Related Works: 8,120 words
        ...
        Total: 31,275 words
```

---

### `/bib-check`
Checks bibliography.bib for common issues and undefined citations.

**Use when:**
- After adding new citations
- Before final submission
- Debugging citation errors

**Example:**
```
User: /bib-check
Claude: Bibliography Check Results:
        ✓ 142 entries, 138 cited
        ⚠ Undefined citation: missing_ref_2023
```

---

### `/check-todos`
Finds all TODO/FIXME comments in LaTeX files.

**Use when:**
- Planning work sessions
- Preparing for thesis defense
- Tracking remaining tasks

**Example:**
```
User: /check-todos
Claude: TODOs Found: 12
        High Priority (FIXME): 2
        Medium Priority (TODO): 7
        Low Priority (NOTE): 3
```

---

### `/review`
Comprehensive review of chapter structure, content quality, and LaTeX best practices.

**Use when:**
- Reviewing a completed chapter before moving on
- Preparing chapters for thesis defense
- Getting feedback on structure and presentation
- Checking LaTeX quality and conventions

**Example:**
```
User: /review introduction
Claude: === Chapter Review: Introduction ===
        📊 Overview: ~3,245 words, 4 sections, 2 figures
        ✅ Strengths: Clear narrative, good transitions
        ⚠️  Structure: Missing mini-TOC intro paragraph
        ⚠️  LaTeX: 3 figures not referenced with \autoref
        💡 Recommendations: [prioritized list]
```

**Scope:**
- Can review single chapter: `/review introduction`
- Can review specific sections if needed
- Provides multi-level analysis: structure, content, LaTeX quality

---

### `/biblio-review`
Critical review of bibliography content, coverage, and relevance.

**Use when:**
- Assessing if literature review is comprehensive
- Checking for gaps in citation coverage
- Evaluating quality and recency of sources
- Preparing bibliography for thesis defense

**Example:**
```
User: /biblio-review related_works
Claude: === Bibliography Review: Related Works ===
        📊 Statistics: 45 citations, range 2015-2024
        ✅ Strengths: Good coverage of privacy literature
        ⚠️  Gaps: Missing recent LLM synthesis papers (2024)
        ⚠️  Recency: Weak supervision citations outdated
        💡 Critical missing papers: [list with justification]
```

**Scope:**
- Can review by chapter: `/biblio-review introduction`
- Can review entire thesis: `/biblio-review`
- Can review by topic: `/biblio-review privacy`
- Provides critical analysis of coverage, quality, recency

---

### `/web-search`
Search the web for research papers, documentation, or technical information.

**Use when:**
- Looking for recent papers on specific topics
- Finding documentation for tools/libraries
- Discovering competing approaches or methods
- Filling gaps identified by `/biblio-review`

**Example:**
```
User: /web-search differential privacy clinical data 2024
Claude: === Search Results ===
        📚 Found 8 relevant papers

        Highly Relevant:
        1. "DP-Synthetic: Privacy-Preserving Clinical Text" (2024)
           - Authors: Smith et al.
           - Venue: ACL 2024
           - Key contribution: Novel DP mechanism for text
           - Link: [URL]
```

**Scope:**
- Academic papers: `/web-search [topic] 2024`
- Documentation: `/web-search LaTeX siunitx documentation`
- General info: `/web-search what is k-anonymity`
- Can fetch and summarize papers found

---

## How Skills Work

Skills are markdown files in `.claude/skills/` that provide specialized instructions to Claude Code.

When you invoke a skill (e.g., `/compile`), Claude:
1. Loads the skill instructions from the YAML frontmatter
2. Follows the steps defined in the skill
3. Uses appropriate tools (Bash, Read, etc.)
4. Reports results in the format specified

## Adding New Skills

To create a new skill:

1. Create a `.md` file in `.claude/skills/`
2. **Required:** Include YAML frontmatter at the very top:
   ```markdown
   ---
   name: skill-name
   description: What it does. When to use it.
   ---

   # Skill Title

   ## Instructions
   ...
   ```
3. Write clear instructions after the frontmatter
4. Document the skill here in README.md

**Important:** The YAML frontmatter is required for Claude Code to recognize the skill. The `name` field must be lowercase with hyphens only. The `description` field helps Claude decide when to use the skill.

## Tips

- Skills should be **focused** (do one thing well)
- Skills should be **repeatable** (same result each time)
- Skills should **report**, not auto-fix (ask before modifying files)
- Use existing tools (latexmk, grep) rather than complex custom scripts

## Thesis-Specific Notes

This thesis uses:
- **Build system:** latexmk (configured in `.latexmkrc`)
- **Output directory:** `out/`
- **Main file:** `main.tex`
- **Chapters:** `sources/chapters/*.tex`
- **Bibliography:** `bibliography.bib`

See `CLAUDE.md` for full thesis documentation.
