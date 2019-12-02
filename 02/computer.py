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


if __name__ == '__main__':
    initial_cells = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,9,23,27,2,27,6,31,1,5,31,35,2,9,35,39,2,6,39,43,2,43,13,47,2,13,47,51,1,10,51,55,1,9,55,59,1,6,59,63,2,63,9,67,1,67,6,71,1,71,13,75,1,6,75,79,1,9,79,83,2,9,83,87,1,87,6,91,1,91,13,95,2,6,95,99,1,10,99,103,2,103,9,107,1,6,107,111,1,10,111,115,2,6,115,119,1,5,119,123,1,123,13,127,1,127,5,131,1,6,131,135,2,135,13,139,1,139,2,143,1,143,10,0,99,2,0,14,0'
    run_computer_recover(initial_cells)
    find_key_inputs(initial_cells)
