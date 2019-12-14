import operator
from itertools import islice
from pprint import pprint
from re import compile
from collections import namedtuple
from math import copysign

point = namedtuple("point", "x,y,z")


def signum(i):
    if i:
        return i // abs(i)
    return i


def delta_(a, b):
    return map(operator.sub, a, b)


def gravity(a, b):
    return map(signum, delta_(a, b))


def sum_piecewise(*args):
    return tuple(map(sum, zip(*args)))


def iterate(positions, velocities):
    while True:
        yield (positions, velocities)
        nPos = []
        nVel = []
        for pos, vel in zip(positions, velocities):
            # This incidentally calculates gravity with itself, which is zero and does not harm the sum
            vel = sum_piecewise(vel, *map(lambda x: gravity(x, pos), positions))
            pos = sum_piecewise(pos, vel)
            nPos.append(pos)
            nVel.append(vel)
        (positions, velocities) = (tuple(nPos), tuple(nVel))


def potential_energy(pos):
    return sum(map(abs, pos))


def kinetic_energy(vel):
    return sum(map(abs, vel))


def total_energy(positions, velocities):
    return sum(map(operator.mul, map(potential_energy, positions), map(kinetic_energy, velocities)))


def print_state(i, positions, velocities):
    print("After", i, "steps:")
    for pos, vel in zip(positions, velocities):
        print(
            "pos=<x={: {width}}, y={: {width}}, z={: {width}}>, "
            "vel=<x={: {width}}, y={: {width}}, z={: {width}}>".format(*pos, *vel, width=4))

    print("Total Energy:", total_energy(positions, velocities))


def main():
    def parseLine(line, regex=compile("=(-?\\d+)")):
        return tuple(map(int, regex.findall(line)))

    positions = tuple(map(parseLine, map(str.strip, open("input.txt").readlines())))
    velocities = tuple(tuple(0 for _ in pos) for pos in positions)
    pprint(positions)
    pprint(velocities)

    simulation = enumerate(iterate(positions, velocities))
    states = set()

    for i, state in simulation:
        if not i % 1000:
            print(i)
        if state in states:
            break

    print_state(i, *state)


if __name__ == "__main__":
    main()
