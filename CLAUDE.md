# PhD Thesis - Synthetic Data Generation for Clinical NLP

LaTeX thesis by Simon Meoni. Uses `mimosis` template with `latexmk` for compilation.

## Commands

```bash
latexmk              # Compile (outputs to out/)
latexmk -C && latexmk  # Force full rebuild
```

## Writing Rules

IMPORTANT - These rules differ from defaults and must be followed:

- **Citations**: `\citep{}` for parenthetical, `\citet{}` for textual
- **Acronyms**: Define in `sources/lexicons/acronyms.tex`, use `\gls{acronym}`
- **Numbers/Units**: Use siunitx: `\num{12345}`, `\SI{95}{\percent}`
- **References**: Always use `\label{}` + `\autoref{}`, never hardcode "Figure 3"
- **One sentence per line**: Each sentence on its own line for cleaner git diffs
- **Mini TOC**: Each chapter has `\minitoc` after `\chapter{}` - add paragraph intro before it

## Content Direction

- Privacy-utility trade-offs are central to the thesis
- Facsimile approach: synthetic documents based on real ones (not pure fiction)
- Honest limitations: acknowledge residual risks, no perfect solution exists
- Always show utility metrics alongside privacy metrics

## Key Terms

- **IPP**: Identifiant Permanent Patient
- **Facsimile documents**: Synthetic docs preserving structure of real documents
- **Silver annotations**: Annotations from weak supervision (not gold standard)
- **AlpaCare**: Your synthetic clinical dataset
- **KnowledgeSG**: Competing approach for comparison

## Never

- Don't create new chapters without explicit instruction
- Don't modify `bibliography.bib` structure (only add entries)
- Don't change `main.tex` structure
- Don't remove content without confirmation
- Don't add speculative content not grounded in your research
