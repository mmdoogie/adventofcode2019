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

def djikstra(point_set, neighbors_dict, start_point, end_point = None):
    visited = set()
    weights = dict()
    paths = dict()

    curr_point = start_point
    weights[curr_point] = 0
    paths[curr_point] = [curr_point]
    
    explore = dict()
    explore[curr_point] = 0

    while len(visited) < len(point_set):
        del(explore[curr_point])
        curr_weight = weights[curr_point] + 1
        currPath = paths[curr_point] 
        visited.add(curr_point)
        if end_point is not None and curr_point == end_point:
            break
        if curr_point in neighbors_dict:
            for n in neighbors_dict[curr_point]:
                if n not in weights or curr_weight < weights[n]:
                    weights[n] = curr_weight
                    paths[n] = currPath + [n]
                if n not in visited:
                    explore[n] = curr_weight
        cand = sorted(list(explore.items()), key=lambda x: x[1])
        if len(cand) == 0:
            break
        curr_point, curr_weight = cand[0]

    return weights, paths

com_weights, com_paths = djikstra(objs, deps, 'COM')
print('Part 1:', sum(com_weights.values()))

you_weights, you_paths = djikstra(objs, deps, 'YOU')
print('Part 2:', you_weights['SAN'] - 2)
