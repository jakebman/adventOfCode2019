from IntCode import IntCode

def setup(program):
    program[1] = 12
    program[2] = 2

def main():
    raw_program = input()
    program = list(map(int, raw_program.split(",")))
    print(program)

    setup(program)

    p = IntCode(program)
    val = p.run()
    print(val)
    print(p._program)


if __name__ == "__main__":
    main()
