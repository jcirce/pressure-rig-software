class Tube:
    def __init__(self, name, number, test):
        self.name = name
        self.number = number
        self.test = test

    def __str__(self):
        return f"{self.name}{self.number}_{self.test}"

def CLI_init ():

    try:
        name = input("enter tube name")
        number = input("enter tube number")
        test = input("enter test number")

        tube = Tube(name, number, test)
        print(tube)

    finally:
        return "test begins now"



def CLI ():

    try:
        pressure = float(input("enter pressure[psi]"))


        if(pressure > 30):
            raise Exception

    

    except Exception as e:
        print(e)
        print("error")

CLI_init()

while True:
    CLI()


