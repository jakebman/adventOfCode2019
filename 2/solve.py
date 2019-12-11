
def setup(program):
    program[1] = 12
    program[2] = 2


def value(program, pos):
    return program[pos]


def fetch(program, pos):
    return value(program, value(program, pos))


def store(program, pos, value):
    program[pos] = value


def add(program, PC, *discard):
    arg1 = fetch(program, PC+1)
    arg2 = fetch(program, PC+2)
    store(program, value(program, PC+3), arg1 + arg2)

    return PC + 4


def mult(program, PC, *discard):
    arg1 = fetch(program, PC + 1)
    arg2 = fetch(program, PC + 2)
    store(program, value(program, PC + 3), arg1 * arg2)

    return PC + 4

def halt(*discard):
    return -1

def dispatch(program, PC):
    opcode = value(program, PC)
    return {
        1: add,
        2: mult,
        99: halt
    }[opcode]


def run(program):
    PC = 0
    while PC != -1:
        PC = dispatch(program, PC)(program, PC)

    return program


def main():
    raw_program = input()
    program = list(map(int, raw_program.split(",")))
    print(program)

    setup(program)

    print(run(program))


if __name__ == "__main__":
    main()
