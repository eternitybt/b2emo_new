import cv2
from depth_estimation import *

# MAIN.
for idx_str in ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10']:
    depth_map = cv2.imread('depth_maps/depth' + idx_str + '.jpg')
    print_map(depth_map, idx_str)
    depth_map_eval = sample(depth_map)
    print(evaluate(depth_map_eval))
