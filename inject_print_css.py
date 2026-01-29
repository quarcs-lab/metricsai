#!/usr/bin/env python3
"""
Inject custom CSS into HTML notebook for better PDF printing.
Usage: python inject_print_css.py input.html output.html
"""

import sys
import re

def inject_css(input_html, output_html, css_file='notebook_pdf_styles.css'):
    # Read the CSS
    with open(css_file, 'r') as f:
        css_content = f.read()

    # Read the HTML
    with open(input_html, 'r') as f:
        html_content = f.read()

    # Create CSS style tag
    style_tag = f'\n<style type="text/css">\n{css_content}\n</style>\n'

    # Inject before </head>
    html_with_css = html_content.replace('</head>', style_tag + '</head>')

    # Write output
    with open(output_html, 'w') as f:
        f.write(html_with_css)

    print(f"✓ CSS injected into {output_html}")
    print(f"  Open in browser and use Cmd+P → Save as PDF")
    print(f"  Tables will be smaller and fit better on the page")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python inject_print_css.py input.html output.html")
        sys.exit(1)

    inject_css(sys.argv[1], sys.argv[2])
