#!/usr/bin/env python3
"""
Chapter Standard Verification Script
Verifies individual chapter notebooks against metricsAI template standard
Extended from verify_ch01_04_consistency.py with single-chapter mode
"""

import json
import re
import glob
import sys
from pathlib import Path

# ============================================================================
# EXISTING FUNCTIONS (from verify_ch01_04_consistency.py)
# ============================================================================

def find_notebook(chapter_prefix):
    """Find notebook file matching chapter prefix"""
    pattern = f'notebooks_colab/{chapter_prefix}_*.ipynb'
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No notebook found for {chapter_prefix}")
    return matches[0]

def check_visual_summary(cell):
    """Check if Cell 0 contains visual summary image"""
    if cell['cell_type'] != 'markdown':
        return {'present': False, 'reason': 'Cell 0 is not markdown'}

    content = ''.join(cell['source'])

    # Check for visual summary image
    if 'visual_summary' in content.lower() and '<img' in content:
        # Extract width
        width_match = re.search(r'width="(\d+%?)"', content)
        width = width_match.group(1) if width_match else 'unknown'
        return {
            'present': True,
            'width': width,
            'type': 'Full visual summary'
        }
    elif 'Open In Colab' in content or 'colab' in content.lower():
        return {
            'present': False,
            'type': 'Colab badge only',
            'reason': 'Has Colab badge but no visual summary image'
        }
    else:
        return {
            'present': False,
            'reason': 'No visual summary detected'
        }

def extract_section_numbers(nb):
    """Extract section numbering pattern from headers"""
    sections = []

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])
            # Find headers like "## 1.1", "## 2.3", etc.
            matches = re.findall(r'^##\s+(\d+\.\d+)\s+', content, re.MULTILINE)
            for match in matches:
                sections.append({
                    'number': match,
                    'cell': i,
                    'major': int(match.split('.')[0]),
                    'minor': int(match.split('.')[1])
                })

    return sections

def find_section_gaps(sections):
    """Identify gaps in section numbering"""
    if not sections:
        return []

    gaps = []
    major = sections[0]['major']

    # Group by major section
    by_major = {}
    for s in sections:
        if s['major'] not in by_major:
            by_major[s['major']] = []
        by_major[s['major']].append(s['minor'])

    # Check for gaps within each major section
    for maj, minors in by_major.items():
        minors_sorted = sorted(minors)
        for i in range(len(minors_sorted) - 1):
            current = minors_sorted[i]
            next_num = minors_sorted[i + 1]
            if next_num - current > 1:
                for missing in range(current + 1, next_num):
                    gaps.append(f"{maj}.{missing}")

    return gaps

def count_key_concepts(nb):
    """Count and locate Key Concept boxes"""
    key_concepts = []

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])
            # Look for Key Concept boxes (blockquote format)
            if re.search(r'>\s*\*\*Key Concept', content, re.IGNORECASE):
                # Extract topic (handles both "Key Concept: Title" and "Key Concept X.N: Title")
                topic_match = re.search(r'Key Concept(?:\s+\d+\.\d+)?:?\*?\*?\s*(.+)', content, re.IGNORECASE)
                topic = topic_match.group(1).strip() if topic_match else 'Unknown'
                key_concepts.append({
                    'cell': i,
                    'topic': topic[:60]  # Truncate long topics
                })

    return key_concepts

def analyze_case_study(nb):
    """Analyze case study structure if present"""
    case_study = {
        'present': False,
        'section_number': None,
        'start_cell': None,
        'tasks': 0,
        'task_labels': [],
        'key_concepts': 0,
        'difficulty_labels': False
    }

    # Look for case study section
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])
            # Check for case study section header (with or without section number)
            # Matches: "## 5.12 Case Studies" OR "## Case Study: Title"
            if re.search(r'##\s+(?:\d+\.\d+\s+)?Case Stud(?:y|ies)', content, re.IGNORECASE):
                section_match = re.search(r'##\s+(\d+\.\d+)', content)
                case_study['present'] = True
                case_study['section_number'] = section_match.group(1) if section_match else 'No section number'
                case_study['start_cell'] = i

                # Count tasks in remaining cells
                for j in range(i, len(nb['cells'])):
                    task_content = ''.join(nb['cells'][j]['source']) if nb['cells'][j]['cell_type'] == 'markdown' else ''

                    # Count tasks (looking for "Task 1", "Task 2", etc.)
                    task_match = re.search(r'####\s+Task\s+(\d+)', task_content)
                    if task_match:
                        case_study['tasks'] += 1
                        task_num = task_match.group(1)

                        # Check for difficulty labels
                        label_match = re.search(r'\((GUIDED|SEMI-GUIDED|MORE INDEPENDENT|INDEPENDENT|Guided|Semi-guided|More Independent|Independent)\)', task_content)
                        if label_match:
                            case_study['difficulty_labels'] = True
                            case_study['task_labels'].append({
                                'task': int(task_num),
                                'label': label_match.group(1),
                                'cell': j
                            })

                    # Count Key Concepts within case study
                    if re.search(r'>\s*\*\*Key Concept', task_content, re.IGNORECASE):
                        case_study['key_concepts'] += 1

                break

    return case_study

def check_front_matter(nb):
    """Verify presence of standard front matter sections"""
    front_matter = {
        'title': False,
        'chapter_overview': False,
        'chapter_overview_has_learning_content': False,
        'chapter_overview_has_datasets': False,
        'chapter_overview_has_outline': False,
        'setup': False
    }

    # Check first 6 cells for front matter
    for i in range(min(6, len(nb['cells']))):
        if nb['cells'][i]['cell_type'] == 'markdown':
            content = ''.join(nb['cells'][i]['source'])

            if i == 0 and re.search(r'#\s+Chapter\s+\d+', content, re.IGNORECASE):
                front_matter['title'] = True

            if re.search(r'##\s+Chapter Overview', content, re.IGNORECASE):
                front_matter['chapter_overview'] = True

                # Check for learning content ("What you'll learn", "By the end", etc.)
                if re.search(r"What you'?ll learn|By the end of this chapter|learning objective", content, re.IGNORECASE):
                    front_matter['chapter_overview_has_learning_content'] = True

                # Check for datasets section
                if re.search(r'dataset|data.*used', content, re.IGNORECASE):
                    front_matter['chapter_overview_has_datasets'] = True

                # Check for outline (section numbers like X.1, X.2)
                if re.search(r'\d+\.\d+', content):
                    front_matter['chapter_overview_has_outline'] = True

            if re.search(r'##\s+.*Setup', content, re.IGNORECASE) or '🔧' in content:
                front_matter['setup'] = True

    return front_matter

def check_closing_sections(nb):
    """Check for Key Takeaways and Practice Exercises"""
    closing = {
        'key_takeaways': False,
        'key_takeaways_cell': None,
        'practice_exercises': False,
        'practice_exercises_cell': None,
        'practice_exercises_count': 0,
        'empty_closing_cell': False,
        'case_studies_before_exercises': False  # NEW: track ordering issue
    }

    # Check ALL cells for closing sections (not just last 20)
    # These sections can appear before Case Studies in some chapters
    start_idx = 0

    for i in range(start_idx, len(nb['cells'])):
        if nb['cells'][i]['cell_type'] == 'markdown':
            content = ''.join(nb['cells'][i]['source'])

            if re.search(r'##\s+Key Takeaways', content, re.IGNORECASE):
                closing['key_takeaways'] = True
                closing['key_takeaways_cell'] = i

            if re.search(r'##\s+Practice Exercises', content, re.IGNORECASE):
                closing['practice_exercises'] = True
                closing['practice_exercises_cell'] = i
                # Count exercises (looking for "**Exercise N:**")
                exercises = re.findall(r'\*\*Exercise\s+\d+:', content, re.IGNORECASE)
                closing['practice_exercises_count'] = len(exercises)

            # Check if cell is empty or nearly empty
            if len(content.strip()) < 10:
                closing['empty_closing_cell'] = True

    return closing

def count_transition_cells(nb):
    """Count cells that appear to be transitions between sections"""
    transitions = 0

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source']).lower()
            # Look for transition language
            if any(phrase in content for phrase in [
                'having',
                'now that',
                'next,',
                'moving on',
                'let us now',
                'with this understanding',
                'building on'
            ]):
                # Check if it's a short cell (< 200 chars, typical for transitions)
                if len(content) < 200:
                    transitions += 1

    return transitions

# ============================================================================
# NEW FUNCTIONS (for chapter-standard skill)
# ============================================================================

def check_interpretation_placement(nb):
    """
    Verify that markdown cells following code cells are within correct section boundaries.

    Pattern to verify:
    1. Code cell executes in Section X.Y
    2. Markdown cell (interpretation) follows
    3. Interpretation must be within Section X.Y boundaries (before next section header)

    Returns:
        List of potential misplacements with cell numbers, section context, and preview
    """
    issues = []


    current_section = None
    section_start_cell = None

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])

            # Track section boundaries (## X.Y)
            section_match = re.match(r'^##\s+(\d+\.\d+)\s+', content, re.MULTILINE)
            if section_match:
                current_section = section_match.group(1)
                section_start_cell = i
                continue

        # Check if markdown follows code
        if cell['cell_type'] == 'markdown' and i > 0:
            prev_cell = nb['cells'][i-1]
            if prev_cell['cell_type'] == 'code':
                content = ''.join(cell['source']).strip()

                # Check if likely an interpretation (not a section header, substantial text)
                if (content and
                    not content.startswith('#') and
                    len(content) > 50 and
                    not content.startswith('>')):  # Not a Key Concept box

                    # Calculate distance from section start
                    distance = i - section_start_cell if section_start_cell else None

                    # Flag if far from section start (potential drift)
                    if distance and distance > 8:
                        issues.append({
                            'cell': i,
                            'prev_code_cell': i-1,
                            'current_section': current_section,
                            'section_start_cell': section_start_cell,
                            'distance_from_section_start': distance,
                            'preview': content[:100] + '...' if len(content) > 100 else content,
                            'warning': f'Interpretation text {distance} cells after Section {current_section} start - verify correct section placement'
                        })

    return issues

def check_header_hierarchy(nb):
    """
    Verify proper header hierarchy (H1→H2→H3→H4).
    Ensures no skipped levels and Case Studies use proper structure.
    """
    issues = []


    prev_level = 0

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])

            # Find all headers in this cell
            for line in content.split('\n'):
                header_match = re.match(r'^(#{1,6})\s+(.+)', line)
                if header_match:
                    level = len(header_match.group(1))
                    text = header_match.group(2)

                    # Check for skipped levels
                    if level > prev_level + 1:
                        issues.append({
                            'cell': i,
                            'issue': f'Skipped header level: H{prev_level} → H{level}',
                            'text': text,
                            'line': line
                        })

                    prev_level = level

    return issues

def calculate_compliance_score(findings):
    """
    Calculate 0-100 compliance score based on findings.

    Scoring:
        CRITICAL issues: -10 points each (max -40)
        MINOR issues: -5 points each (max -25)
        SUGGESTIONS: -2 points each (max -10)
    """
    score = 100

    # CRITICAL issues (-10 each, max -60)
    critical_deductions = 0

    if not findings['visual_summary']['present']:
        critical_deductions += 10

    if not findings['front_matter']['chapter_overview']:
        critical_deductions += 10
    elif not findings['front_matter']['chapter_overview_has_learning_content']:
        critical_deductions += 10  # Chapter Overview must include learning content
    elif not findings['front_matter']['chapter_overview_has_datasets'] or not findings['front_matter']['chapter_overview_has_outline']:
        critical_deductions += 5  # Incomplete overview is MINOR, not CRITICAL

    if not findings['case_study']['present']:
        css = findings.get('case_study_structure', {})
        if not (css.get('structure_type') == 'integrated' and css.get('documented')):
            critical_deductions += 10  # Missing case study is CRITICAL

    if not findings['closing']['key_takeaways']:
        critical_deductions += 10

    if not findings['closing']['practice_exercises']:
        critical_deductions += 10

    score -= min(critical_deductions, 60)

    # MINOR issues (-5 each, max -25)
    minor_deductions = 0

    # Section numbering gaps (undocumented)
    if findings['section_gaps']:
        minor_deductions += 5

    # Key Concept count outside range
    kc_count = len(findings['key_concepts'])
    if kc_count < 7 or kc_count > 11:
        minor_deductions += 5

    # Cell count outside range
    if findings['total_cells'] < 45 or findings['total_cells'] > 75:
        minor_deductions += 5

    # Misplaced interpretations
    if findings.get('misplaced_interpretations'):
        count = len(findings['misplaced_interpretations'])
        minor_deductions += min(count * 2, 10)  # -2 each, max -10

    # Missing transition notes
    if findings['transition_cells'] < 2:
        minor_deductions += 5

    

    # Case Studies should come AFTER Practice Exercises
    if findings['case_study']['present'] and findings['closing']['practice_exercises']:
        case_study_cell = findings['case_study']['start_cell']
        exercises_cell = findings['closing']['practice_exercises_cell']
        if case_study_cell is not None and exercises_cell is not None:
            if case_study_cell < exercises_cell:
                minor_deductions += 5  # Wrong ordering

    score -= min(minor_deductions, 25)

    # SUGGESTIONS (-2 each, max -10)
    suggestion_deductions = 0

    # Markdown ratio outside range
    md_ratio = findings['markdown_cells'] / findings['total_cells'] if findings['total_cells'] > 0 else 0
    if md_ratio < 0.70 or md_ratio > 0.80:
        suggestion_deductions += 2

    # Empty closing cell missing
    if not findings['closing']['empty_closing_cell']:
        suggestion_deductions += 2

    # Practice Exercises count outside range
    if findings['closing']['practice_exercises_count'] < 6 or findings['closing']['practice_exercises_count'] > 10:
        suggestion_deductions += 2

    score -= min(suggestion_deductions, 10)

    return max(0, score)

def generate_report(findings, output_format='markdown'):
    """
    Generate human-readable or JSON report.

    Args:
        findings: Dictionary of verification findings
        output_format: 'markdown' or 'json'

    Returns:
        Formatted report string
    """
    if output_format == 'json':
        return json.dumps(findings, indent=2)

    # Markdown report
    report = []
    chapter_num = findings.get('chapter_prefix', 'Unknown')
    file_name = findings['file']

    report.append(f"# Chapter Verification Report: {file_name}")
    report.append(f"\n**Compliance Score**: {findings['compliance_score']}/100")

    # Score tier
    score = findings['compliance_score']
    if score >= 90:
        tier = "⭐⭐⭐⭐⭐ Exemplary (publication-ready)"
    elif score >= 80:
        tier = "⭐⭐⭐⭐ Good (minor fixes needed)"
    elif score >= 70:
        tier = "⭐⭐⭐ Acceptable (improvements needed)"
    elif score >= 60:
        tier = "⭐⭐ Needs work (significant issues)"
    else:
        tier = "⭐ Not compliant (major restructuring)"

    report.append(f"**Tier**: {tier}\n")

    # CRITICAL issues
    critical = collect_critical_issues(findings)
    if critical:
        report.append("## ❌ CRITICAL Issues (Must Fix)\n")
        for issue in critical:
            report.append(f"- **{issue['title']}**")
            report.append(f"  - {issue['description']}")
            if 'fix' in issue:
                report.append(f"  - Fix: {issue['fix']}")
            if 'reference' in issue:
                report.append(f"  - Reference: {issue['reference']}")
            report.append("")
    else:
        report.append("## ✅ CRITICAL Issues\nNone found!\n")

    # MINOR issues
    minor = collect_minor_issues(findings)
    if minor:
        report.append("## ⚠️ MINOR Issues (Should Fix)\n")
        for issue in minor:
            report.append(f"- **{issue['title']}**")
            report.append(f"  - {issue['description']}")
            if 'fix' in issue:
                report.append(f"  - Fix: {issue['fix']}")
            report.append("")
    else:
        report.append("## ✅ MINOR Issues\nNone found!\n")

    # SUGGESTIONS
    suggestions = collect_suggestions(findings)
    if suggestions:
        report.append("## 💡 SUGGESTIONS (Nice to Have)\n")
        for suggestion in suggestions:
            report.append(f"- **{suggestion['title']}**")
            report.append(f"  - {suggestion['description']}")
            report.append("")
    else:
        report.append("## ✅ SUGGESTIONS\nNone!\n")

    # Auto-fixable items
    auto_fixable = identify_auto_fixable(findings)
    if auto_fixable:
        report.append("## 🔧 Auto-Fixable Items\n")
        report.append("The following can be fixed automatically with `--apply`:\n")
        for item in auto_fixable:
            report.append(f"- {item}")
        report.append(f"\nRun: `/chapter-standard {chapter_num} --apply`\n")

    # Summary metrics
    report.append("## 📊 Summary Metrics\n")
    report.append(f"- **Total cells**: {findings['total_cells']} (target: 45-75)")
    report.append(f"- **Markdown cells**: {findings['markdown_cells']} ({findings['markdown_cells']/findings['total_cells']*100:.0f}% | target: 70-80%)")
    report.append(f"- **Code cells**: {findings['code_cells']}")
    report.append(f"- **Key Concepts**: {len(findings['key_concepts'])} (target: 7-11)")
    if findings['case_study']['present']:
        report.append(f"- **Case Study**: ✅ Present (Section {findings['case_study']['section_number']}, {findings['case_study']['tasks']} tasks)")
    else:
        report.append(f"- **Case Study**: ❌ Not found")
    report.append(f"- **Practice Exercises**: {findings['closing']['practice_exercises_count']} (target: 6-10)")

    # Chapter Overview status
    if findings['front_matter']['chapter_overview']:
        overview_status = "✅ Present"
        if not findings['front_matter']['chapter_overview_has_learning_content']:
            overview_status += " (missing learning content)"
        report.append(f"- **Chapter Overview**: {overview_status}")
    else:
        report.append(f"- **Chapter Overview**: ❌ Not found")

    return '\n'.join(report)

def collect_critical_issues(findings):
    """Collect all CRITICAL issues from findings"""

    issues = []

    # Learning Objectives redundancy (CRITICAL)
    if findings.get('learning_obj_redundancy', {}).get('has_redundancy'):
        lr = findings['learning_obj_redundancy']
        issues.append({
            'title': 'Redundant Learning Objectives section detected',
            'description': f"Cell {lr['learning_obj_cell']} has separate Learning Objectives section, but Cell {lr['chapter_overview_cell']} Chapter Overview already contains 'What you\'ll learn' bullets",
            'fix': 'Remove the standalone Learning Objectives section (template allows EITHER separate Learning Objectives OR integrated in Chapter Overview, NOT both)',
            'reference': 'CH06 standardization removed redundant Learning Objectives'
        })



    if not findings['visual_summary']['present']:
        issues.append({
            'title': 'Missing visual summary image (Cell 0)',
            'description': f"Cell 0 has: {findings['visual_summary'].get('reason', 'Unknown issue')}",
            'fix': 'Add <img> tag with visual_summary.jpg',
            'reference': 'See CH02 Cell 0 or TEMPLATE_REQUIREMENTS.md'
        })

    if not findings['front_matter']['chapter_overview']:
        issues.append({
            'title': 'Missing Chapter Overview section',
            'description': 'No "## Chapter Overview" header found',
            'fix': 'Add Chapter Overview with: intro, learning content ("What you\'ll learn"), datasets used, chapter outline',
            'reference': 'See CH01/CH02 Chapter Overview (CRITICAL - this is a required template component)'
        })
    elif not findings['front_matter']['chapter_overview_has_learning_content']:
        issues.append({
            'title': 'Chapter Overview missing learning content',
            'description': 'Chapter Overview exists but does not include learning objectives/content',
            'fix': 'Add "What you\'ll learn:" section with bullet points describing learning outcomes',
            'reference': 'See CH01 Cell 2 or CH02 Cell 2 - both have "What you\'ll learn:" sections'
        })
    elif not findings['front_matter']['chapter_overview_has_datasets']:
        issues.append({
            'title': 'Chapter Overview missing datasets description',
            'description': 'Chapter Overview exists but does not list datasets used',
            'fix': 'Add "Datasets used:" section with dataset descriptions',
            'reference': 'See CH01/CH02 Chapter Overview'
        })
    elif not findings['front_matter']['chapter_overview_has_outline']:
        issues.append({
            'title': 'Chapter Overview missing chapter outline',
            'description': 'Chapter Overview exists but does not list chapter sections',
            'fix': 'Add "Chapter outline:" listing all sections (X.1, X.2, etc.)',
            'reference': 'See CH01/CH02 Chapter Overview'
        })
    # Check case study - but skip if integrated structure is documented
    css = findings.get('case_study_structure', {})
    if not findings['case_study']['present']:
        # Skip CRITICAL error if this is a documented integrated case study structure
        if css.get('structure_type') == 'integrated' and css.get('documented'):
            # This is handled in MINOR issues as INFO
            pass
        else:
            issues.append({
                'title': 'Missing Case Study section',
                'description': 'No "## X.Y Case Studies" section found',
                'fix': 'Add Case Study section with: research intro, 6 progressive tasks, wrap-up (or document integrated structure in Chapter Overview)',
                'reference': 'See CH02 Section 2.8 or MASTER_TEMPLATE_CHAPTER_STRUCTURE.md (If intentional, document exception)'
            })

    if not findings['closing']['key_takeaways']:
        issues.append({
            'title': 'Missing Key Takeaways section',
            'description': 'No "## Key Takeaways" header found',
            'fix': 'Add Key Takeaways section with 5-7 thematic groups',
            'reference': 'See CH02 Key Takeaways or TEMPLATE_REQUIREMENTS.md'
        })

    if not findings['closing']['practice_exercises']:
        issues.append({
            'title': 'Missing Practice Exercises section',
            'description': 'No "## Practice Exercises" header found',
            'fix': 'Add Practice Exercises section with 6-10 exercises',
            'reference': 'See CH02 Practice Exercises or TEMPLATE_REQUIREMENTS.md'
        })

    return issues

def collect_minor_issues(findings):
    """Collect all MINOR issues from findings"""
    issues = []

    # Case study structure (integrated vs standard) - MINOR
    if findings.get('case_study_structure'):
        css = findings['case_study_structure']
        if css['structure_type'] == 'integrated' and not css['has_case_study_section']:
            if css['documented']:
                # Documented integrated structure - add as INFO
                issues.append({
                    'title': f'Integrated case study structure detected (documented)',
                    'description': f'Sections are case studies (early section count: {css["early_section_count"]}). Design note documents this intentional deviation.',
                    'fix': 'No action needed - documented design choice',
                    'severity': 'INFO'
                })
            else:
                # Integrated but not documented - MINOR
                issues.append({
                    'title': f'Integrated case study structure (not documented)',
                    'description': f'Sections appear to be case studies (early section count: {css["early_section_count"]}), but no formal X.11 section and no design note explaining structure',
                    'fix': 'Add design note to Chapter Overview explaining intentional integrated case study structure',
                    'reference': 'CH08 uses documented integrated structure where sections 8.1-8.4 ARE the case studies'
                })
        elif not css['has_case_study_section'] and css['structure_type'] == 'unknown':
            # Missing case studies entirely - keep as existing CRITICAL issue
            pass

    


    # Section numbering gaps
    if findings['section_gaps']:
        issues.append({
            'title': f"Section numbering gaps: {', '.join(findings['section_gaps'])}",
            'description': 'Sections are not sequential',
            'fix': 'Document as reserved sections OR renumber sequentially'
        })

    # Key Concept count
    kc_count = len(findings['key_concepts'])
    if kc_count < 7:
        issues.append({
            'title': f'Key Concept count too low: {kc_count} (target: 7-11)',
            'description': f'Current locations: Cells {", ".join(str(kc["cell"]) for kc in findings["key_concepts"])}',
            'fix': f'Add {7 - kc_count} more Key Concept boxes in main content'
        })
    elif kc_count > 11:
        issues.append({
            'title': f'Key Concept count too high: {kc_count} (target: 7-11)',
            'description': f'Current locations: Cells {", ".join(str(kc["cell"]) for kc in findings["key_concepts"])}',
            'fix': 'Consider consolidating or removing some Key Concepts'
        })

    # Cell count
    if findings['total_cells'] < 45:
        issues.append({
            'title': f'Total cell count too low: {findings["total_cells"]} (target: 45-75)',
            'description': 'Chapter may lack sufficient content',
            'fix': 'Add more explanatory text, examples, or exercises'
        })
    elif findings['total_cells'] > 75:
        issues.append({
            'title': f'Total cell count too high: {findings["total_cells"]} (target: 45-75)',
            'description': 'Chapter may be too long',
            'fix': 'Consider splitting into multiple chapters or removing content'
        })

    # Misplaced interpretations
    if findings.get('misplaced_interpretations'):
        for interp in findings['misplaced_interpretations']:
            issues.append({
                'title': f"Potential misplaced interpretation: Cell {interp['cell']}",
                'description': interp['warning'],
                'fix': f"Verify Cell {interp['cell']} belongs to Section {interp['current_section']}"
            })

    # Missing transition notes
    if findings['transition_cells'] < 2:
        issues.append({
            'title': f'Few transition notes: {findings["transition_cells"]} (target: 2-4)',
            'description': 'Transitions help connect major sections',
            'fix': 'Add transition notes between major section groups'
        })

    # Case Studies should come AFTER Practice Exercises
    if findings['case_study']['present'] and findings['closing']['practice_exercises']:
        case_study_cell = findings['case_study']['start_cell']
        exercises_cell = findings['closing']['practice_exercises_cell']
        if case_study_cell is not None and exercises_cell is not None:
            if case_study_cell < exercises_cell:
                issues.append({
                    'title': f'Case Studies section comes BEFORE Practice Exercises',
                    'description': f'Case Studies at Cell {case_study_cell}, Practice Exercises at Cell {exercises_cell}',
                    'fix': 'Move Case Studies section to AFTER Practice Exercises (correct order: Key Takeaways → Practice Exercises → Case Studies)',
                    'reference': 'See CH01/CH02 structure: Case Studies is the last major section'
                })

    # Case study task count
    if findings['case_study']['present'] and findings['case_study']['tasks'] != 6:
        issues.append({
            'title': f"Case study task count: {findings['case_study']['tasks']} (target: 6)",
            'description': f"Section {findings['case_study']['section_number']} has wrong number of tasks",
            'fix': 'Add or remove tasks to reach 6 progressive tasks'
        })

    # Case study Key Concepts
    if findings['case_study']['present']:
        cs_kc = findings['case_study']['key_concepts']
        if cs_kc < 2 or cs_kc > 3:
            issues.append({
                'title': f"Case study Key Concepts: {cs_kc} (target: 2-3)",
                'description': 'Case studies should have 2-3 Key Concept boxes',
                'fix': 'Add or remove Key Concepts to reach 2-3'
            })

    return issues

def collect_suggestions(findings):
    """Collect all SUGGESTIONS from findings"""
    suggestions = []

    # Markdown ratio
    md_ratio = findings['markdown_cells'] / findings['total_cells'] if findings['total_cells'] > 0 else 0
    if md_ratio < 0.70:
        suggestions.append({
            'title': f'Markdown ratio low: {md_ratio*100:.0f}% (target: 70-80%)',
            'description': 'Consider adding more explanatory text'
        })
    elif md_ratio > 0.80:
        suggestions.append({
            'title': f'Markdown ratio high: {md_ratio*100:.0f}% (target: 70-80%)',
            'description': 'Consider adding more code examples'
        })

    # Empty closing cell
    if not findings['closing']['empty_closing_cell']:
        suggestions.append({
            'title': 'No empty closing cell',
            'description': 'Add empty markdown cell at end for visual spacing'
        })

    # Practice Exercises count
    pe_count = findings['closing']['practice_exercises_count']
    if pe_count < 6 and pe_count > 0:
        suggestions.append({
            'title': f'Practice Exercises count low: {pe_count} (target: 6-10)',
            'description': 'Consider adding more practice exercises'
        })
    elif pe_count > 10:
        suggestions.append({
            'title': f'Practice Exercises count high: {pe_count} (target: 6-10)',
            'description': 'Consider removing some exercises or splitting into categories'
        })

    return suggestions

def identify_auto_fixable(findings):
    """Identify issues that can be automatically fixed"""
    fixable = []

    if not findings['visual_summary']['present']:
        fixable.append("Add visual summary image template to Cell 0")

    kc_count = len(findings['key_concepts'])
    if kc_count < 7:
        fixable.append(f"Add {7 - kc_count} Key Concept placeholder boxes")

    if not findings['closing']['empty_closing_cell']:
        fixable.append("Add empty closing cell")

    return fixable


def check_learning_objectives_redundancy(nb):
    """
    Detect if both Learning Objectives section AND Chapter Overview
    with 'What you'll learn' exist (redundancy).

    Template allows EITHER:
    - Separate Learning Objectives section, OR
    - Chapter Overview with integrated "What you'll learn" bullets

    But NOT both.

    Returns:
        dict with 'has_redundancy', 'has_learning_objectives', 'has_chapter_overview_with_learning'
    """
    has_learning_objectives = False
    has_chapter_overview_with_learning = False
    learning_obj_cell = None
    chapter_overview_cell = None

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source'])

            # Check for standalone Learning Objectives section
            if re.search(r'^##\s+Learning Objectives', source, re.MULTILINE):
                has_learning_objectives = True
                learning_obj_cell = i

            # Check for Chapter Overview with "What you'll learn"
            if re.search(r'^##\s+Chapter Overview', source, re.MULTILINE):
                if "what you'll learn" in source.lower() or "what you will learn" in source.lower():
                    has_chapter_overview_with_learning = True
                    chapter_overview_cell = i

    has_redundancy = has_learning_objectives and has_chapter_overview_with_learning

    return {
        'has_redundancy': has_redundancy,
        'has_learning_objectives': has_learning_objectives,
        'has_chapter_overview_with_learning': has_chapter_overview_with_learning,
        'learning_obj_cell': learning_obj_cell,
        'chapter_overview_cell': chapter_overview_cell
    }

def check_case_study_structure(nb, chapter_num):
    """
    Detect if chapter uses integrated case study structure
    (like CH08) vs. standard structure with separate X.11 section.

    Integrated structure: Sections X.1-X.N are themselves case studies
    Standard structure: X.1-X.N content + X.11 Case Studies

    Args:
        nb: Notebook JSON
        chapter_num: Chapter number (e.g., 8 for ch08)

    Returns:
        dict with 'structure_type', 'has_case_study_section', 'early_section_count', 'documented'
    """
    sections = []
    has_design_note = False

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source'])

            # Find all section headers (e.g., "## 8.1", "## 8.2")
            matches = re.findall(rf'^##\s+{chapter_num}\.(\d+)', source, re.MULTILINE)
            sections.extend(matches)

            # Check for design note documenting integrated structure
            if 'design note' in source.lower() and 'integrated case study' in source.lower():
                has_design_note = True

    # Check if has formal X.11 (or X.10-X.20) Case Studies section
    has_case_study_section = any(
        int(s) >= 10 for s in sections if s.isdigit()
    )

    # Check if sections 1-4 suggest integrated case studies
    early_sections = [s for s in sections if s.isdigit() and int(s) <= 4]
    integrated_case_studies = len(early_sections) >= 3

    # Determine structure type
    if has_case_study_section:
        structure_type = 'standard'
    elif integrated_case_studies:
        structure_type = 'integrated'
    else:
        structure_type = 'unknown'

    return {
        'structure_type': structure_type,
        'has_case_study_section': has_case_study_section,
        'early_section_count': len(early_sections),
        'documented': has_design_note,
        'all_sections': sections
    }

def analyze_chapter(chapter_prefix):
    """
    Perform comprehensive analysis of a single chapter.

    Args:
        chapter_prefix: Chapter identifier (e.g., 'ch05')

    Returns:
        Dictionary of findings with all verification results
    """
    notebook_path = find_notebook(chapter_prefix)

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Run all checks
    findings = {
        'chapter_prefix': chapter_prefix,
        'file': Path(notebook_path).name,
        'total_cells': len(nb['cells']),
        'markdown_cells': sum(1 for c in nb['cells'] if c['cell_type'] == 'markdown'),
        'code_cells': sum(1 for c in nb['cells'] if c['cell_type'] == 'code'),
        'visual_summary': check_visual_summary(nb['cells'][0]) if nb['cells'] else {'present': False},
        'front_matter': check_front_matter(nb),
        'sections': extract_section_numbers(nb),
        'section_gaps': None,  # Computed below
        'key_concepts': count_key_concepts(nb),
        'case_study': analyze_case_study(nb),
        'learning_obj_redundancy': check_learning_objectives_redundancy(nb),
        'case_study_structure': check_case_study_structure(nb, int(chapter_prefix[2:])),
        'closing': check_closing_sections(nb),
        'transition_cells': count_transition_cells(nb),
        'header_hierarchy': check_header_hierarchy(nb),
        'misplaced_interpretations': check_interpretation_placement(nb)
    }

    # Compute section gaps
    findings['section_gaps'] = find_section_gaps(findings['sections'])

    # Calculate compliance score
    findings['compliance_score'] = calculate_compliance_score(findings)

    return findings

def verify_single_chapter(chapter_prefix, output_format='markdown'):
    """
    Main entry point for single chapter verification.

    Args:
        chapter_prefix: Chapter identifier (e.g., 'ch05')
        output_format: 'markdown' or 'json'

    Returns:
        Formatted report string
    """
    try:
        findings = analyze_chapter(chapter_prefix)
        report = generate_report(findings, output_format)
        return report
    except FileNotFoundError as e:
        error_msg = f"Error: {e}\n\nAvailable chapters in notebooks_colab/:\n"
        pattern = 'notebooks_colab/ch*.ipynb'
        matches = glob.glob(pattern)
        if matches:
            for match in sorted(matches):
                error_msg += f"  - {Path(match).stem[:4]}\n"
        else:
            error_msg += "  (none found)\n"
        return error_msg
    except Exception as e:
        return f"Error verifying chapter: {e}"

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

def main():
    """Main execution for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python verify_chapter.py <chapter> [--json]")
        print("\nExamples:")
        print("  python verify_chapter.py ch05")
        print("  python verify_chapter.py ch05 --json")
        sys.exit(1)

    chapter = sys.argv[1]

    # Normalize chapter format (ch05 or 5 → ch05)
    if not chapter.startswith('ch'):
        chapter = f'ch{int(chapter):02d}'

    output_format = 'json' if '--json' in sys.argv else 'markdown'

    print(verify_single_chapter(chapter, output_format))

if __name__ == '__main__':
    main()
