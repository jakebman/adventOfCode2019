from collections import namedtuple

point = namedtuple("point", "x y")


def add(p1, p2):
    return point(p1.x + p2.x, p1.y + p2.y)


def iterate(pos, delta, n):
    while n:
        pos = add(pos, delta)
        yield pos
        n -= 1


lookup = {
    "U": point(1, 0),
    "D": point(-1, 0),
    "L": point(0, 1),
    "R": point(0, -1),
}


def walk(dirs):
    p = point(0, 0)

    for dir in dirs:
        c = dir[0]
        n = int(dir[1:])
        for np in iterate(p, lookup[c], n):
            p = np
            yield p


def manhattan(p):
    return abs(p.x) + abs(p.y)


def main():
    path1 = input().split(",")
    path2 = input().split(",")
    print(path1)
    circuit1 = list(walk(path1))
    circuit2 = list(walk(path2))
    intersection = set(circuit1).intersection(set(circuit2))
    print("Intersect at", intersection)
    steps = lambda p: circuit1.index(p) + circuit2.index(p)
    shortest = min(intersection, key=steps)
    print("Shortest", shortest, steps(shortest))
    print("Done")


if __name__ == "__main__":
    main()
