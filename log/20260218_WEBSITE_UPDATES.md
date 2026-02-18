# Website Updates — 2026-02-18

## Summary

Updated the project website (`index.html`) with two new learning resources and a complete redesign of the footer Acknowledgments section to improve transparency, accountability, and integrity in the use of AI.

## More Resources (2 new entries)

- **AI Ethics** (DataCamp course) — Core principles of ethical AI, strategies to minimize biases, and methods to build user trust. Category: AI for Economics.
- **Using AI Tools Ethically in Research & Education** (YouTube video by Dr Amina Yonis, Dubai AI Week 2025) — Plays in embedded video modal. Category: AI for Economics.

Total resources: 20 (was 18).

## Acknowledgments Section (complete redesign)

Replaced the old "AI Content Disclaimer" with a structured "Acknowledgments" section containing four subsections:

### Purpose & Responsibility

- Purpose statement: "AI tools were used to make high-quality educational materials more accessible and to reduce barriers for students worldwide."
- Responsibility statement: "All AI-generated content was reviewed, edited, and approved by Carlos Mendez. This author takes full responsibility for the accuracy and quality of all content in this project, including materials produced with the assistance of AI tools."

### AI Tools (with hyperlinks and model versions)

| Content Type | Tool | Model | Link |
|---|---|---|---|
| Visual Summaries | Google Gemini | Gemini 3.0 Pro | gemini.google.com |
| Podcast | Google NotebookLM | Gemini 3.0 Pro | notebooklm.google.com |
| Video Overviews | Google NotebookLM | Gemini 3.0 Pro | notebooklm.google.com |
| AI Slides | Google NotebookLM | Gemini 3.0 Pro | notebooklm.google.com |
| Quiz & AI Tutor | Google NotebookLM + EdCafe AI | Gemini 3.0 Pro | notebooklm.google.com, edcafe.ai |
| Website & Notebooks | Claude Code (Anthropic) | Claude Opus 4.6 | claude.ai/code |

Timestamp: "Tool versions as of February 2026."

### Datasets, Examples, and PDF Slides

- Originally created (and shared with permission) by A. Colin Cameron.

### License

- CC BY-NC-SA 4.0 (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International)
- Includes official badge image and link to the deed.

### Disclaimer (closing)

- AI content accuracy disclaimer with "Found an issue? Submit feedback on GitHub" cross-reference linking to the GitHub issues page.

## Pinned Resources ("Must check" feature)

Added a pinning system to the More Resources section. Pinned resources:
- Always appear first in any filtered view (sorted above non-pinned)
- Display an amber "Must check" badge with thumbtack icon next to the type badge
- Are never hidden by the "Show More" button

Pinned resources (4):
1. **Using AI Tools Ethically in Research & Education** (ai/video)
2. **AI Ethics** (ai/course)
3. **AI for Economists** (ai/website)
4. **Python Programming for Economics and Finance** (python/course)

Implementation: `pinned: true` property on resource objects, sort in `renderResources()`, badge in `createResourceCard()`.

## Files Modified

- `index.html` — resources, acknowledgments, and pinning feature
