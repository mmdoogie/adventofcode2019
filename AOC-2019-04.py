from itertools import pairwise

with open('data/aoc-2019-04.txt') as f:
    dat = [x.strip() for x in f.readlines()]

def valid_pwd_pt1(val):
    as_str = f'{val:06n}'

    if len(as_str) != 6:
        return False

    if sum([str(10 * p + p) in as_str for p in range(10)]) == 0:
        return False

    for a, b in pairwise(as_str):
        if b < a:
            return False

    return True

in_range = [int(x) for x in dat[0].split('-')]

valid_cnt = 0
for pwd in range(in_range[0], in_range[1] + 1):
    if valid_pwd_pt1(pwd):
        valid_cnt += 1

print('Part 1:', valid_cnt)

def valid_pwd_pt2(val):
    as_str = f'{val:06n}'

    if len(as_str) != 6:
        return False

    rep_ok = False
    for p in range(10):
        rep_val = str(p) + str(p)
        if rep_val in as_str:
            rep_ok = True
            for _ in range(4):
                rep_val = rep_val + str(p)
                if rep_val in as_str:
                    rep_ok = False
            if rep_ok:
                break
    if not rep_ok:
        return False

    if sum([str(10 * p + p) in as_str for p in range(10)]) == 0:
        return False

    for a, b in pairwise(as_str):
        if b < a:
            return False

    return True

valid_cnt_2 = 0
for pwd in range(in_range[0], in_range[1] + 1):
    if valid_pwd_pt2(pwd):
        valid_cnt_2 += 1

print('Part 2:', valid_cnt_2)
