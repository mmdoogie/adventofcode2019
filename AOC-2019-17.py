from IntcodeComputer import IntcodeComputer, PartialResult
from itertools import combinations

with open('data/aoc-2019-17.txt') as f:
    dat = [x.strip() for x in f.readlines()]

base_program = [int(x) for x in dat[0].split(',')]

def part1(output = False):
    ic = IntcodeComputer(base_program)
    rc = ic.run_partial()
    assert rc == PartialResult.TERMINATED
    out = ic.all_outputs()

    y = 0
    x = 0
    scaffold = {}

    for o in out:
        if o == 10:
            x = 0
            y += 1
            if output:
                print()
            continue
        
        if o == 35:
            scaffold[(x, y)] = True

        if o == ord('^'):
            start_pt = (x, y)
            start_dir = (0, -1)
        elif o == ord('v'):
            start_pt = (x, y)
            start_dir = (0, 1)
        elif o == ord('<'):
            start_pt = (x, y)
            start_dir = (-1, 0)
        elif o == ord('>'):
            start_pt = (x, y)
            start_dir = (1, 0)

        if output:
            print(chr(o), end='')
        x += 1

    total = 0
    for sx, sy in scaffold.keys():
        adj = [(sx-1, sy), (sx+1, sy), (sx, sy-1), (sx, sy+1)]
        if sum([a in scaffold for a in adj]) >= 3:
            total += sx*sy

    return total, scaffold, start_pt, start_dir

total, scaffold, start_pt, start_dir = part1()
print('Part 1:', total)

def traverse(scaffold, start_pt, start_dir):
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    didx = dirs.index(start_dir)

    x, y = start_pt
    path = []

    while True:
        tcx, tcy = dirs[(didx - 1) % 4]
        if (x + tcx, y + tcy) in scaffold:
            turn = -1
            pc = 'L'
        else:
            tcx, tcy = dirs[(didx + 1) % 4]
            if (x + tcx, y + tcy) not in scaffold:
                break
            turn = 1
            pc = 'R'

        didx = (didx + turn) % 4

        cnt = 0
        while True:
            x += tcx
            y += tcy
            if (x, y) not in scaffold:
                x -= tcx
                y -= tcy
                break
            cnt += 1
        path += [pc + ',' + str(cnt)]

    return path

def find_solution(full_path):
    matches = []
    pathlen = len(full_path)
    for i, p in enumerate(full_path):
        maxlen = 0
        for j in range(i + 1, pathlen):
            subpath = ','.join(full_path[i:j])
            if len(subpath) > 20:
                break
            if subpath in ','.join(full_path[i+1:]):
                if len(subpath) > maxlen:
                    maxlen = len(subpath)
                    maxmatch = subpath
        if maxlen > 0 and maxmatch not in matches:
            matches += [maxmatch]

    matches.sort(key=lambda x: len(x), reverse=True)

    for subs in combinations(matches, 3):
        res = ','.join(full_path)
        for i, s in enumerate(subs):
            repl = chr(ord('A') + i)
            res = res.replace(s, repl)
        if 'L' in res or 'R' in res:
            continue
        return subs, res

def line_to_vals(txt):
    return [ord(c) for c in txt] + [10]

def vals_to_txt(vals):
    return ''.join([chr(v) for v in vals]).strip()

def part2(scaffold, start_pt, start_dir, output = False):
    full_path = traverse(scaffold, start_pt, start_dir)
    final_trav = ','.join(full_path)
    if output:
        print(final_trav)

    subs, res = find_solution(full_path)

    p = list(base_program)
    p[0] = 2
    ic = IntcodeComputer(p)
    rc = ic.run_partial()
    assert rc == PartialResult.WAIT_INPUT

    if output:
        print(vals_to_txt(ic.all_outputs()), end=' ')
        print(res)
    ic.queue_inputs(line_to_vals(res))

    for s in subs:
        rc = ic.run_partial()
        assert rc == PartialResult.WAIT_INPUT
        if output:
            print(vals_to_txt(ic.all_outputs()), end=' ')
            print(s)
        ic.queue_inputs(line_to_vals(s))

    rc = ic.run_partial()
    assert rc == PartialResult.WAIT_INPUT

    noline = 'n'
    if output:
        print(vals_to_txt(ic.all_outputs()), end=' ')
        print(noline)
    ic.queue_inputs(line_to_vals(noline))
    rc = ic.run_partial()
    assert rc == PartialResult.TERMINATED

    vals = ic.all_outputs()
    if output:
        print(vals_to_txt(vals))
    return vals[-1]

print('Part 2:', part2(scaffold, start_pt, start_dir))
