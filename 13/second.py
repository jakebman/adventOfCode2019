import threading
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
        #print(queue.get())
        pass


def main():
    raw_program = open("input.txt").readline()
    program = list(map(int, raw_program.split(",")))

    program[0] = 2
    print("Added 2 quarters to the machine")

    debug = Queue()
    setDebugStream(lambda *args: debug.put(args))
    debugThread = Thread(name="Debug Printer", target=debugPrinter, args=[debug], daemon=True)
    debugThread.start()

    field = defaultdict(int)
    score = [0]

    commands = Queue()
    a = IntCode(program, name="game", input=joystickReader(field, score, commands), output=commands.put, )
    control = a.run_as_thread()

    painter = Thread(name="game painter", target=gamePainter, args=(commands, field, score))
    painter.start()

    control.join()
    painter.join()


def showField(field):
    if not field:
        print("Field is empty")
        return
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


def gamePainter(commands, field, score=None):
    if score is None:
        score = [0]
    position = point(0, 0)
    while True:
        try:
            col = commands.get(timeout=3)
            row = commands.get(timeout=3)
            tileId = commands.get(timeout=3)
            if row == 0 and col == -1:
                score[0] = tileId
            else:
                field[point(row, col)] = tileId
        except Empty:
            print("Waiting...")

    pprint(field)
    showField(field)

    summary = Counter(field.values())
    describe = {DESCRIBE[key]: value for key, value in summary.items()}
    for tile, count in describe.items():
        print("There are", count, tile, "tiles")
    print(len(list(tile for tile in field.values() if tile)), "visible tiles")
    print("score is", score)


def joystickReader(field, score, commandQueue):
    def read_joystick(*_):
        while not commandQueue.empty():
            pass
        showField(field)
        print("Score is", score)
        commands = "<.>"
        command = "!"
        while command and command not in commands:
            command = input("Move paddle? (<,>, or empty)")
        if command:
            return commands.index(command) - 1
        else:
            return 0

    return read_joystick


if __name__ == "__main__":
    main()
