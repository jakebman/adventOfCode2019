from itertools import permutations
from threading import Thread
from time import sleep

from IntCode import IntCode, setDebugStream

from queue import Queue


def main():
    raw_program = open("input.txt").readline()
    program = list(map(int, raw_program.split(",")))

    values = {}
    for phases in permutations(range(5,10)):
        value = spawnThreads(phases, program)
        print(phases, "got", value)
        values[phases] = value
    sleep(5)
    second = lambda x: x[1]
    l = list(values.items())
    l.sort(key=second)

    for item in l:
        print(item)
    best = max(values.items(), key=second)
    print(best)

def debugPrinter(queue):
    while True:
        print(queue.get())

def spawnThreads(phases, program):
    queues = [Queue() for _ in phases]
    queues.append(queues[0])  # for wraparound
    names = [chr(ord("A") + i) for i in range(len(phases))]

    debug = Queue()
    setDebugStream(lambda *args: debug.put(args))
    Thread(name="Debug Printer", target=debugPrinter, args=[debug]).start()
    threads = []
    for phase, input, output, name in zip(phases, queues, queues[1:], names):
        input.put(phase)

        a = IntCode(program, input=input.get, output=output.put, name=name)
        thread = Thread(name=name, target=a.run)
        threads.append(thread)
        thread.start()
        print("Spawned", name, "with", phase)
    # initial input
    queues[0].put(0)

    for thread in threads:
        print("joining", thread.getName())
        thread.join()

    got = queues[0].get()
    print("Joined all for perm", phases, "and got", got)
    return got


if __name__ == "__main__":
    main()
