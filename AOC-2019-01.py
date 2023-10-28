with open('data/aoc-2019-01.txt') as f:
    dat = [x.strip() for x in f.readlines()]

fuels = [int(m) // 3 - 2 for m in dat]
totalFuel = sum(fuels)

print('Part 1:', totalFuel)

for f in fuels:
    addFuel = f // 3 - 2
    while addFuel > 0:
        totalFuel += addFuel
        addFuel = addFuel // 3 - 2

print('Part 2:', totalFuel)
