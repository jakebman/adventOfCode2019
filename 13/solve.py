from itertools import permutations
from pprint import pprint
from threading import Thread
from collections import defaultdict, namedtuple, Counter

from IntCode import IntCode, setDebugStream

from queue import Queue, Empty

point = namedtuple("point", "row column")

DISPLAY = {
    0: " ",
    1: "|",
    2: "#",
    3: "_",
    4: "o",
}
DESCRIBE = {
    0: "empty",
    1: "wall",
    2: "block",
    3: "paddle",
    4: "ball",
}


def debugPrinter(queue):
    while True:
        print(queue.get())


def main():
    raw_program = open("input.txt").readline()
    program = list(map(int, raw_program.split(",")))

    debug = Queue()
    setDebugStream(lambda *args: debug.put(args))
    debugThread = Thread(name="Debug Printer", target=debugPrinter, args=[debug], daemon=True)
    debugThread.start()

    queries = Queue()
    commands = Queue()
    a = IntCode(program, name="game", input=queries.get, output=commands.put)
    control = a.run_as_thread()

    painter = Thread(name="game painter", target=gamePainter, args=(queries, commands))
    painter.start()

    control.join()
    painter.join()


def showField(field):
    upperLeft = point(min(x.row for x in field), min(x.column for x in field))
    lowerRight = point(max(x.row for x in field), max(x.column for x in field))
    rows = lowerRight.row - upperLeft.row + 1
    cols = lowerRight.column - upperLeft.column + 1
    grid = [[" " for x in range(cols)] for y in range(rows)]
    for p in field:
        row, col = p
        row -= upperLeft.row
        col -= upperLeft.column
        grid[row][col] = DISPLAY[field[p]]
    for row in grid:
        print("".join(row))


def query(p, field):
    if p in field:
        return field[p]
    return 0


def gamePainter(queries, commands):
    field = defaultdict(int)
    position = point(0, 0)
    while True:
        queries.put(query(position, field))
        try:
            col = commands.get(timeout=3)
            row = commands.get(timeout=3)
            tileId = commands.get(timeout=3)
            field[point(row, col)] = tileId
        except Empty:
            print("Done painting")
            break

    pprint(field)
    showField(field)

    summary = Counter(field.values())
    describe = {DESCRIBE[key]: value for key, value in summary.items()}
    for tile, count in describe.items():
        print("There are", count, tile, "tiles")
    print(len(list(tile for tile in field.values() if tile)), "visible tiles")


if __name__ == "__main__":
    main()
