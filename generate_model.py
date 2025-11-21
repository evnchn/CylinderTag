import os
import glob
import math

CYLINDER_DIAMETER_CM = 3.2
r = CYLINDER_DIAMETER_CM / 2 * 10  # mm
circumference = CYLINDER_DIAMETER_CM * math.pi * 10  # mm

txt_dir = './CTag_Generated_FromID/'
output_file = './model_from_coords.model'

with open(output_file, 'w') as out:
    txt_files = sorted(glob.glob(os.path.join(txt_dir, 'cy*_corners.txt')))
    N = len(txt_files)
    out.write(f"{N} 12\n")
    for txt_file in txt_files:
        with open(txt_file, 'r') as f:
            lines = f.readlines()
        
        width, height = map(int, lines[0].strip().split())
        scale = circumference / width
        
        all_coords = []
        for i in range(1, len(lines), 4):
            coords = []
            for j in range(4):
                x, y = map(float, lines[i + j].strip().split())
                coords.append((x, y))
            all_coords.append(coords)
        
        # Extract ID
        base_name = os.path.basename(txt_file)
        id_num = int(base_name.split('_')[0][2:])
        
        # Output block
        out.write("\n")  # newline before each block
        out.write(f"{id_num}\n")
        out.write("0.000000 0.000000 -500.000000\n")  # position
        out.write("0 1 0\n")  # direction
        
        count = 0
        for coords in all_coords:
            for x, y in coords:
                theta = (x / width) * 2 * math.pi - math.pi / 2
                X = r * math.cos(theta)
                Z = 500.0 + r * math.sin(theta)
                Y = (y - height / 2) * scale
                out.write(f"{count} {X:.6f} {-Y:.6f} {-Z:.6f}\n")
                count += 1

print(f"Model saved to {output_file}")