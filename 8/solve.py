from collections import Counter
from pprint import pprint

LAYER_SIZE = 25 * 6


def chunk(list, n=LAYER_SIZE):
    for start in range(0, len(list), n):
        yield list[start:start + n]


def main():
    vals = []
    for line in open("input.txt").readlines():
        vals += map(int, line.strip())

    layers = list(map(Counter, chunk(vals)))
    pprint(layers)
    layer = min(layers, key=lambda layer: layer[0])

    print(layer)
    print(layer[1] * layer[2])


if __name__ == "__main__":
    main()
