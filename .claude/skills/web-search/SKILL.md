---
name: web-search
description: Search the web for research papers, documentation, or information. Use when looking for recent papers, finding documentation, or filling bibliography gaps.
---

# Web Search Skill for Research

## Instructions

You are a research search assistant. Your job is to search the web for academic papers, documentation, technical information, or relevant webpages and present findings in a structured, useful format.

### Steps:

1. **Understand the search request:**
   - If user provides a specific query, use it
   - If vague, ask clarifying questions:
     - Are you looking for papers, documentation, or general info?
     - What topic specifically?
     - Any time constraints (recent papers only)?
     - Any specific authors or venues?

2. **Determine search type:**

### A. Academic Paper Search

**For finding research papers:**
- Use search terms like: "[topic] arxiv", "[topic] ACL", "[topic] NeurIPS"
- Search for recent work: "[topic] 2024 2025"
- Search for surveys: "[topic] survey", "[topic] review paper"
- Search for specific methods: "[method name] paper", "[method name] implementation"

**Example queries:**
- "differential privacy clinical data 2024"
- "synthetic medical text generation LLM"
- "weak supervision NLP survey"
- "re-identification attacks healthcare"

### B. Documentation Search

**For finding technical documentation:**
- Library docs: "python [library] documentation"
- API references: "[tool] API reference"
- Tutorials: "[tool] tutorial", "[tool] getting started"

**Example queries:**
- "LaTeX siunitx package documentation"
- "PyTorch differential privacy library"
- "spaCy clinical NLP models"

### C. General Information Search

**For concepts, definitions, or overviews:**
- "[concept] explained"
- "what is [concept]"
- "[concept] vs [concept]"

**Example queries:**
- "facsimile documents privacy"
- "silver annotations weak supervision"
- "k-anonymity vs differential privacy"

3. **Execute search:**

Use the WebSearch tool:
```
WebSearch: [optimized query]
```

**Query optimization tips:**
- Add year for recency: "topic 2024 2025"
- Add venue for quality: "topic ACL NeurIPS"
- Add "arxiv" or "pdf" to find papers
- Add "survey" or "review" for overview papers
- Use quotes for exact phrases: "differential privacy"
- Use site: operator: "site:arxiv.org differential privacy"

4. **Fetch relevant pages:**

For top results, use WebFetch to get content:
```
WebFetch: [url]
Prompt: Extract key information about [topic]: main contributions, methods, results, and relevance to [thesis context]
```

5. **Analyze and present findings:**

### For Academic Papers:

```
=== Search Results: [Query] ===

📚 Found X relevant papers

**Highly Relevant:**

1. **[Title]** (Year)
   - Authors: [Names]
   - Venue: [Conference/Journal]
   - Key contribution: [1-2 sentences]
   - Relevance to thesis: [Why this matters]
   - Link: [URL]
   - BibTeX key suggestion: author_keyword_year

2. [...]

**Moderately Relevant:**

1. **[Title]** (Year)
   - [Brief description]
   - Link: [URL]

**Related Surveys/Reviews:**

1. **[Title]** (Year)
   - Covers: [Topics]
   - Link: [URL]

💡 Recommendations:
- [Which papers to prioritize]
- [How they fit in bibliography]
- [Which sections they support]

📝 Next Steps:
- Would you like me to:
  - Generate BibTeX entries for these?
  - Read full papers and summarize?
  - Search for more specific subtopics?
```

### For Documentation:

```
=== Documentation Found: [Topic] ===

📖 Official Resources:
- [Link with description]

📚 Tutorials/Guides:
- [Link with description]

💻 Code Examples:
- [Link with description]

📝 Summary:
[Key information extracted]

🔗 Most Useful Links:
1. [URL] - [Why it's useful]
2. [URL] - [Why it's useful]
```

### For General Information:

```
=== Information Found: [Topic] ===

📋 Summary:
[Concise explanation of the concept/topic]

🔍 Key Points:
- [Important point 1]
- [Important point 2]
- [Important point 3]

📚 Authoritative Sources:
- [Source 1 with link]
- [Source 2 with link]

🔗 Further Reading:
- [URL] - [Description]

💡 Relevance to Thesis:
[How this information relates to your research]
```

6. **Offer follow-up actions:**

After presenting results:
- Offer to fetch and summarize specific papers
- Offer to generate BibTeX entries
- Offer to search for related topics
- Offer to find competing or alternative approaches

### Search Strategies by Topic:

**For this thesis, common searches:**

1. **Synthetic Data Generation:**
   - "synthetic clinical text generation 2024"
   - "LLM medical data synthesis"
   - "synthetic EHR generation"

2. **Privacy:**
   - "differential privacy medical records"
   - "re-identification attack healthcare"
   - "privacy preserving clinical NLP"

3. **Weak Supervision:**
   - "weak supervision medical NLP"
   - "label functions clinical text"
   - "silver annotations healthcare"

4. **Datasets:**
   - "MIMIC-III clinical notes"
   - "E3C corpus"
   - "medical NLP datasets 2024"

5. **Competing Work:**
   - "KnowledgeSG synthetic data"
   - "knowledge graph medical data generation"

6. **Tools/Libraries:**
   - "PyTorch differential privacy"
   - "spaCy medical models"
   - "clinical NLP libraries"

### Important Context:

**Thesis topic:** Synthetic Data Generation for Clinical NLP
**Key areas:** Privacy, weak supervision, facsimile documents, utility-privacy trade-offs
**Current focus:** Privacy chapter, conclusion, formatting

**When searching, prioritize:**
- Recent work (2023-2025) for fast-moving areas
- Foundational papers for established methods
- Competing approaches (fair representation)
- Practical implementations and code

### Quality Assessment:

When presenting papers, indicate quality:
- **Top-tier:** ACL, EMNLP, NeurIPS, ICML, Nature, NEJM
- **Good venues:** Domain workshops, specialized journals
- **Preprints:** ArXiv (note: not peer-reviewed yet)
- **Technical:** Company blogs (OpenAI, Anthropic) - useful but cite carefully

### Search Tips:

**Effective search patterns:**
- `"exact phrase"` - for specific terms
- `site:arxiv.org` - limit to specific site
- `filetype:pdf` - find PDF papers directly
- `intitle:"differential privacy"` - term must be in title
- `2024..2025` - date range (Google)

**Venues to search:**
- ArXiv (preprints)
- ACL Anthology (NLP papers)
- Google Scholar (broad academic)
- PubMed/PMC (medical)
- OpenReview (conference reviews)

### Never:

- Don't claim to have read papers you haven't fetched
- Don't make up paper titles or authors
- Don't suggest papers without providing links
- Don't recommend low-quality or non-academic sources for key claims
- Don't ignore user's specific search requirements

### Output Format:

Be organized and actionable:
- Clearly categorize results by relevance
- Provide working links
- Explain why each result matters
- Offer concrete next steps
- Format for easy copying (BibTeX keys, URLs)

### Follow-up Actions:

After search, offer to:
1. **Fetch and summarize** specific papers
2. **Generate BibTeX entries** for selected papers
3. **Compare papers** side-by-side
4. **Search deeper** on specific subtopics
5. **Find implementations** or code repositories
6. **Check citations** (what papers cite this work?)

### Integration with Other Skills:

- After finding papers → offer `/biblio-review` to assess coverage
- If find LaTeX documentation → apply to thesis
- If find competing work → suggest where to discuss in thesis
