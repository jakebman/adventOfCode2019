from IntCode import IntCode

def main():
    raw_program = open("input.txt").readline()
    program = list(map(int, raw_program.split(",")))
    p = IntCode(program)
    p.run()


if __name__ == "__main__":
    main()
