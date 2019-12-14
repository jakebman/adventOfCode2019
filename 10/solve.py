from collections import namedtuple, defaultdict
from math import copysign
from fractions import gcd
from pprint import pprint
from fractions import Fraction


def signum(x):
    return copysign(1, x)


point = namedtuple("point", "column row")  # TODO: order can get verrry confusing, but this is the order in the Q.
vector = namedtuple("vector", "dc dr")


def diff(a, b):
    dc = a.column - b.column
    dr = a.row - b.row

    return rectify(dc, dr)


def rectify(dc, dr):
    if dc == 0:
        dr = signum(dr)
    if dr == 0:
        dc = signum(dc)
    g = gcd(dc, dr)
    dc /= g
    dr /= g
    return vector(dc, dr)


def main():
    grid = list(map(str.strip, open("input.txt").readlines()))
    comets = []
    for row, cells in enumerate(grid):
        for column, cell in enumerate(cells):
            if cell == "#":
                comets.append(point(column, row))

    pprint(comets)
    print(len(comets), "comets in the sky")
    deltas = set()
    vectors = defaultdict(set)
    for a in comets:
        for b in comets:
            if a != b:
                vector = diff(a, b)
                deltas.add(vector)
                vectors[a].add(vector)
    print(len(deltas), "vectors between them")
    best = max(vectors.items(), key=lambda x: len(x[1]))
    print("best is", best[0], "with", len(best[1]), "seen")


if __name__ == "__main__":
    main()
