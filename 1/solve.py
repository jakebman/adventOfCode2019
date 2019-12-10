#! /usr/bin/env python3

def intInput():
    return int(input())

def main():
    total = 0
    while True:
        print(total)
        i = intInput() // 3 - 2
        total+=i;

if __name__ == "__main__":
    main()
