# Thesis Improvement Plan

**Date:** 2025-11-10

---

## Current Structure

- **Chapter 1:** Related Works (59 KB)
- **Chapter 2:** Synthetic Generation - Core (41 KB)
- **Chapter 3:** Generation Improvements (22 KB)
- **Chapter 4:** Weak Annotations (43 KB)
- **Introduction:** Commented out
- **Conclusion:** Empty

**Total:** ~180 pages

---

## 1. Privacy Chapter (NEW - Unify Content)

**Create dedicated privacy chapter after annotation work**

### Structure:
1. **Privacy Framework** - Threat model, DP foundations
2. **Facsimile vs Fictional Documents** - Why keep link to real docs
3. **Data Utility Analysis** ⭐ **PROMINENT** - Metrics, trade-offs, preliminary DP+paraphrasing results
4. **Privacy Evaluation** - Re-identification attacks (45-76% linkage, 89-96% discrimination)
5. **Remediation Strategies** - Paraphrasing, noise injection, filtering
6. **KnowledgeSG Comparison**:
   - They evaluate identifier completion, we evaluate re-identification
   - DP effective for re-identification, not identification
   - Our contributions: AlpaCare, seed documents, explicit trade-offs

---

## 2. Annotation Chapter Improvements

### Add:
1. **Contextual positioning** - Precursor work, relevant for multilingual/low-resource settings
2. **Institution-specific language** - Each hospital has own "language", automation valuable
3. **Small models + regulation** - Advantage in current GDPR/HIPAA context
4. **Expanded conclusion**:
   - Ensemble LLM annotation techniques
   - Diversity through mixing
   - When to use LLMs vs small models
5. **Pseudo-MIMIC evaluation** - Train/test both synthetic with silver annotations (weakness but insightful)

---

## 3. Conclusion Chapter (Write from Scratch)

### Sections:
1. **Summary of Contributions**
2. **Residual Risks & Limitations**
   - Privacy: no zero-risk, re-identification remains possible
   - Silver annotations ceiling
   - Context-dependent constraints
3. **Comparative Analysis** - KnowledgeSG strengths vs our contributions
4. **Applications Beyond Medical** - Legal, financial, any sensitive domain
5. **Recommendations** - When to use facsimile vs fictional, privacy-utility navigation
6. **Future Directions**:
   - Remediation frameworks
   - Better evaluation metrics
   - Alternative approaches (document rewriting, federated learning)
   - Regulatory alignment

**Tone:** Demonstrate "understanding of the stakes" - honest about limits, no perfect solution

---

## 4. Appendix Expansions

### Add:
- **A. Datasets** - MIMIC-III, E3C, AlpaCare, synthetic stats
- **B. ICD-9 Analysis** - Hierarchy, distribution, imbalance
- **C. Detailed Evaluation** - Per-class results, confusion matrices, error analysis
- **D. Computational Resources** ⭐
  - **Carbon footprint** (expand current mention)
  - **Time costs** (NEW - generation, training, inference)
  - Hardware specs
- **E. Code & Reproducibility** - Repo structure, setup, hyperparameters

---

## 5. Formatting Quick Wins

### High Priority:
- [ ] **Mini-TOC introductions** - Paragraph before each minitoc
- [ ] **Convert enumerations** - (1, 2) → proper LaTeX lists
- [ ] **Number formatting** - Use `siunitx` for large numbers
- [ ] **Transitions** - Add sentences between chapters/sections
- [ ] **Break text blocks** - Split paragraphs > 10 lines

---

## 6. Chapter Ordering

### Recommended:
```
Introduction
→ Related Works
→ Generation Process (merge Ch 2 & 3 OR keep separate)
→ Annotation Work
→ Privacy Analysis (NEW unified chapter) ⭐
→ Conclusion & Discussion
→ Appendices
```

**Rationale:** Privacy at end (conscious of residual risks, comes after methodology)

---

## 7. Key Themes

1. **Facsimile documents** - Based on real docs, not too far from reality, maintain utility
2. **Data utility central** - Especially in privacy chapter, show noise doesn't destroy value
3. **Precursor work** - Annotation work initiated years ago, aligns with current LLM trends
4. **Honest limitations** - No zero-risk, understand stakes, context-dependent
5. **Composite evaluation** - Marriage of different approaches for future work

---

## 8. Action Items by Priority

### Priority 1 (Quick Wins - 1-2 weeks):
- Mini-TOC intros, list formatting, number formatting, transitions

### Priority 2 (Content Expansion - 2-3 weeks):
- Annotation improvements, carbon footprint/time costs, KnowledgeSG discussion

### Priority 3 (Major Work - 3-4 weeks):
- Privacy chapter unification, conclusion writing, appendix expansion

---

## Summary

**Main tasks:**
1. Unify privacy → dedicated chapter with data utility prominent
2. Write conclusion → residual risks, future directions, honest limitations
3. Improve flow → transitions, intros, formatting
4. Expand appendices → datasets, detailed results, computational metrics

**Key contribution:** Precursor work in privacy-preserving synthetic clinical data with honest privacy-utility trade-off assessment.
