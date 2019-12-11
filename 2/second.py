from IntCode import IntCode

def setup(program):
    program[1] = 12
    program[2] = 2

def main():
    raw_program = input()
    program = list(map(int, raw_program.split(",")))
    print(program)

    golden = list(program)

    for first in range(100):
        for second in range(100):
            program = list(golden)
            program[1] = first
            program[2] = second
            value = IntCode(program).run()
            print("Trying", (first, second), "got", value)

            if value == 19690720:
                print("Found it. Submit ", 100 * first + second)
                return


if __name__ == "__main__":
    main()
