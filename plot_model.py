import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import glob
import os

# Define views
views = [
    {'elev': 30, 'azim': -60, 'name': 'default'},
    {'elev': 0, 'azim': 90, 'name': 'side'},
    {'elev': 90, 'azim': 0, 'name': 'top'},
    {'elev': -90, 'azim': 0, 'name': 'bottom'},
    {'elev': 0, 'azim': 0, 'name': 'front'},
    {'elev': 0, 'azim': 180, 'name': 'back'},
]

# Function to parse a model file
def parse_model_file(filepath):
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    blocks = []
    i = 1  # Skip first line
    while i < len(lines):
        id_ = int(lines[i])
        pos = list(map(float, lines[i+1].split()))
        ori = list(map(float, lines[i+2].split()))
        points = []
        for j in range(96):
            parts = lines[i+3+j].split()
            idx = int(parts[0])
            x, y, z = map(float, parts[1:])
            points.append((x, y, z))
        blocks.append({'id': id_, 'pos': pos, 'ori': ori, 'points': points})
        i += 3 + 96
    return blocks

# Get all .model files
model_files = glob.glob('*.model')

for model_file in model_files:
    basename = os.path.splitext(model_file)[0]
    folder = f'plot_{basename}'
    os.makedirs(folder, exist_ok=True)
    
    blocks = parse_model_file(model_file)
    
    for block in blocks:
        block_id = block['id']
        block_folder = f'{folder}/block_{block_id}'
        os.makedirs(block_folder, exist_ok=True)
        
        points = block['points']
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [p[2] for p in points]
        
        # 3D views
        for view in views:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(xs, ys, zs, c=zs, cmap='viridis')
            for idx, (x, y, z) in enumerate(zip(xs, ys, zs)):
                if idx < 33:
                    ax.text(x, y, z, str(idx), fontsize=8)
            # Draw planes using every 4 points
            for i in range(0, len(points), 4):
                if i+3 < len(points):
                    verts = [(points[i][0], points[i][1], points[i][2]),
                             (points[i+1][0], points[i+1][1], points[i+1][2]),
                             (points[i+2][0], points[i+2][1], points[i+2][2]),
                             (points[i+3][0], points[i+3][1], points[i+3][2])]
                    poly = Poly3DCollection([verts], alpha=0.3, facecolors='cyan', edgecolors='black', linewidths=0.5)
                    ax.add_collection3d(poly)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(f'3D Scatter Plot - {basename} Block {block_id} - {view["name"]} view')
            ax.view_init(elev=view['elev'], azim=view['azim'])
            plt.savefig(f'{block_folder}/{basename}_block_{block_id}_{view["name"]}.png')
            plt.close(fig)
        
        # 2D projections
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        axs[0].scatter(xs, ys, c=zs, cmap='viridis')
        for idx, (x, y) in enumerate(zip(xs, ys)):
            if idx < 33:
                axs[0].text(x, y, str(idx), fontsize=6)
        axs[0].set_xlabel('X')
        axs[0].set_ylabel('Y')
        axs[0].set_title('XY Projection')
        
        axs[1].scatter(xs, zs, c=ys, cmap='viridis')
        for idx, (x, z) in enumerate(zip(xs, zs)):
            if idx < 33:
                axs[1].text(x, z, str(idx), fontsize=6)
        axs[1].set_xlabel('X')
        axs[1].set_ylabel('Z')
        axs[1].set_title('XZ Projection')
        
        axs[2].scatter(ys, zs, c=xs, cmap='viridis')
        for idx, (y, z) in enumerate(zip(ys, zs)):
            if idx < 33:
                axs[2].text(y, z, str(idx), fontsize=6)
        axs[2].set_xlabel('Y')
        axs[2].set_ylabel('Z')
        axs[2].set_title('YZ Projection')
        
        plt.tight_layout()
        plt.savefig(f'{block_folder}/{basename}_block_{block_id}_projections.png')
        plt.close(fig)

print("All plots generated for all .model files")