import itertools
from IntcodeComputer import IntcodeComputer

with open('data/aoc-2019-25.txt') as f:
    dat = [x.strip() for x in f.readlines()]

base_program = [int(x) for x in dat[0].split(',')]
ic = IntcodeComputer(base_program)

def interactive():
    while True:
        ic.run_partial()
        print(''.join([chr(x) for x in ic.all_outputs()]))
        istr = input()
        ic.queue_inputs([ord(x) for x in istr] + [10])

def to_ascii(dat):
    return ''.join([chr(x) for x in dat])

def from_ascii(dat):
    vals = [ord(x) for x in dat]
    if vals[-1] != 10:
        return vals + [10]
    else:
        return vals

def parse_room(room):
    parse = {}
    doorMode = False
    doors = []
    itemMode = False
    items = []
    for l in [x.strip() for x in room.split('\n')]:
        if l.startswith('=='):
            if 'name' in parse:
                parse['doors'] = doors
                parse['items'] = items
                return parse
            parse['name'] = l.strip('= ')
        elif l.startswith('Door'):
            doorMode = True
        elif l.startswith('Item'):
            doorMode = False
            itemMode = True
        elif l.startswith('- '):
            if doorMode:
                doors += [l.strip('- ')]
            elif itemMode:
                items += [l.strip('- ')]
            else:
                assert doorMode or itemMode
        elif l.startswith('Command'):
            parse['doors'] = doors
            parse['items'] = items
            return parse

reverse = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
trap_items = ['infinite loop', 'molten lava', 'photons', 'escape pod', 'giant electromagnet']
dirs = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}
rooms = {}
visited = set()
i_have = set()
long_dirs = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}

def explore():
    ic.run_partial()
    first_room = parse_room(to_ascii(ic.all_outputs()))
    first_room['pos'] = '*'
    visited.add('*')
    rooms[first_room['name']] = first_room
    return dfs(first_room, None)

def dfs(room, fromdir):
    path = room['pos']
    for d in room['doors']:
        if fromdir is not None and d == reverse[fromdir]:
            continue
        np = path + d[0]
        if np in visited:
            continue
        ic.queue_inputs(from_ascii(d))
        ic.run_partial()
        o = to_ascii(ic.all_outputs())
        parse = parse_room(o)
        parse['pos'] = np
        visited.add(np)
        rooms[parse['name']] = parse
        for i in parse['items']:
            if i in trap_items:
                continue
            ic.queue_inputs(from_ascii('take ' + i))
            ic.run_partial()
            ic.all_outputs()
            i_have.add(i)
        if not parse['name'].startswith('Pressure'):
            dfs(parse, d)
    if fromdir is not None:
        retdir = reverse[fromdir]
        ic.queue_inputs(from_ascii(retdir))
        ic.run_partial()
        ic.all_outputs()
    return path


loc = explore()
assert loc == '*'
for d in rooms['Security Checkpoint']['pos']:
    if d in long_dirs:
        ic.queue_inputs(from_ascii(long_dirs[d]))
        ic.run_partial()
        ic.all_outputs()

def try_combos():
    all_items = list(i_have)
    for r in range(len(all_items)):
        for combo in itertools.combinations(all_items, r):
            for ci in [c for c in combo if c not in i_have]:
                ic.queue_inputs(from_ascii('take ' + ci))
                ic.run_partial()
                o = ic.all_outputs()
                i_have.add(ci)
            for hi in [h for h in i_have if h not in combo]:
                ic.queue_inputs(from_ascii('drop ' + hi))
                ic.run_partial()
                ic.all_outputs()
                i_have.remove(hi)
            ic.queue_inputs(from_ascii('north'))
            ic.run_partial()
            out = to_ascii(ic.all_outputs())
            if not 'Security Checkpoint' in out:
                return out, combo

out, combo = try_combos()
print('Part 1:', out.split('typing ')[1].split(' ')[0])






