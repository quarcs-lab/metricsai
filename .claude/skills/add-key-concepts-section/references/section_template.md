# Quarto markdown skeleton for the Key Concepts section

This file is the **single source of truth** for the Quarto fence syntax used by the section. If Quarto's recommended nesting depth ever changes, edit this file and re-run the skill on each chapter — no other files need to change.

## Per-concept block

Each concept renders as one of these blocks. The skill replaces `{TERM}`, `{DEFINITION}`, `{EXAMPLE}`, and `{ANALOGY}` with drafted content.

```markdown
**{TERM}:** {DEFINITION}

::::: {.columns}
:::: {.column width="50%"}
::: {.callout-tip collapse="true" appearance="simple" title="Example"}
{EXAMPLE}
:::
::::
:::: {.column width="50%"}
::: {.callout-note collapse="true" appearance="simple" title="Analogy"}
{ANALOGY}
:::
::::
:::::
```

**Fence depth rules (must respect):**

- Outer wrapper for `.columns` uses **5 colons**: `:::::`.
- Each `.column` uses **4 colons**: `::::`.
- Each callout (`.callout-tip` / `.callout-note`) uses **3 colons**: `:::`.

This explicit nesting depth was tested in the chapter 1 pilot — Quarto rendered without "fence not closed" warnings in both light and dark themes.

## Section wrapper

The skill wraps N concept blocks with this header and intro:

```markdown
## Key Concepts

{N_WORD} core ideas anchor this chapter. Skim them before you start, and come back when a term feels fuzzy. Each entry pairs a concrete example using the chapter's data with a non-technical analogy. Click a panel to expand it.

{CONCEPT_BLOCK_1}

{CONCEPT_BLOCK_2}

...

{CONCEPT_BLOCK_N}
```

`{N_WORD}` is the spelled-out count: "Five", "Six", "Seven", or "Eight".

A single blank line separates consecutive concept blocks. A blank line precedes `## Setup` (the next section).

## Insertion contract

The skill inserts the assembled section **between `## Chapter Overview` and `## Setup`**. Anchor for the `Edit` tool: the literal string `"\n\n## Setup"` preceded by the chapter outline's last bullet (which the skill reads from the .qmd to ensure uniqueness).

Old string in the Edit:

```
- {LAST_BULLET_OF_CHAPTER_OUTLINE}

## Setup
```

New string:

```
- {LAST_BULLET_OF_CHAPTER_OUTLINE}

{ASSEMBLED_KEY_CONCEPTS_SECTION}

## Setup
```

## What NOT to include

- **No "Tip" line** about Colab degradation. The export script (`scripts/export_qmd_to_ipynb.py:strip_key_concepts`) removes the entire section from `.ipynb` automatically; readers in Colab never see it, so a Colab-targeted tip is misleading. (This was the chapter 1 follow-up cleanup — do not re-introduce.)
- **No section number** (e.g., not `## 1.0 Key Concepts`). The section is a glossary, not a content step.
- **No images** inside callouts.
- **No code cells** inside callouts. (Inline `` `code` `` formatting is fine; fenced ``` ```python ``` ``` blocks are not.)
