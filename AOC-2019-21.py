from IntcodeComputer import IntcodeComputer, PartialResult, IOMode

with open('data/aoc-2019-21.txt') as f:
    dat = [x.strip() for x in f.readlines()]

base_program = [int(x) for x in dat[0].split(',')]

def run_springscript(script):
    ic = IntcodeComputer(base_program, io_mode = IOMode.ASCII)
    res = ic.run_partial()
    assert res == PartialResult.WAIT_INPUT
    out = ic.all_outputs()
    ic.queue_inputs('\n'.join(script) + '\n')
    res = ic.run_partial()
    out1 = ic.out_deque.pop()
    if out1 > 256:
        return out1
    else:
        print(ic.all_outputs() + chr(out1))

def part1():
    return run_springscript(['OR A T', 'AND B T', 'AND C T', 'AND D T', 'NOT T J', 'AND D J', 'WALK'])

print('Part 1:', part1())

def part2():
    return run_springscript(['OR A T', 'AND B T', 'AND C T', 'AND D T', 'NOT T J', 'AND D J', 'AND H J', 'NOT A T', 'OR T J', 'RUN'])

print('Part 2:', part2())
