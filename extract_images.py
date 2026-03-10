import re
import base64
import os
import hashlib

HTML_FILE = "Yaaro Da Dhaba & Cafe.html"
OUTPUT_HTML = "Yaaro Da Dhaba & Cafe_images.html"
IMAGES_DIR = "images"

os.makedirs(IMAGES_DIR, exist_ok=True)

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Match base64 image data URIs in src attributes
pattern = r'src="(data:image/(png|jpeg|jpg|gif|webp|svg\+xml);base64,([A-Za-z0-9+/=\s]+?))"'

seen = {}  # hash -> filename
count = 0

def replace_base64(match):
    global count
    full_data_uri = match.group(1)
    img_type = match.group(2)
    b64_data = match.group(3).strip()

    # Compute hash to deduplicate
    data_hash = hashlib.md5(b64_data[:200].encode()).hexdigest()

    if data_hash in seen:
        filepath = seen[data_hash]
    else:
        count += 1
        ext = img_type.replace("jpeg", "jpg").replace("svg+xml", "svg")
        filename = f"image_{count}.{ext}"
        filepath = f"{IMAGES_DIR}/{filename}"

        # Decode and save the image
        try:
            img_bytes = base64.b64decode(b64_data)
            with open(filepath, "wb") as img_file:
                img_file.write(img_bytes)
            size_kb = len(img_bytes) / 1024
            print(f"  Saved: {filepath} ({size_kb:.1f} KB)")
        except Exception as e:
            print(f"  ERROR decoding image_{count}: {e}")
            return match.group(0)

        seen[data_hash] = filepath

    return f'src="{filepath}"'

print("Extracting base64 images from HTML...\n")
new_html = re.sub(pattern, replace_base64, html)

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(new_html)

orig_size = os.path.getsize(HTML_FILE) / 1024
new_size = os.path.getsize(OUTPUT_HTML) / 1024
print(f"\nDone! Extracted {count} unique images.")
print(f"Original HTML: {orig_size:.1f} KB")
print(f"New HTML:      {new_size:.1f} KB")
print(f"Saved to:      {OUTPUT_HTML}")
