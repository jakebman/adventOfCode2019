from collections import defaultdict


def debug(*args):
    print("\t", *args)


opcode_names = {
    1: "add",
    2: "mult",
    3: "input",
    4: "output",
    99: "halt",
}


class IntCode:
    def __init__(self, program):
        self._arg_mode = defaultdict(int)
        self._program = program
        self._PC = 0

        self._opcodes = {
            1: self.add,
            2: self.mult,
            3: self.input,
            4: self.output,
            99: self.halt
        }

    def value(self, pos):
        """Retrieve the value of a particular memory address"""
        return self._program[pos]

    def fetch(self, indirect):
        """Retrieve the value of a memory address named from this given memory address (an indirect/pointer thing)"""
        return self.value(self.value(indirect))

    def store(self, pos, value):
        self._program[pos] = value
        debug("Stored", value, "to", pos, "=", self._program[pos])

    def input(self):
        PC = self._PC
        take = int(input())
        self.store_argument(1, take)
        return PC + 2

    def output(self):
        PC = self._PC
        out = self.read_argument(1)
        print(out)
        return PC + 2

    def add(self):
        PC = self._PC
        sum = self.read_argument(1) + self.read_argument(2)
        self.store_argument(3, sum)
        return PC + 4

    def store_argument(self, arg, sum):
        """Like in read_argument, arg positions start at 1 (arg 0 is the opcode)"""
        self.store(self.value(self._PC + arg), sum)

    def mult(self):
        PC = self._PC
        product = self.read_argument(1) * self.read_argument(2)
        self.store_argument(3, product)
        return PC + 4

    def halt(self):
        return -1

    def run(self):
        while self._PC != -1:
            self._PC = self.dispatch()()

        return self._program[0]

    def read_argument(self, arg_pos):
        """ argument positions start at 1 (the opcode is value 0)"""
        mode = self._arg_mode[arg_pos]

        result = {
            0: self.fetch,  # position mode (could be "direct addressing", or 'indirect value')
            1: self.value,  # immediate mode -- just read the value at the position
        }[mode](self._PC + arg_pos)

        return result

    def dispatch(self):
        opcode = self.value(self._PC)  # TODO: read_argument(0), maybe?
        modes = opcode // 100
        opcode %= 100

        debug("PC={}, op={}, modes={}".format(self._PC, opcode_names[opcode], str(modes)[::-1]))

        self._arg_mode = defaultdict(int)
        mode_pos = 0
        while modes:
            mode_pos += 1
            self._arg_mode[mode_pos] = modes % 10
            modes //= 10

        return self._opcodes[opcode]
