# Standardization Checklist for CH09-17

**Purpose**: Prevent issues encountered in CH08 standardization
**Created**: February 7, 2026
**Applies to**: Chapters 09-17 (remaining chapters)

Use this checklist BEFORE and DURING standardization to avoid common pitfalls.

---

## Pre-Standardization Analysis (5 minutes)

**Before making any changes:**

- [ ] Read chapter to understand its current structure
- [ ] Check if Chapter Overview exists and has "What you'll learn:" bullets
  - ✅ If YES: Do NOT add separate Learning Objectives section
  - ⚠️ If NO: Add standalone Learning Objectives section (6-10 bullets)
- [ ] Identify chapter structure:
  - [ ] Standard (regular content + separate case studies) → Add X.11 section
  - [ ] Integrated (sections ARE case studies like CH08) → Document in Overview
  - [ ] Other → Document and flag for review

**Commands to run:**
```bash
# View chapter structure
head -50 notebooks_colab/ch##_*.ipynb

# Run baseline verification
cd .claude/skills/chapter-standard
python scripts/verify_chapter.py ch##
```

---

## During Standardization

**After each major addition:**

- [ ] Run verification (`/chapter-standard ch##`) to check progress
- [ ] Address any CRITICAL issues immediately
- [ ] Check for redundancy warnings

**If chapter uses integrated case study structure:**

- [ ] Add design note to Chapter Overview explaining structure
  ```markdown
  **Design Note:** This chapter uses an integrated case study structure where
  sections X.1-X.N ARE the case studies [list domains]. Unlike other chapters
  that have regular content sections plus a separate "Case Studies" section,
  this chapter's entire focus is on applying [topic] to diverse real-world
  problems. This intentional structure maximizes hands-on experience.
  ```
- [ ] Document deviation in log file
- [ ] Accept -5 points (MINOR, still publication-ready)

---

## Post-Standardization Verification

**Before considering chapter complete:**

- [ ] Run `/chapter-standard ch##`
- [ ] Confirm CRITICAL issues = 0
- [ ] Verify score ≥ 80/100 (Good tier or higher)
- [ ] Check for Learning Objectives redundancy warning
- [ ] Verify PDF generates successfully (1.0-2.0 MB)

**Expected compliance:**
- Target: 85-90/100 (Good to Exemplary)
- Minimum acceptable: 80/100 (Good tier)
- Time estimate: 2.5-3.0 hours per chapter

---

## Common Pitfalls (Learned from CH08)

### ❌ DON'T:

1. **Add Learning Objectives when Chapter Overview has "What you'll learn"**
   - Causes redundancy (CRITICAL -10 points)
   - Template allows EITHER Learning Objectives OR integrated Overview (not both)
   - CH06-08 use integrated Overview format

2. **Force X.11 Case Studies section on integrated case study chapters**
   - Some chapters (like CH08) have sections 1-4 AS case studies
   - Adding separate X.11 would be redundant
   - Instead: document the intentional design in Chapter Overview

3. **Skip documenting intentional deviations from template**
   - If chapter structure differs, explain WHY in design note
   - Helps future readers understand the choice
   - Reduces confusion during review

4. **Wait until end to run verification**
   - Run verification after each major phase
   - Fix issues immediately when detected
   - Prevents compounding errors

5. **Ignore MINOR issues**
   - MINOR issues still impact score (-5 points each)
   - Some are easy to fix (transitions, design notes)
   - Aim for 0 CRITICAL, <3 MINOR

### ✅ DO:

1. **Choose EITHER Learning Objectives OR integrated Overview (not both)**
   - Read existing chapter first
   - If Overview has "What you'll learn" → don't add separate Learning Objectives
   - If no "What you'll learn" → add Learning Objectives section

2. **Document design choices in Chapter Overview**
   - Explain any deviation from standard template
   - Use "Design Note:" prefix for clarity
   - Reference similar chapters if applicable

3. **Run verification after each major phase**
   - Baseline verification before changes
   - Verify after adding Learning Objectives/Overview
   - Verify after adding Key Concepts
   - Verify after adding Practice Exercises
   - Final verification before PDF generation

4. **Accept -5 points for documented deviations**
   - Integrated case study structure: -5 points (acceptable)
   - Few transition notes: -5 points (can address easily)
   - Don't force changes that break pedagogical flow

5. **Use templates from CH06-08 for consistency**
   - Key Concept format: `> **Key Concept:**` (no emoji)
   - Practice Exercises: 8 progressive exercises
   - Key Takeaways: 6 thematic groups with bullets

---

## Quick Reference: Template Requirements

### Learning Objectives vs. Chapter Overview

**Option 1 (Legacy CH01-05):**
- Cell 1: `## Learning Objectives` (6-10 bullets)
- Cell 2: `## Chapter Overview` (intro only, no "What you'll learn")

**Option 2 (Recommended CH06+):**
- Cell 1/2: `## Chapter Overview` (intro + "What you'll learn:" + outline)
- No separate Learning Objectives section

**CRITICAL ERROR:** Having both → -10 points

### Case Study Structures

**Standard (most chapters):**
- X.1-X.N: Regular content sections
- X.11: Case Studies (6 tasks, 2-3 Key Concepts)

**Integrated (CH08-like):**
- X.1-X.N: ARE the case studies
- No X.11 section
- MUST have design note in Chapter Overview

**CRITICAL ERROR:** Missing both → -15 points

### Key Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Total cells | 45-75 | CH08 has 73 after fixes |
| Markdown ratio | 70-80% | CH08: 74% |
| Key Concepts | 7-11 | Distributed evenly |
| Practice Exercises | 6-10 | Progressive difficulty |
| Compliance score | ≥80/100 | Good tier minimum |
| PDF size | 1.0-2.0 MB | CH08: 1.67 MB |

---

## Verification Commands

**Run baseline check:**
```bash
cd .claude/skills/chapter-standard
python scripts/verify_chapter.py ch## > ../../log/ch##_baseline.txt
```

**Run updated verification (after fixes):**
```bash
python scripts/verify_chapter.py ch## > ../../log/ch##_final.txt
```

**Compare before/after:**
```bash
diff log/ch##_baseline.txt log/ch##_final.txt
```

---

## Example Workflow (2.5-3.0 hours)

1. **Baseline & Backup** (5 min)
   - Create timestamped backup
   - Run baseline verification
   - Document starting score

2. **Learning Objectives/Overview** (15 min)
   - Check if Overview has "What you'll learn"
   - If YES: enhance existing bullets
   - If NO: add Learning Objectives section
   - **Verify no redundancy**

3. **Key Concepts** (30-40 min)
   - Add 7-9 Key Concept boxes
   - Distribute evenly across sections
   - Use template format (no emoji)

4. **Key Takeaways** (15 min)
   - Restructure or enhance existing summary
   - 6 thematic groups with bullets
   - Add "Next Steps" and "You have mastered" closing

5. **Practice Exercises** (30 min)
   - Add 8 progressive exercises
   - Cover all major topics
   - Final exercise is comprehensive synthesis

6. **Verification & PDF** (20 min)
   - Run verification, confirm score ≥80
   - Generate PDF (nbconvert → inject CSS → Playwright)
   - Verify PDF size 1.0-2.0 MB

7. **Documentation & Commit** (15-20 min)
   - Create comprehensive log file
   - Commit with detailed message
   - Update README if needed

---

## Success Criteria

| Criterion | Target | How to Verify |
|-----------|--------|---------------|
| CRITICAL issues | 0 | Verification report |
| Compliance score | ≥80/100 | Verification report |
| No redundancy | ✅ | No Learning Obj redundancy warning |
| PDF generated | Yes | File exists, 1.0-2.0 MB |
| Documentation | Complete | Log file exists with metrics |
| Time | ≤3.0 hrs | Track actual time spent |

---

## Lessons from CH06-08

**CH06** (61→88, Good tier):
- Pilot chapter validated workflow
- Section ordering issue discovered
- 2.5 hours actual time

**CH07** (49→93, Exemplary tier):
- Applied correct section ordering
- Used template-compliant formats
- 3.0 hours actual time

**CH08** (49→85, Good tier):
- **Issue 1**: Added redundant Learning Objectives ❌
- **Issue 2**: Integrated case study structure not documented initially ⚠️
- **Fixes**: Removed redundancy, added design note ✅
- 2.5 hours + 2.0 hours fixes = 4.5 hours total

**Key Insight**: Following this checklist prevents the 2.0-hour fix overhead!

---

## Questions to Ask Before Starting

1. Does this chapter already have a Chapter Overview with "What you'll learn:" bullets?
   - YES → Don't add Learning Objectives section
   - NO → Add Learning Objectives section

2. What is the chapter's natural structure?
   - Regular content → Plan for X.11 Case Studies
   - Case study focused → Plan for integrated structure + design note

3. What's the current baseline score?
   - <50: Expect 3.0+ hours
   - 50-70: Expect 2.5-3.0 hours
   - 70+: Expect 2.0-2.5 hours

4. Are there any chapter-specific quirks?
   - Document them in the plan
   - Add to design note if significant
   - Flag for user review if uncertain

---

**Ready to start? Follow this checklist step-by-step to standardize CH09-17 efficiently and correctly!**

**Remember:** It's better to spend 5 minutes checking for redundancy upfront than 2 hours fixing it later!
