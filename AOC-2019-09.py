from itertools import permutations
from collections import namedtuple, deque
from enum import Enum

class ParamSrc(Enum):
    NONE = 0
    PROGRAM = 1
    INPUT = 2

class ResultDest(Enum):
    NONE = 0
    PROGRAM = 1
    OUTPUT = 2
    PC = 3
    RB = 4

EvalResult = namedtuple('EvalResult', ['mem_change', 'output', 'new_pc', 'new_rb'])

class Instr:
    def __init__(self, opcode, param_cnt, param_src, result_dest, eval_fun):
        self.opcode = opcode
        self.param_cnt = param_cnt
        self.param_src = param_src
        self.result_dest = result_dest
        self.eval_fun = eval_fun

    def eval(self, program, start_pc, rb, inputs = []):
        pc = start_pc
        op = program[pc]
        assert op % 100 == self.opcode, 'Wrong opcode requested for eval'

        if op == 99:
            return EvalResult({}, [], None, None)

        pc += 1
        op = op // 10

        if self.param_src == ParamSrc.PROGRAM:
            params = []
            for i in range(self.param_cnt):
                op = op // 10
                param_mode = op % 10
                if param_mode == 0:
                    if program[pc + i] in program:
                        params += [program[program[pc + i]]]
                    else:
                        params += [0]
                elif param_mode == 1:
                    params += [program[pc + i]]
                elif param_mode == 2:
                    params += [program[program[pc + i] + rb]]
                else:
                    assert False, 'Invalid param_mode for src'
            pc += self.param_cnt
        elif self.param_src == ParamSrc.INPUT:
            params = inputs
        elif self.param_src == ParamSrc.NONE:
            params = []
        else:
            assert False, 'Invalid ParamSrc'

        val = self.eval_fun(*params)

        if self.result_dest == ResultDest.PROGRAM:
            op = op // 10
            param_mode = op % 10
            if param_mode == 0:
                return EvalResult({program[pc]: val}, [], pc + 1, rb)
            elif param_mode == 1:
                assert False, 'WTF'
                return EvalResult({program[pc]: val}, [], pc + 1, rb)
            elif param_mode == 2:
                return EvalResult({program[pc] + rb: val}, [], pc + 1, rb)
            else:
                assert False, 'Invalid param_mode for dest'
        elif self.result_dest == ResultDest.OUTPUT:
            return EvalResult({}, [val], pc, rb)
        elif self.result_dest == ResultDest.PC:
            if val:
                return EvalResult({}, [], params[-1], rb)
            else:
                return EvalResult({}, [], pc, rb)
        elif self.result_dest == ResultDest.RB:
            return EvalResult({}, [], pc, rb + val)
        else:
            assert False, 'Invalid ResultDest'

IC_INSTRS = { 1:  Instr(1,  2, ParamSrc.PROGRAM, ResultDest.PROGRAM, lambda a, b: a + b),
              2:  Instr(2,  2, ParamSrc.PROGRAM, ResultDest.PROGRAM, lambda a, b: a * b),
              3:  Instr(3,  1, ParamSrc.INPUT,   ResultDest.PROGRAM, lambda a: a),
              4:  Instr(4,  1, ParamSrc.PROGRAM, ResultDest.OUTPUT,  lambda a: a),
              5:  Instr(5,  2, ParamSrc.PROGRAM, ResultDest.PC,      lambda a, b: a != 0),
              6:  Instr(6,  2, ParamSrc.PROGRAM, ResultDest.PC,      lambda a, b: a == 0),
              7:  Instr(7,  2, ParamSrc.PROGRAM, ResultDest.PROGRAM, lambda a, b: 1 if a < b else 0),
              8:  Instr(8,  2, ParamSrc.PROGRAM, ResultDest.PROGRAM, lambda a, b: 1 if a == b else 0),
              9:  Instr(9,  1, ParamSrc.PROGRAM, ResultDest.RB,      lambda a: a),
              99: Instr(99, 0, ParamSrc.NONE,    ResultDest.NONE,    None) 
            }

with open('data/aoc-2019-09.txt') as f:
    dat = [x.strip() for x in f.readlines()]

base_program = [int(x) for x in dat[0].split(',')]

def run_program(base_program, inp):
    program = {i: v for i, v in enumerate(base_program)}
    pc = 0
    rb = 0
    outputs = []
    inp_deque = deque(inp)

    while pc is not None:
        opcode = program[pc] % 100
        instr = IC_INSTRS[opcode]
        if instr.param_src == ParamSrc.INPUT:
            instr_inp = [inp_deque.popleft()]
        else:
            instr_inp = []
        er = instr.eval(program, pc, rb, instr_inp)
        outputs += er.output
        for k, v in er.mem_change.items():
            program[k] = v
        pc = er.new_pc
        rb = er.new_rb

    return outputs

def part1():
    out = run_program(base_program, [1])
    return out[0]

print('Part 1:', part1())

def part2():
    out = run_program(base_program, [2])
    return out[0]

print('Part 2:', part2())
