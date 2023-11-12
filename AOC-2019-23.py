from IntcodeComputer import IntcodeComputer

with open('data/aoc-2019-23.txt') as f:
    dat = [x.strip() for x in f.readlines()]

base_program = [int(x) for x in dat[0].split(',')]

def part1():
    ics = {}
    for addr in range(50):
        ic = IntcodeComputer(base_program)
        ics[addr] = ic
        ic.input(addr)
        ic.run_partial()

    outputs = {}
    while True:
        inputs = outputs
        outputs = {}
        for addr in range(50):
            if addr in inputs:
                for ip in inputs[addr]:
                    ics[addr].queue_inputs(ip)
            else:
                ics[addr].input(-1)
            ics[addr].run_partial()
            if len(o := ics[addr].all_outputs()) > 0:
                for op in [o[i:i+3] for i in range(0, len(o), 3)]:
                    addr, x, y = op
                    if addr == 255:
                        return y
                    if addr in outputs:
                        outputs[addr] += [[x, y]]
                    else:
                        outputs[addr] = [[x, y]]

print('Part 1:', part1())

def part2():
    ics = {}
    for addr in range(50):
        ic = IntcodeComputer(base_program)
        ics[addr] = ic
        ic.input(addr)
        ic.run_partial()

    outputs = {}
    natvalue = None
    lastnaty = None
    while True:
        inputs = outputs
        outputs = {}
        for addr in range(50):
            if addr in inputs:
                for ip in inputs[addr]:
                    ics[addr].queue_inputs(ip)
            else:
                ics[addr].input(-1)
            ics[addr].run_partial()
            if len(o := ics[addr].all_outputs()) > 0:
                for op in [o[i:i+3] for i in range(0, len(o), 3)]:
                    addr, x, y = op
                    if addr == 255:
                        natvalue = [[x, y]]
                    if addr in outputs:
                        outputs[addr] += [[x, y]]
                    else:
                        outputs[addr] = [[x, y]]
        if len(outputs.keys()) == 0:
            outputs[0] = natvalue
            newnaty = natvalue[0][1]
            if newnaty == lastnaty:
                return lastnaty
            lastnaty = newnaty

print('Part 2:', part2())
