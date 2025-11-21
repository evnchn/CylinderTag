# Prevent Octave from thinking that this
# is a function file:

1;

pkg load image;

global tag_length

tag_length = 1200;

function plot_tag(ID, ratio)
    global tag_length
    for i=1:size(ID,1)
        background=ones(tag_length,1.5*tag_length/ratio*size(ID,2));
        [height, width] = size(background);
        all_coords = {};
        for j=1:size(ID,2)
            [background, coords_now] = draw(background,j-1,ID(i,j),ratio);
            all_coords = [all_coords, coords_now];
        end
        imwrite(background,['./CTag_Generated_FromID/cy' num2str(i-1) '.bmp'])
        fid = fopen(['./CTag_Generated_FromID/cy' num2str(i-1) '_corners.txt'], 'w');
        fprintf(fid, '%d %d\n', width, height);
        for k=1:length(all_coords)
            coords = all_coords{k};
            for p=1:4
                fprintf(fid, '%f %f\n', coords(p,1), coords(p,2));
            end
        end
        fclose(fid);
    end
end

function [background, coords]=draw(background, cnt, ID_now, ratio)
    global tag_length
    decoder=[1.47,0;1.54,0;1.61,0;1.68,0;1.68,1;1.61,1;1.54,1;1.47,1];
    white_ratio=0.2;
    left=fix(ID_now/8)+1;
    right=mod(ID_now,8)+1;
    block_pos_left=roots([-1 tag_length (white_ratio/2+white_ratio*white_ratio/4-0.2*decoder(left,1))*tag_length*tag_length]);
    block_pos_left=block_pos_left((block_pos_left>0));
    block_pos_left=block_pos_left((block_pos_left<tag_length*(1-white_ratio)));
    if decoder(left,2)
        block_pos_left = max(block_pos_left);
    else
        block_pos_left = min(block_pos_left);
    end
    block_pos_right=roots([-1 tag_length (white_ratio/2+white_ratio*white_ratio/4-0.2*decoder(right,1))*tag_length*tag_length]);
    block_pos_right=block_pos_right((block_pos_right>0));
    block_pos_right=block_pos_right((block_pos_right<tag_length*(1-white_ratio)));
    if decoder(right,2)
        block_pos_right = max(block_pos_right);
    else
        block_pos_right = min(block_pos_right);
    end
    coords1 = [tag_length/ratio * 1.5 * cnt 0; tag_length/ratio * 1.5 * cnt + tag_length/ratio 0; tag_length/ratio * 1.5 * cnt + tag_length/ratio block_pos_right-tag_length*white_ratio/2; tag_length/ratio * 1.5 * cnt block_pos_left-tag_length*white_ratio/2];
    x1 = coords1(:,1);
    y1 = coords1(:,2);
    mask1 = poly2mask(x1, y1, size(background,1), size(background,2));
    background(mask1) = 0;
    coords2 = [tag_length/ratio * 1.5 * cnt + tag_length/ratio tag_length; tag_length/ratio * 1.5 * cnt tag_length; tag_length/ratio * 1.5 * cnt block_pos_left + tag_length*white_ratio/2; tag_length/ratio * 1.5 * cnt + tag_length/ratio block_pos_right + tag_length*white_ratio/2];
    x2 = coords2(:,1);
    y2 = coords2(:,2);
    mask2 = poly2mask(x2, y2, size(background,1), size(background,2));
    background(mask2) = 0;
    coords = {coords1, coords2};
end

% Create directory if it doesn't exist
if ~exist('./CTag_Generated_FromID', 'dir')
    mkdir('./CTag_Generated_FromID');
end

% Load the marker file
filename = 'CTag_2f12c.marker';  % Change this to the desired .marker file
fid = fopen(filename, 'r');
if fid == -1
    error('Cannot open file: %s', filename);
end
header = fscanf(fid, '%d', 3);
tag_number = header(1);
tag_col = header(2);
feature_size = header(3);
ID = zeros(tag_number, tag_col);
for i = 1:tag_number
    ID(i, :) = fscanf(fid, '%d', tag_col);
end
fclose(fid);

height_width_ratio = 15;  % Assumed ratio, adjust if needed

plot_tag(ID, height_width_ratio);

disp('Bitmaps generated in ./CTag_Generated_FromID/');