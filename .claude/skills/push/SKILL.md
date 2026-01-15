---
name: push
description: Push commits to remote repository. Use when pushing changes, after committing, or when user says /push.
---

# Git Push Skill

## Instructions

You are a git push assistant. Your job is to safely push commits to the remote repository.

### Steps:

1. **Check current state:**
   ```bash
   git status
   git log origin/master..HEAD --oneline
   ```

2. **Verify what will be pushed:**
   - Show commits that will be pushed
   - Confirm branch name
   - Check if remote is up to date

3. **Check for potential issues:**
   ```bash
   git fetch origin
   git status
   ```
   - If behind remote, warn user about potential conflicts
   - If diverged, suggest pull first

4. **Push to remote:**
   ```bash
   git push origin master
   ```
   Or if on a different branch:
   ```bash
   git push origin [branch-name]
   ```

5. **Verify success:**
   ```bash
   git status
   ```

### Output Format:

```
📤 Pushing to origin/master...

Commits to push:
- abc1234 feat(privacy): add DP analysis
- def5678 fix(bib): correct citations

✓ Push successful!
```

Or if issues:

```
⚠️  Remote has new commits.

Options:
1. Pull first: git pull --rebase origin master
2. Force push (not recommended): git push --force

Recommendation: Pull first to avoid conflicts.
```

### Safety Checks:

- Never force push to master without explicit user request
- Warn if pushing more than 5 commits at once
- Warn if pushing large files (> 10MB)
- Check that thesis compiles before pushing (optional)

### Overleaf Integration:

If the repository is synced with Overleaf:
- Changes will appear in Overleaf after push
- Overleaf may take a few seconds to sync
- Conflicts can occur if editing in both places

### Never:

- Don't force push without explicit permission
- Don't push to wrong branch
- Don't push if there are uncommitted changes (warn user)
- Don't push broken code/LaTeX without warning
