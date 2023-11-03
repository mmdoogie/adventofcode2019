from collections import namedtuple
from IntcodeComputer import IntcodeComputer, PartialResult

with open('data/aoc-2019-11.txt') as f:
    dat = [x.strip() for x in f.readlines()]

base_program = [int(x) for x in dat[0].split(',')]

Point = namedtuple('Point', ['x', 'y'])

def do_paint(initial_val = 0):
    ic = IntcodeComputer(base_program)

    panels = {}
    curr_point = Point(0, 0)
    face_dirs = [Point(0, -1), Point(1,0), Point(0, 1), Point(-1, 0)]
    face_idx = 0

    ic.input(initial_val)
    res = ic.run_partial()
    while res != PartialResult.TERMINATED:
        panel_color = ic.output()
        face_rot = ic.output()

        panels[curr_point] = panel_color
        face_idx = (face_idx + (2 * face_rot - 1)) % 4
        curr_point = Point(curr_point.x + face_dirs[face_idx].x, curr_point.y + face_dirs[face_idx].y)

        if curr_point in panels:
            ic.input(panels[curr_point])
        else:
            ic.input(0)

        res = ic.run_partial()

    return panels

print('Part 1:', len(do_paint().keys()))

panels = do_paint(initial_val = 1)
locs = panels.keys()
min_x = min([l.x for l in locs])
max_x = max([l.x for l in locs])
min_y = min([l.y for l in locs])
max_y = max([l.y for l in locs])

print('Part 2:')
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        pixel = Point(x, y)
        if Point(x, y) in panels and panels[Point(x,y)] == 1:
            print('##', end='')
        else:
            print('  ', end='')
    print()

