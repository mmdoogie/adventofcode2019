from math import gcd, atan2, pi
from collections import namedtuple

with open('data/aoc-2019-10.txt') as f:
    dat = [x.strip() for x in f.readlines()]

Point = namedtuple('Point', ['x', 'y'])

asteroids = set()

for y, l in enumerate(dat):
    for x, c in enumerate(l):
        if c == '#':
            asteroids.add(Point(x, y))

def dist(src, dst):
    return abs(dst.x - src.x) + abs(dst.y - src.y)

def angle(slp):
    if slp.x < 0 and slp.y < 0:
        return atan2(slp.y, slp.x) + 5 * pi / 2
    else:
        return atan2(slp.y, slp.x) + pi / 2

visible = {}
vslopes = {}
for cand in asteroids:
    slopes = {}
    for oth in asteroids:
        if cand == oth:
            continue
        dx = oth.x - cand.x
        dy = oth.y - cand.y

        adx = abs(dx)
        ady = abs(dy)

        if adx == 0:
            dx = 0
            dy = dy // ady
        elif ady == 0:
            dx = dx // adx
            dy = 0
        elif adx == ady:
            dx = dx // adx
            dy = dy // ady
        else:
            dx = dx // gcd(adx, ady)
            dy = dy // gcd(adx, ady)

        slp = Point(dx, dy)
        dst = adx + ady
        if slp not in slopes:
            slopes[slp] = [oth]
        else: 
            slopes[slp] += [oth]

    visible[cand] = len(slopes.keys())
    vslopes[cand] = slopes

sta_loc, max_visible = max(visible.items(), key = lambda x: x[1])
print('Part 1:', max_visible)

assert len(vslopes[sta_loc].keys()) > 200
elim = sorted(vslopes[sta_loc].items(), key = lambda x: angle(x[0]))[199]
dists = {x: dist(sta_loc, x) for x in elim[1]}
last_ast = sorted(dists, key = lambda x: x[1])[0]
print('Part 2:', last_ast.x * 100 + last_ast.y)
