---
name: commit
description: Create a conventional commit with proper format. Use when committing changes, after completing a task, or when user says /commit.
---

# Git Commit Skill

## Instructions

You are a git commit assistant. Your job is to create clean, well-formatted commits following conventional commit standards.

### Commit Format

Use the format: `<type>(<scope>): <description>`

**Types:**
- `feat`: New feature or content
- `fix`: Bug fix or correction
- `docs`: Documentation changes
- `refactor`: Code/content restructuring
- `chore`: Maintenance tasks (config, dependencies)
- `style`: Formatting changes (no content change)
- `test`: Adding or updating tests

**Scope (for this thesis):**
- `intro`, `related`, `synth`, `weak`, `privacy`, `discussion`, `conclusion` - chapters
- `bib` - bibliography
- `fig` - figures/tables
- `config` - LaTeX/build configuration
- `claude` - Claude Code configuration

### Steps:

1. **Check current status:**
   ```bash
   git status
   git diff --stat
   ```

2. **Analyze changes:**
   - What files were modified?
   - What is the nature of the changes?
   - Group related changes logically

3. **Stage appropriate files:**
   - Stage related changes together
   - Don't mix unrelated changes in one commit
   - Ask user if unsure what to include

4. **Draft commit message:**
   - Keep first line under 72 characters
   - Use imperative mood ("add" not "added")
   - Focus on WHY, not just WHAT
   - Add body if changes need explanation

5. **Create commit:**
   ```bash
   git add [files]
   git commit -m "$(cat <<'EOF'
   type(scope): short description

   Optional longer description if needed.

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```

6. **Verify:**
   ```bash
   git log -1 --stat
   ```

### Examples:

```
feat(privacy): add differential privacy analysis section
fix(bib): correct duplicate citation keys
docs(claude): add custom skills for thesis workflow
refactor(intro): restructure motivation section
chore(config): update latexmk settings
style(synth): fix table formatting
```

### Multi-line Example:

```
feat(weak): implement silver annotation pipeline

- Add label function definitions
- Integrate with Snorkel framework
- Include evaluation metrics

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Important Notes:

- Always show user the staged changes before committing
- Ask for confirmation if changes are significant
- Don't commit files that shouldn't be tracked (.aux, .log, etc.)
- Don't commit secrets or credentials
- Keep commits atomic (one logical change per commit)

### Never:

- Don't commit without showing the user what will be committed
- Don't use vague messages like "update files" or "fix stuff"
- Don't commit unrelated changes together
- Don't skip the Co-Authored-By line
