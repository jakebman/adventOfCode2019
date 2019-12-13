from collections import Counter
from pprint import pprint

LAYER_WIDTH = 25
LAYER_SIZE = LAYER_WIDTH * 6


def chunk(list, n=LAYER_SIZE):
    for start in range(0, len(list), n):
        yield list[start:start + n]


def main():
    vals = []
    for line in open("input.txt").readlines():
        vals += map(int, line.strip())

    layers = list(chunk(vals))

    image = [2] * LAYER_SIZE
    for layer in layers[::-1]:
        for pos, pixel in enumerate(layer):
            if pixel != 2:
                image[pos] = pixel

    ascii = map({1:"X", 0:" ", 2:" "}.get, image)
    pprint(list("".join(line) for line in chunk(list(ascii), LAYER_WIDTH)))


if __name__ == "__main__":
    main()
