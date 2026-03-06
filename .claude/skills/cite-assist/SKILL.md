---
name: cite-assist
description: Verify citations when writing. Check bibliography locally, search online if missing, fix hallucinations. Use proactively during writing.
proactive: true
---

# Citation Assistant

## Workflow

When writing text with citations:

### 1. Write text with `\citep{}` or `\citet{}`

### 2. For each citation, check if it exists locally

```
Grep: pattern="citationKey" path="bibliography.bib"
```

### 3. If NOT in bibliography.bib

**Search online to verify the citation is real:**
- Use WebSearch to find the paper
- Verify: title, authors, year, venue match what you claimed

**If citation exists online:**
- Verify the **venue** (conference/journal vs arXiv preprint) via WebSearch
- Use `@inproceedings` for conference papers, `@article` for journals/arXiv preprints
- Always include the `url` field linking to the paper
- For arXiv-only papers, use `journal = {arXiv preprint arXiv:XXXX.XXXXX}`
- For conference papers, find the exact proceedings name, pages if available
- Propose BibTeX entry to add
- Justify why this citation supports the claim

```
Citation needed: [citationKey]
Claim: "[what you wrote]"

Found: [Paper title] by [Authors], [Year]
Venue: [Conference/Journal or arXiv preprint]
URL: [link]

Proposed BibTeX:
@inproceedings{citationKey,
    title = {...},
    author = {...},
    booktitle = {...},
    year = {...},
    url = {...},
}

Justification: This paper supports the claim because [reason].

Add to bibliography.bib? [Y/n]
```

**If citation is hallucinated (doesn't exist or doesn't match):**
- Immediately re-edit the text
- Either find a real citation or remove the claim

```
Hallucination detected: [citationKey]
Claimed: "[what you wrote]"
Reality: Paper doesn't exist / doesn't say this

Re-editing text to fix...
```

### 4. Summary after writing

```
Citations verified:
- \citep{existing1} - in bib
- \citep{existing2} - in bib

Citations to add:
- \citep{newKey} - [proposed entry]

Fixed hallucinations:
- Removed claim about X (no valid citation)
```

## Rules

- Always verify before proposing
- Never invent citations
- If unsure, search first
- Fix mistakes immediately
- Always verify the **publication venue** (search for "paper_title conference" or check arxiv/ACL Anthology/OpenReview)
- Always include a `url` field in bib entries
- Use the correct entry type: `@inproceedings` for conferences, `@article` for journals/arXiv
- For long author lists, include first ~10 authors then `and others`
