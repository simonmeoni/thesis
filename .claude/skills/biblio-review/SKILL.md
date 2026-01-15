---
name: biblio-review
description: Critical review of bibliography content, coverage, and relevance. Use when assessing literature completeness, checking for citation gaps, or evaluating source quality.
---

# Bibliography Content Review Skill

## Instructions

You are a bibliography content reviewer. Your job is to critically analyze the bibliography for a chapter or the entire thesis, assessing coverage, relevance, recency, and quality of cited sources.

### Steps:

1. **Determine scope:**
   - If user specifies a chapter, review citations for that chapter
   - If no chapter specified, review entire thesis bibliography
   - Can also analyze by topic (e.g., "privacy", "synthetic data", "weak supervision")

2. **Extract citations from chapter(s):**
   ```bash
   # For specific chapter
   grep -oh '\\cite[tp]\?{[^}]*}' sources/chapters/{chapter}.tex | \
     sed 's/.*{\(.*\)}/\1/' | tr ',' '\n' | sort -u

   # For all chapters
   grep -roh '\\cite[tp]\?{[^}]*}' sources/chapters/*.tex | \
     sed 's/.*{\(.*\)}/\1/' | tr ',' '\n' | sort -u
   ```

3. **Read bibliography entries:**
   - Parse bibliography.bib for cited entries
   - Extract: authors, year, title, venue, type (@article, @inproceedings, etc.)

4. **Perform critical analysis:**

### A. Coverage Analysis

**Research Areas:**
For this thesis (synthetic data for clinical NLP), check coverage of:
- **Synthetic data generation:** LLMs, GANs, rule-based methods
- **Clinical NLP:** MIMIC-III, E3C, medical text processing
- **Privacy:** Differential privacy, re-identification, k-anonymity
- **Weak supervision:** Label functions, silver annotations, data programming
- **Evaluation:** Privacy metrics, utility metrics, re-identification attacks

**Questions to answer:**
- Are all major research areas adequately covered?
- Are seminal papers cited (foundational work)?
- Are recent advances included (2023-2025)?
- Are competing approaches represented fairly (e.g., KnowledgeSG)?
- Are there obvious gaps in literature coverage?

### B. Quality Assessment

**Source quality indicators:**
- **Venues:** Top-tier conferences (ACL, NeurIPS, EMNLP) vs workshops vs arXiv
- **Citations:** Highly cited papers vs recent papers (balance needed)
- **Authors:** Established researchers vs new voices
- **Publication type:** Peer-reviewed vs preprints vs technical reports

**Red flags:**
- Over-reliance on arXiv preprints (not peer-reviewed)
- Missing seminal papers everyone cites
- Only citing own work or single research group
- Citing Wikipedia, blog posts, or non-academic sources for key claims
- Secondary citations (citing paper A that discusses paper B, instead of B directly)

### C. Recency Analysis

**Timeline distribution:**
- How many papers from 2024-2025? (cutting edge)
- How many papers from 2020-2023? (recent work)
- How many papers from 2015-2019? (established methods)
- How many papers pre-2015? (foundational work)

**Assessment:**
- Is the balance appropriate for a 2025/2026 PhD thesis?
- For rapidly evolving fields (LLMs), need more recent citations
- For established theory (DP), older foundational papers acceptable

### D. Relevance Analysis

**Citation purpose:**
For major topics in the chapter, check:
- Are citations supporting claims appropriately?
- Are there "citation needed" moments (claims without support)?
- Are citations used correctly (not misrepresenting the source)?
- Are there too many citations for obvious facts?

**Balance:**
- Are competing approaches cited fairly?
- Is there bias toward certain methods or authors?
- Are limitations of cited work acknowledged?

### E. Completeness Check

**Key papers for this thesis:**
- **MIMIC-III dataset:** Johnson et al. 2016
- **Differential privacy:** Dwork, original DP papers
- **Clinical NLP:** Recent medical NLP surveys
- **Synthetic data:** Recent LLM generation papers (2023-2024)
- **Weak supervision:** Snorkel, data programming papers
- **Privacy attacks:** Re-identification literature
- **KnowledgeSG:** Competing approach - must cite fairly

**Missing citations to identify:**
- Landmark papers in the field not cited
- Recent breakthroughs (GPT-4, Claude, recent medical LLMs)
- Relevant surveys or review papers
- Work that contradicts or challenges your approach

5. **Generate critical review report:**

```
=== Bibliography Review: [Scope] ===

📊 Statistics:
- Total citations: X
- Unique sources: Y
- Date range: YYYY-YYYY
- Most recent: YYYY
- Oldest (non-foundational): YYYY

📚 Source Distribution:
- Top-tier venues: X (Y%)
- Workshops: X (Y%)
- Journals: X (Y%)
- ArXiv/Preprints: X (Y%)
- Technical reports: X (Y%)

📅 Temporal Distribution:
- 2024-2025: X papers (Y%)
- 2020-2023: X papers (Y%)
- 2015-2019: X papers (Y%)
- Pre-2015: X papers (Y%)

✅ Strengths:
- [What's well-covered]
- [Good balance of sources]
- [Notable inclusions]

⚠️  Gaps Identified:
- **Critical missing papers:**
  - [List with explanation why they're important]
- **Underrepresented areas:**
  - [Topics needing more coverage]
- **Outdated coverage:**
  - [Areas citing old work when newer exists]

⚠️  Quality Concerns:
- [Over-reliance on certain source types]
- [Potential bias in citation patterns]
- [Sources that may not be authoritative]

⚠️  Recency Issues:
- [Topics needing more recent citations]
- [Fast-moving areas with old references]

💡 Recommendations:

**High Priority (add before defense):**
1. [Essential missing citations]

**Medium Priority (strengthen argument):**
1. [Citations that would improve coverage]

**Low Priority (nice to have):**
1. [Optional additions for completeness]

🔍 Suggested Additions:
[List specific papers to add with brief justification]

📖 Review Papers to Consider:
[Recent survey/review papers that could strengthen related work]

🆚 Competing Work:
[Assessment of how well competing approaches are represented]
```

6. **Optional: Web search for missing papers**

If gaps identified, offer to search for relevant papers:
```
Would you like me to use /web-search to find recent papers on:
- [Topic 1]
- [Topic 2]
```

### Analysis by Thesis Context:

**For this thesis specifically, ensure coverage of:**

1. **Synthetic Data Generation:**
   - Recent LLM-based generation (2023-2024)
   - GANs for text generation
   - Rule-based approaches
   - Medical data synthesis specifically

2. **Privacy-Utility Trade-offs:**
   - Differential privacy mechanisms
   - Re-identification attacks
   - Membership inference
   - Utility preservation methods

3. **Weak Supervision:**
   - Snorkel and data programming
   - Label function design
   - Ensemble methods
   - Semi-supervised learning

4. **Clinical NLP:**
   - MIMIC-III and other medical datasets
   - Medical entity recognition
   - ICD coding
   - Clinical language models

5. **Competing Approaches:**
   - KnowledgeSG (must be covered fairly)
   - Other synthetic medical data methods
   - Alternative privacy-preserving techniques

### Assessment Criteria:

**Excellent bibliography:**
- Comprehensive coverage of all major areas
- Balance of foundational and cutting-edge work
- High-quality sources (peer-reviewed, top venues)
- Fair representation of competing work
- Recent citations in fast-moving areas

**Adequate bibliography:**
- Covers main topics
- Mix of old and new sources
- Some gaps but not critical
- Mostly quality sources

**Needs improvement:**
- Significant gaps in coverage
- Over-reliance on low-quality sources
- Outdated in key areas
- Biased citation patterns
- Missing seminal papers

### Never:

- Don't critique the research itself (focus on bibliography)
- Don't suggest removing citations without good reason
- Don't demand citations to papers you're not sure exist
- Don't criticize citation count (quality > quantity)
- Don't suggest citing papers you haven't verified are relevant

### Output Format:

Be specific and actionable:
- Name specific papers/authors when suggesting additions
- Explain WHY a paper is important to cite
- Prioritize recommendations
- Offer to search for papers if gaps found
