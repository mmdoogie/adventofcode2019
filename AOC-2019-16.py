from itertools import chain, repeat, cycle, islice, accumulate
import operator

with open('data/aoc-2019-16.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def place_iter(place):
    return islice(cycle(chain(repeat(0, place), repeat(1, place), repeat(0, place), repeat(-1, place))), 1, None)

def phase(inp):
    return [abs(sum([a*b for a,b in zip(place_iter(p+1), inp)])) % 10 for p in range(len(inp))]

def part1():
    inp = [int(d) for d in dat[0]]
    for r in range(100):
        inp = phase(inp)
    return inp[0:8]

print('Part 1:', ''.join([str(v) for v in part1()]))

def part2():
    inp = [int(d) for d in dat[0]]
    full_inp = inp * 10000
    offset = int(dat[0][0:7])
    part_inp = full_inp[offset:]
    assert len(part_inp) < offset

    for r in range(100):
        cs = [0] + list(accumulate(part_inp, operator.add))
        part_inp = [(cs[-1] - c) % 10 for c in cs]
    return part_inp[0:8]

print('Part 2:', ''.join([str(v) for v in part2()]))
