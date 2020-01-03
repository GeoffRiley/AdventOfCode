import threading
from collections import defaultdict
from time import sleep

from intcode.intcode import Intcode


class NetSix(object):
    def __init__(self, init_mem: str):
        self._processors = []
        for n in range(50):
            p = Intcode(init_mem, f'NIC-{n:02}')
            p.receiver(n)
            p.id = n
            p.connect(receiver=self._receiver, sender=self._sender)
            self._processors.append(p)
        self._out_queues = defaultdict(list)
        self._idle = [False for _ in range(50)]
        self.nat_packet = None
        self.last_nat_packet = [None, None]

    def _receiver(self, processor, output, trace=False):
        self._idle[processor.id] = False
        self._out_queues[processor.id].append(output)
        if len(self._out_queues[processor.id]) == 3:
            proc, x, y = self._out_queues[processor.id]
            self._out_queues[processor.id].clear()
            if proc == 255:
                self.nat_packet = [x, y]
                print(f'NAT set: ({x},{y})')
                # print(f'Part 1: {y}')
                # return
            else:
                if proc not in range(50):
                    raise EnvironmentError(f'Unrecognised processor {proc} with params: x:{x}, y;{y}')
                self._processors[proc].receiver(x)
                self._processors[proc].receiver(y)

    def _sender(self, processor):
        self._idle[processor.id] = True
        return -1

    def start_threads(self, trace=False):
        threads = []
        for a in self._processors:
            t = threading.Thread(target=a.simulate, kwargs={'trace': trace})
            threads.append(t)
            t.start()
        # idle_count = 10
        while any(t.is_alive() for t in threads):
            if all(self._idle) and self.nat_packet:
                # idle_count -= 1
                # if idle_count == 0:
                x, y = self.nat_packet
                self._processors[0].receiver(x)
                self._processors[0].receiver(y)
                self._idle[0] = False
                print(f'NAT send to 0: ({x},{y})')
                if self.last_nat_packet == self.nat_packet:
                    print(f'************** Part 2: {y}')
                self.last_nat_packet = self.nat_packet
                self.nat_packet = None
                # idle_count = 10
            # else:
            # idle_count = 10
            sleep(0.0001)


if __name__ == '__main__':
    with open('input') as f:
        mem_code = f.read()
    net = NetSix(mem_code)
    net.start_threads()

    '''
    Part 1: 18192
    That's the right answer! You are one gold star closer to rescuing Santa. 
    You got rank 728 on this star's leaderboard. [Continue to Part Two]
    Part 2: 10738
    '''
