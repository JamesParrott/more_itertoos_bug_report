import itertools

class Doubler:
    def __init__(self, numbers):
        self.numbers = numbers
        self.it = None

    def __iter__(self):
        if self.it is not None:
            print('BBBBBB!!')
        self.it = iter(self.numbers)
        return self

    def __next__(self):
        return next(self.it)

doubles = iter(Doubler(range(10)))

for x in itertools.islice(doubles, 5):
    print(x)