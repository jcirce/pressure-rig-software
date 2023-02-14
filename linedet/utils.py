import numpy as np

def pixel_distances(corners, shape):
    p = np.reshape(corners, shape)
    dist = []
    for i in range(p.shape[0]):
        #horiz distance
        for j in range(p[i].shape[0]-1):
        # print(p[i], type(p[i]))
            point1 = p[i][j]
            point2 = p[i][j+1]
            horiz_dist = np.linalg.norm(point1 - point2)
            dist.append(horiz_dist)
        #vert distance
        if i == p.shape[0]-1:
            break
        else:
            for k in range(p[i].shape[0]):
                vpoint1 = p[i][k]
                vpoint2 = p[i+1][k]
                vert_dist = np.linalg.norm(vpoint1-vpoint2)
                dist.append(vert_dist)
    npdist = np.array(dist)
    avg_dist = np.average(npdist)
    std_dev = np.std(npdist)
    print("avg dist btwn pixels: " + str(avg_dist))
    print("std dev: " + str(std_dev))
    return avg_dist
