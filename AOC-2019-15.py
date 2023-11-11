from Djikstra import Djikstra
from IntcodeComputer import IntcodeComputer, PartialResult
from collections import deque

with open('data/aoc-2019-15.txt') as f:
    dat = [x.strip() for x in f.readlines()]

base_program = [int(x) for x in dat[0].split(',')]
ic = IntcodeComputer(base_program)

seen = set()
walls = set()
spaces = set()
oxy = None

def point_for_dir(x, y, d):
    if d == 1:
        return (x, y - 1)
    elif d == 2:
        return (x, y + 1)
    elif d == 3:
        return (x - 1, y)
    elif d == 4:
        return (x + 1, y)

def return_dir(d):
    if d == 1:
        return 2
    elif d == 2:
        return 1
    elif d == 3:
        return 4
    elif d == 4:
        return 3

def explore(state, x, y, d):
    ic.input(d)
    ic.run_partial()
    res = ic.output()

    rpt = point_for_dir(x, y, d)
    state[rpt] = res

    if res != 0:
        for xd in range(1, 5):
            if point_for_dir(*rpt, xd) not in state:
                explore(state, *rpt, xd)

        ic.input(return_dir(d))
        ic.run_partial()
        res = ic.output()
        assert res != 0

state = {}
explore(state, 0, 0, 1)
explore(state, 0, 0, 2)
explore(state, 0, 0, 3)
explore(state, 0, 0, 4)

oxy = [k for k, v in state.items() if v == 2][0]
spaces = [k for k, v in state.items() if v != 0]
neighbors = {}
for sp in spaces:
    ngh_cand = [point_for_dir(*sp, d) for d in range(1, 5)]
    ngh = [n for n in ngh_cand if n in spaces]
    neighbors[sp] = ngh

weights, paths = Djikstra(neighbors, (0, 0), oxy)
print('Part 1:', weights[oxy])

weights, paths = Djikstra(neighbors, oxy)
print('Part 2:', max(weights.values()))
