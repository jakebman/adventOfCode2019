from collections import defaultdict
from threading import Thread

debug = lambda *args: print("\t", *args, flush=True)


def setDebugStream(newDebug):
    global debug
    debug = newDebug


opcode_names = {
    1: "add",
    2: "mult",
    3: "input",
    4: "output",
    5: "jump-if-true",
    6: "jump-if-false",
    7: "less than",
    8: "equals",
    9: "relative-base",
    99: "halt",
}


class IntCode:
    def __init__(self, program, input=input, output=print, name="unnamed"):
        self._arg_mode = defaultdict(int)
        self._program = defaultdict(int, enumerate(program))  # flexible ram
        self._PC = 0
        self._input = input
        self._output = output
        self._name = name
        self._relative_base = 0

        self._opcodes = {
            1: self.add,
            2: self.mult,
            3: self.input,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            9: self.relative_base,
            99: self.halt
        }

    def value(self, pos):
        """Retrieve the value of a particular memory address"""
        return self._program[pos]

    def fetch(self, indirect):
        """Retrieve the value of a memory address named from this given memory address (an indirect/pointer thing)"""
        return self.value(self.value(indirect))

    def fetch_offest(self, indirect):
        """Retrieve the value of a memory address named from this given memory address, offset by the current
        relative base """
        return self.value(self.value(indirect) + self._relative_base)

    def store(self, pos, value):
        was = self._program[pos]
        self._program[pos] = value
        debug(self._name, "Stored", value, "to", pos, "=", self._program[pos], "was", was)

    def input(self):
        PC = self._PC
        take = int(self._input(self._name + "<prompt>"))
        debug(self._name, "Got", take, "from input")
        self.store_argument(1, take)
        return PC + 2

    def output(self):
        PC = self._PC
        out = self.read_argument(1)
        self._output(out)
        return PC + 2

    def add(self):
        PC = self._PC
        sum = self.read_argument(1) + self.read_argument(2)
        self.store_argument(3, sum)
        return PC + 4

    def store_argument(self, arg, value):
        """Like in read_argument, arg positions start at 1 (arg 0 is the opcode)"""

        pos = self.value(self._PC + arg)
        if self._arg_mode[arg] == 2:  # Quick and dirty solution for arg modes. Refactor this if we need another.
            pos += self._relative_base
        self.store(pos, value)

    def mult(self):
        PC = self._PC
        product = self.read_argument(1) * self.read_argument(2)
        self.store_argument(3, product)
        return PC + 4

    def jump_if_true(self):
        PC = self._PC
        if self.read_argument(1):  # "if the first parameter is non-zero,"
            return self.read_argument(2)
        else:
            return PC + 3

    def jump_if_false(self):
        PC = self._PC
        if not self.read_argument(1):  # "if the first parameter is zero,"
            return self.read_argument(2)
        else:
            return PC + 3

    def less_than(self):
        PC = self._PC
        if self.read_argument(1) < self.read_argument(2):  # "if the first parameter is less than the second parameter"
            self.store_argument(3, 1)
        else:
            self.store_argument(3, 0)
        return PC + 4

    def equals(self):
        PC = self._PC
        if self.read_argument(1) == self.read_argument(2):  # "if the first parameter is equal to the second parameter"
            self.store_argument(3, 1)
        else:
            self.store_argument(3, 0)
        return PC + 4

    def relative_base(self):
        PC = self._PC
        self._relative_base += self.read_argument(1)
        return PC + 2

    def halt(self):
        return -1

    def run(self):
        while self._PC != -1:
            self._PC = self.dispatch()()

        return self._program[0]

    def run_as_thread(self, input=None, output=None):
        if input:
            self._input = input
        if output:
            self._output = output
        thread = Thread(name=self._name, target=self.run)
        thread.start()

        return thread

    def read_argument(self, arg_pos):
        """ argument positions start at 1 (the opcode is value 0)"""
        mode = self._arg_mode[arg_pos]

        result = {
            0: self.fetch,  # position mode (could be "direct addressing", or 'indirect value')
            1: self.value,  # immediate mode -- just read the value at the position
            2: self.fetch_offest,  # relative mode - position mode, but offset the pointer by the relative base register
        }[mode](self._PC + arg_pos)

        return result

    def dispatch(self):
        opcode = self.value(self._PC)  # TODO: read_argument(0), maybe?
        modes = opcode // 100
        opcode %= 100

        debug("{}:{} PC={}, modes={}".format(self._name, opcode_names[opcode], self._PC, str(modes)[::-1]))

        self._arg_mode = defaultdict(int)
        mode_pos = 0
        while modes:
            mode_pos += 1
            self._arg_mode[mode_pos] = modes % 10
            modes //= 10

        return self._opcodes[opcode]
