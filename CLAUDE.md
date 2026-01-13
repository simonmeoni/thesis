# PhD Thesis - Synthetic Data Generation for Clinical NLP

> LaTeX thesis on synthetic data generation for clinical natural language processing

## Overview

**Title:** Synthetic Data Generation for Clinical Natural Language Processing
**Author:** Simon Meoni
**Document Class:** mimosis (custom thesis template)
**Default Model:** Claude Opus 4.5 (configured in settings)

## Structure

```
sources/
├── chapters/          # Main thesis chapters
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── related_works.tex
│   ├── synthetic_generation_cl4health_2025.tex
│   ├── synthetic_generation_improvements.tex
│   ├── weak_annotations.tex
│   ├── discussion.tex
│   ├── conclusion.tex
│   └── appendix.tex
├── title/             # Title page
├── lexicons/          # Acronyms, glossary, custom commands
│   ├── acronyms.tex
│   ├── glossary.tex
│   └── commands.tex
figures/               # Figures and tables (mostly .tex tables)
styles/                # Custom styles
bibliography.bib       # Bibliography
main.tex              # Main document
.latexmkrc            # Build configuration
```

## Compilation

Use latexmk (configured in `.latexmkrc`):

```bash
latexmk              # Compile main.tex
latexmk -c           # Clean auxiliary files
latexmk -C           # Clean all generated files including PDF
latexmk -pvc         # Continuous preview mode
```

Output files are in `out/` directory.

## Custom Skills

LaTeX-specific skills available:

### Compilation & Analysis
```bash
/compile             # Compile thesis and show errors/warnings
/word-count          # Count words in thesis chapters
/check-todos         # Find TODO/FIXME comments in LaTeX files
```

### Quality Review
```bash
/review [chapter]    # Review chapter structure, content, and LaTeX quality
/bib-check           # Check bibliography for technical issues (syntax, duplicates)
/biblio-review [scope] # Critical review of bibliography content and coverage
```

### Research & Search
```bash
/web-search [query]  # Search web for papers, documentation, or information
```

## Writing Rules

### MUST

- **Citations**: Use `\citep{}` for parenthetical, `\citet{}` for textual
- **Acronyms**: Define in `sources/lexicons/acronyms.tex`, use `\gls{acronym}`
- **Math**: Use `\( \)` for inline, `\[ \]` or equation environment for display
- **Numbers**: Use `\num{12345}` from siunitx for large numbers
- **Units**: Use `\SI{value}{unit}` from siunitx (e.g., `\SI{95}{\percent}`)
- **Figures**: Always use `\label{fig:name}` and reference with `\autoref{fig:name}`
- **Tables**: Always use `\label{tab:name}` and reference with `\autoref{tab:name}`
- **Lists**: Use proper LaTeX environments (itemize, enumerate, description)
- **Line length**: Keep .tex lines under 100 characters when practical

### Structure

- **Chapter order**: Introduction → Related Works → Generation (Ch 3-4) → Annotation → Privacy → Discussion → Conclusion
- **Section depth**: Use `\section`, `\subsection`, `\subsubsection` (avoid deeper)
- **Mini TOC**: Each chapter has `\minitoc` after `\chapter{}` - add paragraph intro before it

### Formatting

- **Paragraphs**: Break long paragraphs (> 10 lines) into smaller ones
- **Transitions**: Add connecting sentences between major sections
- **Tables**: Use booktabs style (`\toprule`, `\midrule`, `\bottomrule`)
- **Code**: Use `algorithm2e` for algorithms, `Verbatim` for code snippets
- **Lists**: Avoid inline enumerations like (1), (2), (3) - use proper `\begin{enumerate}`

### Content Guidelines

From `NOTES.md` improvement plan:

1. **Privacy focus**: Privacy-utility trade-offs are central to the thesis
2. **Facsimile approach**: Synthetic documents based on real ones (not pure fiction)
3. **Honest limitations**: Acknowledge residual risks, no perfect solution exists
4. **Data utility**: Always show utility metrics alongside privacy metrics
5. **Computational costs**: Report carbon footprint and time costs when relevant

## Key Terminology

- **IPP**: Identifiant Permanent Patient (patient identifier)
- **Facsimile documents**: Synthetic documents that preserve structure of real documents
- **Silver annotations**: Annotations from weak supervision models (not gold standard)
- **AlpaCare**: Your synthetic clinical dataset
- **Differential Privacy (DP)**: Privacy framework used in thesis
- **KnowledgeSG**: Competing approach for synthetic data generation

## Research Context

**Main contributions:**
1. Synthetic clinical document generation preserving document structure
2. Weak supervision techniques for annotation with limited labels
3. Privacy-utility trade-off analysis with re-identification experiments
4. Comparison with KnowledgeSG approach (AlpaCare, seed documents, explicit trade-offs)

**Key datasets:** MIMIC-III, E3C, AlpaCare (synthetic)

**Related work:** KnowledgeSG, differential privacy in healthcare, weak supervision

## Thesis Status (from NOTES.md)

**Current:** ~180 pages

**Chapters:**
- Introduction ✓
- Related Works ✓ (59 KB)
- Synthetic Generation Core ✓ (41 KB)
- Generation Improvements ✓ (22 KB)
- Weak Annotations ✓ (43 KB)
- Discussion (in progress)
- Conclusion (to write)

**Priority tasks:**
1. Unify privacy content into dedicated chapter
2. Write conclusion with honest limitations
3. Improve formatting (mini-TOC intros, lists, transitions)
4. Expand appendices (datasets, computational costs)

## Commands

### Editing Workflow

1. **Before editing:** Read the relevant chapter first using Read tool
2. **Understand context:** Check surrounding content and chapter structure
3. **Make targeted edits:** Avoid over-engineering or unnecessary changes
4. **Verify compilation:** Use `/compile` to check for LaTeX errors
5. **Check output:** Review changes in generated PDF when needed

### File References

When referencing content, use format: `file:line` (e.g., `sources/chapters/introduction.tex:45`)

### Never

- Don't create new chapters without explicit instruction
- Don't modify `bibliography.bib` structure (only add entries)
- Don't change `main.tex` structure (chapter includes, package loading)
- Don't remove content without confirmation
- Don't add speculative or hypothetical content
- Don't use `@observe` decorator (thesis uses different tracing)

## Build System

LaTeXmk configuration (`.latexmkrc`):
- Uses pdflatex (or XeLaTeX/LuaLaTeX if `\ifxetexorluatex` is true)
- Runs bibtex for bibliography
- Runs makeglossaries for acronyms/glossary
- Outputs to `out/` directory
- Cleans auxiliary files automatically

**Packages used:**
- `siunitx` - number and unit formatting
- `booktabs` - professional tables
- `algorithm2e` - algorithms
- `hyperref` - hyperlinks and bookmarks
- `minitoc` - mini table of contents per chapter
- `glossaries` - acronyms and glossary

## Common Issues

**Bibliography not updating:** Run `latexmk -C && latexmk` to force full rebuild

**Glossary/Acronyms not showing:** Ensure `makeglossaries` is installed:
```bash
which makeglossaries
```

**Font issues:** Check if TeX Gyre Pagella is installed, or compile with pdflatex

**Long compilation time:** First run is slow (bibliography, glossaries). Incremental builds faster.

**Undefined citations:** Ensure citation keys match `bibliography.bib` entries exactly

## LaTeX Best Practices

1. **Always compile after changes** - Use `/compile` to catch errors early
2. **Use semantic commands** - Define custom commands in `sources/lexicons/commands.tex`
3. **Reference by label** - Never hardcode "Figure 3" - use `\autoref{fig:label}`
4. **Break long lines** - Makes diffs cleaner and easier to review
5. **One sentence per line** - Alternative style for better version control

## Notes

See `NOTES.md` for:
- Detailed improvement plan
- Content structure decisions
- Priority tasks and timeline
- Key themes and contributions
