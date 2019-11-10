import numpy as np
import codecs


class Operand:
    def __init__(self, val, not_operand=False):
        self.val = val
        self.name = str(val)
        self.notOp = not_operand

    def __repr__(self):
        if self.notOp is False:
            return 'x' + self.name
        else:
            return '\u00ACx' + self.name

    def value(self, val):
        if val != 0:
            return False if self.notOp else True
        else:
            return True if self.notOp else False


class Hypothesis:
    def __init__(self):
        self.operands = []

    def value(self, values):
        value = True
        for x, index in enumerate(values):
            for op in self.operands:
                if op.val == index + 1:
                    t = op.value(x)
                    value &= t
        return value

    def add(self, name, not_operand):
        self.operands.append(Operand(name, not_operand))

    def add_positive_negative(self, name):
        self.add(name, True)
        self.add(name, False)

    def remove_negatives(self, values):
        indices = []
        for index, x in enumerate(values):
            for op_index, op in enumerate(self.operands):
                if op.val == index + 1:
                    t = op.value(x)
                    if t == 0:
                        indices.append(op_index)
        for index in indices[::-1]:
            del self.operands[index]

    def print_to_file(self, file):
        f = codecs.open(file, "w", "utf-8")
        f.write(self.__repr__())
        f.close()

    def __repr__(self):
        string = u''
        for literal in self.operands:
            string += literal.__repr__() + u' \u2227 '
        if len(self.operands) == 0:
            string += '\u2205  '
        return string[:-2]


class ConsistencyAlgorithm:
    # initialize algorithm instance with a file
    # the file should contain a list bigger than 1 of dataset
    # each line contains the values of the inputs x1, x2, x3, x4.... last value is the result value
    # e.g   0 1 0 1 1 1
    #       1 0 1 0 0 1
    #       0 0 1 0 1 0
    # output should return the conjunction which fits the dataset
    def __init__(self, file, file_out):
        self.data = []
        self.read_file(file)
        self.file_out = file_out

    def read_file(self, file):
        training_examples = np.loadtxt(file)
        for line in training_examples:
            x = line[:-1]
            y = line[-1]
            self.data.append([x, y])

    def create_negative_hypothesis(self):
        h = Hypothesis()
        if len(self.data) != 0:
            for i in range(1, len(self.data[0][0]) + 1):
                h.add_positive_negative(i)
        return h

    def run(self):
        h = self.create_negative_hypothesis()
        for x in self.data:
            value = h.value(x[0])
            if x[1] == 1 and value == 0:
                h.remove_negatives(x[0])
        print(h)
        h.print_to_file(self.file_out)


if __name__ == "__main__":
    filename = "data.txt"
    file_output = "output.txt"
    alg = ConsistencyAlgorithm(filename, file_output)
    alg.run()
