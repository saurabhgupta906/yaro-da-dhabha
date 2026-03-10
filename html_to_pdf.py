#!/usr/bin/env python3
"""
Convert HTML to PDF using WeasyPrint
"""

from weasyprint import HTML, CSS
from pathlib import Path

def convert_html_to_pdf(html_file, output_file=None):
    """
    Convert HTML file to PDF
    
    Args:
        html_file: Path to the HTML file
        output_file: Path for the output PDF (optional, defaults to same name with .pdf)
    """
    html_path = Path(html_file).resolve()
    
    if not html_path.exists():
        print(f"Error: HTML file not found: {html_file}")
        return False
    
    if output_file is None:
        output_file = html_path.with_suffix('.pdf')
    else:
        output_file = Path(output_file).resolve()
    
    try:
        print(f"Converting: {html_path}")
        HTML(str(html_path)).write_pdf(str(output_file))
        print(f"✓ PDF created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

if __name__ == "__main__":
    # Convert index.html to PDF
    html_file = r"c:\Users\Priya\Desktop\yaro-da-dhabha\index.html"
    convert_html_to_pdf(html_file)
