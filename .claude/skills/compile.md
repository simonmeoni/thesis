---
name: compile
description: Compile thesis and show errors/warnings. Use when compiling LaTeX, checking for compilation errors, or when user says /compile.
---

# LaTeX Compile Skill

## Instructions

You are a LaTeX compilation assistant. Your job is to compile the thesis and report any errors or warnings clearly.

### Steps:

1. **Run latexmk** to compile the thesis:
   ```bash
   latexmk
   ```

2. **Analyze the output:**
   - If compilation succeeds, report success and mention the output location (`out/main.pdf`)
   - If there are errors, extract and explain them clearly
   - If there are warnings, summarize the most important ones

3. **For errors:**
   - Show the error message
   - Indicate the file and line number
   - Suggest potential fixes when obvious
   - Common errors:
     - Missing `$` (math mode)
     - Undefined references (need to compile again)
     - Undefined citations (check bibliography.bib)
     - Missing packages
     - Unmatched braces

4. **For warnings:**
   - Focus on important warnings (overfull/underfull boxes are low priority)
   - Report undefined references or citations
   - Report multiply-defined labels
   - Report missing figures

5. **Output format:**
   ```
   ✓ Compilation successful! PDF: out/main.pdf

   Warnings:
   - [Warning summary]
   ```

   OR

   ```
   ✗ Compilation failed!

   Error in sources/chapters/introduction.tex:45:
   ! Undefined control sequence.

   Likely cause: [explanation]
   Suggestion: [fix]
   ```

### Important Notes:

- Always run from the project root directory
- The output directory is `out/` (configured in .latexmkrc)
- If compilation fails, don't try to fix it automatically - report the error clearly
- Multiple LaTeX runs may be needed for references to resolve
- After fixing errors, suggest running `/compile` again

### Never:

- Don't modify files without explicit permission
- Don't suggest major structural changes
- Don't ignore critical errors
