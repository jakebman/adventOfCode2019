from cmath import polar
from collections import namedtuple, defaultdict
from math import copysign, gcd, pi
from pprint import pprint
from fractions import Fraction


def signum(x):
    return int(copysign(1, x))


point = namedtuple("point", "column row")  # TODO: order can get verrry confusing, but this is the order in the Q.
vector = namedtuple("vector", "dc dr polar", defaults=(None,))


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
    dc //= g
    dr //= g

    # The Column+ axis points right
    # The Row- axis points up
    # Our zero rotation is Up, rotating clockwise

    # The traditional units:
    # X+ points right
    # Y+ points up
    # Zero is right, rotating couter-clockwise

    # Translate Row- to X+ (our up should be zero)
    # Translate Column+ to Y+ (Y+ is +pi/2 from X+. So too should our Column+, which is right should be +pi/2 from Up)
    phi = polar(complex(-dr, dc))[1]  # returns 0 at UP = dr=1, dc=0, and pi at dr=-1, dc=0, increasing clockwise
    if phi < 0:
        phi += 2*pi
    return vector(dc, dr, phi)


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
    vectorsToComets = defaultdict(lambda: defaultdict(list))
    for a in comets:
        for b in comets:
            if a != b:
                vector = diff(b, a)
                deltas.add(vector)
                vectorsToComets[a][vector].append(b)
    print(len(deltas), "vectors between them")
    best = max(vectorsToComets.items(), key=lambda x: len(x[1]))
    vectorsFromBest = best[1]
    bestLocation = best[0]
    print("best is", bestLocation, "with", len(vectorsFromBest), "seen")

    byRotation = sorted(vectorsFromBest.keys(), key=lambda x: x.polar)
    chosen_vector = byRotation[199]

    candidates = vectorsFromBest[chosen_vector]
    print("chose", chosen_vector, "as 200th target.", " The targets are:", candidates)
    for candidate in candidates:
        print("To choose", candidate, "input", candidate.column * 100 + candidate.row)

    candidate = bestLocation
    while candidate not in candidates:
        candidate = point(candidate.column + chosen_vector.dc, candidate.row + chosen_vector.dr)
    print("The answer is", candidate, "with input of", candidate.column * 100 + candidate.row)


if __name__ == "__main__":
    main()
