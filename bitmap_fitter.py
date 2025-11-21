import os
import glob
from PIL import Image, ImageDraw, ImageFont
import argparse
from math import pi

DPI = 300
CM_TO_INCH = 2.54

def cm_to_pixels(cm):
    return int(cm * DPI / CM_TO_INCH)

A4_WIDTH_CM = 21 * 2 # PATCH: A3 mode
A4_HEIGHT_CM = 29.7
A4_WIDTH_PX = cm_to_pixels(A4_WIDTH_CM)
A4_HEIGHT_PX = cm_to_pixels(A4_HEIGHT_CM)

WIDTH_DEFAULT = 3.2 * pi  # Default width in cm
print(WIDTH_DEFAULT)

parser = argparse.ArgumentParser(description='Fit bitmaps from CTag_Generated folders onto an A4 sheet.')
parser.add_argument('--margin', type=float, default=1.0, help='Margin in cm (default: 1.0)')
parser.add_argument('--gap', type=float, default=0.5, help='Vertical gap between rows in cm (default: 0.5)')
parser.add_argument('--horizontal_gap', type=float, default=3.0, help='Horizontal gap between images in cm (default: 3.0)')
parser.add_argument('--width', type=float, default=WIDTH_DEFAULT, help='Image width in cm (default: 2.0)')
parser.add_argument('--font_size', type=int, default=20, help='Font size for labels (default: 20)')
parser.add_argument('--label_gap', type=int, default=20, help='Vertical gap between image and label in pixels (default: 10)')
args = parser.parse_args()

M = args.margin
G = args.gap
H = args.horizontal_gap
W = args.width
font_size = args.font_size
label_gap = args.label_gap

margin_px = cm_to_pixels(M)
gap_px_vertical = cm_to_pixels(G)
gap_px_horizontal = cm_to_pixels(H)
img_width_px = cm_to_pixels(W)

# Find folders containing 'CTag_Generated'
folders = [d for d in os.listdir('.') if 'CTag_Generated' in d and os.path.isdir(d)]

for folder in folders:
    bmp_files = glob.glob(os.path.join(folder, '*.bmp'))
    # Sort by number in filename
    bmp_files.sort(key=lambda x: int(os.path.basename(x).replace('cy', '').replace('.bmp', '')))

    images = []
    for bmp in bmp_files:
        img = Image.open(bmp).convert('RGB')
        aspect = img.height / img.width
        new_height = int(img_width_px * aspect)
        img_resized = img.resize((img_width_px, new_height), Image.Resampling.LANCZOS)
        filename = os.path.basename(bmp)
        images.append((img_resized, filename))

    page = 1
    # Create canvas
    canvas = Image.new('RGB', (A4_WIDTH_PX, A4_HEIGHT_PX), 'white')
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf", font_size)  # Configurable font size

    x = margin_px
    y = margin_px
    max_y_in_row = 0

    for img, filename in images:
        # Calculate text height
        bbox = draw.textbbox((0, 0), filename, font=font)
        text_height = bbox[3] - bbox[1]
        item_height = img.height + text_height + 2 * label_gap  # Configurable gap

        if x + img.width > A4_WIDTH_PX - margin_px:
            # New row
            x = margin_px
            y += max_y_in_row + gap_px_vertical
            max_y_in_row = 0
        if y + item_height > A4_HEIGHT_PX - margin_px:
            # New page
            os.makedirs(f'fitted_output/{folder}', exist_ok=True)
            output_filename = f'fitted_sheet_{page}.png'
            canvas.save(os.path.join(f'fitted_output/{folder}', output_filename))
            print(f"Fitted sheet {page} for {folder} saved to fitted_output/{folder}/{output_filename}")
            page += 1
            canvas = Image.new('RGB', (A4_WIDTH_PX, A4_HEIGHT_PX), 'white')
            draw = ImageDraw.Draw(canvas)
            x = margin_px
            y = margin_px
            max_y_in_row = 0
        canvas.paste(img, (x, y))
        draw.text((x, y + img.height + label_gap), filename, fill='black', font=font)  # Configurable gap
        x += img.width + gap_px_horizontal
        if item_height > max_y_in_row:
            max_y_in_row = item_height

    # Save the last page
    os.makedirs(f'fitted_output/{folder}', exist_ok=True)
    output_filename = f'fitted_sheet_{page}.png'
    canvas.save(os.path.join(f'fitted_output/{folder}', output_filename))
    print(f"Fitted sheet {page} for {folder} saved to fitted_output/{folder}/{output_filename}")