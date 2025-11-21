import os
import glob
from PIL import Image, ImageDraw
from math import pi

# Directory containing the .txt files
txt_dir = './CTag_Generated_FromID/'
output_dir = './CTag_Visualized_FromID/'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get all .txt files matching the pattern
txt_files = glob.glob(os.path.join(txt_dir, 'cy*_corners.txt'))

for txt_file in txt_files:
    with open(txt_file, 'r') as f:
        lines = f.readlines()
    
    # First line: width height
    width, height = map(int, lines[0].strip().split())
    
    # Remaining lines: polygons, each 4 lines of x y
    all_coords = []
    for i in range(1, len(lines), 4):
        coords = []
        for j in range(4):
            x, y = map(float, lines[i + j].strip().split())
            coords.append((x, y))
        all_coords.append(coords)
    
    # Create a new image with white background (mode 'RGB' for color to allow text)
    image = Image.new('RGB', (width, height), (255, 255, 255))  # white background
    draw = ImageDraw.Draw(image)

    global_id = 0
    
    # Draw each polygon outline and mark corners
    for coords in all_coords:
        # Draw polygon outline
        draw.polygon(coords, outline=(0, 0, 0))  # black outline
        
        # Mark corners with numbers
        for idx, (x, y) in enumerate(coords, start=1):
            # Draw a small circle at the corner
            draw.ellipse((x-3, y-3, x+3, y+3), fill=(255, 0, 0))  # red circle
            # Add text label
            draw.text((x+5, y-5), str(global_id), fill=(0, 0, 0))  # black text
            global_id += 1
    
    # Extract the ID from the filename
    base_name = os.path.basename(txt_file)
    id_num = base_name.split('_')[0][2:]  # e.g., 'cy1' -> '1'
    
    # Save the image
    output_path = os.path.join(output_dir, f'cy{id_num}_visualized.png')
    image.save(output_path)

print(f'Visualizations saved in {output_dir}')