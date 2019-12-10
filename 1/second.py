#! /usr/bin/env python3


def intInput():
    return int(input())


def fuelFor(mass):
    return max(0, mass // 3 - 2)


def rocketEquation(mass):
    if mass < 0: return 0
    sum = 0
    while mass > 0:
        mass = fuelFor(mass)
        sum += mass
        # wrong, because it counts the original mass: sum, mass = sum + mass, fuelFor(mass)
        print(mass, "+", end=" ")
    print("=", sum)
    return sum


def main():
    total = 0
    while True:
        print(total)
        i = rocketEquation(intInput())
        total += i;


if __name__ == "__main__":
    main()
