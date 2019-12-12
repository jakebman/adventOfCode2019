from itertools import permutations

from IntCode import IntCode

from queue import Queue


def main():
    raw_program = open("input.txt").readline()
    program = list(map(int, raw_program.split(",")))

    values = {}
    for phases in permutations(range(5)):
        print(type(phases))
        output = Queue()
        input = Queue()
        output.put(0)
        for pos, phase in enumerate(phases):
            input.put(phase)
            input.put(output.get())
            a = IntCode(program, input=input.get, output=output.put, name=chr(ord("A") + pos))
            a.run()
        value = output.get()
        print(phases, "got", value)
        values[phases] = value
    print(max(values.items(), key=lambda x: x[1]))


if __name__ == "__main__":
    main()
