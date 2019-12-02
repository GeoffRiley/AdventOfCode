from itertools import product


def computer(cells):
    c = [int(v) for v in cells.split(',')]
    c = simulate(c)
    return ','.join(str(v) for v in c)


def simulate(c):
    pc = 0
    while c[pc] != 99:
        if c[pc] == 1:
            c[c[pc + 3]] = c[c[pc + 1]] + c[c[pc + 2]]
            pc += 4
        elif c[pc] == 2:
            c[c[pc + 3]] = c[c[pc + 1]] * c[c[pc + 2]]
            pc += 4
        else:
            raise TypeError
    return c


def run_computer_recover(cells):
    c = [int(v) for v in cells.split(',')]
    c[1] = 12
    c[2] = 2
    c = simulate(c)
    print(c[0])


def find_key_inputs(cells):
    target = 19690720
    result = 0
    for noun, verb in product(range(100), range(100)):
        c = [int(v) for v in cells.split(',')]
        c[1] = noun
        c[2] = verb
        c = simulate(c)
        result = c[0]
        if result == target:
            print(f'Noun: {noun}, Verb: {verb} results in {c[0]}')

OPCODES = {1:'+', 2:'*', 99:'halt'}

def opcode(memory, pc):
    op, a, b, c = memory[pc:pc+4]
    dump = " ".join(f'{v:02x}' for v in memory[pc:pc+4])
    if op < 99:
        return f'{dump} : [{c:02x}] ← [{a:02x}] {OPCODES[op]} [{b:02x}]'
    else:
        return f'{dump} : HALT'

def disassemble(cells):
    memory = [int(v) for v in cells.split(',')]
    targets = set()
    pc = 0
    while pc < len(memory)-3:
        targets.add(memory[pc+1])
        targets.add(memory[pc+2])
        pc += 4
    pc = 0
    targets = sorted(targets)
    while pc < len(memory)-3:
        print(f'{pc:04x} : {opcode(memory,pc)}')
        pc += 4


if __name__ == '__main__':
    initial_cells = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,9,23,27,2,27,6,31,1,5,31,35,2,9,35,39,2,6,39,43,2,43,13,47,2,13,47,51,1,10,51,55,1,9,55,59,1,6,59,63,2,63,9,67,1,67,6,71,1,71,13,75,1,6,75,79,1,9,79,83,2,9,83,87,1,87,6,91,1,91,13,95,2,6,95,99,1,10,99,103,2,103,9,107,1,6,107,111,1,10,111,115,2,6,115,119,1,5,119,123,1,123,13,127,1,127,5,131,1,6,131,135,2,135,13,139,1,139,2,143,1,143,10,0,99,2,0,14,0'
    run_computer_recover(initial_cells)
    find_key_inputs(initial_cells)
    disassemble(initial_cells)

"""
01: noun
02: verb
0000 : 01 00 00 03 : [03] ← [00] + [00] # [03] = 1 + 1 = 2
0004 : 01 01 02 03 : [03] ← [01] + [02] # [03] = noun + verb
0008 : 01 03 04 03 : [03] ← [03] + [04] # [03] = noun + verb + 1
000c : 01 05 00 03 : [03] ← [05] + [00] # [03] = 1 + 1 = 2
0010 : 02 09 01 13 : [13] ← [09] * [01] # [13] = 3 * noun
0014 : 01 13 05 17 : [17] ← [13] + [05] # [17] = (3 * noun) + 1
0018 : 01 09 17 1b : [1b] ← [09] + [17] # [1b] = 3 + (3 * noun) + 1 = (3 * noun) + 4
001c : 02 1b 06 1f : [1f] ← [1b] * [06] # [1f] = ((3 * noun) + 4) * 2 = (6 * noun) + 8
0020 : 01 05 1f 23 : [23] ← [05] + [1f] # [23] = 1 + (6 * noun) + 8 = (6 * noun) + 9
0024 : 02 09 23 27 : [27] ← [09] * [23] # [27] = 3 * ((6 * noun) + 9) = 18 * noun + 27
0028 : 02 06 27 2b : [2b] ← [06] * [27] # [2b] = 2 * (18 * noun + 27) = 36 * noun + 54
002c : 02 2b 0d 2f : [2f] ← [2b] * [0d] # [2f] = (36 * noun + 54) * 5 = 180 * noun + 270
0030 : 02 0d 2f 33 : [33] ← [0d] * [2f] # [33] = 5 * (180 * noun + 270) = 900 * noun + 1350
0034 : 01 0a 33 37 : [37] ← [0a] + [33] # [37] = 4 + (900 * noun + 1350) = 900 * noun + 1354
0038 : 01 09 37 3b : [3b] ← [09] + [37] # [3b] = 3 + (900 * noun + 1354) = 900 * noun + 1357
003c : 01 06 3b 3f : [3f] ← [06] + [3b] # [3f] = 2 + (900 * noun + 1357) = 900 * noun + 1359
0040 : 02 3f 09 43 : [43] ← [3f] * [09] # [43] = (900 * noun + 1359) * 3 = 2700 * noun + 4077
0044 : 01 43 06 47 : [47] ← [43] + [06] # [47] = (2700 * noun + 4077) + 2 = 2700 * noun + 4079
0048 : 01 47 0d 4b : [4b] ← [47] + [0d] # [4b] = (2700 * noun + 4079) + 5 = 2700 * noun + 4084
004c : 01 06 4b 4f : [4f] ← [06] + [4b] # [4f] = 2 + (2700 * noun + 4085) = 2700 * noun + 4086
0050 : 01 09 4f 53 : [53] ← [09] + [4f] # [53] = 3 + (2700 * noun + 4086) = 2700 * noun + 4089
0054 : 02 09 53 57 : [57] ← [09] * [53] # [57] = 3 * (2700 * noun + 4089) = 8100 * noun + 12267
0058 : 01 57 06 5b : [5b] ← [57] + [06] # [5b] = (8100 * noun + 12267) + 2 = 8100 * noun + 12269
005c : 01 5b 0d 5f : [5f] ← [5b] + [0d] # [5f] = (8100 * noun + 12269) + 5 = 8100 * noun + 12274
0060 : 02 06 5f 63 : [63] ← [06] * [5f] # [63] = 2 * (8100 * noun + 12274) = 16200 * noun + 24548
0064 : 01 0a 63 67 : [67] ← [0a] + [63] # [67] = 4 + (16200 * noun + 24548) = 16200 * noun + 24552
0068 : 02 67 09 6b : [6b] ← [67] * [09] # [6b] = (16200 * noun + 24552) * 3 = 48600 * noun + 73656
006c : 01 06 6b 6f : [6f] ← [06] + [6b] # [6f] = 2 + (48600 * noun + 73656) = 48600 * noun + 73658
0070 : 01 0a 6f 73 : [73] ← [0a] + [6f] # [73] = 4 + (48600 * noun + 73658) = 48600 * noun + 73662
0074 : 02 06 73 77 : [77] ← [06] * [73] # [77] = 2 * (48600 * noun + 73662) = 97200 * noun + 147324
0078 : 01 05 77 7b : [7b] ← [05] + [77] # [7b] = 1 + (97200 * noun + 147324) = 97200 * noun + 147325
007c : 01 7b 0d 7f : [7f] ← [7b] + [0d] # [7f] = (97200 * noun + 147325) + 5 = 97200 * noun + 147330
0080 : 01 7f 05 83 : [83] ← [7f] + [05] # [83] = (97200 * noun + 147330) + 1 = 97200 * noun + 147331
0084 : 01 06 83 87 : [87] ← [06] + [83] # [87] = 2 + (97200 * noun + 147331) = 97200 * noun + 147333
0088 : 02 87 0d 8b : [8b] ← [87] * [0d] # [8b] = 5 * (97200 * noun + 147333) = 486000 * noun + 736665
008c : 01 8b 02 8f : [8f] ← [8b] + [02] # [8f] = (486000 * noun + 736665) + verb
0090 : 01 8f 0a 00 : [00] ← [8f] + [0a] # [00] = (486000 * noun + 736665 + verb) + 4 = 486000 * noun + 736669 + verb
0094 : 63 02 00 0e : HALT

Code actually computes: 486000 * noun + 736669 + verb
"""