from Djikstra import Djikstra

with open('data/aoc-2019-06.txt') as f:
    dat = [x.strip() for x in f.readlines()]

pairs = [p.split(')') for p in dat]

deps = {}
objs = set()

for a, b in pairs:
    objs.add(a)
    objs.add(b)

    if a in deps:
        deps[a] += [b]
    else:
        deps[a] = [b]

    if b in deps:
        deps[b] += [a]
    else:
        deps[b] = [a]

com_weights, com_paths = Djikstra(objs, deps, 'COM')
print('Part 1:', sum(com_weights.values()))

you_weights, you_paths = Djikstra(objs, deps, 'YOU')
print('Part 2:', you_weights['SAN'] - 2)
