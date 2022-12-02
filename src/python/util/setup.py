

class Tube:
    def __init__(self):
        self.name = input("enter tube name (ex: D20K or S45M): ")
        self.number = input("enter tube number: ")
        self.test = input("enter test number: ")

    def __str__(self):
        return f"{self.name}{self.number}_{self.test}"


