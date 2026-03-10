import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PyPDF2 import PdfReader, PdfWriter

HTML_FILE = "Yaaro Da Dhaba & Cafe_images.html"
PDF_OUTPUT = "Yaaro Da Dhaba & Cafe.pdf"
PDF_COMPRESSED = "Yaaro Da Dhaba & Cafe_compressed.pdf"

html_path = Path(HTML_FILE).resolve()
if not html_path.exists():
    print(f"ERROR: {HTML_FILE} not found!")
    sys.exit(1)

# Step 1: Convert HTML to PDF using Playwright (Chromium)
print("Step 1: Converting HTML to PDF...")
file_url = html_path.as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(file_url, wait_until="networkidle", timeout=60000)
    page.pdf(
        path=PDF_OUTPUT,
        format="A4",
        print_background=True,
        margin={"top": "10mm", "right": "10mm", "bottom": "10mm", "left": "10mm"},
    )
    browser.close()

pdf_size = os.path.getsize(PDF_OUTPUT) / 1024
print(f"  PDF created: {PDF_OUTPUT} ({pdf_size:.1f} KB)")

# Step 2: Compress the PDF
print("\nStep 2: Compressing PDF...")
reader = PdfReader(PDF_OUTPUT)
writer = PdfWriter()

for page in reader.pages:
    page.compress_content_streams()
    writer.add_page(page)

# Remove unused objects and compress
writer.add_metadata(reader.metadata or {})

with open(PDF_COMPRESSED, "wb") as f:
    writer.write(f)

compressed_size = os.path.getsize(PDF_COMPRESSED) / 1024
reduction = (1 - compressed_size / pdf_size) * 100 if pdf_size > 0 else 0

print(f"  Compressed PDF: {PDF_COMPRESSED} ({compressed_size:.1f} KB)")
print(f"\n--- Summary ---")
print(f"  Original PDF:    {pdf_size:.1f} KB")
print(f"  Compressed PDF:  {compressed_size:.1f} KB")
print(f"  Reduction:       {reduction:.1f}%")

# Verify the compressed PDF is valid
try:
    verify = PdfReader(PDF_COMPRESSED)
    print(f"  Pages:           {len(verify.pages)}")
    print(f"  Status:          Valid (not corrupted)")
except Exception as e:
    print(f"  WARNING: Compressed PDF may be invalid: {e}")

print("\nDone!")
