#!/bin/bash
# Export all Jupyter notebooks to print-ready HTML for PDF conversion
# Usage: ./export_notebooks_to_pdf.sh

echo "📓 Exporting Jupyter notebooks to PDF-ready HTML..."
echo "=========================================="

# Create output directory
mkdir -p notebooks_pdf_ready

# Counter
total=0
success=0

# Export each notebook
for notebook in notebooks_colab/ch*.ipynb; do
    if [ -f "$notebook" ]; then
        total=$((total + 1))
        basename=$(basename "$notebook" .ipynb)

        echo "Processing: $basename"

        # Step 1: Convert to HTML
        jupyter nbconvert --to html "$notebook" \
            --output-dir notebooks_pdf_ready \
            --output "${basename}.html" 2>/dev/null

        if [ $? -eq 0 ]; then
            # Step 2: Inject print CSS
            python3 inject_print_css.py \
                "notebooks_pdf_ready/${basename}.html" \
                "notebooks_pdf_ready/${basename}_printable.html" 2>/dev/null

            if [ $? -eq 0 ]; then
                # Clean up intermediate file
                rm "notebooks_pdf_ready/${basename}.html"
                success=$((success + 1))
                echo "  ✓ Success: ${basename}_printable.html"
            else
                echo "  ✗ Failed to inject CSS"
            fi
        else
            echo "  ✗ Failed to convert to HTML"
        fi
    fi
done

echo ""
echo "=========================================="
echo "📊 Results: $success/$total notebooks exported"
echo ""
echo "Next steps:"
echo "1. Open notebooks_pdf_ready/ folder"
echo "2. Open each *_printable.html file in your browser"
echo "3. Press Cmd+P → Save as PDF"
echo ""
echo "💡 Tip: Tables are formatted smaller to fit on PDF pages"
echo "💡 Tip: Page is set to landscape orientation for better fit"
