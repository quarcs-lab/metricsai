#!/usr/bin/env python3
"""
Proofread metricsAI chapter notebooks for text quality issues.

Usage:
    python3 proofread_chapter.py ch08           # Report only
    python3 proofread_chapter.py ch08 --fix     # Apply safe fixes
    python3 proofread_chapter.py ch08 --json    # JSON output
    python3 proofread_chapter.py --all           # All chapters
"""

import json
import re
import sys
import os
import glob
import argparse
import shutil
from datetime import datetime
from collections import Counter


# ============================================================
# Configuration
# ============================================================

NOTEBOOK_DIR = "notebooks_colab"

# Common concatenation patterns (lowercase fragments that indicate missing spaces)
CONCAT_PATTERNS = [
    r'(?<=[a-z])ofthe(?=[a-z])',
    r'(?<=[a-z])inthe(?=[a-z])',
    r'(?<=[a-z])tothe(?=[a-z])',
    r'(?<=[a-z])andthe(?=[a-z])',
    r'(?<=[a-z])forthe(?=[a-z])',
    r'(?<=[a-z])onthe(?=[a-z])',
    r'(?<=[a-z])isthe(?=[a-z])',
    r'(?<=[a-z])bythe(?=[a-z])',
    r'(?<=[a-z])atthe(?=[a-z])',
    r'(?<=[a-z])fromthe(?=[a-z])',
    r'(?<=[a-z])withthe(?=[a-z])',
    r'(?<=[a-z])thatthe(?=[a-z])',
    r'(?<=[a-z])ofthis(?=[a-z])',
    r'(?<=[a-z])inthis(?=[a-z])',
    r'(?<=[a-z])tothis(?=[a-z])',
    r'(?<=[a-z])holdingsize(?=[a-z])',
]

# Correct word-boundary splits for concatenation fix mode
CONCAT_FIXES = {
    'ofthe': 'of the', 'inthe': 'in the', 'tothe': 'to the',
    'andthe': 'and the', 'forthe': 'for the', 'onthe': 'on the',
    'isthe': 'is the', 'bythe': 'by the', 'atthe': 'at the',
    'fromthe': 'from the', 'withthe': 'with the', 'thatthe': 'that the',
}

# Known long words that should NOT be flagged
KNOWN_LONG_WORDS = {
    'heteroskedasticity', 'homoskedasticity', 'multicollinearity',
    'autocorrelation', 'heteroskedastic', 'homoskedastic',
    'instrumentalvariables', 'endogeneity', 'stationarity',
    'nonstationarity', 'counterfactual', 'unconditional',
    'contemporaneous', 'contemporaneously', 'autoregressive',
    'heteroscedasticity', 'heteroscedastic', 'unbiasedness',
    'inconsistency', 'misspecification', 'overidentification',
    'underidentification', 'semiparametric', 'nonparametric',
    'intercountry', 'crosssectional', 'crosscountry',
    'acknowledgement', 'acknowledgements', 'acknowledgment',
    'congratulations', 'internationally', 'interpretation',
    'interpretations', 'recommendations', 'recommendation',
    'specifications', 'transformations', 'transformation',
    'heterogeneous', 'differentiation', 'differentiated',
    'standardization', 'standardized', 'unstandardized',
    'retransformation', 'underprediction', 'overprediction',
    'parametrically', 'nonparametrically', 'semiparametrically',
    'overestimation', 'underestimation', 'simultaneously',
    'proportionality', 'proportionally', 'disproportionately',
    'counterfactuals', 'quasiexperimental', 'observational',
    'characteristics', 'characteristic',
    'multicollinear', 'approximately', 'approximation',
    'distinguishing', 'distinguishable', 'indistinguishable',
    'reproducibility', 'generalizable', 'generalizability',
}

# Emoji pattern (same as standardization scripts)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "\u23E9-\u23F3"
    "\u23F8-\u23FA"
    "\u200d"
    "\ufe0f"
    "\u20e3"
    "]+",
    flags=re.UNICODE
)

# Box-drawing, geometric shapes, and common text symbols (NOT emoji)
BOX_DRAWING_PATTERN = re.compile(
    "["
    "\u2500-\u257F"  # Box Drawing
    "\u2580-\u259F"  # Block Elements
    "\u25A0-\u25FF"  # Geometric Shapes
    "\u2190-\u21FF"  # Arrows
    "\u2713-\u2714"  # Checkmarks (✓ ✔)
    "\u2022"         # Bullet (•)
    "]+",
    flags=re.UNICODE
)


# ============================================================
# Text extraction helpers
# ============================================================

def strip_code_blocks(text):
    """Remove fenced code blocks from markdown text."""
    return re.sub(r'```[\s\S]*?```', ' ', text)


def strip_inline_code(text):
    """Remove inline code from markdown text."""
    return re.sub(r'`[^`]+`', ' ', text)


def strip_latex(text):
    """Remove LaTeX expressions from text."""
    # Display math
    text = re.sub(r'\$\$[\s\S]*?\$\$', ' ', text)
    # Inline math
    text = re.sub(r'\$[^$]+\$', ' ', text)
    return text


def strip_urls(text):
    """Remove URLs from text."""
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)  # Keep link text
    return text


def strip_html(text):
    """Remove HTML tags from text."""
    return re.sub(r'<[^>]+>', ' ', text)


def strip_markdown_formatting(text):
    """Remove markdown headers, bold, italic markers."""
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'>\s*', '', text)  # blockquotes
    return text


def extract_prose(text):
    """Extract prose text from markdown, removing code, LaTeX, URLs, HTML."""
    text = strip_code_blocks(text)
    text = strip_inline_code(text)
    text = strip_latex(text)
    text = strip_urls(text)
    text = strip_html(text)
    text = strip_markdown_formatting(text)
    return text


# ============================================================
# Issue detection functions
# ============================================================

def check_concatenated_words(text, cell_idx):
    """Detect words that are likely multiple words joined together."""
    issues = []
    prose = extract_prose(text)
    words = re.findall(r'[A-Za-z]+', prose)

    for word in words:
        lower = word.lower()

        # Skip known long words
        if lower in KNOWN_LONG_WORDS:
            continue

        # Skip words that are all uppercase (acronyms) or have underscores
        if word.isupper() and len(word) < 15:
            continue

        # Check for common concatenation patterns
        for pattern in CONCAT_PATTERNS:
            if re.search(pattern, lower):
                issues.append({
                    'cell': cell_idx,
                    'type': 'concatenated_words',
                    'severity': 'CRITICAL',
                    'word': word,
                    'context': _get_context(text, word),
                    'message': f'Likely concatenated words: "{word}"'
                })
                break
        else:
            # Check for very long words (>30 chars, likely concatenated)
            if len(word) > 30:
                issues.append({
                    'cell': cell_idx,
                    'type': 'long_word',
                    'severity': 'CRITICAL',
                    'word': word,
                    'context': _get_context(text, word),
                    'message': f'Suspiciously long word ({len(word)} chars): "{word[:50]}..."'
                })

            # Check for camelCase in prose (not in code/technical terms)
            elif len(word) > 10 and re.search(r'[a-z][A-Z]', word):
                # Skip common patterns like "DataFrame", "GitHub", etc.
                known_camel = {'DataFrame', 'GitHub', 'NumPy', 'SciPy', 'YouTube',
                               'PyTorch', 'TensorFlow', 'JetBrains', 'JavaScript',
                               'TypeScript', 'PowerPoint', 'OneNote', 'LinkedIn',
                               'statsmodels', 'linearmodels', 'matplotlib', 'seaborn',
                               'ElectricCyan', 'SynapsePurple', 'DataPink',
                               'PanelOLS', 'RandomEffects', 'OLSInfluence',
                               'JupyterLab', 'JupyterHub', 'GoogleColab',
                               'CommonMark', 'JetBrainsMono',
                               'CobbDouglas', 'PhillipsCurve', 'AutoEfficiency',
                               'RandHealthInsurance', 'SouthAfricaHealth',
                               'SenateIncumbency', 'InstitutionsGDP',
                               'HealthExpenditure', 'HousePrices', 'LifeExpectancy',
                               'WageEquation', 'GrowthRegression', 'CrossCountry'}
                # Skip file names (words near .DTA, .csv, .xlsx etc.)
                if re.search(rf'{re.escape(word)}\.\w{{2,5}}', text):
                    continue
                if word not in known_camel:
                    issues.append({
                        'cell': cell_idx,
                        'type': 'camel_case_in_prose',
                        'severity': 'MINOR',
                        'word': word,
                        'context': _get_context(text, word),
                        'message': f'Possible missing space (camelCase in prose): "{word}"'
                    })

    return issues


def check_missing_space_after_punctuation(text, cell_idx):
    """Detect missing spaces after periods, commas, etc."""
    issues = []
    prose = extract_prose(text)

    # Missing space after period (lowercase.Uppercase)
    matches = re.finditer(r'([a-z])\.([A-Z])', prose)
    for m in matches:
        # Check surrounding context for file extensions (.DTA, .CSV, .TXT, etc.)
        surrounding = prose[max(0, m.start()-15):min(len(prose), m.end()+10)]
        if re.search(r'\w+\.[A-Z]{2,5}\b', surrounding):
            continue
        # Skip common abbreviations (U.S., e.g., i.e., etc.)
        before = prose[max(0, m.start()-3):m.end()]
        if re.search(r'[A-Z]\.[A-Z]|e\.g|i\.e|vs\.|etc\.|Dr\.|Mr\.|Ms\.|Jr\.|Sr\.', before):
            continue
        context = prose[max(0, m.start()-20):m.end()+20]
        issues.append({
            'cell': cell_idx,
            'type': 'missing_space_period',
            'severity': 'CRITICAL',
            'word': m.group(),
            'context': context.strip(),
            'message': f'Missing space after period: "...{m.group()}..."'
        })

    # Missing space after comma (lowercase,lowercase but not in numbers like 1,000)
    matches = re.finditer(r'([a-z]),([a-z])', prose)
    for m in matches:
        context = prose[max(0, m.start()-20):m.end()+20]
        issues.append({
            'cell': cell_idx,
            'type': 'missing_space_comma',
            'severity': 'CRITICAL',
            'word': m.group(),
            'context': context.strip(),
            'message': f'Missing space after comma: "...{m.group()}..."'
        })

    return issues


def check_doubled_words(text, cell_idx):
    """Detect doubled words like 'the the', 'is is'."""
    issues = []
    prose = extract_prose(text)
    words = prose.split()

    for i in range(len(words) - 1):
        w1 = re.sub(r'[^a-zA-Z]', '', words[i]).lower()
        w2 = re.sub(r'[^a-zA-Z]', '', words[i+1]).lower()
        if w1 and w2 and w1 == w2 and len(w1) > 1:
            # Skip intentional repetitions
            if w1 in ('ha', 'no', 'so', 'oh', 'go', 'do', 'ok', 'bye'):
                continue
            # Skip "Title: Title..." patterns where colon separates header from explanation
            if words[i].rstrip().endswith(':') or words[i].rstrip().endswith(':**'):
                continue
            # Skip when original words differ before stripping (e.g., "25th, 50th" both strip to "th")
            raw1 = re.sub(r'[,;:!?\.\)\(]', '', words[i]).lower()
            raw2 = re.sub(r'[,;:!?\.\)\(]', '', words[i+1]).lower()
            if raw1 != raw2:
                continue
            # Skip when separated by punctuation (e.g., "GDP, GDP per capita", "heteroskedasticity? Heteroskedasticity")
            if re.search(r'[,;)\.?!]$', words[i]):
                continue
            # Skip when next word starts with opening paren (e.g., "assumption (Assumption 3)")
            if words[i+1].startswith('('):
                continue
            context = ' '.join(words[max(0,i-3):i+5])
            issues.append({
                'cell': cell_idx,
                'type': 'doubled_word',
                'severity': 'MINOR',
                'word': f'{words[i]} {words[i+1]}',
                'context': context,
                'message': f'Doubled word: "{words[i]} {words[i+1]}"'
            })

    return issues


def check_emoji_remnants(text, cell_idx):
    """Check for any remaining emoji characters."""
    issues = []
    if EMOJI_PATTERN.search(text):
        emojis = EMOJI_PATTERN.findall(text)
        # Filter out box-drawing/geometric characters used in diagrams
        real_emojis = [e for e in emojis if not BOX_DRAWING_PATTERN.fullmatch(e)]
        if real_emojis:
            issues.append({
                'cell': cell_idx,
                'type': 'emoji_remnant',
                'severity': 'CRITICAL',
                'word': ''.join(real_emojis[:5]),
                'context': '',
                'message': f'Emoji remnants found: {" ".join(real_emojis[:5])}'
            })
    return issues


def check_broken_latex(text, cell_idx):
    """Check for unmatched dollar signs (broken LaTeX)."""
    issues = []

    # Remove code blocks first
    clean = strip_code_blocks(text)
    clean = strip_inline_code(clean)

    # Remove escaped dollar signs (\$) used for currency
    clean = clean.replace('\\$', '')

    # Count single $ (not $$)
    # First remove $$ pairs
    no_display = re.sub(r'\$\$[\s\S]*?\$\$', '', clean)

    # Remove matched inline math pairs
    no_inline = re.sub(r'\$[^$]+\$', '', no_display)

    # Count remaining unmatched $
    dollar_count = no_inline.count('$')
    if dollar_count > 0:
        issues.append({
            'cell': cell_idx,
            'type': 'broken_latex',
            'severity': 'MINOR',
            'word': '',
            'context': '',
            'message': f'Unmatched $ signs ({dollar_count}) - possible broken LaTeX'
        })

    return issues


def check_unclosed_formatting(text, cell_idx):
    """Check for unclosed bold/italic markers."""
    issues = []

    # Remove code blocks and inline code
    clean = strip_code_blocks(text)
    clean = strip_inline_code(clean)
    clean = strip_latex(clean)

    # Check for unclosed bold **
    bold_count = len(re.findall(r'\*\*', clean))
    if bold_count % 2 != 0:
        issues.append({
            'cell': cell_idx,
            'type': 'unclosed_bold',
            'severity': 'MINOR',
            'word': '',
            'context': '',
            'message': f'Odd number of ** markers ({bold_count}) - possible unclosed bold'
        })

    return issues


def check_broken_links(text, cell_idx):
    """Check for broken markdown links."""
    issues = []

    # Find [text]( without closing )
    matches = re.finditer(r'\[([^\]]*)\]\(([^)]*$)', text, re.MULTILINE)
    for m in matches:
        issues.append({
            'cell': cell_idx,
            'type': 'broken_link',
            'severity': 'MINOR',
            'word': m.group()[:60],
            'context': '',
            'message': f'Possible broken link (no closing parenthesis): [{m.group(1)[:30]}](...'
        })

    return issues


def check_long_paragraphs(text, cell_idx):
    """Flag very long paragraphs that may be hard to read."""
    issues = []

    # Split into paragraphs (separated by blank lines)
    paragraphs = re.split(r'\n\s*\n', text)

    for para in paragraphs:
        # Skip code blocks, headers, lists
        if para.strip().startswith(('```', '#', '- ', '1.', '2.', '3.', '>', '|')):
            continue

        # Check paragraph length (prose only)
        prose = extract_prose(para)
        if len(prose.strip()) > 800:
            issues.append({
                'cell': cell_idx,
                'type': 'long_paragraph',
                'severity': 'SUGGESTION',
                'word': '',
                'context': prose[:80].strip() + '...',
                'message': f'Very long paragraph ({len(prose)} chars) - consider splitting'
            })

    return issues


def check_missing_spaces_in_common_patterns(text, cell_idx):
    """Check for common missing-space patterns in notebook markdown."""
    issues = []
    prose = extract_prose(text)

    # Pattern: number immediately followed by word WITHOUT space: "1553the" "0.047Growth"
    # Use raw text (not prose) to check for numbered lists
    matches = re.finditer(r'(\d+\.?\d*)([A-Z][a-z]+)', prose)
    for m in matches:
        full = m.group()
        # Skip things like "2SLS", "1st", "2nd", "3rd", "4th"
        if any(full.startswith(p) for p in ['2SLS', '1st', '2nd', '3rd', '4th']):
            continue
        # Skip numbered list items: "1. This", "2. United" etc.
        # These show up as "1 This" after stripping punctuation
        num_str = m.group(1)
        if num_str.endswith('.'):
            continue
        # Check if this is a numbered list in the original text
        num_val = m.group(1).rstrip('.')
        word = m.group(2)
        list_pattern = rf'{re.escape(num_val)}\.\s+{re.escape(word)}'
        if re.search(list_pattern, text):
            continue
        # Skip section numbers like "8.1 Health", "16.2 Testing"
        if re.match(r'\d+\.\d+$', num_val):
            continue
        # Only flag if it looks wrong and word is substantial
        if len(m.group(2)) > 3:
            context = prose[max(0, m.start()-15):m.end()+15]
            issues.append({
                'cell': cell_idx,
                'type': 'number_word_concat',
                'severity': 'MINOR',
                'word': m.group(),
                'context': context.strip(),
                'message': f'Possible missing space between number and word: "{m.group()}"'
            })

    return issues


# ============================================================
# Helper functions
# ============================================================

def _get_context(text, word, window=40):
    """Get surrounding context for a word in text."""
    idx = text.find(word)
    if idx == -1:
        return ''
    start = max(0, idx - window)
    end = min(len(text), idx + len(word) + window)
    context = text[start:end].replace('\n', ' ').strip()
    if start > 0:
        context = '...' + context
    if end < len(text):
        context = context + '...'
    return context


def find_notebook(chapter):
    """Find notebook file for a given chapter identifier."""
    pattern = os.path.join(NOTEBOOK_DIR, f'{chapter}_*.ipynb')
    matches = glob.glob(pattern)
    if not matches:
        # Try with 'ch' prefix
        if not chapter.startswith('ch'):
            pattern = os.path.join(NOTEBOOK_DIR, f'ch{chapter}_*.ipynb')
            matches = glob.glob(pattern)
    if not matches:
        # Try with zero-padded number
        try:
            num = int(chapter.replace('ch', ''))
            pattern = os.path.join(NOTEBOOK_DIR, f'ch{num:02d}_*.ipynb')
            matches = glob.glob(pattern)
        except ValueError:
            pass
    return matches[0] if matches else None


# ============================================================
# Main proofreading function
# ============================================================

def proofread_notebook(notebook_path, apply_fixes=False):
    """Proofread a notebook and return issues found."""
    with open(notebook_path) as f:
        nb = json.load(f)

    cells = nb['cells']
    all_issues = []

    for i, cell in enumerate(cells):
        if cell['cell_type'] != 'markdown':
            continue

        text = ''.join(cell.get('source', []))
        if not text.strip():
            continue

        # Run all checks
        all_issues.extend(check_concatenated_words(text, i))
        all_issues.extend(check_missing_space_after_punctuation(text, i))
        all_issues.extend(check_doubled_words(text, i))
        all_issues.extend(check_emoji_remnants(text, i))
        all_issues.extend(check_broken_latex(text, i))
        all_issues.extend(check_unclosed_formatting(text, i))
        all_issues.extend(check_broken_links(text, i))
        all_issues.extend(check_long_paragraphs(text, i))
        all_issues.extend(check_missing_spaces_in_common_patterns(text, i))

    # Apply fixes if requested
    fixes_applied = []
    if apply_fixes and all_issues:
        fixes_applied = apply_safe_fixes(notebook_path, nb, all_issues)

    return all_issues, fixes_applied, len(cells), sum(1 for c in cells if c['cell_type'] == 'markdown')


def apply_safe_fixes(notebook_path, nb, issues):
    """Apply safe automated fixes. Returns list of fixes applied."""
    # Create backup
    backup_dir = os.path.join(os.path.dirname(notebook_path), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = os.path.basename(notebook_path).replace('.ipynb', f'_backup_{timestamp}.ipynb')
    backup_path = os.path.join(backup_dir, backup_name)
    shutil.copy2(notebook_path, backup_path)

    cells = nb['cells']
    fixes = []

    for cell_idx in set(issue['cell'] for issue in issues):
        cell = cells[cell_idx]
        if cell['cell_type'] != 'markdown':
            continue

        text = ''.join(cell.get('source', []))
        original = text

        # Fix doubled words (case-sensitive lowercase only to avoid "Title: Title" false positives)
        text = re.sub(r'\b([a-z]+)\s+\1\b', r'\1', text)

        # Fix missing space after period (lowercase.Uppercase), skip file extensions (.DTA, .CSV)
        text = re.sub(r'([a-z])\.([A-Z])(?![A-Z]{1,4}\b)', r'\1. \2', text)

        # Fix missing space after comma (lowercase,lowercase)
        text = re.sub(r'([a-z]),([a-z])', r'\1, \2', text)

        # Fix common concatenation patterns using explicit word-boundary dictionary
        for pattern_str, replacement in CONCAT_FIXES.items():
            text = re.sub(
                rf'(?<=[a-z]){pattern_str}(?=[a-z])',
                replacement,
                text,
                flags=re.IGNORECASE
            )

        # Fix emoji remnants (preserve box-drawing/geometric characters)
        if EMOJI_PATTERN.search(text):
            def replace_emoji(m):
                if BOX_DRAWING_PATTERN.fullmatch(m.group()):
                    return m.group()  # Keep box-drawing chars
                return ''
            text = EMOJI_PATTERN.sub(replace_emoji, text)
            text = re.sub(r'  +', ' ', text)

        if text != original:
            cell['source'] = [text]
            fixes.append(f'Cell {cell_idx}: Applied text fixes')

    if fixes:
        nb['cells'] = cells
        with open(notebook_path, 'w') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)

    return fixes


# ============================================================
# Report generation
# ============================================================

def generate_report(notebook_path, issues, fixes, total_cells, md_cells):
    """Generate human-readable proofreading report."""
    filename = os.path.basename(notebook_path)

    critical = [i for i in issues if i['severity'] == 'CRITICAL']
    minor = [i for i in issues if i['severity'] == 'MINOR']
    suggestions = [i for i in issues if i['severity'] == 'SUGGESTION']

    lines = []
    lines.append(f'# Proofreading Report: {filename}')
    lines.append('')

    # Score
    score = 100
    score -= min(len(critical) * 5, 40)
    score -= min(len(minor) * 2, 20)
    score -= min(len(suggestions) * 1, 10)
    score = max(0, score)

    if score >= 95:
        tier = 'Excellent (publication-ready)'
    elif score >= 85:
        tier = 'Good (minor fixes needed)'
    elif score >= 70:
        tier = 'Acceptable (several issues)'
    else:
        tier = 'Needs work (significant issues)'

    lines.append(f'**Proofreading Score**: {score}/100')
    lines.append(f'**Quality**: {tier}')
    lines.append(f'**Cells checked**: {md_cells} markdown / {total_cells} total')
    lines.append(f'**Issues found**: {len(critical)} critical, {len(minor)} minor, {len(suggestions)} suggestions')
    lines.append('')

    # Critical
    if critical:
        lines.append('## CRITICAL Issues (affect readability)')
        lines.append('')
        for issue in critical:
            lines.append(f'- **Cell {issue["cell"]}**: {issue["message"]}')
            if issue.get('context'):
                lines.append(f'  Context: `{issue["context"][:80]}`')
        lines.append('')
    else:
        lines.append('## CRITICAL Issues')
        lines.append('None found!')
        lines.append('')

    # Minor
    if minor:
        lines.append('## MINOR Issues (should fix)')
        lines.append('')
        for issue in minor:
            lines.append(f'- **Cell {issue["cell"]}**: {issue["message"]}')
            if issue.get('context'):
                lines.append(f'  Context: `{issue["context"][:80]}`')
        lines.append('')
    else:
        lines.append('## MINOR Issues')
        lines.append('None found!')
        lines.append('')

    # Suggestions
    if suggestions:
        lines.append('## SUGGESTIONS (nice to have)')
        lines.append('')
        for issue in suggestions:
            lines.append(f'- **Cell {issue["cell"]}**: {issue["message"]}')
            if issue.get('context'):
                lines.append(f'  Context: `{issue["context"][:80]}`')
        lines.append('')

    # Summary by type
    type_counts = Counter(i['type'] for i in issues)
    if type_counts:
        lines.append('## Issue Summary by Type')
        lines.append('')
        lines.append('| Type | Count |')
        lines.append('|------|-------|')
        for issue_type, count in type_counts.most_common():
            lines.append(f'| {issue_type} | {count} |')
        lines.append('')

    # Fixes applied
    if fixes:
        lines.append('## Fixes Applied')
        lines.append('')
        for fix in fixes:
            lines.append(f'- {fix}')
        lines.append('')

    return '\n'.join(lines)


def generate_json_report(notebook_path, issues, fixes, total_cells, md_cells):
    """Generate JSON report for programmatic use."""
    return json.dumps({
        'file': os.path.basename(notebook_path),
        'total_cells': total_cells,
        'markdown_cells': md_cells,
        'issues': issues,
        'fixes_applied': fixes,
        'summary': {
            'critical': len([i for i in issues if i['severity'] == 'CRITICAL']),
            'minor': len([i for i in issues if i['severity'] == 'MINOR']),
            'suggestions': len([i for i in issues if i['severity'] == 'SUGGESTION']),
        }
    }, indent=2)


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Proofread metricsAI chapter notebooks')
    parser.add_argument('chapter', nargs='?', help='Chapter identifier (e.g., ch08, 08, ch16)')
    parser.add_argument('--fix', action='store_true', help='Apply safe automated fixes')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    parser.add_argument('--all', action='store_true', help='Process all chapters')

    args = parser.parse_args()

    if args.all:
        # Process all chapters
        pattern = os.path.join(NOTEBOOK_DIR, 'ch*_*.ipynb')
        notebooks = sorted(glob.glob(pattern))

        print(f'# Proofreading All Chapters ({len(notebooks)} notebooks)')
        print()
        print('| Chapter | Critical | Minor | Suggestions | Score |')
        print('|---------|----------|-------|-------------|-------|')

        for nb_path in notebooks:
            issues, fixes, total, md = proofread_notebook(nb_path, apply_fixes=args.fix)
            critical = len([i for i in issues if i['severity'] == 'CRITICAL'])
            minor = len([i for i in issues if i['severity'] == 'MINOR'])
            suggestions = len([i for i in issues if i['severity'] == 'SUGGESTION'])

            score = 100 - min(critical * 5, 40) - min(minor * 2, 20) - min(suggestions, 10)
            score = max(0, score)

            name = os.path.basename(nb_path).split('_')[0]
            print(f'| {name} | {critical} | {minor} | {suggestions} | {score}/100 |')

        print()
        return

    if not args.chapter:
        parser.print_help()
        sys.exit(1)

    # Find notebook
    notebook_path = find_notebook(args.chapter)
    if not notebook_path:
        print(f'Error: Could not find notebook for "{args.chapter}"')
        print(f'Looked in: {NOTEBOOK_DIR}/')
        sys.exit(1)

    # Run proofreading
    issues, fixes, total_cells, md_cells = proofread_notebook(notebook_path, apply_fixes=args.fix)

    # Output
    if args.json:
        print(generate_json_report(notebook_path, issues, fixes, total_cells, md_cells))
    else:
        print(generate_report(notebook_path, issues, fixes, total_cells, md_cells))


if __name__ == '__main__':
    main()
