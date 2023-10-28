with open('data/aoc-2019-03.txt') as f:
    dat = [x.strip() for x in f.readlines()]

wire1 = dat[0].split(',')
wire2 = dat[1].split(',')

wire1_pts = {}
x, y, steps = 0, 0, 0
for move in wire1:
    if move[0] == 'R':
        dx = 1
        dy = 0
    elif move[0] == 'L':
        dx = -1
        dy = 0
    elif move[0] == 'D':
        dx = 0
        dy = 1
    elif move[0] == 'U':
        dx = 0
        dy = -1
    else:
        print(f'Invalid move {move}')
        exit()
    dist = int(move[1:])
    if dx != 0:
        for i in range(dist):
            pt = (x + dx * (i + 1), y)
            if pt not in wire1_pts:
                wire1_pts[pt] = steps + i + 1
        x += dx * dist
    else:
        for i in range(dist):
            pt = (x, y + dy * (i + 1))
            if pt not in wire1_pts:
                wire1_pts[pt] = steps + i + 1
        y += dy * dist
    steps += dist

intersects = {}
x, y, steps = 0, 0, 0
for move in wire2:
    if move[0] == 'R':
        dx = 1
        dy = 0
    elif move[0] == 'L':
        dx = -1
        dy = 0
    elif move[0] == 'D':
        dx = 0
        dy = 1
    elif move[0] == 'U':
        dx = 0
        dy = -1
    else:
        print(f'Invalid move {move}')
        exit()
    dist = int(move[1:])
    if dx != 0:
        for i in range(dist):
            pt = (x + dx * (i + 1), y)
            if pt in wire1_pts:
                intersects[pt] = wire1_pts[pt] + steps + i + 1
        x += dx * dist
    else:
        for i in range(dist):
            pt = (x, y + dy * (i + 1))
            if pt in wire1_pts:
                intersects[pt] = wire1_pts[pt] + steps + i + 1
        y += dy * dist
    steps += dist

dists = [abs(x[0]) + abs(x[1]) for x in intersects.keys()]
print('Part 1:', min(dists))
print('Part 2:', min(intersects.values()))
