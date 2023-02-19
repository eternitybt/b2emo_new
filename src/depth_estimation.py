import numpy as np

#GRAYSCALE = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
GRAYSCALE = '@%#*+=-:. '
GRAYSCALE_LEN = len(GRAYSCALE)

def sample(depth_map, fac=1):
    dm_shape_red = (int(depth_map.shape[0])//fac, int(depth_map.shape[1])//fac)
    depth_map_red = np.zeros(dm_shape_red)

    for ix in range(dm_shape_red[1]):
        for iy in range(dm_shape_red[0]):
            depth_map_red[iy][ix] = depth_map[iy*fac][ix*fac][0] * (GRAYSCALE_LEN/256.0)

    return depth_map_red


def evaluate(depth_map):
    LX = depth_map.shape[1]
    LY = depth_map.shape[0]

    DANGER_HORIZON_Y2 = int(LY * (3.0/4.0))
    NPIX_EXTREME_DANGER = LX*(LY - DANGER_HORIZON_Y2)

    DANGER_IGNORE_X = int(LX * (1.0/5.0))
    DANGER_HORIZON_Y1 = int(LY * (1.0/3.0))
    NPIX_DANGER1 = (LX - 2*DANGER_IGNORE_X)*DANGER_HORIZON_Y1
    #NPIX_DANGER2 = (LX - 2*DANGER_IGNORE_X)*(DANGER_HORIZON_Y2 - DANGER_HORIZON_Y1)
    NPIX_DANGER2_LINE = (LX - 2*DANGER_IGNORE_X)

    count = 0
    for iy in range(DANGER_HORIZON_Y2, LY):
        for ix in range(LX):
            if GRAYSCALE[int(depth_map[iy][ix])] != ' ':
                count += 1
            if count > int(0.05*NPIX_EXTREME_DANGER):
                return "EXTREME DANGER"

    count = 0
    for iy in range(0, DANGER_HORIZON_Y1):
        for ix in range(DANGER_IGNORE_X, LX - DANGER_IGNORE_X):
            if GRAYSCALE[int(depth_map[iy][ix])] == ' ':
                count += 1
            if count > int(0.05*NPIX_DANGER1):
                return "DANGER (1): " + str(count/NPIX_DANGER1)

    lines_count = 0
    for iy in range(DANGER_HORIZON_Y1, DANGER_HORIZON_Y2):
        count = 0
        for ix in range(DANGER_IGNORE_X, LX - DANGER_IGNORE_X):
            if GRAYSCALE[int(depth_map[iy][ix])] == ' ':
                count += 1
        if (count < int(0.8*NPIX_DANGER2_LINE)) and (count > int(0.2*NPIX_DANGER2_LINE)):
            lines_count += 1

    if lines_count > int(0.1*(DANGER_HORIZON_Y2 - DANGER_HORIZON_Y1)):
        #return "DANGER (2): " + str(count/NPIX_DANGER2_LINE) + ", iy = " + str(iy)
        return "DANGER (2): lines_count = " + str(lines_count)

    return "SAFE TO PROCEED"


def print_map(depth_map, idx_str=''):
    depth_map_print = sample(depth_map, fac=10)

    print()
    if idx_str == '':
        print('||================================================================================================||')
    else:
        print(f'||========================================= DEPTH MAP {idx_str} =========================================||')
    for iy in range(depth_map_print.shape[0]):
        print('||', end='')
        for ix in range(depth_map_print.shape[1]):
            print(GRAYSCALE[int(depth_map_print[iy][ix])], end='')
            print(GRAYSCALE[int(depth_map_print[iy][ix])], end='')
        print('||')
    print('||================================================================================================||')
