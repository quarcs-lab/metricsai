#!/usr/bin/env python3
"""
Multi-Chapter Consistency Verification Script
Analyzes structural consistency across Chapters 1-4
"""

import json
import re
import glob
from pathlib import Path

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
                # Extract topic (first line after "Key Concept:")
                topic_match = re.search(r'Key Concept:?\*?\*?\s*(.+)', content, re.IGNORECASE)
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
        'key_concepts': 0,
        'difficulty_labels': False
    }

    # Look for case study section
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            content = ''.join(cell['source'])
            # Check for case study section header
            if re.search(r'##\s+\d+\.\d+\s+Case Study', content, re.IGNORECASE):
                section_match = re.search(r'##\s+(\d+\.\d+)', content)
                case_study['present'] = True
                case_study['section_number'] = section_match.group(1) if section_match else 'Unknown'
                case_study['start_cell'] = i

                # Count tasks in remaining cells
                for j in range(i, len(nb['cells'])):
                    task_content = ''.join(nb['cells'][j]['source']) if nb['cells'][j]['cell_type'] == 'markdown' else ''

                    # Count tasks (looking for "Task 1", "Task 2", etc.)
                    if re.search(r'####\s+Task\s+\d+', task_content):
                        case_study['tasks'] += 1

                        # Check for difficulty labels
                        if re.search(r'\(GUIDED\)|\(SEMI-GUIDED\)|\(INDEPENDENT\)', task_content):
                            case_study['difficulty_labels'] = True

                    # Count Key Concepts within case study
                    if re.search(r'>\s*\*\*Key Concept', task_content, re.IGNORECASE):
                        case_study['key_concepts'] += 1

                break

    return case_study

def check_front_matter(nb):
    """Verify presence of standard front matter sections"""
    front_matter = {
        'title': False,
        'learning_objectives': False,
        'chapter_overview': False,
        'setup': False
    }

    # Check first 5 cells for front matter
    for i in range(min(5, len(nb['cells']))):
        if nb['cells'][i]['cell_type'] == 'markdown':
            content = ''.join(nb['cells'][i]['source']).lower()

            if i == 0 and re.search(r'#\s+chapter\s+\d+', content):
                front_matter['title'] = True

            if 'learning objectives' in content:
                front_matter['learning_objectives'] = True

            if 'chapter overview' in content:
                front_matter['chapter_overview'] = True

            if 'setup' in content or '🔧' in content:
                front_matter['setup'] = True

    return front_matter

def check_closing_sections(nb):
    """Check for Key Takeaways and Practice Exercises"""
    closing = {
        'key_takeaways': False,
        'practice_exercises': False,
        'key_takeaways_cell': None,
        'practice_exercises_cell': None,
        'empty_closing_cell': False
    }

    # Check last 20 cells for closing sections
    start_idx = max(0, len(nb['cells']) - 20)

    for i in range(start_idx, len(nb['cells'])):
        if nb['cells'][i]['cell_type'] == 'markdown':
            content = ''.join(nb['cells'][i]['source'])

            if re.search(r'##\s+Key Takeaways', content, re.IGNORECASE):
                closing['key_takeaways'] = True
                closing['key_takeaways_cell'] = i

            if re.search(r'##\s+Practice Exercises', content, re.IGNORECASE):
                closing['practice_exercises'] = True
                closing['practice_exercises_cell'] = i

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

def analyze_chapter(chapter_prefix):
    """Perform comprehensive analysis of a single chapter"""
    notebook_path = find_notebook(chapter_prefix)

    print(f"\n{'='*70}")
    print(f"Analyzing {chapter_prefix}: {Path(notebook_path).name}")
    print(f"{'='*70}")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Run all checks
    findings = {
        'file': Path(notebook_path).name,
        'total_cells': len(nb['cells']),
        'markdown_cells': sum(1 for c in nb['cells'] if c['cell_type'] == 'markdown'),
        'code_cells': sum(1 for c in nb['cells'] if c['cell_type'] == 'code'),
        'visual_summary': check_visual_summary(nb['cells'][0]),
        'front_matter': check_front_matter(nb),
        'sections': extract_section_numbers(nb),
        'section_gaps': None,  # Will compute below
        'key_concepts': count_key_concepts(nb),
        'case_study': analyze_case_study(nb),
        'closing': check_closing_sections(nb),
        'transition_cells': count_transition_cells(nb)
    }

    # Compute section gaps
    findings['section_gaps'] = find_section_gaps(findings['sections'])

    return findings

def print_summary_table(results):
    """Print comparison table across all chapters"""
    print("\n" + "="*100)
    print("CONSISTENCY COMPARISON TABLE")
    print("="*100)

    chapters = sorted(results.keys())

    # Cell counts
    print("\n## Cell Counts")
    print(f"{'Chapter':<10} {'Total':<10} {'Markdown':<12} {'Code':<10} {'MD:Code Ratio':<15}")
    print("-" * 100)
    for ch in chapters:
        r = results[ch]
        ratio = f"{r['markdown_cells']}:{r['code_cells']}"
        print(f"{ch:<10} {r['total_cells']:<10} {r['markdown_cells']:<12} {r['code_cells']:<10} {ratio:<15}")

    # Visual Summary
    print("\n## Visual Summary Image")
    print(f"{'Chapter':<10} {'Present':<10} {'Width':<10} {'Type':<30}")
    print("-" * 100)
    for ch in chapters:
        vs = results[ch]['visual_summary']
        present = '✅ Yes' if vs['present'] else '❌ No'
        width = vs.get('width', 'N/A')
        vtype = vs.get('type', vs.get('reason', 'Unknown'))
        print(f"{ch:<10} {present:<10} {width:<10} {vtype:<30}")

    # Front Matter
    print("\n## Front Matter Sections")
    print(f"{'Chapter':<10} {'Title':<10} {'Learning Obj':<15} {'Overview':<12} {'Setup':<10}")
    print("-" * 100)
    for ch in chapters:
        fm = results[ch]['front_matter']
        title = '✅' if fm['title'] else '❌'
        obj = '✅' if fm['learning_objectives'] else '❌'
        overview = '✅' if fm['chapter_overview'] else '❌'
        setup = '✅' if fm['setup'] else '❌'
        print(f"{ch:<10} {title:<10} {obj:<15} {overview:<12} {setup:<10}")

    # Section Numbering
    print("\n## Section Numbering")
    print(f"{'Chapter':<10} {'Sections':<15} {'Gaps':<30}")
    print("-" * 100)
    for ch in chapters:
        sections = results[ch]['sections']
        if sections:
            section_range = f"{sections[0]['number']} - {sections[-1]['number']}"
            gaps = ', '.join(results[ch]['section_gaps']) if results[ch]['section_gaps'] else 'None (Sequential)'
        else:
            section_range = 'No sections'
            gaps = 'N/A'
        print(f"{ch:<10} {section_range:<15} {gaps:<30}")

    # Key Concepts
    print("\n## Key Concept Boxes")
    print(f"{'Chapter':<10} {'Total Count':<15} {'In Main Content':<20} {'In Case Study':<15}")
    print("-" * 100)
    for ch in chapters:
        kc_total = len(results[ch]['key_concepts'])
        cs = results[ch]['case_study']
        kc_main = kc_total - cs['key_concepts'] if cs['present'] else kc_total
        kc_case = cs['key_concepts'] if cs['present'] else 'N/A'
        print(f"{ch:<10} {kc_total:<15} {kc_main:<20} {str(kc_case):<15}")

    # Case Study
    print("\n## Case Study Structure")
    print(f"{'Chapter':<10} {'Present':<10} {'Section #':<12} {'Tasks':<10} {'Difficulty Labels':<20} {'Key Concepts':<15}")
    print("-" * 100)
    for ch in chapters:
        cs = results[ch]['case_study']
        present = '✅ Yes' if cs['present'] else '❌ No'
        section = cs['section_number'] if cs['section_number'] else 'N/A'
        tasks = cs['tasks'] if cs['present'] else 'N/A'
        labels = '✅ Yes' if cs['difficulty_labels'] else '❌ No' if cs['present'] else 'N/A'
        kc = cs['key_concepts'] if cs['present'] else 'N/A'
        print(f"{ch:<10} {present:<10} {section:<12} {str(tasks):<10} {labels:<20} {str(kc):<15}")

    # Closing Sections
    print("\n## Closing Sections")
    print(f"{'Chapter':<10} {'Key Takeaways':<15} {'Practice Ex':<15} {'Empty Cell':<15}")
    print("-" * 100)
    for ch in chapters:
        closing = results[ch]['closing']
        kt = '✅ Yes' if closing['key_takeaways'] else '❌ No'
        pe = '✅ Yes' if closing['practice_exercises'] else '❌ No'
        empty = '✅ Yes' if closing['empty_closing_cell'] else '❌ No'
        print(f"{ch:<10} {kt:<15} {pe:<15} {empty:<15}")

    # Transition Cells
    print("\n## Transition Cells")
    print(f"{'Chapter':<10} {'Count':<10}")
    print("-" * 100)
    for ch in chapters:
        count = results[ch]['transition_cells']
        print(f"{ch:<10} {count:<10}")

def identify_inconsistencies(results):
    """Identify and categorize inconsistencies"""
    print("\n" + "="*100)
    print("INCONSISTENCY ANALYSIS")
    print("="*100)

    critical = []
    minor = []

    # Check visual summary consistency
    vs_present = [ch for ch, r in results.items() if r['visual_summary']['present']]
    vs_missing = [ch for ch, r in results.items() if not r['visual_summary']['present']]
    if vs_missing:
        critical.append({
            'issue': 'Visual Summary Missing',
            'chapters': vs_missing,
            'fix': f"Add visual summary images to: {', '.join(vs_missing)}"
        })

    # Check case study consistency
    cs_present = [ch for ch, r in results.items() if r['case_study']['present']]
    cs_missing = [ch for ch, r in results.items() if not r['case_study']['present']]
    if cs_missing:
        critical.append({
            'issue': 'Case Study Missing',
            'chapters': cs_missing,
            'fix': f"Add case study or document exception for: {', '.join(cs_missing)}"
        })

    # Check task difficulty labels in case studies
    cs_no_labels = [ch for ch, r in results.items() if r['case_study']['present'] and not r['case_study']['difficulty_labels']]
    if cs_no_labels:
        minor.append({
            'issue': 'Task Difficulty Labels Missing',
            'chapters': cs_no_labels,
            'fix': f"Add (GUIDED), (SEMI-GUIDED), etc. labels to: {', '.join(cs_no_labels)}"
        })

    # Check Key Concepts in case studies
    cs_kc_counts = {ch: r['case_study']['key_concepts'] for ch, r in results.items() if r['case_study']['present']}
    if cs_kc_counts and len(set(cs_kc_counts.values())) > 1:
        minor.append({
            'issue': 'Inconsistent Key Concepts in Case Studies',
            'chapters': [f"{ch} ({count})" for ch, count in cs_kc_counts.items()],
            'fix': "Standardize to 2 Key Concept boxes per case study (CH02 template)"
        })

    # Check section gaps
    gaps_present = {ch: r['section_gaps'] for ch, r in results.items() if r['section_gaps']}
    if gaps_present:
        minor.append({
            'issue': 'Section Numbering Gaps',
            'chapters': [f"{ch} (missing {', '.join(gaps)})" for ch, gaps in gaps_present.items()],
            'fix': "Document gaps as reserved sections OR renumber sequentially"
        })

    # Print findings
    print("\n### CRITICAL INCONSISTENCIES (Must Fix)")
    print("-" * 100)
    if critical:
        for i, issue in enumerate(critical, 1):
            print(f"\n{i}. {issue['issue']}")
            print(f"   Affected chapters: {', '.join(issue['chapters'])}")
            print(f"   Recommended fix: {issue['fix']}")
    else:
        print("✅ No critical inconsistencies found!")

    print("\n### MINOR INCONSISTENCIES (Nice to Fix)")
    print("-" * 100)
    if minor:
        for i, issue in enumerate(minor, 1):
            print(f"\n{i}. {issue['issue']}")
            print(f"   Affected chapters: {', '.join(str(ch) for ch in issue['chapters'])}")
            print(f"   Recommended fix: {issue['fix']}")
    else:
        print("✅ No minor inconsistencies found!")

    return {'critical': critical, 'minor': minor}

def main():
    """Main execution"""
    print("="*100)
    print("MULTI-CHAPTER CONSISTENCY VERIFICATION")
    print("Analyzing Chapters 1-4 for structural consistency")
    print("="*100)

    chapters = ['ch01', 'ch02', 'ch03', 'ch04']
    results = {}

    # Analyze each chapter
    for ch in chapters:
        try:
            results[ch] = analyze_chapter(ch)
        except Exception as e:
            print(f"❌ Error analyzing {ch}: {e}")
            continue

    # Print comparison tables
    if results:
        print_summary_table(results)
        inconsistencies = identify_inconsistencies(results)

        # Summary
        print("\n" + "="*100)
        print("SUMMARY")
        print("="*100)
        print(f"Chapters analyzed: {len(results)}")
        print(f"Critical issues: {len(inconsistencies['critical'])}")
        print(f"Minor issues: {len(inconsistencies['minor'])}")

        if inconsistencies['critical'] or inconsistencies['minor']:
            print("\n⚠️  Inconsistencies detected - see details above")
        else:
            print("\n✅ All chapters are structurally consistent!")

    print("\n" + "="*100)
    print("Verification complete!")
    print("="*100)

if __name__ == '__main__':
    main()
