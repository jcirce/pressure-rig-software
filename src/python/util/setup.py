

class Tube:
    def __init__(self, name, number, test):
        self.name = name
        self.number = number
        self.test = test

    def __str__(self):
        return f"{self.name}{self.number}_{self.test}"


