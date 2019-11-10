import numpy as np


class Operand:
    def __init__(self, name, not_operand=False):
        self.val = name
        self.name = str(name)
        self.notOp = not_operand

    def __repr__(self):
        if self.notOp is False:
            return 'x' + self.name
        else:
            return 'not(x' + self.name + ')'

    def value(self, val):
        if val != 0:
            if self.notOp:
                return False
            else:
                return True
        else:
            if self.notOp:
                return True
            else:
                return False


class Hypothesis:
    def __init__(self):
        self.operands = []

    def value(self, values):
        value = True
        for x, index in enumerate(values):
            for op in self.operands:
                if op.val == index+1:
                    t = op.value(x)
                    value &= t
        return value

    def add(self, name, not_operand):
        self.operands.append(Operand(name, not_operand))

    def add_positive_negative(self, name):
        self.add(name, True)
        self.add(name, False)

    def remove_negatives(self, values):
        for index, x in enumerate(values):
            operands = self.operands
            for op_index, op in enumerate(self.operands):
                if op.val == index+1:
                    t = op.value(x)
                    if t == 0:
                        del operands[op_index]
        self.operands = operands

    def __repr__(self):
        string = 'HYPOTHESIS : '
        for literal in self.operands:
            string += literal.__repr__() + ','
        return string


class ConsistencyAlgorithm:

    def __init__(self, file):
        self.data = []
        self.read_file(file)

    def read_file(self, file):
        training_examples = np.loadtxt(file)
        for line in training_examples:
            x = line[:-1]
            y = line[-1]
            self.data.append([x, y])

    def create_negative_hypothesis(self):
        h = Hypothesis()
        for i in range(1, len(self.data)+1):
            h.add_positive_negative(i)
        return h

    def run(self):
        h = self.create_negative_hypothesis()
        for x in self.data:
            value = h.value(x[0])
            if x[1] == 1 and value == 0:
                h.remove_negatives(x[0])
            if value == 1:
                pass
        print(h)


if __name__ == "__main__":
    filename = "data.txt"
    alg = ConsistencyAlgorithm(filename)
    alg.run()
