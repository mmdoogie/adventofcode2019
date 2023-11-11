def Djikstra(neighbors_dict, start_point, end_point = None):
    visited = set()
    weights = dict()
    paths = dict()

    curr_point = start_point
    weights[curr_point] = 0
    paths[curr_point] = [curr_point]

    explore = dict()
    explore[curr_point] = 0

    while True:
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

def WeightedDjikstra(neighbors_dict, weights_dict, start_point, end_point = None):
    visited = set()
    weights = dict()
    paths = dict()

    curr_point = start_point
    weights[curr_point] = 0
    paths[curr_point] = [curr_point]

    explore = dict()
    explore[curr_point] = 0

    while True:
        del(explore[curr_point])
        currPath = paths[curr_point]
        visited.add(curr_point)
        if end_point is not None and curr_point == end_point:
            break
        if curr_point in neighbors_dict:
            for n in neighbors_dict[curr_point]:
                curr_weight = weights[curr_point] + weights_dict[(curr_point, n)]
                if n not in weights or curr_weight < weights[n]:
                    weights[n] = curr_weight
                    paths[n] = currPath + [n]
                if n not in visited:
                    explore[n] = curr_weight
        cand = sorted(list(explore.items()), key=lambda x: x[1])
        if len(cand) == 0:
            break
        curr_point, _ = cand[0]

    return weights, paths
