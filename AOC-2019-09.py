from IntcodeComputer import IntcodeComputer, PartialResult

with open('data/aoc-2019-09.txt') as f:
    dat = [x.strip() for x in f.readlines()]

base_program = [int(x) for x in dat[0].split(',')]

def part1():
    ic = IntcodeComputer(base_program)
    ic.input(1)
    res = ic.run_partial()
    assert res == PartialResult.TERMINATED
    return ic.output()

print('Part 1:', part1())

def part2():
    ic = IntcodeComputer(base_program)
    ic.input(2)
    res = ic.run_partial()
    assert res == PartialResult.TERMINATED
    return ic.output()

print('Part 2:', part2())
