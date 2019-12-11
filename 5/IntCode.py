class IntCode:
    def __init__(self, program):
        self._program = program
        self._PC = 0

        self._opcodes = {
            1: self.add,
            2: self.mult,
            99: self.halt
        }

    def value(self, pos):
        return self._program[pos]

    def fetch(self, indirect):
        return self.value(self.value(indirect))

    def store(self, pos, value):

        self._program[pos] = value
        print("Stored", value, "to", pos, "=", self._program[pos])

    def add(self):
        PC = self._PC

        sum = self.fetch(PC + 1) + self.fetch(PC + 2)
        print("add", {"PC": PC, "first": self.value(PC + 1), "second": self.value(PC + 2), "out": sum,
                      "to": self.value(PC + 3)})
        self.store(self.value(PC + 3), sum)
        return PC + 4

    def mult(self):
        PC = self._PC
        product = self.fetch(PC + 1) * self.fetch(PC + 2)
        print("multiply", {"PC": PC, "first": self.value(PC + 1), "second": self.value(PC + 2), "out": product,
                           "to": self.value(PC + 3)})
        self.store(self.value(PC + 3), product)
        return PC + 4

    def halt(self):
        return -1

    def run(self):
        while self._PC != -1:
            self._PC = self.dispatch()()

        return self._program[0]

    def dispatch(self):
        return self._opcodes[self.value(self._PC)]
