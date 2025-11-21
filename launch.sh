#!/bin/bash

# Build the project
cd build
cmake ..
make
cd ..

# Create output directory
mkdir -p macout

# Process all PNG files in macin
for file in macin/*.png; do
    if [ -f "$file" ]; then
        base=$(basename "$file")
        output="macout/$base"
        echo "Processing $file -> $output"
        ./build/CylinderTag "$file" CTag_2f12c.marker model_from_coords.model cameraParams_MacbookM4.yml "$output"
    fi
done