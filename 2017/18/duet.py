import multiprocessing.pool
import queue
from collections import defaultdict


def duet(inp, process_id=-1, inqueue=None, outqueue=None):
    registers = defaultdict(lambda: 0)
    freq = 0
    if process_id >= 0:
        registers['p'] = process_id

    def reg_or_val(s: str) -> int:
        if len(s) == 1 and s.isalpha():
            return registers[s]
        else:
            return int(s)

    ip = 0
    while 0 <= ip < len(inp):
        line = inp[ip]
        mnemonic, *params = line.split()
        if mnemonic == 'snd':
            if process_id < 0:
                freq = reg_or_val(params[0])
            else:
                if outqueue:
                    outqueue.put(reg_or_val(params[0]))
                freq += 1
        elif mnemonic == 'set':
            registers[params[0]] = reg_or_val(params[1])
        elif mnemonic == 'add':
            registers[params[0]] += reg_or_val(params[1])
        elif mnemonic == 'mul':
            registers[params[0]] *= reg_or_val(params[1])
        elif mnemonic == 'mod':
            registers[params[0]] %= reg_or_val(params[1])
        elif mnemonic == 'rcv':
            if process_id < 0:
                if registers[params[0]] != 0:
                    registers[params[0]] = freq
                    break
            else:
                if inqueue:
                    try:
                        registers[params[0]] = inqueue.get(timeout=5)
                    except queue.Empty:
                        return freq
        elif mnemonic == 'jgz':
            if reg_or_val(params[0]) > 0:
                ip += reg_or_val(params[1])
                continue
        else:
            print(f'Bad mnemonic {mnemonic} at {ip}')
        ip += 1
    return freq


if __name__ == '__main__':
    with open('input.txt') as prog_file:
        prog_lines = prog_file.read().splitlines(keepends=False)
        print(f'Day 18, part 1: {duet(prog_lines)}')

        pool = multiprocessing.pool.ThreadPool(processes=2)
        buff_0 = multiprocessing.Queue()
        buff_1 = multiprocessing.Queue()
        proc_0 = pool.apply_async(duet, (prog_lines, 0, buff_0, buff_1))
        proc_1 = pool.apply_async(duet, (prog_lines, 1, buff_1, buff_0))

        print(f'Day 18, part 2: {proc_1.get()}')
        # Day 18, part 1: 8600
        # Day 18, part 2: 7239
