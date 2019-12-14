from itertools import permutations
from pprint import pprint
from threading import Thread
from collections import defaultdict, namedtuple

from IntCode import IntCode, setDebugStream

from queue import Queue, Empty

point = namedtuple("point", "row column")
UP = point(-1, 0)
DOWN = point(1, 0)
LEFT = point(0, -1)
RIGHT = point(0, 1)
CLOCKWISE = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,
}
COUNTERCLOCKWISE = {
    UP: LEFT,
    LEFT: DOWN,
    DOWN: RIGHT,
    RIGHT: UP,
}


def debugPrinter(queue):
    while True:
        print(queue.get())


def main():
    raw_program = open("input.txt").readline()
    program = list(map(int, raw_program.split(",")))

    debug = Queue()
    setDebugStream(lambda *args: debug.put(args))
    Thread(name="Debug Printer", target=debugPrinter, args=[debug]).start()

    queries = Queue()
    commands = Queue()
    a = IntCode(program, name="control", input=queries.get, output=commands.put)
    control = a.run_as_thread()
    field = {}
    Thread(name="hull painter", target=hullPainter, args=(queries, commands, field)).start()
    control.join()
    pprint(field)
    print(len(field))


def query(p, field):
    if p in field:
        return field[p]
    return 0


def hullPainter(queries, commands, field):
    position = point(0, 0)
    direction = UP
    while True:
        queries.put(query(position, field))
        try:
            paint = commands.get(timeout=3)
            turnRight = commands.get(timeout=3)
            field[position] = paint
            if turnRight:
                direction = CLOCKWISE[direction]
            else:
                direction = COUNTERCLOCKWISE[direction]
            position = point(position.row + direction.row, position.column + direction.column)
        except Empty:
            print("Done painting")
            break

    pprint(field)
    print(len(field))


if __name__ == "__main__":
    main()
