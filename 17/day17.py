import os
import re
import random

def parse(input):
    with open(input, 'r') as f:
        registers, program = f.read().split("\n\n")
        registers = registers.split("\n")
        A, B, C = [int(r.split(": ")[1]) for r in registers]

        program = list(map(int, program.split(": ")[1].split(",")))

        return {"A": A, "B": B, "C": C}, program

def combo(v, regs):
    if 0 <= v <= 3:
        return v
    if v == 4:
        return regs["A"]
    elif v == 5:
        return regs["B"]
    elif v == 6:
        return regs["C"]
    assert False

def dec_combo(v):
    if 0 <= v <= 3:
        return v
    if v == 4:
        return A
    elif v == 5:
        return B
    elif v == 6:
        return C
    assert False

A = "A"
B = "B"
C = "C"

def decompile(program):
    decompiled = []

    pc = 0
    while pc < len(program):
        op = program[pc]
        if op == 0:
            decompiled.append("{}{}".format("A = A / 2^", dec_combo(program[pc + 1])))
        elif op == 1:
            decompiled.append("{} {}".format("B = B XOR", program[pc + 1]))
        elif op == 2:
            decompiled.append("{} {} {}".format("B =", dec_combo(program[pc + 1]), "mod 8"))
        elif op == 3:
            decompiled.append("{} {}".format("jnz", program[pc + 1]))
        elif op == 4:
            decompiled.append("{}".format("B = B XOR C"))
        elif op == 5:
            decompiled.append("{} {} {}".format("out", dec_combo(program[pc + 1]), "mod 8"))
        elif op == 6:
            decompiled.append("{}{}".format("B = A / 2^", dec_combo(program[pc + 1])))
        elif op == 7:
            decompiled.append("{}{}".format("C = A / 2^", dec_combo(program[pc + 1])))
        pc += 2

    return decompiled

def opcode(op, operand, regs, output, program, p):
    pc = None
    if op == 0:
        numerator = regs[A]
        regs[A] = numerator // (2 ** combo(operand, regs))
    elif op == 1:
        regs[B] ^= operand
    elif op == 2:
        regs[B] = combo(operand, regs) % 8
    elif op == 3:
        if regs[A] != 0:
            pc = operand
    elif op == 4:
        regs[B] ^= regs[C]
    elif op == 5:
        output.append(combo(operand, regs) % 8)
    elif op == 6:
        numerator = regs[A]
        regs[B] = numerator // (2 ** combo(operand, regs))
    elif op == 7:
        numerator = regs[A]
        regs[C] = numerator // (2 ** combo(operand, regs))

    # print(regs, output, decompile(program[p:p+2]))
    # if pc is not None:
    #     print("loop restart")
    # if output:
    #     print(int(''.join(map(str, output)), 8))

    return pc

def run(program, regs):
    operand = None
    pc = 0
    output = []
    while pc < len(program):
        operand = program[pc + 1]
        npc = opcode(program[pc], operand, regs, output, program, pc)
        if npc is None:
            pc += 2
        else:
            pc = npc

        assert pc % 2 == 0 
    
    return output

def rec(nn, regs, program, target, i):
    if i == -1:
        regs[A] = nn
        regs[B] = 0
        regs[C] = 0

        if run(program, regs) == target:
            return nn
    else:
        for j in range(0, 8):
            val = (nn << 3) + j
            regs[A] = val
            regs[B] = 0
            regs[C] = 0
            res = run(program, regs)
            if res == target[i:]:
                print(res)
                res = rec(val, regs, program, target, i - 1)
                if res:
                    return res
    
def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    regs, program = parse(day_path)
    print('\n'.join(decompile(program)))
    part1 = run(program, regs)

    digits = []
    target = [2,4,1,1,7,5,1,5,4,3,5,5,0,3,3,0]
    part2 = rec(0, regs, program, target, len(target) - 1)

    return ','.join(map(str, part1)), part2

print(solve("input.txt"))