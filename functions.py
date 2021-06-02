ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return filename[1] in ALLOWED_EXTENSIONS


def to16(x):
    x = hex(x)[2:]
    if len(x) == 1:
        x = '0' + x
    return (x)


def get_distance(r, g, b, c):
    return (((r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2) ** (1 / 2))


def move_centroid(c, cl):
    sr, sg, sb = 0, 0, 0
    for (r, g, b) in cl:
        sr += r
        sg += g
        sb += b
    n = len(cl)
    c = (sr // n, sg // n, sb // n)
    return (c)


def init_centroid(data, imheight, imwidth):
    centroids = set()
    max_value = [(256, 256, 256) for x in range(3)]
    min_value = [(-1, -1, -1) for x in range(3)]

    n = len(data)

    for i in range(3):
        for point in data:
            if point not in centroids:
                if point[i] < max_value[i][i]:
                    max_value[i] = point
        if max_value[i] != (256, 256, 256):
            centroids.add(max_value[i])

        for point in data:
            if point not in centroids:
                if point[i] > min_value[i][i]:
                    min_value[i] = point
        if min_value[i] != (-1, -1, -1):
            centroids.add(min_value[i])

    return (list(centroids), len(centroids))


def get_clasters(data, centroids, clasters, status):
    k = len(centroids)
    new_clasters = [[] for x in range(k)]

    for (r, g, b) in data:
        min_distance = (100000000, 0)
        for i in range(k):
            distance = (get_distance(r, g, b, centroids[i]), i)
            if distance[0] < min_distance[0]:
                min_distance = distance
        new_clasters[min_distance[1]].append((r, g, b))

    mark = True
    for i in range(k):
        mark = mark and (new_clasters[i] == clasters[i])
    if mark:
        status = 'done'

    return (new_clasters, status)


def getDC(im, imwidth, imheight):
    data = list(im.getdata())
    clasters = [[] for x in range(6)]
    status = 'progress'
    centroids, k = init_centroid(data, imheight, imwidth)
    while status == 'progress':
        clasters, status = get_clasters(data, centroids, clasters, status)
        for i in range(k):
            centroids[i] = move_centroid(centroids[i], clasters[i])

    new_clasters = [(centroids[i], len(clasters[i])) for i in range(k)]
    new_clasters.sort(key=lambda param: -param[1])
    return new_clasters, k