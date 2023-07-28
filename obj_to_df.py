def calculate_distance(vertices, edges, grid_size):
    
    
    grid = np.full((grid_size, grid_size, grid_size), 9999)  # initializing the grid with a large value

    # iterate over each line segment
    for edge in edges:
        for i in range(len(edge)-1):
            v1 = vertices[edge[i]].astype(int)
            v2 = vertices[edge[i + 1]  ].astype(int)

            #bresenham algorithm to get the voxels 
            voxels = get_line_voxels2(v1, v2, grid_size)

            # distance from the line segment for each voxel and 
            #update the grid
            for voxel in voxels:
                x, y, z = voxel
                voxel_center = np.array([x + 0.5, y + 0.5, z + 0.5])
                dist = point_to_line_dist9(voxel_center, v1, v2)
                grid[x, y, z] = min(grid[x, y, z], dist)
            
    return grid

#bresenham algorithm to get the voxels 
def get_line_voxels2(p1, p2, grid_size):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)
    sx = 1 if x2 >= x1 else -1
    sy = 1 if y2 >= y1 else -1
    sz = 1 if z2 >= z1 else -1

    voxels = []
    x, y, z = x1, y1, z1

    # Driving axis is X-axis
    if dx >= dy and dx >= dz:
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while x != x2:
            voxels.append((x, y, z))
            if p1 >= 0:
                y += sy
                p1 -= 2 * dx
            if p2 >= 0:
                z += sz
                p2 -= 2 * dx
            x += sx
            p1 += 2 * dy
            p2 += 2 * dz

    # Driving axis is Y-axis
    elif dy >= dx and dy >= dz:
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y != y2:
            voxels.append((x, y, z))
            if p1 >= 0:
                x += sx
                p1 -= 2 * dy
            if p2 >= 0:
                z += sz
                p2 -= 2 * dy
            y += sy
            p1 += 2 * dx
            p2 += 2 * dz

    # Driving axis is Z-axis
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z != z2:
            voxels.append((x, y, z))
            if p1 >= 0:
                y += sy
                p1 -= 2 * dz
            if p2 >= 0:
                x += sx
                p2 -= 2 * dz
            z += sz
            p1 += 2 * dy
            p2 += 2 * dx

    voxels.append((x2, y2, z2))  
    return voxels
def point_to_line_dist9(p, p1, p2):
    # the distance between point p and the line segment defined by points p1 and p2

    v = p2 - p1
    w = p - p1
    
    t = np.dot(w, v) / np.dot(v, v)

    # parameter t to the range [0, 1]
    t = max(0, min(1, t))

    # closest point on the line segment
    closest_point = p1 + t * v

    # Check if the closest point lies within the line segment
    if t < 0:
        closest_point = p1
    elif t > 1:
        closest_point = p2

    # distance between p and the closest point
    dist = np.linalg.norm(p - closest_point)

    return dist

vertices, edges = load_obj("network_29.obj")
grid_size =400
grid = calculate_distance2_new_main(vertices, edges, grid_size)
